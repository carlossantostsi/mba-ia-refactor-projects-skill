# Playbook de Refatoração — Before / After

## 1. God Class / God Method
Before:
```python
# app.py
@app.route('/produtos')
def listar_produtos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM produtos')
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])
```
After:
```python
# routes/produto_routes.py
@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    return produto_controller.listar_produtos()
```
```python
# controllers/produto_controller.py
from services.produto_service import listar_produtos

def listar_produtos():
    produtos = listar_produtos()
    return {'success': True, 'data': produtos}
```
```python
# services/produto_service.py
from models.produto_model import get_todos_produtos

def listar_produtos():
    return get_todos_produtos()
```

## 2. Hardcoded Credentials
Before:
```python
app.config['SECRET_KEY'] = 'minha-chave-super-secreta'
```
After:
```python
# config/settings.py
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')
```

## 3. SQL Injection / Queries concatenadas
Before:
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
```
After:
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
```

## 4. Controllers com lógica de negócio pesada
Before:
```python
@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    itens = request.json['itens']
    # validações de estoque, total, insert de pedido e itens
```
After:
```python
# controllers/pedido_controller.py
from services.pedido_service import criar_pedido

def criar_pedido(request_data):
    return criar_pedido(request_data)
```

## 5. API Deprecated
Before:
```js
const bodyParser = require('body-parser');
app.use(bodyParser.json());
```
After:
```js
app.use(express.json());
```

## 6. Duplicação de código / DRY
Before:
```python
for row in rows:
    result.append({
        'id': row['id'],
        'nome': row['nome'],
        ...
    })
```
After:
```python
from utils.mapper import row_to_dict
result = [row_to_dict(row) for row in rows]
```

## 7. Error handling inconstante
Before:
```python
try:
    ...
except Exception as e:
    return jsonify({'erro': str(e)}), 500
```
After:
```python
raise ServiceError('Falha ao acessar o banco', status_code=500)
```

## 8. Configuração centralizada
Before:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
```
After:
```python
# config/settings.py
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///tasks.db')
```
