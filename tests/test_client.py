import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from asyncari.client import Client
from asyncari.model import Channel, Bridge, Playback, LiveRecording, StoredRecording, Endpoint, DeviceState, Sound

@pytest.fixture
def mock_taskgroup():
    return MagicMock()

@pytest.fixture
def mock_http_client():
    return MagicMock()

@pytest.fixture
def client(mock_taskgroup, mock_http_client):
    return Client(mock_taskgroup, "http://localhost:8088/", ["test_app"], mock_http_client)

@pytest.mark.asyncio
async def test_client_initialization(client):
    assert client.base_url == "http://localhost:8088/"
    assert client._apps == ["test_app"]
    assert client.taskgroup is not None
    assert client.swagger is not None

@pytest.mark.asyncio
async def test_client_generate_id(client):
    client._id_seq = 0
    generated_id = client.generate_id("test")
    assert generated_id.startswith("ARI.")
    assert generated_id.endswith(".test1")

@pytest.mark.asyncio
async def test_client_is_my_id(client):
    client._id_name = "ARI.test"
    assert client.is_my_id("ARI.test")
    assert client.is_my_id("ARI.test.1")
    assert not client.is_my_id("ARI.other")

@pytest.mark.asyncio
async def test_client_connect(client):
    with patch("asyncari.client.AsynchronousHttpClient") as mock_http_client:
        mock_http_client.return_value = AsyncMock()
        async with client.connect("http://localhost:8088/", "test_app", "username", "password") as ari_client:
            assert isinstance(ari_client, Client)

@pytest.mark.asyncio
async def test_client_close(client):
    client.swagger.close = AsyncMock()
    await client.close()
    client.swagger.close.assert_called_once()

@pytest.mark.asyncio
async def test_client_get_repo(client):
    client.repositories = {"test_repo": "test_value"}
    assert client.get_repo("test_repo") == "test_value"
    assert client.get_repo("non_existent_repo") is None

@pytest.mark.asyncio
async def test_client_on_event(client):
    handler = client.on_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client

@pytest.mark.asyncio
async def test_client_on_object_event(client):
    handler = client.on_object_event("test_event", Channel, "Channel")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_channel_event(client):
    handler = client.on_channel_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_bridge_event(client):
    handler = client.on_bridge_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_playback_event(client):
    handler = client.on_playback_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_live_recording_event(client):
    handler = client.on_live_recording_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_stored_recording_event(client):
    handler = client.on_stored_recording_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_endpoint_event(client):
    handler = client.on_endpoint_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_device_state_event(client):
    handler = client.on_device_state_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None

@pytest.mark.asyncio
async def test_client_on_sound_event(client):
    handler = client.on_sound_event("test_event")
    assert handler.event_type == "test_event"
    assert handler.client == client
    assert handler.mangler is not None
