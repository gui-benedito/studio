from flask import Flask, render_template, request, redirect
import pymysql
app = Flask("__name__")

def create_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='fatec',
            database='studio',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao MySQL: {e}")
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
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO cliente (name, numero, email, atividades)
                VALUES (%s, %s, %s, %s)
            ''', (name, numero, email, atividades_str))
            conn.commit()
    except pymysql.MySQLError as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()

    return redirect('/cadastro')

@app.route("/clientes")
def mostrar_cliente():
    conn = create_connection()
    try:
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM cliente")
        clientes = cursor.fetchall()
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()
    return render_template("clientes.html", clientes=clientes)

@app.route("/delete_cliente/<int:id>", methods=["POST"])
def delete_cliente(id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        conn.close()
    return redirect('/clientes')