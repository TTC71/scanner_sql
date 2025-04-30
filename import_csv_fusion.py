import sqlite3
import csv
import os

DB_PATH = "produits.db"
CSV_PATH = "produits.csv"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    quantite INTEGER,
    prix REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS codes_barres (
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

        cur.execute("SELECT id FROM produits WHERE nom = ? AND prix = ?", (nom, prix))
        existing = cur.fetchone()

        if existing:
            id_produit = existing[0]
        else:
            cur.execute("INSERT INTO produits (nom, quantite, prix) VALUES (?, ?, ?)", (nom, quantite, prix))
            id_produit = cur.lastrowid

        for key in ["Code1", "Code2", "Code3"]:
            code = row[key].strip()
            if code:
                cur.execute("INSERT OR IGNORE INTO codes_barres (code, id_produit) VALUES (?, ?)", (code.upper(), id_produit))

conn.commit()
conn.close()
print("Fusion CSV → DB terminée avec succès.")
