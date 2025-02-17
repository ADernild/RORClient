"""
Copyright (c) 2025 ADernild

Licensed under the MIT License. See LICENSE file in the project root for full license information.

Author: ADernild
Email: alex@dernild.dk
Project: RORClient
Description: Unit tests for the RORClient models.
Date: 2025-02-17
"""

import unittest
from datetime import date

from pydantic import HttpUrl, ValidationError

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


class TestModels(unittest.TestCase):
    def test_admin_created(self):
        admin_created = AdminCreated(date=date(2018, 11, 14), schema_version="1.0")
        self.assertEqual(admin_created.date, date(2018, 11, 14))
        self.assertEqual(admin_created.schema_version, "1.0")

    def test_admin_last_modified(self):
        admin_last_modified = AdminLastModified(
            date=date(2024, 12, 11), schema_version="2.1"
        )
        self.assertEqual(admin_last_modified.date, date(2024, 12, 11))
        self.assertEqual(admin_last_modified.schema_version, "2.1")

    def test_admin(self):
        admin = Admin(
            created=AdminCreated(date=date(2018, 11, 14), schema_version="1.0"),
            last_modified=AdminLastModified(
                date=date(2024, 12, 11), schema_version="2.1"
            ),
        )
        self.assertEqual(admin.created.date, date(2018, 11, 14))
        self.assertEqual(admin.last_modified.date, date(2024, 12, 11))

    def test_external_id(self):
        external_id = ExternalId(all=["501100006356"], preferred=None, type="fundref")
        self.assertEqual(external_id.all, ["501100006356"])
        self.assertIsNone(external_id.preferred)
        self.assertEqual(external_id.type, "fundref")

    def test_link(self):
        link = Link(type="website", value=HttpUrl("https://www.sdu.dk"))
        self.assertEqual(link.type, "website")
        self.assertEqual(link.value, HttpUrl("https://www.sdu.dk"))

    def test_location(self):
        geonames_details = GeonamesDetails(
            continent_code="EU",
            continent_name="Europe",
            country_code="DK",
            country_name="Denmark",
            country_subdivision_code="83",
            country_subdivision_name="South Denmark",
            lat=55.39594,
            lng=10.38831,
            name="Odense",
        )
        location = Location(geonames_details=geonames_details, geonames_id=2615876)
        self.assertEqual(location.geonames_details.name, "Odense")
        self.assertEqual(location.geonames_id, 2615876)

    def test_name(self):
        name = Name(lang=None, types=["acronym"], value="SDU")
        self.assertIsNone(name.lang)
        self.assertEqual(name.types, ["acronym"])
        self.assertEqual(name.value, "SDU")

    def test_relationship(self):
        relationship = Relationship(
            label="Centre for Cosmology and Particle Physics Phenomenology",
            type="child",
            id=HttpUrl("https://ror.org/04y51qn38"),
        )
        self.assertEqual(
            relationship.label,
            "Centre for Cosmology and Particle Physics Phenomenology",
        )
        self.assertEqual(relationship.type, "child")
        self.assertEqual(relationship.id, HttpUrl("https://ror.org/04y51qn38"))
        self.assertEqual(relationship.id_without_prefix, "04y51qn38")

    def test_institution(self):
        institution = Institution(
            admin=Admin(
                created=AdminCreated(date=date(2018, 11, 14), schema_version="1.0"),
                last_modified=AdminLastModified(
                    date=date(2024, 12, 11), schema_version="2.1"
                ),
            ),
            domains=["sdu.dk"],
            established=1998,
            external_ids=[
                ExternalId(all=["501100006356"], preferred=None, type="fundref"),
                ExternalId(
                    all=["grid.10825.3e"], preferred="grid.10825.3e", type="grid"
                ),
                ExternalId(all=["0000 0001 0728 0170"], preferred=None, type="isni"),
                ExternalId(
                    all=["Q2166335", "Q39641498"], preferred="Q2166335", type="wikidata"
                ),
            ],
            id=HttpUrl("https://ror.org/03yrrjy16"),
            links=[
                Link(type="website", value=HttpUrl("https://www.sdu.dk")),
                Link(
                    type="wikipedia",
                    value=HttpUrl(
                        "http://en.wikipedia.org/wiki/University_of_Southern_Denmark"
                    ),
                ),
            ],
            locations=[
                Location(
                    geonames_details=GeonamesDetails(
                        continent_code="EU",
                        continent_name="Europe",
                        country_code="DK",
                        country_name="Denmark",
                        country_subdivision_code="83",
                        country_subdivision_name="South Denmark",
                        lat=55.39594,
                        lng=10.38831,
                        name="Odense",
                    ),
                    geonames_id=2615876,
                )
            ],
            names=[
                Name(lang=None, types=["acronym"], value="SDU"),
                Name(lang="en", types=["alias"], value="South Danish University"),
                Name(lang="da", types=["label"], value="Syddansk Universitet"),
                Name(
                    lang="en",
                    types=["ror_display", "label"],
                    value="University of Southern Denmark",
                ),
            ],
            relationships=[
                Relationship(
                    label="Centre for Cosmology and Particle Physics Phenomenology",
                    type="child",
                    id=HttpUrl("https://ror.org/04y51qn38"),
                ),
                Relationship(
                    label="Bandim Health Project",
                    type="related",
                    id=HttpUrl("https://ror.org/002nf6q61"),
                ),
                Relationship(
                    label="Odense University Hospital",
                    type="related",
                    id=HttpUrl("https://ror.org/00ey0ed83"),
                ),
            ],
            status="active",
            types=["education", "funder"],
        )
        self.assertEqual(institution.id_without_prefix, "03yrrjy16")
        self.assertEqual(institution.status, "active")

    def test_invalid_institution_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            Institution(
                admin=Admin(
                    created=AdminCreated(date=date(2018, 11, 14), schema_version="1.0"),
                    last_modified=AdminLastModified(
                        date=date(2024, 12, 11), schema_version="2.1"
                    ),
                ),
                domains=[],
                established=None,
                external_ids=[],
                id=HttpUrl(""),
                links=[],
                locations=[],
                names=[],
                relationships=[],
                status="active",
                types=[],
            )

    def test_invalid_institution_incorrect_types(self):
        with self.assertRaises(ValidationError):
            Institution(
                admin="invalid",  # type: ignore
                domains="invalid",  # type: ignore
                established="invalid",  # type: ignore
                external_ids="invalid",  # type: ignore
                id="invalid",  # type: ignore
                links="invalid",  # type: ignore
                locations="invalid",  # type: ignore
                names="invalid",  # type: ignore
                relationships="invalid",  # type: ignore
                status=None,  # type: ignore
                types="invalid",  # type: ignore
            )


if __name__ == "__main__":
    unittest.main()
