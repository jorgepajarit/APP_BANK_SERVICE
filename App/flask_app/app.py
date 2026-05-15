import os
import requests
import jwt
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "super-secret-bank-key"

# Configuration
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def get_auth_headers():
    token = session.get('token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def decode_token(token):
    try:
        # We don't verify signature here just to get the user_id for the summary call
        # In a real app, the backend should provide this or we should verify with a public key
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except:
        return {}

@app.route("/")
def index():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_view'))

@app.route("/login", methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = requests.post(f"{API_BASE_URL}/auth/login", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                session['token'] = data['access_token']
                session['username'] = username
                
                payload = decode_token(data['access_token'])
                session['user_id'] = payload.get('user_id', 1)
                
                return redirect(url_for('dashboard'))
            else:
                flash("Credenciales inválidas. Intente de nuevo.", "error")
        except Exception as e:
            flash(f"Error al conectar con el servidor: {str(e)}", "error")
            
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if 'token' not in session:
        return redirect(url_for('login_view'))
        
    user_id = session.get('user_id', 1)
    try:
        # Get financial summary
        summary_res = requests.get(f"{API_BASE_URL}/banking/summary/{user_id}", headers=get_auth_headers())
        summary = summary_res.json() if summary_res.status_code == 200 else {"accounts": [], "wallets": []}
        
        # Get movements (from first account if exists)
        movements = []
        accounts = summary.get('accounts', [])
        if accounts:
            acc_id = accounts[0]['id']
            mov_res = requests.get(f"{API_BASE_URL}/banking/accounts/{acc_id}/movements", headers=get_auth_headers())
            if mov_res.status_code == 200:
                movements = mov_res.json()
                
        return render_template("dashboard.html", accounts=accounts, movements=movements)
    except Exception as e:
        flash(f"Error al cargar datos: {str(e)}", "error")
        return render_template("dashboard.html", accounts=[], movements=[])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_view'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
