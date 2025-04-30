from flask import Flask, request, jsonify
import sqlite3
import os
import csv

app = Flask(__name__)
DB_PATH = "produits.db"
CSV_PATH = "produits.csv"

def importer_csv_si_necessaire():
    if not os.path.exists(DB_PATH):
        print("Import initial de produits.csv vers produits.db...")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS codes_barres")
        cur.execute("DROP TABLE IF EXISTS produits")

        cur.execute("""
            CREATE TABLE produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                quantite INTEGER,
                prix REAL
            )
        """)

        cur.execute("""
            CREATE TABLE codes_barres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                id_produit INTEGER,
                FOREIGN KEY (id_produit) REFERENCES produits(id)
            )
        """)

        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nom = row["Produits"][:100]
                quantite = int(row["Quantité"])
                prix = float(row["Prix"])
                cur.execute("INSERT INTO produits (nom, quantite, prix) VALUES (?, ?, ?)", (nom, quantite, prix))
                id_produit = cur.lastrowid
                for key in ["Code1", "Code2", "Code3"]:
                    code = row[key].strip()
                    if code:
                        cur.execute("INSERT OR IGNORE INTO codes_barres (code, id_produit) VALUES (?, ?)", (code.upper(), id_produit))

        conn.commit()
        conn.close()
        print("Import terminé.")

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

# Lancement automatique de l'import si la base n'existe pas
importer_csv_si_necessaire()

# Pour Render / Gunicorn
# pas de app.run() ici car c'est géré par gunicorn
