"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Asynchronous client for interacting with the ROR API.
Date: 2025-02-17
"""

import asyncio
import logging
from typing import ClassVar, List, Optional

import backoff
import httpx
from pydantic import BaseModel, PrivateAttr

from .models.institution import Institution

logger = logging.getLogger(__name__)


class AsyncRORClient(BaseModel):
    """
    An asynchronous client for interacting with the ROR API.

    Attributes:
        base_url (str): The base URL of the ROR API.
    """

    base_url: ClassVar = "https://api.ror.org/v2/"
    _client: httpx.AsyncClient = PrivateAttr()

    def __init__(self) -> None:
        """Initializes the HTTPX client for connection reuse."""
        super().__init__()
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "User-Agent": "RORClient https://github.com/ADernild/RORClient",
            },
        )

    async def __aenter__(self):
        """Allows the client to be used as an async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensures the HTTPX async client is closed when exiting context."""
        await self._client.aclose()

    async def close(self):
        """Closes the HTTPX async client."""
        await self._client.aclose()

    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, httpx.HTTPStatusError),
        max_time=60,
        on_backoff=lambda details: logger.warning(
            f"Backing off {details.get('wait', 'unknown')} seconds after {details.get('tries', 'unknown')} tries"
        ),
    )
    async def get_institution(self, ror_id: str) -> Optional[Institution]:
        """
        Fetches a single institution by its ROR ID asynchronously.

        Args:
            ror_id (str): The ROR ID of the institution.

        Returns:
            Optional[Institution]: An Institution object if found, otherwise None.

        Raises:
            ValueError: If the response status code is unexpected.
        """
        if not ror_id:
            raise ValueError("ror_id cannot be None or empty")

        logger.debug(f"Fetching institution with ROR ID: {ror_id}")
        response = await self._client.get(f"organizations/{ror_id}")

        if response.status_code == 200:
            return Institution(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Unexpected response: {response.status_code}")

    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, httpx.HTTPStatusError),
        max_time=60,
        on_backoff=lambda details: logger.warning(
            f"Backing off {details.get('wait', 'unknown')} seconds after {details.get('tries', 'unknown')} tries"
        ),
    )
    async def get_multiple_institutions(self, ror_ids: List[str]) -> List[Institution]:
        """
        Fetches multiple institutions by their ROR IDs asynchronously.

        Args:
            ror_ids (List[str]): A list of ROR ID strings.

        Returns:
            List[Institution]: A list of Institution objects.

        Raises:
            ValueError: If the IDs list is empty.
        """
        if not ror_ids:
            raise ValueError("ror_ids cannot be empty")

        logger.debug(f"Fetching multiple institutions: {ror_ids}")

        # Reuse get_institution() instead of a helper function
        tasks = [self.get_institution(ror_id) for ror_id in ror_ids]
        results = await asyncio.gather(*tasks)

        return [result for result in results if result is not None]
