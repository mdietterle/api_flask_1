# pip install Flask
from flask import Flask, request, jsonify
import sqlite3

# criar uma instância da classe Flask
app = Flask(__name__)

# Configuração do banco de dados sqlite3
DATABASE = 'database.db'

# Conectar ao BD
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Criar a tabela de dados, se ainda não existir
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Rota raiz para explicar o uso da API
"""
Retorna as rotas básicas da API
"""
@app.route('/')
def home():
    return """
    <h1>Bem vindo à API FLASK</h1>
    <p>Esta API permite que você execute operações na tabela 'dados'</p>
    <p>Rotas disponíveis</p>
    <ul>
        <li>POST /dados - Adiciona um novo dado. Envie um JSON com os campos 
            'nome' e 'idade'.</li>
        <li>GET /dados - Retorna todos os dados da tabela</li>
        <li>GET /dados/{id} - Retorna um dado em específico</li>
        <li>PUT /dados/{id} - Atualiza um dado existente. Envie um JSON com os campos 
            'nome' e 'idade'.</li>
        <li>DELETE /dados/{id} - Deleta um dado existente</li>
    </ul>
    """

"""
    Inicializa o Banco de dados e cria as tabelas.
    
    :returns Banco de Dados inicializado
"""
@app.route('/initdb')
def initialize_database():
    init_db()
    return 'Banco de dados inicializado'

# Rota para adicionar um novo dado
@app.route('/dados', methods=['POST'])
def manage_dados():
    nome = request.json.get('nome')
    idade = request.json.get('idade')
    id_cidade = request.json.get('id_cidade')

    if not nome or not idade or not id_cidade:
        return jsonify({'error': 'Nome, idade e id da cidade são obrigatórios'})

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO dados (NOME, IDADE, ID_CIDADE) VALUES (?, ?, ?)', (nome, idade, id_cidade))
        db.commit()
        return jsonify({'message': 'Dados inseridos com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para adicionar uma nova cidade
@app.route('/cidades', methods=['POST'])
def add_cidade():
    cidade = request.json.get('nome_cidade')
    uf = request.json.get('uf_cidade')

    if not cidade or not uf :
        return jsonify({'error': 'Cidade e UF são obrigatórios'})

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO cidades (NOME_CIDADE, UF_CIDADE) VALUES (?, ?)', (cidade, uf))
        db.commit()
        return jsonify({'message': 'Dados inseridos com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para obter todos os dados
@app.route('/dados', methods=['GET'])
def get_dados():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM dados')
        dados = cursor.fetchall()
        return jsonify([dict(row) for row in dados])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para obter todas as cidades
@app.route('/cidades', methods=['GET'])
def get_cidades():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cidades')
        dados = cursor.fetchall()
        return jsonify([dict(row) for row in dados])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para buscar um ID específico
@app.route('/dados/<int:dado_id>', methods=['GET'])
def get_dado(dado_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM dados WHERE id = ?', (dado_id,))
        dado = cursor.fetchone()
        if dado:
            return jsonify(dict(dado))
        else:
            return jsonify({'error': 'Dado não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para buscar uma cidade específica por ID
@app.route('/cidades/<int:cidade_id>', methods=['GET'])
def get_cidade(cidade_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM cidades WHERE id_cidade = ?', (cidade_id,))
        dado = cursor.fetchone()
        if dado:
            return jsonify(dict(dado))
        else:
            return jsonify({'error': 'Dado não encontrado'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Rota para deletar dados
@app.route('/dados/<int:dado_id>', methods=['DELETE'])
def delete_dado(dado_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM dados WHERE id = ?', (dado_id,))
        db.commit()
        return jsonify({'message': 'Registro deletado com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# Rota para deletar cidades
@app.route('/cidades/<int:cidade_id>', methods=['DELETE'])
def delete_cidade(cidade_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM cidades WHERE id_cidade = ?', (cidade_id,))
        db.commit()
        return jsonify({'message': 'Registro deletado com sucesso'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Alterar dados da pessoa
@app.route('/dados/<int:dado_id>', methods=['PUT'])
def update_dado(dado_id):
    nome = request.json.get('nome')
    idade = request.json.get('idade')
    id_cidade = request.json.get('id_cidade')

    if not nome or not idade or not id_cidade:
        return jsonify({'error': 'Nome, idade e id da cidade são obrigatórios'}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE dados set nome = ?, idade = ?, id_cidade = ? WHERE id = ?', (nome, idade, id_cidade, dado_id))
        db.commit()
        return jsonify({'message': 'Dados alterados com sucesso!'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# Alterar dados da cidade
@app.route('/cidades/<int:cidade_id>', methods=['PUT'])
def update_cidade(cidade_id):
    nome = request.json.get('nome_cidade')
    uf = request.json.get('uf_cidade')

    if not nome or not uf:
        return jsonify({'error': 'Nome e uf são obrigatórios'}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE dados set nome_cidade = ?, uf_cidade = ? WHERE id = ?', (nome, uf, id_cidade, cidade_id))
        db.commit()
        return jsonify({'message': 'Dados alterados com sucesso!'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/pessoascidade/<str:nome_cidade>', methods=['GET'])
def pessoas_cidade(nome_cidade):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('select dados.nome, dados.idade, cidades.nome_cidade, cidades.uf_cidade from dados, cidades WHERE cidades.nome_cidade = ? and dados.id_cidade = cidades.id_cidade', (nome_cidade,))
        dados = cursor.fetchall()
        return jsonify([dict(row) for row in dados])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

# inicializar a aplicação FLASK
if __name__ == '__main__':
    app.run(debug=True)
