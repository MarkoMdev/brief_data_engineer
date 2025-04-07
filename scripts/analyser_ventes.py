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
    df_ca = query_to_df(conn, """
        SELECT SUM(v.quantity * p.prix) AS chiffre_affaires
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
    """)

    afficher_resultats("Chiffre d'affaires", df_ca)
    df_ca.to_sql('chiffre_affaires', conn, if_exists='replace', index=False)

    # 4.b. Ventes par produit enrichie
    df_ventes_produit = query_to_df(conn, """
        SELECT 
            p.nom AS produit,
            p.prix AS prix_unitaire,
            SUM(v.quantity) AS nombre_vendu,
            ROUND(SUM(v.quantity * p.prix),2) AS chiffre_affaires_produit
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
        GROUP BY v.id_produit
        ORDER BY chiffre_affaires_produit DESC
    """)
    afficher_resultats("Ventes par produit", df_ventes_produit)
    df_ventes_produit.to_sql('ventes_produit', conn, if_exists='replace', index=False)

    # 4.c. Ventes par ville
    df_ventes_ville = query_to_df(conn, """
        SELECT 
            m.ville,
            COUNT(*) AS nombre_ventes,
            SUM(v.quantity) AS quantite_totale,
            ROUND(SUM(v.quantity * p.prix),2) AS chiffre_affaires_ville
        FROM ventes v
        JOIN produits p ON v.id_produit = p.id_produit
        JOIN magasins m ON v.id_magasin = m.id_magasin
        GROUP BY m.ville
        ORDER BY chiffre_affaires_ville DESC
    """)
    afficher_resultats("Ventes par ville", df_ventes_ville)
    df_ventes_ville.to_sql('ventes_ville', conn, if_exists='replace', index=False)

    conn.close()
