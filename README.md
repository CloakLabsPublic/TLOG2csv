TLOG2csv
========
This is a small set of python utilities for reading IBM TLOG (binary) files
and writing csv files that can be imported into an analytics platform.

IBM TLOG files are created by IBM POS (Point Of Sale) terminals. IBM has a
large investment in proprietary code that processes these files.

The TLOG format was originally optimized for compactness and ease of writing but
upon close inspection doesn't really reduce file size by more than a few
percent. One could speculate endlessly about why IBM might create such a
convoluted file format ;)

The focus is on extracting line-item level transaction details from the file.
A "line item" is a individual item purchased like a pack of gum. A "transaction"
is a collection of line items tied together by a purchaser, a cashier,
a timestamp, a method of payment, a store ID, etc...

Line items can include for sale items as well as various forms of credit such
as coupons.

The utlities so far include two python files unpack-tlog.py and transform.py

unpack-tlog takes a packed binary TLOG file and outputs an intermediate csv
file filtered down to specific data of interest (a raw TLOG file contains
numerous administrative transactions that so far hold little analytic interest)

This intermediate csv file has variable length rows and cannot be input
to analytics systems.

transform.py reads the csv file output by unpack-tlog into a rectangular csv
file with labeled and consistent columns. In doing so it also "flattens" the
data by including transaction level items at the line item level. The "grain"
of the final data file is at the item level. This is much easier to import into
analytic systems than two normalized relational files.

Files are expected on the command line, therefore usage is as follows:

    $ python unpack-tlog.py < rawTLOG.dat > intermediate.csv
    $ python transform.py < intermediate.csv > final.csv

or in combination:

    $ python unpack-tlog.py < rawTLOG.dat | python transform.py > final.csv

This post was invaluable in being able to reverse engineer the TLOG format:

    http://www.ogf.org/pipermail/dfdl-wg/2012-September/001987.html

This Websphere documentation otoh was indecipherable to a non-websphere
expert. You might find it more helpful than I did.

    http://pic.dhe.ibm.com/infocenter/wmbhelp/v8r0m0/index.jsp?topic=%2Fcom.ibm.etools.mft.samples.tlog61v21.doc%2Fdoc%2Foverview.htm

Sample data is available from

    http://www-01.ibm.com/support/docview.wss?uid=pos1R1003439

I have included eamtrana.dat in this repo for easy access and testing.
It is the base TLOG file that contains a series of test transactions.

If you explore the full sample data you can see scanned images of receipts
(invaluable) as well as XML versions of the data (also invaluable).

Regrettably the IBM test data uses the same values for different fields and
so for example I have yet to be able to distinguish the placement of the
StoreID and the cashier number. Both are 0001 in the test data. If anyone
can tell me which is which that would be awesome.

I logged my reverse engineering train of thought in storytime.md

The utilities are missing unit tests. Right now eamtrana.dat is the only
test data file I have, I could use more. A regression test can be done with:

    $ python unpack-tlog.py < eamtrana.dat > testIntermediate.csv
    $ python transform.py < testIntermediate.csv > testFinal.csv
    $ diff testIntermediate.csv intermediate.csv
    $ diff testFinal.csv final.csv

Both those final diffs should be zero. Then again it's possible that either
of those base csv files already contains one or more errors. That's where
checking against the scanned image receipts is important.

Note: The IBM TLOG format exists in multiple versions and individual stores can
customize certain fields. It's a messy world.
