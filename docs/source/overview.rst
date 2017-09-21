Overview
========

openprocurement.auctions.insider contains documentaion concerning the new type of the Deposit Guarantee Fund auctions.

The procedure to be used is **dgfInsider** which states for the insolvent bank property and the creditor claim right.


Features
--------

* Auction consists of 3 stages: Dutch auction, sealed bid and best bid parts.
* The only date Organizer has to provide is a preferable day for the auction, the rest will be calculated automatically. 
* Organizer can't edit procedure's significant properties (*Auction.value*, etc.).
* Bidders can enter the auction till the end of the Dutch part (tenderPeriod.endDate =  auctionPeriod.startDate + Dutch part duration).
* There is obligatory participant qualification (*Bid.selfQualified*) via guarantee payment. It has to be paid till 16:00 of the auction day and submitted by the platform.
* URL for the bidder's participation in auction is generated and sent to the platform right after the platform has denoted (bid.qualified: true) and changed bidder's status to `active`.
* Bids with the `value` mentioned will be rejected.
* *Auction.value* is gradually decreasing per 1% during the Dutch part.
* Bidder can't delete his bid within the first part of the auction.
* The maximum number of steps within the Dutch part is 80. 
* In case of no bid has been made within Dutch auction, the whole procedure will be marked as unsuccessful.
* The `minimalStep` field is optional (value that will be always automatically set is 0). 


Conventions
-----------

API accepts `JSON <http://json.org/>`_ or form-encoded content in
requests.  It returns JSON content in all of its responses, including
errors.  Only the UTF-8 character encoding is supported for both requests
and responses.

All API POST and PUT requests expect a top-level object with a single
element in it named `data`.  Successful responses will mirror this format. 
The data element should itself be an object, containing the parameters for
the request.  In the case of creating a new auction, these are the fields we
want to set on the auction itself.

If the request was successful, we will get a response code of `201`
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new auction,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an `errors` field at the top level
containing a list of problems.  We look at the first one and print out its
message.


Project status
--------------

The project has pre alpha status.

The source repository for this project is on GitHub: 
`<https://github.com/openprocurement/openprocurement.auctions.insider>`_.
 

Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_

API stability
-------------

API is relatively stable. The changes in the API are communicated via 
`Open Procurement API <https://groups.google.com/group/open-procurement-api>`_ 
maillist.


Next steps
----------
You might find it helpful to look at the :ref:`tutorial`.
