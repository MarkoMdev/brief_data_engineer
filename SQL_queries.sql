-- Création de la base de données et des tables

-- Table des produits
CREATE TABLE IF NOT EXISTS produits (
    id_produit STRING PRIMARY KEY,
    nom STRING,
    prix FLOAT,
    stock INTEGER
)

-- Table des magasins
CREATE TABLE IF NOT EXISTS magasins (
    id_magasin INTEGER PRIMARY KEY,
    ville STRING,
    nombre_salaries INTEGER
)

-- Table des ventes
CREATE TABLE IF NOT EXISTS ventes (
    date DATE,
    id_magasin INTEGER,
    id_produit STRING,
    quantity INTEGER,
    PRIMARY KEY (date, id_magasin, id_produit, quantity),
    FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin),
    FOREIGN KEY (id_produit) REFERENCES produits(id_produit)
)

-- Insertion de données dans les tables

-- Table des produits
INSERT OR IGNORE INTO produits (id_produit, nom, prix, stock)
VALUES (?, ?, ?, ?)

-- Table des magasins
INSERT OR IGNORE INTO magasins (id_magasin, ville, nombre_salaries)
VALUES (?, ?, ?)

-- Table des ventes
INSERT OR IGNORE INTO ventes (date, id_produit, quantity, id_magasin)
VALUES (?, ?, ?, ?)

-- Requêtes pour effectuer des analyses sur les données

-- Chiffre d'affaires total
SELECT SUM(v.quantity * p.prix) AS chiffre_affaires
FROM ventes v
JOIN produits p ON v.id_produit = p.id_produit

-- Ventes totales par produit
SELECT 
    p.nom AS produit,
    p.prix AS prix_unitaire,
    SUM(v.quantity) AS nombre_vendu,
    ROUND(SUM(v.quantity * p.prix),2) AS chiffre_affaires_produit
FROM ventes v
JOIN produits p ON v.id_produit = p.id_produit
GROUP BY v.id_produit
ORDER BY chiffre_affaires_produit DESC

-- Ventes totales par magasin
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
