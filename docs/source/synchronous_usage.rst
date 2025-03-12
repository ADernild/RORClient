Synchronous API Calls
=====================

The synchronous client allows you to make API calls to the ROR API in a blocking manner. This is useful for applications that do not require asynchronous operations.

Initializing the Synchronous Client
-----------------------------------

To initialize the synchronous client, you can use either of the following methods:

Method 1: Using `with`
^^^^^^^^^^^^^^^^^^^^^^

Using the `with` statement ensures proper resource management and context handling by automatically closing the client when done:

.. code-block:: python

   from rorclient import RORClient

   with RORClient() as client:
       # Fetch an institution
       institution = client.get_institution("04x81pg59")
       print(institution)

       # Fetch multiple institutions
       institutions = client.get_multiple_institutions(["04x81pg59", "03y42pg52"])
       for inst in institutions:
           print(inst)

Method 2: Direct Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also initialize the client directly and manually close it when done:

.. code-block:: python

   from rorclient import RORClient

   client = RORClient()

   try:
       # Fetch an institution
       institution = client.get_institution("04x81pg59")
       print(institution)

       # Fetch multiple institutions
       institutions = client.get_multiple_institutions(["04x81pg59", "03y42pg52"])
       for inst in institutions:
           print(inst)
   finally:
       client.close()  # Manually close the client

Fetching an Institution
-----------------------

You can fetch an institution by its ROR ID using the ``get_institution`` method. This is demonstrated in the examples above.

Fetching Multiple Institutions
------------------------------

To fetch multiple institutions by their ROR IDs, use the ``get_multiple_institutions`` method. This is also demonstrated in the examples above.

These examples demonstrate how to use the synchronous client to interact with the ROR API.
