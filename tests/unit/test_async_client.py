import asyncio
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from rorclient.async_client import AsyncRORClient
from rorclient.models import Institution


@pytest.fixture
def async_ror_client():
    return AsyncRORClient(prefetch_relationships=False, max_depth=0)


@pytest.mark.asyncio
async def test_get_institution_success(
    async_ror_client,
    valid_institution_data_dict,
    valid_institution_data,
):
    mock_response = httpx.Response(200)
    mock_response.json = AsyncMock(return_value=valid_institution_data_dict)

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        institution = await async_ror_client.get_institution("01cwqze88")
        assert institution == valid_institution_data


@pytest.mark.asyncio
async def test_get_institution_not_found(async_ror_client):
    mock_response = httpx.Response(404)

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        institution = await async_ror_client.get_institution("01cwqze88")
        assert institution is None


@pytest.mark.asyncio
async def test_get_institution_error(async_ror_client):
    mock_response = httpx.Response(500)
    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        with pytest.raises(ValueError):
            await async_ror_client.get_institution("invalid_id")


@pytest.mark.asyncio
async def test_get_multiple_institutions_success(
    async_ror_client,
    valid_institution_data,
    valid_institution_data_dict,
):
    mock_response = httpx.Response(200)
    mock_response.json = AsyncMock(return_value=valid_institution_data_dict)

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        institutions = await async_ror_client.get_multiple_institutions(
            ["01cwqze88", "01cwqze88"]
        )
        assert len(institutions) == 2
        assert institutions[0] == valid_institution_data


@pytest.mark.asyncio
async def test_get_multiple_institutions_error(async_ror_client):
    mock_response = httpx.Response(500)

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        with pytest.raises(ValueError):
            await async_ror_client.get_multiple_institutions(["invalid_id"])
