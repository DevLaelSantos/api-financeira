def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "teste@teste.com", "password": "senha12345"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "teste@teste.com"
    assert "password" not in response.json() # Garante que a senha não vaze

def test_register_duplicate_user(client):
    # Tenta registrar o mesmo usuário de novo
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "teste@teste.com", "password": "senha12345"}
    )
    assert response.status_code == 400 # Erro esperado: E-mail já cadastrado