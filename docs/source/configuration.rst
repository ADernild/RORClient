Configuration
=============

The RORClient library allows you to configure various settings to customize its behavior. Below are some examples of how to configure the client for different use cases.

Base Configuration
------------------

To get started, you can optionally configure the base URL and retry settings. Here's an example if you want to change these values:

.. code-block:: python

   from rorclient.config import config

   # Set the base URL for the ROR API
   config.base_url = "https://api.ror.org/v2/"

   # Set the maximum retry time and number of retries
   config.max_retry_time = 60  # seconds
   config.max_retries = 5

Customizing Retry Behavior
--------------------------

You can customize the retry behavior by adjusting the ``max_retry_time`` and ``max_retries`` parameters. For example, if you want to increase the number of retries:

.. code-block:: python

   config.max_retries = 10

This configuration will make the client attempt to retry failed requests up to 10 times before giving up.

Custom Base URL for Self-Hosted Instances
-----------------------------------------

If you are hosting your own local instance of the ROR API (using `ROR API GitHub repository <https://github.com/ror-community/ror-api>`_), you can change the ``base_url`` to point to your local instance. Here's an example:

.. code-block:: python

   from rorclient.config import config

   # Set the base URL for your self-hosted ROR API
   config.base_url = "http://localhost:3000/v2/"

By setting the ``base_url``, you can tailor the RORClient library to work with your privately hosted instance.
