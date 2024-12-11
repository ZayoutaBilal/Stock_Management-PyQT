import sqlite3

# ==================== Connexion à la base de données ====================
def connect_db():
    return sqlite3.connect("gestion_stock.db")

# ==================== Table Client ====================
def creer_table_client():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def ajouter_client(nom, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Client (nom, email) VALUES (?, ?)", (nom, email))
    conn.commit()
    conn.close()

def lire_clients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Client")
    clients = cursor.fetchall()
    conn.close()
    return clients

def modifier_client(id, nom, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Client SET nom = ?, email = ? WHERE id = ?", (nom, email, id))
    conn.commit()
    conn.close()

def supprimer_client(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Client WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ==================== Table Produit ====================
def creer_table_produit():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prix REAL,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()

def ajouter_produit(nom, prix,quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Produit (nom, prix,quantity) VALUES (?, ?, ?)", (nom, prix, quantity))
    conn.commit()
    conn.close()

def lire_produits():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Produit")
    produits = cursor.fetchall()
    conn.close()
    return produits

def get_produit_quantite(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM Produit WHERE id = ?", (id,))
    quantity = cursor.fetchone()
    conn.close()
    return quantity[0]

def set_produit_quantite(id,sq):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Produit SET quantity = quantity - ? WHERE id = ?", (sq, id))
    conn.commit()
    conn.close()

def modifier_produit(id, nom, prix ,quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Produit SET nom = ?, prix = ? ,quantity = ? WHERE id = ?", (nom, prix, quantity, id))
    conn.commit()
    conn.close()

def supprimer_produit(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Produit WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ==================== Table Commande ====================
def creer_table_commande():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Commande (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            produit_id INTEGER,
            quantite INTEGER,
            date_column DATE,
            FOREIGN KEY (client_id) REFERENCES Client(id) ON DELETE CASCADE,
            FOREIGN KEY (produit_id) REFERENCES Produit(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def ajouter_commande(client_id, produit_id, quantite,date_column):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Commande (client_id, produit_id, quantite,date_column) VALUES (?, ?, ?,?)", (client_id, produit_id, quantite,date_column))
    conn.commit()
    conn.close()

def lire_commandes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Commande.id, Client.nom, Produit.nom, Commande.quantite , Commande.date_column
        FROM Commande
        JOIN Client ON Commande.client_id = Client.id
        JOIN Produit ON Commande.produit_id = Produit.id
    """)
    commandes = cursor.fetchall()
    conn.close()
    return commandes

def modifier_commande(id, client_id, produit_id, quantite):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Commande SET client_id = ?, produit_id = ?, quantite = ? WHERE id = ?", (client_id, produit_id, quantite, id))
    conn.commit()
    conn.close()

def supprimer_commande(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Commande WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ==================== Initialisation des tables ====================
def init_db():
    creer_table_client()
    creer_table_produit()
    creer_table_commande()

if __name__ == "__main__":
    init_db()
