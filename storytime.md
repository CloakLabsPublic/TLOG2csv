Notes on the IBM TLOG data file.

eamtrana.dat has 65 lines. From the scanned receipts in ../SampleTLOG/ReceiptImages we see those 65 lines
cover at least 12 individual receipts plus a few miscellaneous transactions such as "loan." I suspect that
a "loan" is used to register the initial cash balance in the drawer.

The first byte determines the type of each major event
Type 20 (space) events contain 8-16 fields. Interestingly, some type 20 events have literal numbers in
columns 9-13, for example "900" and "-900" or at least they sure look like literal numbers (the XML files
seem to confirm this hypothesis. 

Timestamps only appear in type 20 and type 00 events and then always in column 4.
Timestamps are of the form yymmddhhmm where hh is in 24hr time.

The 00 events start with two 4 digit numbers, 0001 and 000N. The first 0001 is likely the store number
whereas the second one increments with each transaction and is more likely a transaction number.

The 00 events all have multiple "records" that follow on the same line in the TLOG. These are likely to be
the individual items in the basket.

The first 00 event in the file is followed by 6 records each of which has 12500 in column 3. This
12500 is likely to be the LOAN ammount in cents. I don't understand why it's repeated over 6 lines though.
Only the first line also has 12500 in column 7. Columns 6,8,10,12,14,16 have a series of integers which are
incremented by one on each subsequent record. Then each record ends with a 99.

Line 14 in eamtrana.dat starts what I believe is the first real basket transaction.

	00,0001,0002,0310242309,00,13,1,1,1704,,18,2,,3,

  00 is event indicator for a new transaction
  0001 is the register number
  0002 is the transaction number
  0310242309 is the timestamp. Oct 24, 2003 11:09
  00 dk
  13 dk
  1 dk (but there is a 01 after the store number on the receipt)
  1 dk (but there is another 01 after the transaction number on the receipt)
  1704 has to be the total for the transaction $17.04 but it's interesting that this shows up before the
       individual line items
  18 dk
  2 dk
  3 dk

Then we get the first line item record:

	01,1,100,1,000000,12,,01

Note the absence of store ID, transaction ID, or timestamp here. 8 columns total.

We can see from the receipt that the first line item was for $1.00 so the 100 in column 3 is likely the amount.

The second line item has:

	01,2,894,4,991000,16396,2050,01

Again we have 8 columns which is good in terms of consistency!

We can see from the receipt that the 2nd line item was for 8.94 so column 3 is again the amount.
What's odd here is that on the printed receipt we see 2.99 lb @ 2.99 lb MAN WT which means manual weighing
but neither the 2.99 lbs or $2.99/lb are in the data.

The 991000 code in column 5 is interesting - that might be the SKU for CANDY which we see on the receipt.
The first item had no SKU so that 000000 might indicate that in column 5 of the first item.

Oh! Except now I see the next line is:

	02,2,,,1,299,299,64

That's where the weight and price per pound are. We just can't tell them apart (crappy example IBM!)
This means that a 02 code likely extends a 01 row with price per pound (or unit) information.

The next row is:

	01,3,150,999,000000,140,,01

Again column 3 is the price, here $1.50. The receipt shows a sku of "item 3" afaict but I think the
number in column 2 is just the item number in the basket (1:N). I can't tell what that 140 is.

Let's look at the XML version - all I can find there matching "140" is a sequence number but I can't
find it for the other line items so I think it's a false indicator.

One of the fields at the item level has to tell us if the item is taxable or not otherwise how could the
register figure out tax at the end? This is a bit of a mystery. The "F" and "B" flags at the end of each
item on the scanned register receipts might be a clue but sometimes these are missing entirely.

It looks like the 01 at the end of each item corresponds to

	<IBMGroceryItemIndicat3>01</IBMGroceryItemIndicat3>

in the XML file. At least it's in the right area (just at the end of a <LineItem> block).

The next line is:

	01,4,100,999,000000,140,2,01

This shows up on the receipt as item 4 for $1.00.

I'm noticing that the receipt has either F, B, -F, or -B following the value of most items. wtf does that mean?

Item 4 is followed by another modifier line:

	02,2,1,4,2,40000200,1,

But that doesn't seem to correspond to anything on the printed receipt.

The next line is item 5:

	01,5,125,1,000000,12292,,01

125 is the price $1.25. This item is printed oddly on the receipt and I can't see why.

Skipping ahead to item 8:

	01,8,5,999,000000,16524,2050,01
	02,2,,,1,29,16,80

Now we know that the 29,16 on the 02 code correspond to 0.16lb at $0.29/lb so we can decipher manual weight
items. This row has the same 2050 code we saw before in column 7 but a different SKU in column 6 (16524)

The last two lines of this transaction are:

	05,11,1704,,,00
	07,31,,,,554,,,

That 05 code likely corresponds to the "CASH" line. Since the shopper provided exact change the end
of the receipt says ".00" for change which might be blank on this 07 code line.

That second column in the 07 line is 31 which is the $0.31 in tax.

The bottom of the receipt says that the cashier was "Jeff" which is likely a code somewhere in the
transaction header.

Let's move on to transaction 0003 which is going to be more interesting because there are coupons!

	00,0001,0003,0310242311,00,26,1,1,1129,,17,105,,11,4194328

Type 00, store 0001, transaction 0003, October 24, 2003 23:11, $11.29

The receipt shows a total of $9.43 but there are $1.86 in coupons so that matches to the amount of $11.29
in column 9.

	10,1,112

Haven't seen a 10 record before. No idea.

	11,15,46111111111,0,0001,,

Haven't seen an 11 either. No idea.

	01,1,100,1,000000,12,,01

First item is $1.00, no sku.

	01,2,296,4,991000,16396,2050,01
	02,2,,,1,299,99,64

Second item is 0.99lb of candy manual weight at $2.99/lb for a total of $2.96.

	01,3,150,999,000000,140,,01

Third item is $1.50

	01,4,100,999,000000,140,2,01
	02,2,1,4,2,40000200,1,

Fourth item is $1. Can't see why there's a modifier on this one. No apparent impact.

	01,5,20,1,000000,12292,,01

Fifth item is $0.20. Still not really sure where the sku column is. Still betting on column 6.

	01,6,100,999,000000,140,,01

Sixth item is $1.00

	01,85000,25,999,000000,1036,,73

Now we see our first coupon which is #85000. The coupon value is $.25 (column 3). I can't see
how to detect this pattern yet since there is no minus sign for a credit. What's indicating that this
is a coupon?

	11,,-13,16,,,

Ah ha! A coupon item is followed by an 11 code with 7 columns.

	01,7,199,999,000000,140,,01

Seventh item at $1.99

	01,85001,150,999,000000,1037,,73
	11,,-13,0,,,5001

Next item at $1.50 is a coupon 85001

	01,8,33,999,000000,16524,2050,01
	02,2,,,1,29,114,80

Eighth item is $0.33, manual weight 1.14lb @ 0.29/lb.
 
	01,85002,11,999,000000,17421,2050,73
	02,,,,1,10,114,80
	11,,-13,0,,,5002

Another coupon but note how this 01 record has both a 02 and 11 modifier. It looks like a manual weight
item 1.14lb @ $0.10/lb AND a coupon. This must be a coupon for a manual weight item - $0.10 discount/lb
for example. It shows up as $0.11 value but a credit.

	10,1,29

Here's another one of those strange 10 lines with only 3 fields.

	01,1,100,1,000000,12,,01

The last item on the receipt at $1.00

	11,1212,0,186,0,3,
	11,1414,046111111111,0,186,03,,,,,

Then the transaction closes with:

	05,11,943,,,00
	07,31,,,,582,,,

The 05 with 943 is $9.43 balance. No change on this transaction either. The $0.31 in tax is in
column 2 of the 07 line.

In receipts0002.jpg on the left side we see that someone signed off at 10/24/03 11:11. This is followed
by a number of error messages and then "User Options Complete" also at 11:11. The corresponding set of
lines in eamtrana.dat is:

	00,0001,0004,0310242311,17,2,1,1,2833,,,3,,,
	20,0001,0004,0310242311,11,1,3,1,,,,
	20,0001,0005,0310242311,11,1,1,1,,,,

The first 2 are transaction 0004 so they go together. The 3rd one is 0005. I wish I could figure out
where the cashier ID sits. As far as data export though these events don't seem to have value.

Then we pick up again with:

	20,0001,0005,0310242312,01,1,85000,2,7,-25,1,0,,,1,
	20,0001,0005,0310242312,01,1,85001,2,7,-150,1,0,,,00,
	20,0001,0005,0310242312,01,1,85002,3,7,-49,491,0,,,00,

These are a minute later and likely correspond to the cashier signing in again although we don't have
a scanned tape of that. Not sure what these 85000-2 numbers mean either.

Now we have a new transaction at 10/24/03 23:12.

	00,0001,0005,0310242312,00,24,1,1,1127,,15,16,,4,4259928
	01,1,100,1,000000,12,,01
	01,2,296,4,991000,16396,2050,01
	02,2,,,1,299,99,64
	10,1,31
	11,15,46111111111,0,0001,,
	01,3,150,999,000000,140,,01
	01,4,100,999,000000,140,2,01
	02,2,1,4,2,40000200,1,
	01,6,100,999,000000,140,,01
	01,85000,25,999,000000,1036,,73
	11,,-13,16,,,
	01,7,199,999,000000,140,,01
	01,85001,150,999,000000,1037,,73
	11,,-13,0,,,5001
	01,8,142,999,000000,16524,2050,01
	02,2,,,1,29,491,80
	01,85002,49,999,000000,17421,2050,73
	02,,,,1,10,491,80
	11,,-13,0,,,5002
	11,1212,0,224,0,3,
	11,1414,046111111111,0,224,03,,,,,
	05,41,903,,4264296355273423,50
	16,4141,1,903,303331303234323331323134,413030,37333132333720202020,0000000008
	07,40,,,,691,,,

The new thing here is this code 16 event which has some long numbers in it. It's hard to tell whether
the fields in it are packed or not because we see "031024231214:A00:731237    :" in columns 5-7.
Could these be the authorization codes coming back from the credit card processor?

These 8500x codes in column 2 of code 01 records are perplexing. Some come without follow-on code 11 lines
that have a promo code 500x in the last column. Not sure why there's a mismatch or what it means. Also the
8500x in column 2 is out of order with the item sequence number that normally progresses 0..1..2 and so on.

In a sense that doesn't matter too much since we really don't want to keep CC info but it would be nice
to know exactly where it is. See 00000019.01.XML for the XML version of this transaction. The XML has:

	<CustomerAccountID>046111111111</CustomerAccountID>
	<AccountID>4264296355273423</AccountID>

<AccountID> sure looks like a credit card number. <CustomerAccountID> looks more like a frequent shopper
card ID. We can see that column 5 of the 05 event line has the CC#. The last 11 event line also has the
<CustomerAccountID> in column 3. Whew, I was wondering where those were going to show up! Why are there
multiple code 11 lines and what do the others mean? Only the last code 11 line appears to have a frequent
shopper in it as a positive integer in column 3. Negative integers or 0 are not frequent shopper numbers.

Where is the store ID in the data? This silly example has a store ID of 0001 but also a register # of 0001
so it's impossible to distinguish them unless one of those 1s on a code 20 line tells us the store ID. Will
need different sample data to tell them apart.

Something else I gleaned from the XML files. The 5002 at the end of:

	11,,-13,0,,,5002

Corresponds to a "promotion code." This is no doubt going to be important in analytics.

Also in a 01 line such as "01,7,199,999,000000,140,,01"
The 000000 in column 5 shows up in the XML as <FamilyCode>000000</FamilyCode>

Let's move on to receipts0003.jpg (see also 00000034.01.XML). This also has a signoff followed by a bunch
of errors:

	00,0001,0006,0310242312,17,1,1,1,1127,,,1,,8,
	20,0001,0006,0310242312,11,1,3,1,,,,
	20,0001,0007,0310242313,11,1,1,1,,,,
	20,0001,0007,0310242313,01,1,85000,2,7,-25,1,0,,,00,
	20,0001,0007,0310242313,01,1,85001,2,7,-150,1,0,,,00,
	20,0001,0007,0310242313,01,1,85002,3,7,-9,91,0,,,00,
	20,0001,0007,0310242313,01,1,6,2,8,100,1,1,100,,00,
	20,0001,0007,0310242313,01,1,85000,2,7,25,1,0,,,00,
	20,0001,0007,0310242313,01,1,7,2,8,199,1,1,199,,00,
	20,0001,0007,0310242313,01,1,85001,2,7,150,1,0,,,00,
	20,0001,0007,0310242314,08,1,999200,03,
	20,0001,0007,0310242314,01,1,85001,2,7,-150,1,0,,,00,
	20,0001,0007,0310242314,01,1,7,2,8,199,1,1,199,,00,
	20,0001,0007,0310242314,01,1,85001,2,7,150,1,0,,,00,

That's a whole lot of code 20 lines for nothing going on. Then we get the next basket:

	00,0001,0007,0310242315,00,30,1,1,730,498,27,56,,12,4259928
	11,15,46111111111,0,0001,,
	01,1,100,1,000000,12,,01
	01,4,100,999,000000,140,2,01
	02,2,1,4,2,40000200,1,
	01,6,100,999,000000,140,,01
	01,85000,25,999,000000,1036,,73
	11,,-13,16,,,
	01,7,199,999,000000,140,,01
	01,85001,150,999,000000,1037,,73
	11,,-13,0,,,5001
	01,8,26,999,000000,16524,2050,01
	02,2,,,1,29,91,80
	01,85002,9,999,000000,17421,2050,73
	02,,,,1,10,91,80
	11,,-13,0,,,5002
	01,6,100,999,000000,1164,128,81
	01,85000,25,999,000000,1036,128,73
	01,7,199,999,000000,1164,128,81
	01,85001,150,999,000000,1037,128,73
	01,7,199,999,000000,140,,01
	01,85001,150,999,000000,1037,,73
	11,,-13,0,,,5001
	01,7,199,999,000000,1164,128,81
	01,85001,150,999,000000,1037,128,73
	10,1,22
	11,1212,0,9,0,1,
	11,1414,046111111111,0,9,01,,,,,
	05,21,223,,0860861190,50
	16,4141,1,223,303331303234323331343538,413030,37333132333720202020,0000000009
	07,6,,,,126,,,

The new stuff this time is that we have a check transaction instead of a credit card or cash.

That last 05 code line has 0860861190 in column 5 which turns out to be the DL#. This is annoyingly
placed in the same position as the CC# in the earlier transaction but since we seek to drop both
it doesn't really matter. Now, how can we tell that this was a check and not a CC or cash?

The first transaction had a code 05 line of 05,11,1704,,                ,00
The second one had                          05,11, 943,,                ,00
The third transaction had a code 05 line of 05,41, 903,,4264296355273423,50
This (4th) one has                          05,21, 223,,      0860861190,50

Column 3 is the amount and column 5 is the ID# (DL or CC#) so my bet is that in column 2
11 means cash, 41 means "credit card" and "21" means "check." We'll see on future transactions.

The last code 11 line has 046111111111 in column 3 which is again the frequent shopper number. It looks like
such lines always have 1414 in column 2 which is probably a sub-code indicating a frequent shopper number
record.

The printed receipt shows "STORE ACCOUNT #999-999-999" which I don't see anywhere in the data. Maybe this
doesn't come through. Not important.

The printed receipt also shows "APPROVAL # REF # 73" but where that 73 comes from isn't obvious either.

On to receipts0004.jpg. Here we have a check cashing transaction:

	00,0001,0008,0310242315,01,3,1,1,,,17,3,,12,
	05,21,1000,,0860861190,50
	16,4141,1,1000,303331303234323331353334,413030,37333132333720202020,0000000010
	09,11,1000

This is interesting in that there is no amount in column 9 of the code 00 line. This makes sense since
nothing was purchased. The customer's DL# is in column 4 of the code 05 line as usual. We have another
very complicated code 16 line and this time a new 09 line with 1000 in column 3 which I'm going to guess
is cash tendered. Does this kind of stuff need to go into the export?

Next we have an opaque block of:

	00,0001,0009,0310242315,03,7,1,1,,,14,,,5,
	10,1,55
	13,1,1000,,,11,1000,21,,31,,41,,51,,61,,71,,81,,99
	13,1,1000,,,12,,22,,32,,42,,52,,62,,72,,82,,99
	13,1,1000,,,13,,23,,33,,43,,53,,63,,73,,83,,99
	13,1,1000,,,14,,24,,34,,44,,54,,64,,74,,84,,99
	13,1,1000,,,15,,25,,35,,45,,55,,65,,75,,85,,99
	13,1,1000,,,16,,26,,36,,46,,56,,66,,76,,86,,99

The transaction 00 has no amount again and it has no line items following it. The code 13 lines
all have 1000 in column 3 which is the amount tendered in the previous check cashing transaction. Perhaps
this is a redundant version of that. The code 13 lines have the same strange progression of integer numbers.
Probably can be ignored.

Then we have:

	20,0001,0010,0310242316,01,1,2,3,8,59797,19999,1,299,,00,

Another housekeeping record...

Then (top right of receipts0004.jpg and 00000038.01.XML)

	00,0001,0010,0310242316,00,11,1,1,60054,59797,32,5,,5,4194312
	01,1,100,1,000000,12,,01
	01,2,59797,4,991000,16396,2050,01
	02,2,,,1,299,19999,64
	11,15,46111111111,0,0001,,
	01,3,150,999,000000,140,,01
	01,2,59797,4,991000,17420,2178,81
	02,2,,,1,299,19999,64
	10,1,2222
	11,1414,046111111111,0,,,,,,,
	05,11,257,,,00
	07,7,,,,150,,,

The nominal amount of this transaction is $600.54 but there's a correction of $597.97 for 199.99 lbs
of candy (what, someone bought their own weight in candy?) This reduces the net amount to 2.57 which
doesn't show up explicitly in the code 00 line. It looks like on a code 00 line the "corrections" amount
is in column 10 (typically blank).

Let's look at the reversal in detail:

	01,2,59797,4,991000,16396, 2050,01
	02,2,     , ,     1,  299,19999,64

	(2 lines omitted)

	01,2,59797,4,991000,17420, 2178,81
	02,2,     , ,     1,  299,19999,64

The first is a charge of a manual weight item and the second is a reversal of same.
The code 02 lines are identical. The manual weight code of 2050 changes to a 2178 for the reversal.
This is a delta of 128 which means that Bit7 of IBMGroceryItemIndicat2 indicates a reversal!

Not sure what 16396 is relative to 17420 although these appear to be bit vectors. Somewhere buried in there
is the VOID flag!

"B" items on the receipt are taxable. Don't see where this shows up in the data :( Need to compare
the XML for a taxable and non-taxable item line by line and bit by bit.

Moving on to receipts0005.jpg.

The usual housekeeping events:

	20,0001,0011,0310242317,08,1,9,03,
	20,0001,0011,0310242317,08,1,9,03,
	20,0001,0011,0310242318,06,1,4,,,,
	20,0001,0011,0310242336,06,1,5,,,,
	20,0001,0011,0310242336,01,1,3,2,8,150,1,2,300,,00,

Transaction #0011 at 10/24/03 23:36 for $3.53 with credits of $1.90:

	00,0001,0011,0310242336,00,10,1,1,353,190,9,10,1073,99,2

	01,1,100,1,000000,12,,01	Item 1 for $1.00
	01,4,100,999,000000,140,2,01	Item 4 for $1.00, taxable
	02,2,1,4,2,40000200,1,		Modifier for item 4 but this is not a manual weight item?
	01,3,150,999,000000,140,,01	Item 3 for $1.50 taxable
	01,3,150,999,000000,1164,128,81	Item 3 cancelled? See the 128 in column 7.
	03,01,2000,40,			This is new - $0.40 discount in column 4
	10,1,22
	05,11,200,,,00			Cash payment $2.00
	09,11,37
	07,3,,,,80,,,			$0.03 in tax

Lower left of receipts0005.jpg

	20,0001,0012,0310242336,01,1,1,2,8,100,1,0,100,,00,	Housekeeping entries
	20,0001,0012,0310242336,01,1,4,2,8,100,1,2,400,,00,

Transaction #0012 for $2.00 with $2.00 in credits (net zero)

	00,0001,0012,0310242337,00,8,1,1,200,200,19,7,,4,

	01,4,100,999,000000,140,2,01	Item 4 for $1.00, taxable
	02,2,1,4,2,40000200,1,		Modifier for item 4
	01,1,100,1,000000,12,,01	Item 1 for $1.00
	01,1,100,1,000000,1036,128,81	Void item 1 for $1.00, again 128 in column 7 01000000
	01,4,100,999,000000,1164,130,81	Void item 4 for $1.00, 130 in column 7 01000010 (why is 2 bit set?)
	02,2,,4,2,40000200,1,		Modifier for previous row
	10,1,22				dk
	05,11,,,,00			Cash transaction for $0.00

Top right of receipts0005.jpg

	00,0001,0013,0310242337,00,4,1,1,136,,2,38,,9,32	Transaction #0013 for $1.36, no credits
	01,8,130,999,000000,16524,2050,01			Item 8 for $1.30, taxable
	02,2,,,1,29,447,80					Modifier for previous row, 4.47# at $0.29/#
	05,51,136,,,00						Payment is W.I.C. (51)
	07,6,,,,130,,,						$0.06 in tax

Bottom right of receipts0005.jpg

	00,0001,0014,0310242338,00,5,1,1,299,,3,13,,4,	Transaction #0014 for $2.99
	01,7,199,999,000000,140,,01			Item 7 for $1.99, taxable
	01,4,100,999,000000,140,2,01			Item 4 for $1.00
	02,2,1,4,2,40000200,1,				Modifier for previous line
	05,32,300,,,00					Payment $3.00 in PAPER FOOD STAMPS (52)
	09,11,1						Haven't seen a code 09 before!

Top left of receipts0006.jpg

	00,0001,0015,0310242338,00,10,1,1,247,60,3,28,,10,	Transaction #0016 for $2.47, $0.60 credits
	01,4,100,999,000000,140,2,01				Item #4 for $1.00
	02,2,1,4,2,40000200,1,					Modifier for previous line
	01,6,100,999,000000,140,,01				Item #6 for $1.00
	03,01,2000,40,						Discount on first item for $0.40
	04,01,2000,40,						Void discount on first item
	03,02,1000,20,						Discount on second item for $0.20
	05,21,300,,0860861190,50				$3.00 paid by check, DL#0860861190
	16,4141,1,300,303331303234323333383435,413030,37333132333720202020,0000000012	Probably approval
	09,11,113						dk
	07,7,,,,180,,,						$0.17 tax

	20,0001,0016,0310242339,08,1,9,03,
	
	00,0001,0016,0310242339,17,7,1,1,62019,60745,,3,,8,	Not sure what this means, no items follow it!
	
	20,0001,0016,0310242339,11,1,3,1,,,,				Housekeeping
	20,0001,0017,0310242339,11,1,1,1,,,,
	20,0001,0017,0310242339,01,1,9,2,4,900,1,0,900,,00,207000,11,
	20,0001,0017,0310242339,01,1,9,2,4,900,1,0,900,,00,
	20,0001,0017,0310242339,01,1,9,2,4,900,1,0,900,,00,207000,11,
	20,0001,0017,0310242339,01,1,9,2,4,900,1,0,900,,00,
	20,0001,0017,0310242339,01,1,9,2,4,-900,1,0,900,,00,207000,11,
	20,0001,0017,0310242339,01,1,9,2,4,-900,1,0,900,,00,
	20,0001,0017,0310242339,01,1,9,2,4,900,1,0,900,,00,207000,11,
	20,0001,0017,0310242339,01,1,9,2,4,900,1,0,900,,00,		
	20,0001,0017,0310242339,01,1,9,2,4,-900,1,0,900,,00,207000,11,
	20,0001,0017,0310242339,01,1,9,2,4,-900,1,0,900,,00,

Top right of receipts0006.jpg

	00,0001,0017,0310242340,00,16,1,1,475,,17,2,,9,65600	Transaction #0017 for $4.75, no credits
	01,8,356,999,000000,16524,2050,01			Item #8 for $3.56, 2050=manual weight, taxable
	02,2,,,1,29,1227,80					12.27# at $0.29/#
	01,1,100,1,000000,12,,01				Item #1 for $1.00
	01,9,900,999,207000,1036,,41				Item #9 for $9.00
	17,9,900,999,207,1036,,00,11				
	01,9,900,999,207000,1036,2050,41			Item #9 for $9.00
	02,2,,,1,900,1,
	17,9,900,999,207,1036,2050,00,11			
	01,9,900,999,207000,1036,128,41				Void Item #9 (see 128 in column 7)
	17,9,900,999,207,1036,128,00,11
	01,9,900,999,207000,1036,,41				Item #9 for $9.00
	17,9,900,999,207,1036,,00,11
	01,9,900,999,207000,1036,128,41				Void Item #9
	17,9,900,999,207,1036,128,00,11
	05,11,1375,,,00						Cash (11) for $13.75
	07,19,,,,356,,,						$0.19 in tax

Deduced Field mappings:
=======================

	00 lines
	--------
	code
	register#
	transaction#
	datetime
	dk
	dk
	dk
	dk
	debits (cents)
	voids, coupons, discounts (cents)
	dk
	dk
	dk
	dk
	dk

	01 lines
	--------
	code
	sku
	amount
	groceryDepartment
	FamilyCodeCurrent (3bytes) FamilyCodePrevious (3bytes)
	IBMGroceryItemIndicat1 of 32 bits
	IBMGroceryItemIndicat2 of 16 bits. Manual weight item if 2050 bits set, reversal if 128 bit set
	IBMGroceryItemIndicat3. 73 indicates a coupon.

	02 lines
	--------
	code
	IBMMultiPricingGroup
	dk
	dk
	IBMGrocerySaleQuantity
	price per unit
	units
	IBMGroceryItemCommonIndicat1 - bit vector of 8 bits

	03 lines
	--------
	code
	item sequence number
	discount code
	discount amount

	04 lines
	--------
	code
	item sequence number
	dk
	discount VOID amount

	05 lines
	--------
	code
	payment method (11=cash, 21=check, 32=food stamps, 41=credit card, 51=WIC)
	amount
	dk
	CustomerID# (DL or CC) PII!
	dk

	07 lines
	--------
	code
	tax amount
	dk*7

	11 lines
	--------
	code
	dk
	ShopperID (if dk=1414)
	dk*varying number

	10 lines
	--------
	No clue

	13 lines
	--------
	No clue

What we'd like for output:
==========================
	storeID
	registerID
	transactionID
	dateTimeStamp
	sku
	amount
	qty
	price/unit
	discountAmount
	discountCode
	paymentMethodCode
	shopperID
	IBMMultiPricingGroup
	IBMGrocerySaleQuantity
	groceryDepartment
	FamilyCodeCurrent (3bytes)
	FamilyCodePrevious (3bytes)
	IBMGroceryItemCommonIndicat1

We should tally up the receipt line items and verify that the net amount matches the transaction header
as a quality check.
