"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Unit tests for the RORClient asynchronous client.
Date: 2025-02-17
"""

import asyncio
import unittest
from unittest.mock import MagicMock, patch

from pydantic import HttpUrl

from rorclient.async_client import AsyncRORClient
from rorclient.models.institution import Institution


class TestAsyncRORClient(unittest.TestCase):
    @patch("httpx.AsyncClient.get")
    def test_get_institution(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "admin": {
                "created": {"date": "2018-11-14", "schema_version": "1.0"},
                "last_modified": {"date": "2024-12-11", "schema_version": "2.1"},
            },
            "domains": ["sdu.dk"],
            "established": 1998,
            "external_ids": [
                {"all": ["501100006356"], "preferred": None, "type": "fundref"},
                {
                    "all": ["grid.10825.3e"],
                    "preferred": "grid.10825.3e",
                    "type": "grid",
                },
                {"all": ["0000 0001 0728 0170"], "preferred": None, "type": "isni"},
                {
                    "all": ["Q2166335", "Q39641498"],
                    "preferred": "Q2166335",
                    "type": "wikidata",
                },
            ],
            "id": "https://ror.org/03yrrjy16",
            "links": [
                {"type": "website", "value": "https://www.sdu.dk"},
                {
                    "type": "wikipedia",
                    "value": "http://en.wikipedia.org/wiki/University_of_Southern_Denmark",
                },
            ],
            "locations": [
                {
                    "geonames_details": {
                        "continent_code": "EU",
                        "continent_name": "Europe",
                        "country_code": "DK",
                        "country_name": "Denmark",
                        "country_subdivision_code": "83",
                        "country_subdivision_name": "South Denmark",
                        "lat": 55.39594,
                        "lng": 10.38831,
                        "name": "Odense",
                    },
                    "geonames_id": 2615876,
                }
            ],
            "names": [
                {"lang": None, "types": ["acronym"], "value": "SDU"},
                {"lang": "en", "types": ["alias"], "value": "South Danish University"},
                {"lang": "da", "types": ["label"], "value": "Syddansk Universitet"},
                {
                    "lang": "en",
                    "types": ["ror_display", "label"],
                    "value": "University of Southern Denmark",
                },
            ],
            "relationships": [
                {
                    "label": "Centre for Cosmology and Particle Physics Phenomenology",
                    "type": "child",
                    "id": "https://ror.org/04y51qn38",
                },
                {
                    "label": "Bandim Health Project",
                    "type": "related",
                    "id": "https://ror.org/002nf6q61",
                },
                {
                    "label": "Odense University Hospital",
                    "type": "related",
                    "id": "https://ror.org/00ey0ed83",
                },
            ],
            "status": "active",
            "types": ["education", "funder"],
        }
        mock_get.return_value = mock_response

        client = AsyncRORClient()
        institution = asyncio.run(client.get_institution("03yrrjy16"))

        if institution is None:
            self.fail("Institution should not be None")

        self.assertIsInstance(institution, Institution)
        self.assertEqual(institution.id, HttpUrl("https://ror.org/03yrrjy16"))
        self.assertEqual(institution.status, "active")

    @patch("httpx.AsyncClient.get")
    def test_get_institution_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = AsyncRORClient()
        institution = asyncio.run(client.get_institution("03yrrjy16"))

        self.assertIsNone(institution)

    @patch("httpx.AsyncClient.get")
    def test_get_multiple_institutions(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "admin": {
                "created": {"date": "2018-11-14", "schema_version": "1.0"},
                "last_modified": {"date": "2024-12-11", "schema_version": "2.1"},
            },
            "domains": ["sdu.dk"],
            "established": 1998,
            "external_ids": [
                {"all": ["501100006356"], "preferred": None, "type": "fundref"},
                {
                    "all": ["grid.10825.3e"],
                    "preferred": "grid.10825.3e",
                    "type": "grid",
                },
                {"all": ["0000 0001 0728 0170"], "preferred": None, "type": "isni"},
                {
                    "all": ["Q2166335", "Q39641498"],
                    "preferred": "Q2166335",
                    "type": "wikidata",
                },
            ],
            "id": "https://ror.org/03yrrjy16",
            "links": [
                {"type": "website", "value": "https://www.sdu.dk"},
                {
                    "type": "wikipedia",
                    "value": "http://en.wikipedia.org/wiki/University_of_Southern_Denmark",
                },
            ],
            "locations": [
                {
                    "geonames_details": {
                        "continent_code": "EU",
                        "continent_name": "Europe",
                        "country_code": "DK",
                        "country_name": "Denmark",
                        "country_subdivision_code": "83",
                        "country_subdivision_name": "South Denmark",
                        "lat": 55.39594,
                        "lng": 10.38831,
                        "name": "Odense",
                    },
                    "geonames_id": 2615876,
                }
            ],
            "names": [
                {"lang": None, "types": ["acronym"], "value": "SDU"},
                {"lang": "en", "types": ["alias"], "value": "South Danish University"},
                {"lang": "da", "types": ["label"], "value": "Syddansk Universitet"},
                {
                    "lang": "en",
                    "types": ["ror_display", "label"],
                    "value": "University of Southern Denmark",
                },
            ],
            "relationships": [
                {
                    "label": "Centre for Cosmology and Particle Physics Phenomenology",
                    "type": "child",
                    "id": "https://ror.org/04y51qn38",
                },
                {
                    "label": "Bandim Health Project",
                    "type": "related",
                    "id": "https://ror.org/002nf6q61",
                },
                {
                    "label": "Odense University Hospital",
                    "type": "related",
                    "id": "https://ror.org/00ey0ed83",
                },
            ],
            "status": "active",
            "types": ["education", "funder"],
        }
        mock_get.return_value = mock_response

        client = AsyncRORClient()
        institutions = asyncio.run(
            client.get_multiple_institutions(["03yrrjy16", "04y51qn38"])
        )

        self.assertEqual(len(institutions), 2)
        self.assertIsInstance(institutions[0], Institution)
        self.assertIsInstance(institutions[1], Institution)


if __name__ == "__main__":
    unittest.main()
