import sqlite3
from flask import Flask, request, redirect, render_template, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "troque-esta-chave-por-uma-muito-segura"

DB_PATH = 'fitlife.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        # validação básica de confirmação de senha
        if password != request.form.get('confirm-password', ''):
            error = "Senhas não conferem."
            return render_template('signup.html', error=error)
        pw_hash = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                (name, email, pw_hash)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            error = "E-mail já cadastrado."
            return render_template('signup.html', error=error)
        finally:
            conn.close()

        return redirect(url_for('login'))
    # GET
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        pw    = request.form['password']

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], pw):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            error = "E-mail ou senha inválidos."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    user = conn.execute(
        'SELECT name FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()
    conn.close()

    return render_template('dashboard.html', user_name=user['name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
