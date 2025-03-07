import pytest

from rorclient.base import BaseRORClient


def test_validate_ror_id():
    client = BaseRORClient()
    valid_ror_id = "01cwqze88"
    client._validate_ror_id(valid_ror_id)  # Should not raise an exception

    invalid_ror_id = "invalid_id"
    with pytest.raises(ValueError):
        client._validate_ror_id(invalid_ror_id)


def test_extract_ror_id():
    client = BaseRORClient()
    url = "https://ror.org/01cwqze88"
    extracted_id = client._extract_ror_id(url)
    assert extracted_id == "01cwqze88"

    ror_id = "01cwqze88"
    extracted_id = client._extract_ror_id(ror_id)
    assert extracted_id == "01cwqze88"


def test_process_institution_data(mocker):
    client = BaseRORClient(prefetch_relationships=True)
    institution_data = {
        "relationships": [
            {
                "id": "https://ror.org/related",
                "type": "related",
                "label": "Related Organization",
            }
        ]
    }

    # Mock the get_institution method
    mock_get_institution = mocker.patch.object(
        client, "get_institution", return_value="Mocked Institution"
    )

    processed_data = client._process_institution_data(institution_data, depth=0)
    assert processed_data["relationships"][0]["record"] == "Mocked Institution"
    mock_get_institution.assert_called_once_with("related", 1)
