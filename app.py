from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import base64
import hashlib

app = Flask(__name__)

def generate_key(password: str) -> bytes:
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        message = request.form["message"]
        password = request.form["password"]
        action = request.form["action"]

        key = generate_key(password)
        fernet = Fernet(key)

        try:
            if action == "encrypt":
                result = fernet.encrypt(message.encode()).decode()
            elif action == "decrypt":
                result = fernet.decrypt(message.encode()).decode()
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
