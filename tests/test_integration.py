import pytest
from unittest.mock import AsyncMock, patch
import asyncari

@pytest.fixture
def mock_client():
    with patch("asyncari.connect") as mock_connect:
        mock_connect.return_value = AsyncMock()
        yield mock_connect

@pytest.mark.asyncio
async def test_integration_connect(mock_client):
    async with asyncari.connect("http://localhost:8088/", "test_app", "username", "password") as client:
        assert client is not None
        assert client.base_url == "http://localhost:8088/"
        assert client._apps == ["test_app"]

@pytest.mark.asyncio
async def test_integration_authentication(mock_client):
    async with asyncari.connect("http://localhost:8088/", "test_app", "username", "password") as client:
        assert client.swagger.http_client.auth.username == "username"
        assert client.swagger.http_client.auth.password == "password"

@pytest.mark.asyncio
async def test_integration_api_calls(mock_client):
    async with asyncari.connect("http://localhost:8088/", "test_app", "username", "password") as client:
        client.swagger.channels.list = AsyncMock(return_value=[])
        channels = await client.swagger.channels.list()
        assert channels == []
        client.swagger.bridges.list = AsyncMock(return_value=[])
        bridges = await client.swagger.bridges.list()
        assert bridges == []
        client.swagger.endpoints.list = AsyncMock(return_value=[])
        endpoints = await client.swagger.endpoints.list()
        assert endpoints == []
