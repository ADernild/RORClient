"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Unit tests for the RORClient models.
"""

from datetime import date

import pytest
from pydantic import HttpUrl, ValidationError

from rorclient.models import Admin, Institution, Location, Relationship


def test_admin_valid_data(valid_admin_data):
    admin = valid_admin_data
    assert admin.created.date == date(2018, 11, 14)
    assert admin.created.schema_version == "1.0"
    assert admin.last_modified.date == date(2024, 12, 11)
    assert admin.last_modified.schema_version == "2.1"


def test_admin_missing_required_field():
    data = {"created": {"date": "2018-11-14", "schema_version": "1.0"}}
    with pytest.raises(ValidationError):
        Admin(**data)  # type: ignore


def test_location_valid_data(valid_locations):
    location = valid_locations[0]
    assert location.geonames_details.name == "Odense"
    assert location.geonames_id == 1234567


def test_location_missing_required_field():
    data = {"geonames_id": 2615876}
    with pytest.raises(ValidationError):
        Location(**data)  # type: ignore


def test_relationship_valid_data(valid_relationships):
    relationship = valid_relationships[0]
    assert relationship.label == "Related Organization"
    assert relationship.type == "related"
    assert relationship.id == HttpUrl("https://ror.org/00aa0aa00")


def test_relationship_missing_required_field():
    data = {"label": "Related Organization", "type": "related"}
    with pytest.raises(ValidationError):
        Relationship(**data)  # type: ignore


def test_institution_valid_data(valid_institution_data):
    institution = valid_institution_data
    assert institution.id == HttpUrl("https://ror.org/00ee0ee00")
    assert institution.status == "active"
    assert len(institution.names) == 4


def test_institution_id_without_prefix(valid_institution_data):
    print(valid_institution_data.id_without_prefix)
    assert valid_institution_data.id_without_prefix == "00ee0ee00"


def test_institution_missing_required_field():
    data = {
        "admin": {
            "created": {"date": "2018-11-14", "schema_version": "1.0"},
            "last_modified": {"date": "2024-12-11", "schema_version": "2.1"},
        },
        "domains": ["sdu.dk"],
        "established": 1998,
        "external_ids": [],
        "links": [],
        "locations": [],
        "names": [],
        "relationships": [],
        "status": "active",
        "types": ["education", "funder"],
    }
    with pytest.raises(ValidationError):
        Institution(**data)
