import sqlite3
import pandas as pd
from config import DB_PATH

def query_to_df(conn, query):
    return pd.read_sql_query(query, conn)

def afficher_resultats(titre, df):
    print(f"\n📊 {titre}")
    print(df.to_markdown(index=False))

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)

    # 4.a. Chiffre d’affaires total (quantity × prix)
    df_ca_total = query_to_df(conn, """
        SELECT SUM(v.quantity * p.prix) AS chiffre_affaires_total
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
    """)

    afficher_resultats("Chiffre d'affaires total", df_ca_total)

    # 4.b. Ventes par produit enrichie
    df_par_produit = query_to_df(conn, """
        SELECT 
            p.nom AS produit,
            p.prix AS prix_unitaire,
            SUM(v.quantity) AS quantite_totale,
            SUM(v.quantity * p.prix) AS total_ventes
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
        GROUP BY v.id_produit
        ORDER BY total_ventes DESC
    """)
    afficher_resultats("Ventes par produit (quantité + CA)", df_par_produit)


    # 4.c. Ventes par ville
    df_par_ville = query_to_df(conn, """
        SELECT 
            m.ville,
            COUNT(*) AS nombre_ventes,
            SUM(v.quantity) AS quantite_totale,
            SUM(v.quantity * p.prix) AS total_ventes
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
        JOIN magasins m ON v.id_magasin = m.id_magasin
        GROUP BY m.ville
        ORDER BY total_ventes DESC
    """)
    afficher_resultats("Ventes par ville", df_par_ville)


    conn.close()
