Advanced Usage
==============

This section provides more detailed information on advanced features of the RORClient, including the use of the `prefetch_relationships` flag and the `max_depth` parameter.

Prefetching Relationships
-------------------------

The `prefetch_relationships` flag allows you to automatically fetch related data when making API calls. When set to `True`, the client will retrieve additional information about institutions, such as their relationships with other organizations, affiliations, and more. This means that if an institution has related institutions, those related institutions' records will be fetched and nested within the main institution's record.

### Example

Consider an institution with ROR ID "04x81pg59" that has a relationship with another institution with ROR ID "03y42pg52". When `prefetch_relationships` is set to `True`, the client will fetch and nest the related institution's record within the main institution's record.

.. code-block:: python

   from rorclient import RORClient

   # Initialize the synchronous client with prefetch_relationships enabled
   with RORClient(prefetch_relationships=True) as client:
       institution = client.get_institution("04x81pg59")
       print(institution)

In this example, `institution` will contain a nested record for the related institution with ROR ID "03y42pg52".

Max Depth
---------

The `max_depth` parameter controls the depth of nested relationships that are fetched when using the `prefetch_relationships` flag. A higher `max_depth` value allows the client to retrieve more levels of related data, but it may also increase the response time and data size.

### Example

Consider an institution with ROR ID "04x81pg59" that has a relationship with another institution with ROR ID "03y42pg52", which in turn has a relationship with yet another institution with ROR ID "02z53pg53". By default, `max_depth` is set to 2. This means the client will fetch up to two levels of related data.

.. code-block:: python

   from rorclient import RORClient

   # Initialize the synchronous client with prefetch_relationships enabled and max_depth set to 2
   with RORClient(prefetch_relationships=True, max_depth=2) as client:
       institution = client.get_institution("04x81pg59")
       print(institution)

In this example, `institution` will contain a nested record for the related institution with ROR ID "03y42pg52", and that record will also contain a nested record for the related institution with ROR ID "02z53pg53".

If you set `max_depth` to 1, only the first level of relationships will be fetched:

.. code-block:: python

   from rorclient import RORClient

   # Initialize the synchronous client with prefetch_relationships enabled and max_depth set to 1
   with RORClient(prefetch_relationships=True, max_depth=1) as client:
       institution = client.get_institution("04x81pg59")
       print(institution)

In this case, `institution` will contain a nested record for the related institution with ROR ID "03y42pg52", but that record will not contain any further nested records.

.. admonition:: Considerations

    - **Performance**: Higher values for `max_depth` can lead to longer response times and larger data payloads.
    - **Use Case**: Choose a `max_depth` that suits your application's needs. For applications requiring only basic information, a lower `max_depth` is recommended.

These advanced features provide flexibility in how you interact with the ROR API, allowing you to tailor the data retrieval process to your specific requirements.
