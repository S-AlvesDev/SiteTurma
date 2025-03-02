from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)

# Simulação de banco de dados (armazenamento em memória)
usuarios = {}

# Configuração de chave secreta para sessões
app.secret_key = 'chave_secreta'

@app.route('/mural')
def mural():
    if 'logged_in' in session and session['logged_in']:
        return render_template('mural.html')
    return redirect(url_for('home'))  # Redireciona para a página inicial se não estiver logado

@app.route('/')
def home():
    # Verifica se o usuário está logado
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html', logged_in=True)
    return render_template('index.html', logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    senha = data.get("senha", "").strip()
    
    # Verifica se o usuário está no banco de dados simulado
    if email in usuarios and usuarios[email]["senha"] == senha:
        session['logged_in'] = True
        session['username'] = usuarios[email]["nome"]
        return jsonify({"success": True, "username": usuarios[email]["nome"]})
    
    return jsonify({"success": False, "message": "Usuário ou senha inválidos."})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get("nome", "").strip()
    sobrenome = data.get("sobrenome", "").strip()
    email = data.get("email", "").strip()
    senha = data.get("senha", "").strip()
    
    # Valida o email e verifica se o usuário já existe
    if not email:
        return jsonify({"success": False, "message": "Email inválido."})
    if email in usuarios:
        return jsonify({"success": False, "message": "Usuário já cadastrado."})
    
    usuarios[email] = {"nome": nome, "sobrenome": sobrenome, "senha": senha}
    return jsonify({"success": True})

@app.route('/logout')
def logout():
    # Remove a chave 'logged_in' da sessão para fazer o logout
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
