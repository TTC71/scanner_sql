
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "produits.db"

@app.route("/produit")
def get_produit():
    code = request.args.get("code", "").strip().upper()
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

if __name__ == "__main__":
    app.run(debug=True)
