Asynchronous API Calls
======================

The asynchronous client allows you to make API calls to the ROR API in a non-blocking manner. This is useful for applications that require concurrent operations.

Initializing the Asynchronous Client
------------------------------------

To initialize the asynchronous client, you can use either of the following methods:

Method 1: Using `async with`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the `async with` statement ensures proper resource management and context handling by automatically closing the client when done:

.. code-block:: python

   from rorclient import AsyncRORClient
   import asyncio

   async def main():
       async with AsyncRORClient() as client:
           # Fetch an institution
           institution = await client.get_institution("04x81pg59")
           print(institution)

           # Fetch multiple institutions
           institutions = await client.get_multiple_institutions(["04x81pg59", "03y42pg52"])
           for inst in institutions:
               print(inst)

   asyncio.run(main())

Method 2: Direct Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also initialize the client directly and manually close it when done:

.. code-block:: python

   from rorclient import AsyncRORClient
   import asyncio

   async def main():
       client = AsyncRORClient()

       try:
           # Fetch an institution
           institution = await client.get_institution("04x81pg59")
           print(institution)

           # Fetch multiple institutions
           institutions = await client.get_multiple_institutions(["04x81pg59", "03y42pg52"])
           for inst in institutions:
               print(inst)
       finally:
           await client.close()  # Manually close the client

   asyncio.run(main())

Fetching an Institution
-----------------------

You can fetch an institution by its ROR ID using the ``get_institution`` method. This is demonstrated in the examples above.

Fetching Multiple Institutions
------------------------------

To fetch multiple institutions by their ROR IDs, use the ``get_multiple_institutions`` method. This is also demonstrated in the examples above.

These examples demonstrate how to use the asynchronous client to interact with the ROR API.
