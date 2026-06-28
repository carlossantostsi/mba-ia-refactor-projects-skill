from flask import jsonify, request
from services.store_service import create_order, list_all_orders, list_orders_for_user, sales_report, update_order_status


def criar_pedido():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])
        if not usuario_id:
            return jsonify({"erro": "Usuario ID é obrigatório"}), 400
        if not itens or len(itens) == 0:
            return jsonify({"erro": "Pedido deve ter pelo menos 1 item"}), 400
        resultado = create_order(usuario_id, itens)
        if "erro" in resultado:
            return jsonify({"erro": resultado["erro"], "sucesso": False}), 400
        return jsonify({"dados": resultado, "sucesso": True, "mensagem": "Pedido criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def listar_pedidos_usuario(usuario_id):
    try:
        pedidos = list_orders_for_user(usuario_id)
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def listar_todos_pedidos():
    try:
        pedidos = list_all_orders()
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def atualizar_status_pedido(pedido_id):
    try:
        dados = request.get_json()
        novo_status = dados.get("status", "")
        if novo_status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
            return jsonify({"erro": "Status inválido"}), 400
        update_order_status(pedido_id, novo_status)
        return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def relatorio_vendas():
    try:
        relatorio = sales_report()
        return jsonify({"dados": relatorio, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
