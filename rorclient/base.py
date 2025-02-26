"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Base class for ROR API client.
Date: 2025-02-26
"""

import logging
from abc import ABC, abstractmethod
from typing import Coroutine, Generic, List, Optional, TypeVar, Union

import httpx

from rorclient.config import config
from rorclient.models import Institution

T = TypeVar("T")


class BaseRORClient:
    """
    Base class for ROR clients, encapsulating shared logic.
    """

    def __init__(
        self, prefetch_relationships: bool = False, max_depth: int = 2
    ) -> None:
        """Initializes the shared attributes."""
        self.prefetch_relationships = prefetch_relationships
        self.max_depth = max_depth
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "RORClient https://github.com/ADernild/RORClient",
        }

    def _initialize_client(
        self, client: Union[httpx.Client, httpx.AsyncClient]
    ) -> None:
        """Initializes the HTTP client with shared configuration."""
        client.base_url = str(config.base_url)
        client.headers.update(self.headers)

    def _validate_ror_id(self, ror_id: str) -> None:
        """Validates the ROR ID."""
        if not ror_id:
            raise ValueError("ror_id cannot be None or empty")

    def _validate_ror_ids(self, ror_ids: List[str]) -> None:
        """Validates the list of ROR IDs."""
        if not ror_ids:
            raise ValueError("ror_ids cannot be empty")

    def _process_institution_data(self, institution_data: dict, depth: int) -> dict:
        """Processes institution data to prefetch relationships if needed."""
        if self.prefetch_relationships and depth < self.max_depth:
            institution_data["relationships"] = [
                {
                    **rel,
                    "record": self.get_institution(rel["id"].split("/")[-1], depth + 1),
                }
                for rel in institution_data["relationships"]
            ]
        return institution_data

    @abstractmethod
    def get_institution(
        self, ror_id: str, depth: int = 0
    ) -> Union[T, Coroutine[None, None, T]]:
        """Abstract method to fetch a single institution by its ROR ID."""
        pass
