# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.core.config import settings

@pytest.fixture(scope="module")
def client():
    """
    Fixture que proporciona un cliente de prueba para la API FastAPI.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_supabase_client():
    """
    Fixture que simula el cliente de Supabase para evitar llamadas a la BD real.
    """
    with patch("app.db.supabase_client.get_supabase_client") as mock_client:
        # Creamos un mock que imita la estructura de respuesta de Supabase
        mock_instance = MagicMock()
        mock_instance.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": "test-id"}])
        mock_instance.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        mock_instance.rpc.return_value.execute.return_value = MagicMock(data="guest")
        mock_client.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_user_token_headers():
    """
    Fixture que proporciona un token JWT simulado y los encabezados de autenticación.
    """
    # En un caso real, este token sería generado por Supabase.
    # Para pruebas, podemos usar un token dummy que no será validado si mockeamos `get_current_user`.
    # Sin embargo, es mejor simular la validación.
    dummy_payload = {"sub": "test-user-id", "email": "test@example.com", "role": "authenticated"}
    
    # Importamos aquí para evitar dependencias circulares
    from jose import jwt
    from app.core.config import settings
    
    dummy_token = jwt.encode(dummy_payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
    
    return {"Authorization": f"Bearer {dummy_token}"}

@pytest.fixture
def mock_current_user(mock_user_token_headers):
    """
    Fixture que simula la dependencia `get_current_user` para devolver un usuario de prueba.
    """
    with patch("app.core.security.get_current_user") as mock_user:
        mock_user.return_value = {"id": "test-user-id", "email": "test@example.com"}
        yield mock_user