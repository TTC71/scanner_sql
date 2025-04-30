
import sqlite3
import csv

DB_PATH = "produits.db"
CSV_PATH = "produits.csv"

def import_csv():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clean tables
    cur.execute("DELETE FROM codes_barres")
    cur.execute("DELETE FROM produits")

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nom = row["Produits"][:100].strip()
            quantite = int(row["Quantité"]) if row["Quantité"].isdigit() else 0
            prix = float(row["Prix"].replace(",", "."))

            cur.execute("INSERT INTO produits (nom, quantite, prix) VALUES (?, ?, ?)", (nom, quantite, prix))
            produit_id = cur.lastrowid

            for key in ["Code1", "Code2", "Code3"]:
                code = row[key].strip().upper()
                if code:
                    cur.execute("INSERT OR IGNORE INTO codes_barres (code, id_produit) VALUES (?, ?)", (code, produit_id))

    conn.commit()
    conn.close()
    print("Import terminé.")

if __name__ == "__main__":
    import_csv()
