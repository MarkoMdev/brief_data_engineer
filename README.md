# 📊 Projet d'analyse des ventes - Sélection Data Engineer - Simplon

Ce projet consiste à concevoir une architecture simple pour analyser les ventes d'une PME, en utilisant SQLite, Docker, et Python.

## 🚀 Objectifs

- Concevoir une architecture en deux services (exécution de scripts + base de données SQLite)
- Collecter des données en ligne (produits, magasins, ventes)
- Construire une base relationnelle
- Réaliser des analyses SQL sur les ventes :
  - Chiffre d'affaires total
  - Ventes par produit
  - Ventes par ville

---

## 🏗️ Architecture

Deux services Docker :

| Service | Rôle | Volumes/Ports |
|--------|------|----------------|
| `app` | Exécute les scripts Python d'import et d'analyse | Monté sur `./` |
| `db` | Fournit une CLI SQLite pour accéder à la base (`ventes.db`) | `./data:/workspace` |

Les deux services partagent un réseau Docker et un volume `data/` contenant la base SQLite.

---

## 🧱 Structure du projet

```
projet-ventes/
├── data/                  ← Base SQLite stockée ici
├── scripts/               ← Scripts Python
│   ├── init_db.py
│   ├── analyser_ventes.py
│   └── config.py        ← Fichier de configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── Makefile               ← Raccourcis d'exécution
```

---

## ⚙️ Pré-requis

- Docker
- (facultatif) `make` pour simplifier les commandes

---

## 🧪 Utilisation

### 1. 🔨 Construire l'image

```bash
make build
```

### 2. 🧬 Initialiser la base et importer les données

```bash
make init
```

### 3. 📊 Lancer les analyses SQL

```bash
make analyse
```

### 4. 🧪 Tout faire (import + analyse)

```bash
make full
```

---

## 📈 Requêtes réalisées

### 4.a - Chiffre d'affaires total

```sql
SELECT SUM(v.quantity * p.prix) FROM ventes v JOIN produits p ON v.id_produit = p.id_produit;
```

### 4.b - Ventes par produit

Affiche : produit, prix unitaire, quantité totale, CA total

### 4.c - Ventes par ville

Affiche : ville, nombre de ventes, CA total

---

## 🛡️ Hypothèses et contraintes

- La table `ventes` n'a pas d'identifiant unique fourni → une **clé primaire composite** est définie sur `(date, id_produit, id_magasin, quantity)` pour éviter les doublons exacts.
- Si deux ventes strictement identiques existent dans la source, une seule sera importée.
- Les scripts sont conçus pour être **relançables sans réinsérer les doublons** (`INSERT OR IGNORE`).

---

## 📎 Sources des données (CSV)

- Produits : [Lien CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv)
- Magasins : [Lien CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv)
- Ventes : [Lien CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv)

---

## 🙋 Auteurs

Projet réalisé dans le cadre de la sélection Data Engineer chez Simplon.
