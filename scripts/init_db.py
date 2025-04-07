import requests
import pandas as pd
import sqlite3
import os
from io import StringIO
from config import DB_PATH, CSV_URLS

# === UTILS ===

def create_connection(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def fetch_csv(url):
    print(f"⬇️ Téléchargement depuis : {url}")
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return pd.read_csv(StringIO(response.text))

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id_produit STRING PRIMARY KEY,
        nom STRING,
        prix FLOAT,
        stock INTEGER
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magasins (
        id_magasin INTEGER PRIMARY KEY,
        ville STRING,
        nombre_salaries INTEGER
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        date DATE,
        id_magasin INTEGER,
        id_produit STRING,
        quantity INTEGER,
        PRIMARY KEY (date, id_magasin, id_produit, quantity),
        FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin),
        FOREIGN KEY (id_produit) REFERENCES produits(id_produit)
    )""")

    conn.commit()
    print("✅ Tables créées.")

def insert_data(conn, table, df):
    cursor = conn.cursor()
    
    if table == "produits":
        df.rename(columns={"ID Référence produit": "id_produit", "Nom": "nom", "Prix": "prix", "Stock": "stock"}, inplace=True)
        for _, row in df.iterrows():
            cursor.execute("""
            INSERT OR IGNORE INTO produits (id_produit, nom, prix, stock)
            VALUES (?, ?, ?, ?)""", (row['id_produit'], row['nom'], float(row['prix']), int(row['stock'])))

    elif table == "magasins":
        df.rename(columns={"ID Magasin": "id_magasin", "Ville": "ville", "Nombre de salariés": "nombre_salaries"}, inplace=True)
        for _, row in df.iterrows():
            cursor.execute("""
            INSERT OR IGNORE INTO magasins (id_magasin, ville, nombre_salaries)
            VALUES (?, ?, ?)""", (int(row['id_magasin']), row['ville'], int(row['nombre_salaries'])))

    elif table == "ventes":
        df.rename(columns={"Date": "date", "ID Magasin": "id_magasin", "ID Référence produit": "id_produit", "Quantité": "quantity"}, inplace=True)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        for _, row in df.iterrows():
            cursor.execute("""
            INSERT OR IGNORE INTO ventes (date, id_produit, quantity, id_magasin)
            VALUES (?, ?, ?, ?)""", (row['date'], row['id_produit'], int(row['quantity']), int(row['id_magasin'])))

    conn.commit()
    print(f"✅ {len(df)} lignes insérées dans la table `{table}` (doublons ignorés).")

# === MAIN ===

if __name__ == "__main__":
    print("📊 Initialisation...")

    conn = create_connection(DB_PATH)
    create_tables(conn)

    for table, url in CSV_URLS.items():
        try:
            df = fetch_csv(url)
            insert_data(conn, table, df)
        except Exception as e:
            print(f"❌ Erreur pour {table} : {e}")

    conn.close()
    print("🏁 Terminé.")
