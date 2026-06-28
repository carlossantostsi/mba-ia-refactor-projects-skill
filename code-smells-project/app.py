from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from database import get_db
from controllers import (
    buscar_produto,
    buscar_produtos,
    criar_pedido,
    criar_produto,
    criar_usuario,
    deletar_produto,
    health_check,
    listar_pedidos_usuario,
    listar_produtos,
    listar_todos_pedidos,
    listar_usuarios,
    login,
    relatorio_vendas,
    atualizar_produto,
    atualizar_status_pedido,
    buscar_usuario,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["DEBUG"] = Config.DEBUG
CORS(app)

app.add_url_rule("/produtos", "listar_produtos", listar_produtos, methods=["GET"])
app.add_url_rule("/produtos/busca", "buscar_produtos", buscar_produtos, methods=["GET"])
app.add_url_rule("/produtos/<int:id>", "buscar_produto", buscar_produto, methods=["GET"])
app.add_url_rule("/produtos", "criar_produto", criar_produto, methods=["POST"])
app.add_url_rule("/produtos/<int:id>", "atualizar_produto", atualizar_produto, methods=["PUT"])
app.add_url_rule("/produtos/<int:id>", "deletar_produto", deletar_produto, methods=["DELETE"])

app.add_url_rule("/usuarios", "listar_usuarios", listar_usuarios, methods=["GET"])
app.add_url_rule("/usuarios/<int:id>", "buscar_usuario", buscar_usuario, methods=["GET"])
app.add_url_rule("/usuarios", "criar_usuario", criar_usuario, methods=["POST"])
app.add_url_rule("/login", "login", login, methods=["POST"])

app.add_url_rule("/pedidos", "criar_pedido", criar_pedido, methods=["POST"])
app.add_url_rule("/pedidos", "listar_todos_pedidos", listar_todos_pedidos, methods=["GET"])
app.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", listar_pedidos_usuario, methods=["GET"])
app.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", atualizar_status_pedido, methods=["PUT"])

app.add_url_rule("/relatorios/vendas", "relatorio_vendas", relatorio_vendas, methods=["GET"])
app.add_url_rule("/health", "health_check", health_check, methods=["GET"])


@app.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health",
        },
    })


@app.route("/admin/reset-db", methods=["POST"])
def reset_database():
    from services.store_service import reset_database as reset_store_database

    reset_store_database()
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200


@app.route("/admin/query", methods=["POST"])
def executar_query():
    dados = request.get_json() or {}
    query = dados.get("sql", "")
    if not query:
        return jsonify({"erro": "Query não informada"}), 400

    try:
        from services.store_service import execute_query

        result = execute_query(query)
        return jsonify({"dados": result, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    get_db()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
