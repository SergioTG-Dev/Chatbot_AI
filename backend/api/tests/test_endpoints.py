import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_read_citizen():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Crear un ciudadano
        citizen_data = {
            "dni": "12345678",
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        }
        response = await ac.post("/api/v1/citizens/", json=citizen_data)
        assert response.status_code == 201
        created_citizen = response.json()
        assert created_citizen["dni"] == "12345678"

        # Leer el ciudadano por DNI
        response = await ac.get(f"/api/v1/citizens/{created_citizen['dni']}")
        assert response.status_code == 200
        assert response.json()["first_name"] == "Test"

@pytest.mark.asyncio
async def test_create_ticket_with_invalid_dni():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        ticket_data = {
            "citizen_dni": "00000000", # DNI que no existe
            "title": "Bache en la calle",
            "description": "Hay un bache grande",
            "department_id": "some-uuid" # Necesitarías un UUID real de un departamento
        }
        response = await ac.post("/api/v1/tickets/", json=ticket_data)
        assert response.status_code == 404
        assert "Citizen with given DNI not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert "Gestión Gubernamental" in response.json()["message"]