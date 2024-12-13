import pytest
from unittest.mock import patch, MagicMock
from main import app, big_query_client as app_client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch.object(app_client, 'load_table_from_uri')
@patch.object(app_client, 'get_table')
def test_main_endpoint(mock_get_table, mock_load_table_from_uri, client):
    # Mock load job
    mock_load_job = MagicMock()
    mock_load_table_from_uri.return_value = mock_load_job

    # Mock BigQuery table
    mock_table = MagicMock()
    mock_table.num_rows = 50
    mock_get_table.return_value = mock_table

    # Test the endpoint
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert data['data'] == 50

    # Verify mocks were called
    mock_load_table_from_uri.assert_called_once()
    mock_load_job.result.assert_called_once()
    mock_get_table.assert_called_once()
