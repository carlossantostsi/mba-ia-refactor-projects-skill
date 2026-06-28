from flask import jsonify, request
from services.store_service import authenticate_user, create_user, get_user_by_id, list_users


def listar_usuarios():
    try:
        usuarios = list_users()
        return jsonify({"dados": usuarios, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def buscar_usuario(user_id):
    try:
        usuario = get_user_by_id(user_id)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True}), 200
        return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def criar_usuario():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        nome = dados.get("nome", "")
        email = dados.get("email", "")
        senha = dados.get("senha", "")
        if not nome or not email or not senha:
            return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400
        user_id = create_user(nome, email, senha)
        return jsonify({"dados": {"id": user_id}, "sucesso": True}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def login():
    try:
        dados = request.get_json()
        email = dados.get("email", "") if dados else ""
        senha = dados.get("senha", "") if dados else ""
        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400
        usuario = authenticate_user(email, senha)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
        return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
