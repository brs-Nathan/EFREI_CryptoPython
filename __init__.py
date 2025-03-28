from cryptography.fernet import Fernet
from flask import Flask
import base64  

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Bienvenue sur le service de chiffrement/déchiffrement !"

def generer_fernet(cle_utilisateur):
    try:
        cle_bytes = base64.urlsafe_b64decode(cle_utilisateur)
        return Fernet(cle_bytes)
    except Exception:
        return None  

@app.route('/encrypt/<string:cle>/<string:valeur>', strict_slashes=False)
def encryptage(cle, valeur):
    f = generer_fernet(cle)
    if f is None:
        return "Erreur : Clé invalide. Utilisez une clé de 32 octets encodée en base64."

    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<string:cle>/<string:token>', strict_slashes=False)
def decryptage(cle, token):
    f = generer_fernet(cle)
    if f is None:
        return "Erreur : Clé invalide. Utilisez une clé de 32 octets encodée en base64."

    try:
        token_bytes = token.encode()
        valeur_decryptee = f.decrypt(token_bytes)
        return f"Valeur décryptée : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
