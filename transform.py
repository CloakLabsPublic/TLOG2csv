#!/usr/bin/python
# Transform an unpacked TLOG file in CSV format into a rectangular CSV file with one line per transaction item

import fileinput
import string
import re
import csv
import sys

def str2dec(self): # deal with conversion of empty strings
    if self == '':
        return Decimal(0)
    else:
        return Decimal(self)

def str2int(self): # deal with conversion of empty strings
    if self == '':
        return int(0)
    else:
        return int(self)

from decimal import * # for dealing with decimal numbers (the IBM terminals do everything in cents)
getcontext().prec = 2
writer = csv.writer(sys.stdout)

storeID = '0000' # I haven't found this in the TLOG file yet, it may come from the filename itself
arrayOfItems = [] # this is used to accumulate items that might be modified by later lines
#IBMGroceryItemIndicat2 = ''
amountPaid = 0

# write the header row with column names

writer.writerows([['storeID',                       #0
                   'registerID',                    #1
                   'transactionID',                 #2
                   'itemIndex',                     #3
                   'timeStamp',                     #4
                   'sku',                           #5
                   'amount',                        #6 in CENTS
                   'groceryDepartment',             #7
                   'familyCodeCurrent',             #8
                   'familyCodePrevious',            #9
                   'IBMGroceryItemIndicat1',        #10
                   'IBMGroceryItemIndicat2',        #11
                   'IBMGroceryItemIndicat3',        #12
                   'IBMMultiPricingGroup',          #13
                   'IBMGrocerySaleQuantity',        #14
                   'unitPrice',                     #15 in CENTS
                   'quantity',                      #16
                   'IBMGroceryItemCommonIndicat1',  #17
                   'discountAmount',                #18 in CENTS
                   'discountCode',                  #19
                   'paymentMethod',                 #20
                   'customerID',],])                #21

for row in csv.reader(iter(sys.stdin.readline, '')): # read csv from stdin (unbuffered)

    code = row[0] # this should be a 2 byte string
    assert len(code) == 2

    if code == '00': # new transaction
        itemIndex = 0
        registerID = row[1]
        transactionID = row[2]
        timeStamp = row[3]
        debits = str2int(row[8])
        credits = str2int(row[9])

# reset the item level fields
        sku = ''
        amount = ''
        groceryDepartment = ''
        familyCodeCurrent = ''
        familyCodePrevious = ''
        IBMGroceryItemIndicat1 = ''
        IBMGroceryItemIndicat2 = ''
        IBMGroceryItemIndicat3 = ''
        customerID = ''

    elif code == '01': # new line item
        itemIndex += 1
        sku = row[1]
        amount = str2int(row[2])
        groceryDepartment = row[3]
        familyCodeCurrent = row[4][0:3]
        familyCodePrevious = row[4][3:6]
        IBMGroceryItemIndicat1 = row[5]
        IBMGroceryItemIndicat2 = row[6]
        IBMGroceryItemIndicat3 = row[7]

        if ( str2int(IBMGroceryItemIndicat2) & 128 ) == 128: # reversal
            amount = -amount

        if str2int(IBMGroceryItemIndicat3) == 73: # indicates a coupon so reverse the sign
            amount = -amount

        arrayOfItems.append([storeID,                   #0
                             registerID,                #1
                             transactionID,             #2
                             itemIndex,                 #3
                             timeStamp,                 #4
                             sku,                       #5
                             amount,                    #6
                             groceryDepartment,         #7
                             familyCodeCurrent,         #8
                             familyCodePrevious,        #9
                             IBMGroceryItemIndicat1,    #10
                             IBMGroceryItemIndicat2,    #11
                             IBMGroceryItemIndicat3     #12
                             ])

        [arrayOfItems[itemIndex-1].append('') for i in range(0,10)] # pad array with nulls

    elif ( code == '02' ):
        if ( ( str2int(IBMGroceryItemIndicat2) & 2050 ) == 2050 ) & bool(row[7]): # modifies a line item, typically with manual weight info
            IBMMultiPricingGroup = row[1]
            IBMGrocerySaleQuantity = row[4]
            unitPrice = str2int(row[5])
            quantity = str2int(row[6])
            IBMGroceryItemCommonIndicat1 = row[7]
            arrayOfItems[itemIndex-1][13:17] = [IBMMultiPricingGroup,           #13
                                                IBMGrocerySaleQuantity,         #14
                                                unitPrice,                      #15
                                                quantity,                       #16
                                                IBMGroceryItemCommonIndicat1    #17
                                               ]

    elif code == '03': # discount
        r = str2int(row[1])
        discountCode = str2int(row[2]) # the discount code
        discountAmount = str2int(row[3]) # the discount amount is recorded but the original amount will remain unchanged
        arrayOfItems[r-1][18:19] = [ discountAmount, discountCode ]

    elif code == '04': # VOID a discount
        r = str2int(row[1])
        discountCode = ''
        discountAmount = ''
        arrayOfItems[r-1][18:19] = [ discountAmount, discountCode ]

    elif ( code == '11' ) & ( row[1] == '1414'): # lines with customerIDs
        customerID = row[2]

    elif code == '05': # closes a transaction with payment info
        paymentMethod = row[1]
        amountPaid = str2int(row[2])
        #assert paymentMethod > 0
        sumOfItemAmounts = 0
        for r in range(0,itemIndex):
            arrayOfItems[r][20:21] = [paymentMethod, customerID]
            sumOfItemAmounts += arrayOfItems[r][6] - str2int(arrayOfItems[r][18])

        writer.writerows(arrayOfItems) # flush the current list of items

# reset the transaction level variables

        arrayOfItems = []
        registerID = ''
        transactionID = ''
        timeStamp = ''

    elif code == '07': # tax line
        tax = str2int(row[1])
        # print amountPaid,debits,credits,tax,debits-credits,sumOfItemAmounts+tax #debugging


