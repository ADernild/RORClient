from datetime import date

import pytest
from pydantic import HttpUrl

from rorclient.models import (
    Admin,
    AdminCreated,
    AdminLastModified,
    ExternalId,
    GeonamesDetails,
    Institution,
    Link,
    Location,
    Name,
    Relationship,
)


@pytest.fixture
def valid_admin_data_dict():
    return {
        "created": {"date": "2018-11-14", "schema_version": "1.0"},
        "last_modified": {"date": "2024-12-11", "schema_version": "2.1"},
    }


@pytest.fixture
def valid_admin_data(valid_admin_data_dict):
    return Admin(**valid_admin_data_dict)


@pytest.fixture
def valid_external_ids_list():
    return [
        {"type": "GRID", "preferred": None, "all": ["grid.123456.7"]},
        {"type": "isni", "preferred": None, "all": ["1234 1234 1234 1234"]},
        {"type": "wikidata", "preferred": None, "all": ["Q1234567", "Q76543212"]},
    ]


@pytest.fixture
def valid_external_ids(valid_external_ids_list):
    return [ExternalId(**external_id) for external_id in valid_external_ids_list]


@pytest.fixture
def valid_links_list():
    return [
        {"type": "website", "value": "https://www.example.com"},
        {
            "type": "wikipedia",
            "value": "http://en.wikipedia.org/wiki/example",
        },
    ]


@pytest.fixture
def valid_links(valid_links_list):
    return [Link(**link) for link in valid_links_list]


@pytest.fixture
def valid_geonames_details_dict():
    return {
        "continent_code": "EU",
        "continent_name": "Europe",
        "country_code": "DK",
        "country_name": "Denmark",
        "country_subdivision_code": "83",
        "country_subdivision_name": "South Denmark",
        "lat": 58.32141,
        "lng": 10.12345,
        "name": "Odense",
    }


@pytest.fixture
def valid_geonames_details(valid_geonames_details_dict):
    return GeonamesDetails(**valid_geonames_details_dict)


@pytest.fixture
def valid_locations_list(valid_geonames_details_dict):
    return [{"geonames_details": valid_geonames_details_dict, "geonames_id": 1234567}]


@pytest.fixture
def valid_locations(valid_locations_list):
    return [Location(**location) for location in valid_locations_list]


@pytest.fixture
def valid_names_list():
    return [
        {"lang": None, "types": ["acronym"], "value": "EX"},
        {"lang": "en", "types": ["alias"], "value": "Examples"},
        {"lang": "da", "types": ["label"], "value": "Eksempel"},
        {
            "lang": "en",
            "types": ["ror_display", "label"],
            "value": "Example",
        },
    ]


@pytest.fixture
def valid_relationships_list():
    return [
        {
            "label": "Related Organization",
            "type": "related",
            "id": "https://ror.org/00aa0aa00",
            "record": None,
        },
        {
            "label": "Child Organization",
            "type": "child",
            "id": "https://ror.org/00bb0bb00",
            "record": None,
        },
    ]


@pytest.fixture
def valid_relationships(valid_relationships_list):
    return [Relationship(**relationship) for relationship in valid_relationships_list]


@pytest.fixture
def valid_institution_data_dict(
    valid_admin_data_dict,
    valid_external_ids_list,
    valid_links_list,
    valid_locations_list,
    valid_names_list,
    valid_relationships_list,
):
    return {
        "admin": valid_admin_data_dict,
        "domains": ["example.org"],
        "established": 1998,
        "external_ids": valid_external_ids_list,
        "id": "https://ror.org/00ee0ee00",
        "links": valid_links_list,
        "locations": valid_locations_list,
        "names": valid_names_list,
        "relationships": valid_relationships_list,
        "status": "active",
        "types": ["education", "funder"],
    }


@pytest.fixture
def valid_institution_data(valid_institution_data_dict):
    return Institution(**valid_institution_data_dict)


@pytest.fixture
def valid_institution_nested_data_dict(valid_institution_data_dict):
    data = valid_institution_data_dict.copy()
    data["relationships"] = [
        {
            "label": "Related Organization",
            "type": "related",
            "id": "https://ror.org/00aa0aa00",
            "record": valid_institution_data_dict,
        },
        {
            "label": "Child Organization",
            "type": "child",
            "id": "https://ror.org/00bb0bb00",
            "record": valid_institution_data_dict,
        },
    ]
    return data


@pytest.fixture
def valid_institution_nested_data(valid_institution_nested_data_dict):
    return Institution(**valid_institution_nested_data_dict)
