import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

class Database:
    def __init__(self, db_name: str = "washafrique.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialise toutes les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table utilisateurs (admins)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'admin',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                tel TEXT UNIQUE NOT NULL,
                email TEXT,
                vehicule TEXT,
                points_fidelite INTEGER DEFAULT 0,
                total_depense REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table services
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix REAL NOT NULL,
                duree INTEGER NOT NULL,
                points INTEGER DEFAULT 1,
                actif INTEGER DEFAULT 1,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table postes de lavage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS postes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                actif INTEGER DEFAULT 1
            )
        ''')
        
        # Table employés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                tel TEXT,
                poste TEXT,
                salaire REAL DEFAULT 0,
                actif INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table réservations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                poste_id INTEGER,
                employe_id INTEGER,
                date TEXT NOT NULL,
                heure TEXT NOT NULL,
                statut TEXT DEFAULT 'en_attente',
                montant REAL NOT NULL,
                montant_paye REAL DEFAULT 0,
                methode_paiement TEXT,
                notes TEXT,
                code_promo TEXT,
                reduction REAL DEFAULT 0,
                points_utilises INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (service_id) REFERENCES services (id),
                FOREIGN KEY (poste_id) REFERENCES postes (id),
                FOREIGN KEY (employe_id) REFERENCES employes (id)
            )
        ''')
        
        # Table paiements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paiements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reservation_id INTEGER NOT NULL,
                montant REAL NOT NULL,
                methode TEXT NOT NULL,
                date_paiement TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (reservation_id) REFERENCES reservations (id)
            )
        ''')
        
        # Table codes promo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes_promo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                valeur REAL NOT NULL,
                date_debut TEXT,
                date_fin TEXT,
                utilisations_max INTEGER DEFAULT -1,
                utilisations_actuelles INTEGER DEFAULT 0,
                actif INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table récompenses fidélité
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recompenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                points_requis INTEGER NOT NULL,
                reduction REAL NOT NULL,
                type TEXT DEFAULT 'pourcentage',
                actif INTEGER DEFAULT 1
            )
        ''')
        
        # Table historique fidélité
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historique_fidelite (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                reservation_id INTEGER,
                points INTEGER NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (reservation_id) REFERENCES reservations (id)
            )
        ''')
        
        # Table produits/stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                quantite INTEGER DEFAULT 0,
                seuil_alerte INTEGER DEFAULT 10,
                unite TEXT DEFAULT 'unité',
                prix_unitaire REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table mouvements stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mouvements_stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produit_id INTEGER NOT NULL,
                quantite INTEGER NOT NULL,
                type TEXT NOT NULL,
                prix REAL DEFAULT 0,
                notes TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produit_id) REFERENCES produits (id)
            )
        ''')
        
        # Table paramètres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametres (
                cle TEXT PRIMARY KEY,
                valeur TEXT NOT NULL
            )
        ''')
        
        # Table notifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                titre TEXT NOT NULL,
                message TEXT NOT NULL,
                destinataire TEXT,
                envoyee INTEGER DEFAULT 0,
                date_envoi TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
        # Créer utilisateur admin par défaut
        cursor.execute("SELECT COUNT(*) as count FROM users")
        if cursor.fetchone()['count'] == 0:
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", password_hash, "admin")
            )
            conn.commit()
        
        # Créer poste par défaut
        cursor.execute("SELECT COUNT(*) as count FROM postes")
        if cursor.fetchone()['count'] == 0:
            cursor.execute("INSERT INTO postes (nom, actif) VALUES ('Poste 1', 1), ('Poste 2', 1)")
            conn.commit()
        
        # Créer récompenses par défaut
        cursor.execute("SELECT COUNT(*) as count FROM recompenses")
        if cursor.fetchone()['count'] == 0:
            recompenses_defaut = [
                ("Bronze - 5% OFF", 10, 5, "pourcentage"),
                ("Silver - 10% OFF", 25, 10, "pourcentage"),
                ("Gold - 15% OFF", 50, 15, "pourcentage"),
                ("Platinum - 20% OFF", 100, 20, "pourcentage")
            ]
            cursor.executemany(
                "INSERT INTO recompenses (nom, points_requis, reduction, type) VALUES (?, ?, ?, ?)",
                recompenses_defaut
            )
            conn.commit()
        
        conn.close()
    
    # ===== USERS =====
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    # ===== CLIENTS =====
    def ajouter_client(self, nom: str, tel: str, email: str = "", vehicule: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (nom, tel, email, vehicule) VALUES (?, ?, ?, ?)",
            (nom, tel, email, vehicule)
        )
        client_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return client_id
    
    def get_client_by_tel(self, tel: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE tel = ?", (tel,))
        client = cursor.fetchone()
        conn.close()
        return dict(client) if client else None
    
    def get_all_clients(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return clients
    
    def update_client_points(self, client_id: int, points: int, operation: str = "add"):
        conn = self.get_connection()
        cursor = conn.cursor()
        if operation == "add":
            cursor.execute(
                "UPDATE clients SET points_fidelite = points_fidelite + ? WHERE id = ?",
                (points, client_id)
            )
        else:
            cursor.execute(
                "UPDATE clients SET points_fidelite = points_fidelite - ? WHERE id = ?",
                (points, client_id)
            )
        conn.commit()
        conn.close()
    
    def update_client_depense(self, client_id: int, montant: float):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET total_depense = total_depense + ? WHERE id = ?",
            (montant, client_id)
        )
        conn.commit()
        conn.close()
    
    # ===== SERVICES =====
    def ajouter_service(self, nom: str, prix: float, duree: int, points: int = 1, description: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO services (nom, prix, duree, points, description) VALUES (?, ?, ?, ?, ?)",
            (nom, prix, duree, points, description)
        )
        service_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return service_id
    
    def get_all_services(self, actif_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if actif_only:
            cursor.execute("SELECT * FROM services WHERE actif = 1 ORDER BY prix")
        else:
            cursor.execute("SELECT * FROM services ORDER BY prix")
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services
    
    def delete_service(self, service_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE services SET actif = 0 WHERE id = ?", (service_id,))
        conn.commit()
        conn.close()
    
    # ===== POSTES =====
    def get_all_postes(self, actif_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if actif_only:
            cursor.execute("SELECT * FROM postes WHERE actif = 1")
        else:
            cursor.execute("SELECT * FROM postes")
        postes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return postes
    
    # ===== EMPLOYÉS =====
    def ajouter_employe(self, nom: str, tel: str = "", poste: str = "", salaire: float = 0) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employes (nom, tel, poste, salaire) VALUES (?, ?, ?, ?)",
            (nom, tel, poste, salaire)
        )
        employe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return employe_id
    
    def get_all_employes(self, actif_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if actif_only:
            cursor.execute("SELECT * FROM employes WHERE actif = 1")
        else:
            cursor.execute("SELECT * FROM employes")
        employes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return employes
    
    # ===== RÉSERVATIONS =====
    def ajouter_reservation(
        self,
        client_id: int,
        service_id: int,
        date: str,
        heure: str,
        montant: float,
        poste_id: int = None,
        employe_id: int = None,
        notes: str = "",
        code_promo: str = "",
        reduction: float = 0,
        points_utilises: int = 0
    ) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO reservations 
            (client_id, service_id, poste_id, employe_id, date, heure, montant, notes, code_promo, reduction, points_utilises, statut)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'en_attente')""",
            (client_id, service_id, poste_id, employe_id, date, heure, montant, notes, code_promo, reduction, points_utilises)
        )
        reservation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reservation_id
    
    def get_reservations_by_date(self, date: str) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, c.nom as client_nom, c.tel as client_tel, c.vehicule,
                   s.nom as service_nom, s.duree, s.points as service_points,
                   e.nom as employe_nom, p.nom as poste_nom
            FROM reservations r
            LEFT JOIN clients c ON r.client_id = c.id
            LEFT JOIN services s ON r.service_id = s.id
            LEFT JOIN employes e ON r.employe_id = e.id
            LEFT JOIN postes p ON r.poste_id = p.id
            WHERE r.date = ?
            ORDER BY r.heure
        """, (date,))
        reservations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reservations
    
    def get_all_reservations(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, c.nom as client_nom, c.tel as client_tel, c.vehicule,
                   s.nom as service_nom, s.prix, s.duree, s.points as service_points
            FROM reservations r
            LEFT JOIN clients c ON r.client_id = c.id
            LEFT JOIN services s ON r.service_id = s.id
            ORDER BY r.date DESC, r.heure DESC
        """)
        reservations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reservations
    
    def update_reservation_statut(self, reservation_id: int, statut: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reservations SET statut = ? WHERE id = ?",
            (statut, reservation_id)
        )
        conn.commit()
        conn.close()
    
    def delete_reservation(self, reservation_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        conn.commit()
        conn.close()
    
    # ===== PAIEMENTS =====
    def ajouter_paiement(self, reservation_id: int, montant: float, methode: str, notes: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paiements (reservation_id, montant, methode, notes) VALUES (?, ?, ?, ?)",
            (reservation_id, montant, methode, notes)
        )
        paiement_id = cursor.lastrowid
        
        # Mettre à jour le montant payé de la réservation
        cursor.execute(
            "UPDATE reservations SET montant_paye = montant_paye + ?, methode_paiement = ? WHERE id = ?",
            (montant, methode, reservation_id)
        )
        
        conn.commit()
        conn.close()
        return paiement_id
    
    # ===== CODES PROMO =====
    def ajouter_code_promo(
        self,
        code: str,
        type: str,
        valeur: float,
        date_debut: str = None,
        date_fin: str = None,
        utilisations_max: int = -1
    ) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO codes_promo (code, type, valeur, date_debut, date_fin, utilisations_max)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (code, type, valeur, date_debut, date_fin, utilisations_max)
        )
        promo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return promo_id
    
    def verifier_code_promo(self, code: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM codes_promo 
            WHERE code = ? AND actif = 1 
            AND (utilisations_max = -1 OR utilisations_actuelles < utilisations_max)
            AND (date_debut IS NULL OR date_debut <= date('now'))
            AND (date_fin IS NULL OR date_fin >= date('now'))""",
            (code,)
        )
        promo = cursor.fetchone()
        conn.close()
        return dict(promo) if promo else None
    
    def utiliser_code_promo(self, code: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE codes_promo SET utilisations_actuelles = utilisations_actuelles + 1 WHERE code = ?",
            (code,)
        )
        conn.commit()
        conn.close()
    
    # ===== STATISTIQUES =====
    def get_stats_dashboard(self) -> Dict:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # RDV aujourd'hui
        cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE date = ?", (today,))
        rdv_today = cursor.fetchone()['count']
        
        # Revenus aujourd'hui
        cursor.execute(
            "SELECT SUM(montant_paye) as total FROM reservations WHERE date = ? AND statut != 'annule'",
            (today,)
        )
        revenus_today = cursor.fetchone()['total'] or 0
        
        # Revenus total
        cursor.execute("SELECT SUM(montant_paye) as total FROM reservations WHERE statut != 'annule'")
        revenus_total = cursor.fetchone()['total'] or 0
        
        # Total clients
        cursor.execute("SELECT COUNT(*) as count FROM clients")
        total_clients = cursor.fetchone()['count']
        
        # RDV en attente
        cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE statut = 'en_attente'")
        rdv_attente = cursor.fetchone()['count']
        
        # Service le plus populaire
        cursor.execute("""
            SELECT s.nom, COUNT(*) as count
            FROM reservations r
            JOIN services s ON r.service_id = s.id
            WHERE r.statut != 'annule'
            GROUP BY r.service_id
            ORDER BY count DESC
            LIMIT 1
        """)
        service_pop = cursor.fetchone()
        service_populaire = service_pop['nom'] if service_pop else "N/A"
        
        conn.close()
        
        return {
            'rdv_today': rdv_today,
            'revenus_today': revenus_today,
            'revenus_total': revenus_total,
            'total_clients': total_clients,
            'rdv_attente': rdv_attente,
            'service_populaire': service_populaire
        }
    
    def get_revenus_par_jour(self, limit: int = 30) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, SUM(montant_paye) as revenus, COUNT(*) as nb_rdv
            FROM reservations
            WHERE statut != 'annule'
            GROUP BY date
            ORDER BY date DESC
            LIMIT ?
        """, (limit,))
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def get_services_stats(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.nom, COUNT(*) as nb_reservations, SUM(r.montant_paye) as revenus
            FROM reservations r
            JOIN services s ON r.service_id = s.id
            WHERE r.statut != 'annule'
            GROUP BY r.service_id
            ORDER BY nb_reservations DESC
        """)
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    # ===== FIDÉLITÉ =====
    def get_recompenses_disponibles(self, points_client: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM recompenses WHERE actif = 1 AND points_requis <= ? ORDER BY points_requis DESC",
            (points_client,)
        )
        recompenses = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return recompenses
    
    def ajouter_historique_fidelite(
        self,
        client_id: int,
        points: int,
        type: str,
        description: str,
        reservation_id: int = None
    ):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO historique_fidelite (client_id, reservation_id, points, type, description)
            VALUES (?, ?, ?, ?, ?)""",
            (client_id, reservation_id, points, type, description)
        )
        conn.commit()
        conn.close()
    
    # ===== PRODUITS/STOCK =====
    def ajouter_produit(self, nom: str, quantite: int, seuil_alerte: int, unite: str, prix_unitaire: float) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produits (nom, quantite, seuil_alerte, unite, prix_unitaire) VALUES (?, ?, ?, ?, ?)",
            (nom, quantite, seuil_alerte, unite, prix_unitaire)
        )
        produit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return produit_id
    
    def get_all_produits(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produits ORDER BY nom")
        produits = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return produits
    
    def get_produits_alerte(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produits WHERE quantite <= seuil_alerte")
        produits = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return produits
    
    def update_stock(self, produit_id: int, quantite: int, type: str, prix: float = 0, notes: str = ""):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enregistrer le mouvement
        cursor.execute(
            "INSERT INTO mouvements_stock (produit_id, quantite, type, prix, notes) VALUES (?, ?, ?, ?, ?)",
            (produit_id, quantite, type, prix, notes)
        )
        
        # Mettre à jour la quantité
        if type == "entree":
            cursor.execute(
                "UPDATE produits SET quantite = quantite + ? WHERE id = ?",
                (quantite, produit_id)
            )
        else:
            cursor.execute(
                "UPDATE produits SET quantite = quantite - ? WHERE id = ?",
                (quantite, produit_id)
            )
        
        conn.commit()
        conn.close()
    
    # ===== BACKUP =====
    def export_all_data(self) -> Dict:
        """Exporte toutes les données en JSON"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        data = {
            'export_date': datetime.now().isoformat(),
            'clients': [],
            'services': [],
            'reservations': [],
            'employes': [],
            'postes': [],
            'produits': [],
            'codes_promo': []
        }
        
        for table in data.keys():
            if table != 'export_date':
                cursor.execute(f"SELECT * FROM {table}")
                data[table] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return data
