from unittest.mock import MagicMock, patch

import pytest

from rorclient.client import RORClient
from rorclient.models import Institution


@pytest.fixture
def mock_httpx_client():
    with patch("rorclient.client.httpx.Client") as MockClient:
        client = MockClient.return_value
        yield client


@pytest.fixture
def ror_client(mock_httpx_client):
    return RORClient(prefetch_relationships=False, max_depth=0)


@pytest.fixture
def ror_client_prefetch(mock_httpx_client):
    return RORClient(prefetch_relationships=True, max_depth=1)


def test_get_institution_success(
    ror_client, mock_httpx_client, valid_institution_data_dict, valid_institution_data
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = valid_institution_data_dict

    mock_httpx_client.get.return_value = mock_response
    print(mock_response)

    institution = ror_client.get_institution("00ee0ee00")
    assert institution == valid_institution_data


def test_get_institution_nested_success(
    ror_client_prefetch,
    mock_httpx_client,
    valid_institution_data_dict,
    valid_institution_nested_data,
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = valid_institution_data_dict

    mock_httpx_client.get.return_value = mock_response
    print(mock_response)

    institution = ror_client_prefetch.get_institution("00ee0ee00")
    assert institution == valid_institution_nested_data


def test_get_institution_not_found(ror_client, mock_httpx_client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_httpx_client.get.return_value = mock_response

    institution = ror_client.get_institution("02abcde99")
    assert institution is None


def test_get_institution_error(ror_client, mock_httpx_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_httpx_client.get.return_value = mock_response

    with pytest.raises(ValueError):
        ror_client.get_institution("invalid_id")


def test_get_multiple_institutions_success(
    ror_client, mock_httpx_client, valid_institution_data_dict, valid_institution_data
):
    mock_responses = [
        MagicMock(status_code=200, json=lambda: valid_institution_data_dict)
        for _ in range(3)
    ]
    mock_httpx_client.get.side_effect = mock_responses

    institutions = ror_client.get_multiple_institutions(
        ["00ee0ee00", "00ee0ee00", "00ee0ee00"]
    )
    assert len(institutions) == 3
    for institution in institutions:
        assert institution == valid_institution_data


def test_get_multiple_institutions_not_found(ror_client, mock_httpx_client):
    mock_responses = [MagicMock(status_code=404) for _ in range(2)]
    mock_httpx_client.get.side_effect = mock_responses

    institutions = ror_client.get_multiple_institutions(["00ee0ee00", "00ee0ee00"])
    assert len(institutions) == 0


def test_get_multiple_institutions_error(ror_client, mock_httpx_client):
    mock_response = MagicMock(status_code=500)
    mock_httpx_client.get.return_value = mock_response

    with pytest.raises(ValueError):
        ror_client.get_multiple_institutions(["invalid_id"])
