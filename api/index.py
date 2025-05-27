from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
import base64
import hashlib

app = Flask(__name__, template_folder='/templates')

@app.route('/generate_key', methods=['POST'])
def generate_key_route():
    data = request.json
    password = data.get('password', '')
    if not password:
        return jsonify({'error': 'Missing password'}), 400
    try:
        key = generate_key(password)
        return jsonify({'key': key.decode()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_key(password):
    # Derive a 32-byte key from the password
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plaintext = data.get('plaintext', '')
    key = data.get('key', '')
    if not plaintext or not key:
        return jsonify({'error': 'Missing plaintext or key'}), 400
    try:
        f = Fernet(key)
        ciphertext = f.encrypt(plaintext.encode()).decode()
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data.get('ciphertext', '')
    key = data.get('key', '')
    if not ciphertext or not key:
        return jsonify({'error': 'Missing ciphertext or key'}), 400
    try:
        f = Fernet(key)
        plaintext = f.decrypt(ciphertext.encode()).decode()
        return jsonify({'plaintext': plaintext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
