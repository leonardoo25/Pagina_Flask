from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave'

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='leonardo',
        password='12345',
        database='base_de_dados'
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = connect_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        db.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/pagina')
        else:
            error = 'Credenciais inválidas. Por favor, tente novamente.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/pagina')
def pagina_protegida():
    if 'user_id' in session:
        mensagem = 'Você acessou a página!'
        return render_template('pagina.html', mensagem=mensagem)
    else:
        return 'Erro: Acesso não autorizado.'

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
