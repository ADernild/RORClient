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
from pydantic import BaseModel

from .models.institution import Institution

logger = logging.getLogger(__name__)


class RORClient(BaseModel):
    """
    A client for interacting with the ROR API.

    Attributes:
        base_url (str): The base URL of the ROR API.
    """

    base_url: ClassVar = "https://api.ror.org/v2/"

    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, httpx.HTTPStatusError),
        max_time=60,
        on_backoff=lambda details: logger.warning(
            f"Backing off {details.get('wait', 'unknown')} seconds after {details.get('tries', 'unknown')} tries"
        ),
    )
    def get_institution(self, id: str) -> Optional[Institution]:
        """
        Fetches a single institution by its ROR ID.

        Args:
            id (str): The ROR ID of the institution.

        Returns:
            Optional[Institution]: An Institution object if found, otherwise None.

        Raises:
            ValueError: If the ID is None or the response status code is not 200 or 404.
        """
        if id is None:
            raise ValueError("id was None")
        url = f"{self.base_url}organizations/{id}"
        logger.debug(f"Fetching {url}")
        headers = {
            "Accept": "application/json",
            "User-Agent": "RORClient https://github.com/ADernild/RORClient",
        }
        response = httpx.get(url, headers=headers)
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
    def get_multiple_institutions(self, ids: List[str]) -> List[Institution]:
        """
        Fetches multiple institutions by their ROR IDs.

        Args:
            ids (List[str]): A list of ROR ID strings.

        Returns:
            List[Institution]: A list of Institution objects.

        Raises:
            ValueError: If the IDs list is empty.
        """
        if len(ids) == 0:
            raise ValueError("ids cannot be empty")
        headers = {
            "Accept": "application/json",
            "User-Agent": "RORClient https://github.com/ADernild/RORClient",
        }
        institutions = []
        for id in ids:
            institution = self.get_institution(id)
            if institution:
                institutions.append(institution)
        return institutions
