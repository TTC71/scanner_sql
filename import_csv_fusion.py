import sqlite3
import csv

DB_PATH = "produits.db"
CSV_PATH = "produits.csv"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(CSV_PATH, newline='', encoding='latin1') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nom = row["Produits"][:100]
        quantite = int(row["Quantité"])
        prix = float(row["Prix"])
        cur.execute("SELECT id FROM produits WHERE nom = ? AND prix = ?", (nom, prix))
        produit = cur.fetchone()
        if produit:
            id_produit = produit[0]
        else:
            cur.execute("INSERT INTO produits (nom, quantite, prix) VALUES (?, ?, ?)", (nom, quantite, prix))
            id_produit = cur.lastrowid

        for key in ["Code1", "Code2", "Code3"]:
            code = row[key].strip()
            if code and code.lower() != "nan":
                cur.execute("INSERT OR IGNORE INTO codes_barres (code, id_produit) VALUES (?, ?)", (code.upper(), id_produit))

conn.commit()
conn.close()
