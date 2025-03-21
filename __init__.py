from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Bienvenue sur le service de chiffrement/déchiffrement !"

def generer_fernet(cle_utilisateur):
    try:
        cle_bytes = base64.urlsafe_b64decode(cle_utilisateur)
        return Fernet(cle_bytes)
    except Exception as e:
        return None  # Retourne None si la clé est invalide

@app.route('/encrypt/<string:cle>/<string:valeur>')
def encryptage(cle, valeur):
    f = generer_fernet(cle)
    if f is None:
        return "Erreur : Clé invalide. Assurez-vous d'utiliser une clé de 32 octets encodée en base64."

    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<string:cle>/<string:token>')
def decryptage(cle, token):
    f = generer_fernet(cle)
    if f is None:
        return "Erreur : Clé invalide. Assurez-vous d'utiliser une clé de 32 octets encodée en base64."

    try:
        token_bytes = token.encode()
        valeur_decryptee = f.decrypt(token_bytes)
        return f"Valeur décryptée : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"

