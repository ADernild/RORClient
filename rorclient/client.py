"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Synchronous client for interacting with the ROR API.
Date: 2025-02-17
"""

import logging
from typing import ClassVar, List, Optional

import backoff
import httpx
from pydantic import BaseModel, PrivateAttr

from .models.institution import Institution

logger = logging.getLogger(__name__)


class RORClient(BaseModel):
    """
    A client for interacting with the ROR API.

    Attributes:
        base_url (str): The base URL of the ROR API.
    """

    base_url: ClassVar = "https://api.ror.org/v2/"
    _client: httpx.Client = PrivateAttr()

    def __init__(self) -> None:
        """Initializes the HTTPX client for connection reuse."""
        super().__init__()
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
                "User-Agent": "RORClient https://github.com/ADernild/RORClient",
            },
        )

    def __enter__(self):
        """Allows the client to be used as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the HTTPX client is closed when exiting context."""
        self._client.close()

    def close(self):
        """Closes the HTTPX client."""
        self._client.close()

    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, httpx.HTTPStatusError),
        max_time=60,
        on_backoff=lambda details: logger.warning(
            f"Backing off {details.get('wait', 'unknown')} seconds after {details.get('tries', 'unknown')} tries"
        ),
    )
    def get_institution(self, ror_id: str) -> Optional[Institution]:
        """
        Fetches a single institution by its ROR ID.

        Args:
            ror_id (str): The ROR ID of the institution.

        Returns:
            Optional[Institution]: An Institution object if found, otherwise None.

        Raises:
            ValueError: If the ID is None or the response status code is unexpected.
        """
        if not ror_id:
            raise ValueError("ror_id cannot be None or empty")

        logger.debug(f"Fetching institution with ROR ID: {ror_id}")
        response = self._client.get(f"organizations/{ror_id}")

        if response.status_code == 200:
            return Institution(**response.json())
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Got {response.status_code} from ROR")

    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, httpx.HTTPStatusError),
        max_time=60,
        on_backoff=lambda details: logger.warning(
            f"Backing off {details.get('wait', 'unknown')} seconds after {details.get('tries', 'unknown')} tries"
        ),
    )
    def get_multiple_institutions(self, ror_ids: List[str]) -> List[Institution]:
        """
        Fetches multiple institutions by their ROR IDs.

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
        institutions = []
        for ror_id in ror_ids:
            institution = self.get_institution(ror_id)
            if institution:
                institutions.append(institution)

        return institutions
