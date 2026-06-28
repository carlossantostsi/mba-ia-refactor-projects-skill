from database import get_db
from config import Config


def _product_from_row(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"],
    }


def _user_from_row(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "senha": row["senha"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }


def _order_from_row(row, db):
    pedido = {
        "id": row["id"],
        "usuario_id": row["usuario_id"],
        "status": row["status"],
        "total": row["total"],
        "criado_em": row["criado_em"],
        "itens": [],
    }
    cursor = db.cursor()
    cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (row["id"],))
    itens = cursor.fetchall()
    for item in itens:
        cursor2 = db.cursor()
        cursor2.execute("SELECT nome FROM produtos WHERE id = ?", (item["produto_id"],))
        prod = cursor2.fetchone()
        pedido["itens"].append(
            {
                "produto_id": item["produto_id"],
                "produto_nome": prod["nome"] if prod else "Desconhecido",
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"],
            }
        )
    return pedido


def list_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos ORDER BY id")
    rows = cursor.fetchall()
    return [_product_from_row(row) for row in rows]


def get_product_by_id(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    return _product_from_row(row) if row else None


def create_product(nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria),
    )
    db.commit()
    return cursor.lastrowid


def update_product(product_id, nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
        (nome, descricao, preco, estoque, categoria, product_id),
    )
    db.commit()
    return True


def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    db.commit()
    return True


def list_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios ORDER BY id")
    rows = cursor.fetchall()
    return [_user_from_row(row) for row in rows]


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return _user_from_row(row) if row else None


def authenticate_user(email, senha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    row = cursor.fetchone()
    if row:
        return {"id": row["id"], "nome": row["nome"], "email": row["email"], "tipo": row["tipo"]}
    return None


def create_user(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, senha, tipo),
    )
    db.commit()
    return cursor.lastrowid


def create_order(usuario_id, itens):
    db = get_db()
    cursor = db.cursor()

    total = 0.0
    for item in itens:
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
        produto = cursor.fetchone()
        if produto is None:
            return {"erro": f"Produto {item['produto_id']} não encontrado"}
        if produto["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {produto['nome']}"}
        total += produto["preco"] * item["quantidade"]

    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total),
    )
    pedido_id = cursor.lastrowid

    for item in itens:
        cursor.execute("SELECT preco FROM produtos WHERE id = ?", (item["produto_id"],))
        produto = cursor.fetchone()
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
            (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
        )
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    db.commit()
    return {"pedido_id": pedido_id, "total": total}


def list_orders_for_user(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY id", (usuario_id,))
    rows = cursor.fetchall()
    return [_order_from_row(row, db) for row in rows]


def list_all_orders():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pedidos ORDER BY id")
    rows = cursor.fetchall()
    return [_order_from_row(row, db) for row in rows]


def sales_report():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0]

    desconto = 0
    if faturamento > 10000:
        desconto = faturamento * 0.1
    elif faturamento > 5000:
        desconto = faturamento * 0.05
    elif faturamento > 1000:
        desconto = faturamento * 0.02

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
    }


def update_order_status(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    db.commit()
    return True


def search_products(termo, categoria=None, preco_min=None, preco_max=None):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []
    if termo:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        params.extend([f"%{termo}%", f"%{termo}%"])
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    if preco_min is not None:
        query += " AND preco >= ?"
        params.append(preco_min)
    if preco_max is not None:
        query += " AND preco <= ?"
        params.append(preco_max)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [_product_from_row(row) for row in rows]


def reset_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    return True


def execute_query(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    if query.strip().upper().startswith("SELECT"):
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    db.commit()
    return []


def get_health_summary():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]

    return {
        "status": "ok",
        "database": "connected",
        "counts": {"produtos": produtos, "usuarios": usuarios, "pedidos": pedidos},
        "versao": "1.0.0",
        "ambiente": "producao",
        "db_path": Config.DB_PATH,
        "debug": Config.DEBUG,
        "secret_key": Config.SECRET_KEY,
    }
