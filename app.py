from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_connection():
    try:
        conn = sqlite3.connect('studio.db')
        conn.row_factory = sqlite3.Row  # Para acessar os resultados como dicionários
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            numero VARCHAR(11) NOT NULL,
            email VARCHAR(100) NOT NULL,
            atividades VARCHAR(255)  -- Coluna para armazenar atividades selecionadas
        );
        """)
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao SQLite: {e}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quemsomos")
def quem_somos():
    return render_template("quemsomos.html")

@app.route("/cadastro")
def contatos():
    return render_template("cadastro.html")

@app.route("/addCliente", methods=['POST'])
def addCliente():
    name = request.form['inputName']
    numero = request.form['inputNumero']
    email = request.form['inputEmail']
    atividades = []
    if request.form.get('musculacao'):
        atividades.append('Musculação')
    if request.form.get('pilates'):
        atividades.append('Pilates')
    if request.form.get('funcional'):
        atividades.append('Funcional')
    
    atividades_str = ', '.join(atividades)  # Converte a lista em uma string separada por vírgulas

    conn = create_connection()
    if conn is None:
        return "Falha na conexão com o banco de dados."

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cliente (name, numero, email, atividades)
            VALUES (?, ?, ?, ?)
        ''', (name, numero, email, atividades_str))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()

    return redirect('/cadastro')

@app.route("/clientes")
def mostrar_cliente():
    conn = create_connection()
    if conn is None:
        return "Falha na conexão com o banco de dados."
    
    clientes = []  # Inicializa a variável clientes
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()
    return render_template("clientes.html", clientes=clientes)

@app.route("/delete_cliente/<int:id>", methods=["POST"])
def delete_cliente(id):
    conn = create_connection()
    if conn is None:
        return "Falha na conexão com o banco de dados."

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE id = ?", (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()
    return redirect('/clientes')

if __name__ == "__main__":
    app.run(debug=True)
