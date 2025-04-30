from flask import Flask, request, jsonify
import sqlite3
import os
import import_csv_fusion

app = Flask(__name__)
DB_PATH = "produits.db"

@app.route("/produit")
def get_produit():
    code = request.args.get("code", "").upper()
    if not code:
        return jsonify({"error": "Code-barres manquant"}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT p.nom, p.quantite, p.prix
        FROM produits p
        JOIN codes_barres cb ON cb.id_produit = p.id
        WHERE cb.code = ?
    """, (code,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({
            "produit": row[0],
            "quantite": row[1],
            "prix": row[2]
        })
    else:
        return jsonify({"error": "Produit non trouvé"}), 404

@app.route("/importer")
def importer():
    try:
        import import_csv_fusion
        return jsonify({"message": "Import CSV terminé avec succès."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
