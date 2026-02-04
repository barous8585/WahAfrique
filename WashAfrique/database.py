"""
Adaptateur PostgreSQL pour WashAfrique
Remplace SQLite par PostgreSQL (Supabase)
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import hashlib
import random
import string

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

class DatabasePostgres:
    """Classe Database adaptée pour PostgreSQL"""
    
    def __init__(self):
        """Initialise la connexion PostgreSQL"""
        self.config = self._get_config()
        self.init_database()
    
    def _get_config(self) -> dict:
        """Récupère configuration depuis st.secrets ou db_config.py"""
        # Priorité 1: Streamlit Secrets (pour Cloud)
        if HAS_STREAMLIT:
            try:
                if hasattr(st, 'secrets') and 'postgres' in st.secrets:
                    config = {
                        'host': st.secrets.postgres.host,
                        'port': int(st.secrets.postgres.port),
                        'database': st.secrets.postgres.database,
                        'user': st.secrets.postgres.user,
                        'password': st.secrets.postgres.password
                    }
                    return config
            except Exception as e:
                pass
        
        # Priorité 2: Fichier local (pour développement)
        try:
            from db_config import DB_CONFIG
            return DB_CONFIG
        except ImportError:
            raise Exception(
                "❌ Configuration base de données manquante!\n\n"
                "Pour développement local:\n"
                "1. Copiez db_config.py.template → db_config.py\n"
                "2. Remplissez vos credentials Supabase\n\n"
                "Pour Streamlit Cloud:\n"
                "1. Settings → Secrets\n"
                "2. Ajoutez section [postgres] avec credentials\n"
                "3. Format: [postgres]\\n   host = \"...\"\\n   port = 5432"
            )
    
    def get_connection(self):
        """Crée une connexion PostgreSQL"""
        try:
            conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password'],
                cursor_factory=RealDictCursor,
                connect_timeout=10
            )
            return conn
        except psycopg2.OperationalError as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                raise Exception(f"❌ Timeout connexion à Supabase. Vérifiez:\n1. Votre connexion Internet\n2. Host: {self.config['host']}\n3. Port: {self.config['port']}")
            elif "password" in error_msg.lower():
                raise Exception(f"❌ Authentification échouée. Vérifiez le mot de passe dans Secrets")
            elif "could not translate" in error_msg.lower() or "resolve" in error_msg.lower():
                raise Exception(f"❌ Host introuvable: {self.config['host']}\nVérifiez l'orthographe dans Secrets")
            else:
                raise Exception(f"❌ Erreur connexion PostgreSQL: {error_msg}")
    
    def init_database(self):
        """
        Crée toutes les tables PostgreSQL
        Adapté depuis database.py (SQLite → PostgreSQL)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table employes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employes (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                tel VARCHAR(20) NOT NULL,
                poste VARCHAR(100),
                salaire DECIMAL(10, 2),
                actif BOOLEAN DEFAULT TRUE,
                user_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table services
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                prix DECIMAL(10, 2) NOT NULL,
                duree INTEGER NOT NULL,
                description TEXT,
                actif BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                tel VARCHAR(20) NOT NULL UNIQUE,
                email VARCHAR(200),
                vehicule VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table reservations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                service_id INTEGER REFERENCES services(id),
                employe_id INTEGER REFERENCES users(id),
                date DATE NOT NULL,
                heure TIME NOT NULL,
                statut VARCHAR(20) DEFAULT 'en_cours',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table paiements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paiements (
                id SERIAL PRIMARY KEY,
                reservation_id INTEGER REFERENCES reservations(id),
                montant DECIMAL(10, 2) NOT NULL,
                methode VARCHAR(50) NOT NULL,
                date_paiement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
        # Table parametres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametres (
                id SERIAL PRIMARY KEY,
                cle VARCHAR(100) UNIQUE NOT NULL,
                valeur TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table pointages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pointages (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                type VARCHAR(20) NOT NULL,
                date DATE NOT NULL,
                heure TIME NOT NULL,
                notes TEXT
            )
        ''')
        
        # Table photos_services
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS photos_services (
                id SERIAL PRIMARY KEY,
                reservation_id INTEGER REFERENCES reservations(id),
                type_photo VARCHAR(20) NOT NULL,
                photo_data BYTEA NOT NULL,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                employe_id INTEGER REFERENCES users(id),
                notes TEXT
            )
        ''')
        
        # ===== TABLES SITE CLIENT =====
        
        # Table parametres_site_client
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametres_site_client (
                id SERIAL PRIMARY KEY,
                cle VARCHAR(100) UNIQUE NOT NULL,
                valeur TEXT,
                type VARCHAR(50) DEFAULT 'texte',
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table creneaux_disponibles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS creneaux_disponibles (
                id SERIAL PRIMARY KEY,
                jour_semaine VARCHAR(20) NOT NULL,
                heure_debut TIME NOT NULL,
                heure_fin TIME NOT NULL,
                intervalle_minutes INTEGER DEFAULT 30,
                capacite_simultanee INTEGER DEFAULT 2,
                actif BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Table reservations_web
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations_web (
                id SERIAL PRIMARY KEY,
                code_reservation VARCHAR(20) UNIQUE NOT NULL,
                nom_client VARCHAR(200) NOT NULL,
                tel_client VARCHAR(20) NOT NULL,
                email_client VARCHAR(200),
                service_id INTEGER REFERENCES services(id),
                date_reservation DATE NOT NULL,
                heure_reservation TIME NOT NULL,
                statut VARCHAR(20) DEFAULT 'en_attente',
                notes_client TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                confirmed_at TIMESTAMP
            )
        ''')
        
        # Table avis_clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avis_clients (
                id SERIAL PRIMARY KEY,
                reservation_web_id INTEGER REFERENCES reservations_web(id),
                nom_client VARCHAR(200) NOT NULL,
                note INTEGER NOT NULL CHECK (note BETWEEN 1 AND 5),
                commentaire TEXT,
                photo_url TEXT,
                visible BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
        # Initialiser données par défaut
        self._init_default_data(cursor, conn)
        
        cursor.close()
        conn.close()
    
    def _init_default_data(self, cursor, conn):
        """Initialise données par défaut (admin, paramètres, etc.)"""
        
        # Vérifier si admin existe
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        if cursor.fetchone()['count'] == 0:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                ('admin', 'admin123', 'admin')
            )
        
        # Paramètres par défaut
        params_defaut = [
            ('nom_entreprise', 'WashAfrique Pro'),
            ('heure_ouverture', '08:00'),
            ('heure_fermeture', '19:00')
        ]
        
        for cle, valeur in params_defaut:
            cursor.execute(
                "INSERT INTO parametres (cle, valeur) VALUES (%s, %s) ON CONFLICT (cle) DO NOTHING",
                (cle, valeur)
            )
        
        # Paramètres site client
        params_site_defaut = [
            ("site_actif", "1", "boolean", "Site client activé/désactivé"),
            ("nom_entreprise_site", "WashAfrique Pro", "texte", "Nom affiché sur site client"),
            ("slogan", "Votre voiture mérite le meilleur", "texte", "Slogan page d'accueil"),
            ("couleur_principale", "#667eea", "couleur", "Couleur principale site"),
            ("telephone_contact", "+225 XX XX XX XX", "texte", "Numéro affiché"),
            ("email_contact", "contact@washafrique.com", "texte", "Email contact"),
            ("adresse", "Abidjan, Côte d'Ivoire", "texte", "Adresse entreprise"),
            ("texte_accueil", "Réservez votre lavage en ligne", "textarea", "Texte page accueil"),
            ("reservation_active", "1", "boolean", "Autoriser réservations"),
            ("delai_min_reservation", "2", "nombre", "Heures min avant réservation")
        ]
        
        for cle, valeur, type_param, description in params_site_defaut:
            cursor.execute(
                """INSERT INTO parametres_site_client (cle, valeur, type, description) 
                   VALUES (%s, %s, %s, %s) ON CONFLICT (cle) DO NOTHING""",
                (cle, valeur, type_param, description)
            )
        
        # Créneaux horaires
        jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        for jour in jours:
            cursor.execute(
                """INSERT INTO creneaux_disponibles 
                   (jour_semaine, heure_debut, heure_fin, intervalle_minutes, capacite_simultanee, actif)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   ON CONFLICT DO NOTHING""",
                (jour, '08:00' if jour != 'dimanche' else '00:00',
                 '18:00' if jour != 'dimanche' else '00:00',
                 30, 2, jour != 'dimanche')
            )
        
        conn.commit()


    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Vérifie les credentials d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        # PostgreSQL: pas de hash pour l'instant (à améliorer en production)
        cursor.execute(
            "SELECT id, username, role FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    # ===== CLIENTS =====
    def ajouter_client(self, nom: str, tel: str, email: str = "", vehicule: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (nom, tel, email, vehicule) VALUES (%s, %s, %s, %s)",
            (nom, tel, email, vehicule)
        )
        client_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return client_id
    
    def get_client_by_tel(self, tel: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE tel = %s", (tel,))
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
                "UPDATE clients SET points_fidelite = points_fidelite + %s WHERE id = %s",
                (points, client_id)
            )
        else:
            cursor.execute(
                "UPDATE clients SET points_fidelite = points_fidelite - %s WHERE id = %s",
                (points, client_id)
            )
        conn.commit()
        conn.close()
    
    def update_client_depense(self, client_id: int, montant: float):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET total_depense = total_depense + %s WHERE id = %s",
            (montant, client_id)
        )
        conn.commit()
        conn.close()
    
    # ===== SERVICES =====
    def ajouter_service(self, nom: str, prix: float, duree: int, points: int = 1, description: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO services (nom, prix, duree, points, description) VALUES (%s, %s, %s, %s, %s)",
            (nom, prix, duree, points, description)
        )
        service_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return service_id
    
    def get_all_services(self, actif_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if actif_only:
            cursor.execute("SELECT * FROM services WHERE actif = TRUE ORDER BY prix")
        else:
            cursor.execute("SELECT * FROM services ORDER BY prix")
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services
    
    def delete_service(self, service_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE services SET actif = FALSE WHERE id = %s", (service_id,))
        conn.commit()
        conn.close()
    
    # ===== POSTES =====
    def get_all_postes(self, actif_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if actif_only:
            cursor.execute("SELECT * FROM postes WHERE actif = TRUE")
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
            "INSERT INTO employes (nom, tel, poste, salaire) VALUES (%s, %s, %s, %s)",
            (nom, tel, poste, salaire)
        )
        employe_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return employe_id
    
    def get_all_employes(self, actif_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if actif_only:
            cursor.execute("SELECT * FROM employes WHERE actif = TRUE")
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'en_attente')""",
            (client_id, service_id, poste_id, employe_id, date, heure, montant, notes, code_promo, reduction, points_utilises)
        )
        reservation_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return reservation_id
    
    def get_reservations_by_date(self, date: str) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.client_id, r.service_id, r.poste_id, r.employe_id,
                   r.date, r.heure, r.statut, r.montant, r.montant_paye,
                   r.methode_paiement, r.notes, r.code_promo, r.reduction,
                   r.points_utilises, r.created_at,
                   c.nom as client_nom, c.tel as client_tel, c.vehicule,
                   s.nom as service_nom, s.duree, s.points as service_points,
                   e.nom as employe_nom, p.nom as poste_nom
            FROM reservations r
            LEFT JOIN clients c ON r.client_id = c.id
            LEFT JOIN services s ON r.service_id = s.id
            LEFT JOIN employes e ON r.employe_id = e.id
            LEFT JOIN postes p ON r.poste_id = p.id
            WHERE r.date = %s
            ORDER BY r.heure
        """, (date,))
        reservations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reservations
    
    def get_all_reservations(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.client_id, r.service_id, r.poste_id, r.employe_id,
                   r.date, r.heure, r.statut, r.montant, r.montant_paye,
                   r.methode_paiement, r.notes, r.code_promo, r.reduction,
                   r.points_utilises, r.created_at,
                   c.nom as client_nom, c.tel as client_tel, c.vehicule,
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
            "UPDATE reservations SET statut = %s WHERE id = %s",
            (statut, reservation_id)
        )
        conn.commit()
        conn.close()
    
    def delete_reservation(self, reservation_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
        conn.commit()
        conn.close()
    
    # ===== PAIEMENTS =====
    def ajouter_paiement(self, reservation_id: int, montant: float, methode: str, notes: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paiements (reservation_id, montant, methode, notes) VALUES (%s, %s, %s, %s)",
            (reservation_id, montant, methode, notes)
        )
        paiement_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        
        # Mettre à jour le montant payé de la réservation
        cursor.execute(
            "UPDATE reservations SET montant_paye = montant_paye + %s, methode_paiement = %s WHERE id = %s",
            (montant, methode, reservation_id)
        )
        
        conn.commit()
        conn.close()
        return paiement_id
    
    def get_all_paiements(self) -> List[Dict]:
        """Récupère tous les paiements avec infos clients et services"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.reservation_id, p.montant, p.methode as methode_paiement, 
                   p.date_paiement, p.notes,
                   c.nom as client_nom, s.nom as service_nom
            FROM paiements p
            LEFT JOIN reservations r ON p.reservation_id = r.id
            LEFT JOIN clients c ON r.client_id = c.id
            LEFT JOIN services s ON r.service_id = s.id
            ORDER BY p.date_paiement DESC
        """)
        paiements = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return paiements
    
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
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (code, type, valeur, date_debut, date_fin, utilisations_max)
        )
        promo_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return promo_id
    
    def verifier_code_promo(self, code: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM codes_promo 
            WHERE code = %s AND actif = TRUE 
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
            "UPDATE codes_promo SET utilisations_actuelles = utilisations_actuelles + 1 WHERE code = %s",
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
        cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE date = %s", (today,))
        rdv_today = cursor.fetchone()['count']
        
        # Revenus aujourd'hui - Utilise la table paiements
        cursor.execute(
            "SELECT SUM(montant) as total FROM paiements WHERE DATE(date_paiement) = %s",
            (today,)
        )
        revenus_today = cursor.fetchone()['total'] or 0
        
        # Revenus total - Utilise la table paiements
        cursor.execute("SELECT SUM(montant) as total FROM paiements")
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
            GROUP BY s.id, s.nom
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
            SELECT DATE(date_paiement) as date, SUM(montant) as revenus, COUNT(*) as nb_rdv
            FROM paiements
            GROUP BY DATE(date_paiement)
            ORDER BY DATE(date_paiement) DESC
            LIMIT %s
        """, (limit,))
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def get_services_stats(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.nom, COUNT(*) as nb_reservations, SUM(p.montant) as revenus
            FROM paiements p
            JOIN reservations r ON p.reservation_id = r.id
            JOIN services s ON r.service_id = s.id
            GROUP BY s.id, s.nom
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
            "SELECT * FROM recompenses WHERE actif = TRUE AND points_requis <= %s ORDER BY points_requis DESC",
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
            VALUES (%s, %s, %s, %s, %s)""",
            (client_id, reservation_id, points, type, description)
        )
        conn.commit()
        conn.close()
    
    # ===== PRODUITS/STOCK =====
    def ajouter_produit(self, nom: str, quantite: int, seuil_alerte: int, unite: str, prix_unitaire: float) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produits (nom, quantite, seuil_alerte, unite, prix_unitaire) VALUES (%s, %s, %s, %s, %s)",
            (nom, quantite, seuil_alerte, unite, prix_unitaire)
        )
        produit_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
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
            "INSERT INTO mouvements_stock (produit_id, quantite, type, prix, notes) VALUES (%s, %s, %s, %s, %s)",
            (produit_id, quantite, type, prix, notes)
        )
        
        # Mettre à jour la quantité
        if type == "entree":
            cursor.execute(
                "UPDATE produits SET quantite = quantite + %s WHERE id = %s",
                (quantite, produit_id)
            )
        else:
            cursor.execute(
                "UPDATE produits SET quantite = quantite - %s WHERE id = %s",
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
    
    # ===== GESTION COMPTES EMPLOYÉS =====
    def creer_compte_employe(self, username: str, password: str, email: str = "") -> int:
        """Crée un compte utilisateur pour un employé"""
        conn = self.get_connection()
        cursor = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, email, role) VALUES (%s, %s, %s, %s)",
                (username, password_hash, email, "employe")
            )
            user_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return -1  # Username déjà existant
    
    def lier_employe_user(self, employe_id: int, user_id: int):
        """Lie un employé à son compte utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employes SET user_id = %s WHERE id = %s",
            (user_id, employe_id)
        )
        conn.commit()
        conn.close()
    
    def supprimer_employe(self, employe_id: int):
        """Désactive un employé (soft delete)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE employes SET actif = FALSE WHERE id = %s", (employe_id,))
        conn.commit()
        conn.close()
    
    def modifier_employe(self, employe_id: int, nom: str = None, tel: str = None, poste: str = None, salaire: float = None):
        """Modifie les informations d'un employé"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if nom:
            updates.append("nom = ?")
            params.append(nom)
        if tel:
            updates.append("tel = ?")
            params.append(tel)
        if poste:
            updates.append("poste = ?")
            params.append(poste)
        if salaire is not None:
            updates.append("salaire = ?")
            params.append(salaire)
        
        if updates:
            params.append(employe_id)
            query = f"UPDATE employes SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    # ===== POINTAGES =====
    def enregistrer_pointage(self, user_id: int, type_pointage: str, notes: str = "") -> int:
        """Enregistre un pointage (arrivée/départ)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        heure_str = now.strftime("%H:%M")
        
        cursor.execute(
            "INSERT INTO pointages (user_id, type, date, heure, notes) VALUES (%s, %s, %s, %s, %s)",
            (user_id, type_pointage, date_str, heure_str, notes)
        )
        pointage_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return pointage_id
    
    def get_pointages_jour(self, date_str: str) -> List[Dict]:
        """Récupère tous les pointages d'une date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, u.username, u.role
            FROM pointages p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.date = %s
            ORDER BY p.heure
        """, (date_str,))
        pointages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pointages
    
    def get_pointages_employe(self, user_id: int, date_debut: str = None, date_fin: str = None) -> List[Dict]:
        """Récupère les pointages d'un employé sur une période"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if date_debut and date_fin:
            cursor.execute("""
                SELECT * FROM pointages
                WHERE user_id = %s AND date BETWEEN %s AND %s
                ORDER BY date DESC, heure DESC
            """, (user_id, date_debut, date_fin))
        else:
            cursor.execute("""
                SELECT * FROM pointages
                WHERE user_id = %s
                ORDER BY date DESC, heure DESC
                LIMIT 30
            """, (user_id,))
        
        pointages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pointages
    
    def calculer_heures_travail(self, user_id: int, date_str: str) -> Dict:
        """Calcule les heures de travail d'un employé pour une date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT type, heure FROM pointages
            WHERE user_id = %s AND date = %s
            ORDER BY heure
        """, (user_id, date_str))
        
        pointages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not pointages:
            return {"heures_travail": 0, "arrivee": None, "depart": None}
        
        arrivee = next((p["heure"] for p in pointages if p["type"] == "arrivee"), None)
        depart = next((p["heure"] for p in pointages if p["type"] == "depart"), None)
        
        heures_travail = 0
        if arrivee and depart:
            h_arr = datetime.strptime(arrivee, "%H:%M")
            h_dep = datetime.strptime(depart, "%H:%M")
            delta = h_dep - h_arr
            heures_travail = delta.total_seconds() / 3600
        
        return {
            "heures_travail": round(heures_travail, 2),
            "arrivee": arrivee,
            "depart": depart
        }
    
    # ===== GESTION PHOTOS AVANT/APRÈS =====
    def ajouter_photo_service(self, reservation_id: int, type_photo: str, photo_data: bytes, employe_id: int = None, notes: str = "") -> int:
        """Ajoute une photo (avant ou après) pour un service"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO photos_services (reservation_id, type_photo, photo_data, employe_id, notes) VALUES (%s, %s, %s, %s, %s)",
            (reservation_id, type_photo, photo_data, employe_id, notes)
        )
        photo_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        
        conn.commit()
        conn.close()
        return photo_id
    
    def get_photos_service(self, reservation_id: int, type_photo: str = None) -> List[Dict]:
        """Récupère les photos d'un service (toutes ou filtrées par type)"""
        # Validation de l'ID
        if not reservation_id or reservation_id is None:
            return []
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if type_photo:
            cursor.execute(
                "SELECT * FROM photos_services WHERE reservation_id = %s AND type_photo = %s ORDER BY date_ajout",
                (reservation_id, type_photo)
            )
        else:
            cursor.execute(
                "SELECT * FROM photos_services WHERE reservation_id = %s ORDER BY type_photo, date_ajout",
                (reservation_id,)
            )
        
        photos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return photos
    
    def supprimer_photo_service(self, photo_id: int):
        """Supprime une photo spécifique"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM photos_services WHERE id = %s", (photo_id,))
        conn.commit()
        conn.close()
    
    def get_toutes_photos_services(self, limit: int = 100) -> List[Dict]:
        """Récupère toutes les photos des services (pour galerie) groupées par réservation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT ps.reservation_id, r.date, s.nom as service_nom, c.nom as client_nom, c.vehicule
            FROM photos_services ps
            JOIN reservations r ON ps.reservation_id = r.id
            JOIN services s ON r.service_id = s.id
            JOIN clients c ON r.client_id = c.id
            ORDER BY r.date DESC
            LIMIT %s
        """, (limit,))
        reservations = [dict(row) for row in cursor.fetchall()]
        
        # Pour chaque réservation, récupérer toutes les photos
        for res in reservations:
            cursor.execute("""
                SELECT id, type_photo, photo_data, date_ajout
                FROM photos_services
                WHERE reservation_id = %s
                ORDER BY type_photo, date_ajout
            """, (res['reservation_id'],))
            res['photos'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return reservations
    
    # ===== GESTION PARAMÈTRES ENTREPRISE =====
    
    def get_parametre(self, cle: str, default: str = None) -> Optional[str]:
        """Récupère un paramètre depuis la base"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT valeur FROM parametres WHERE cle = %s", (cle,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result['valeur']
        return default
    
    def set_parametre(self, cle: str, valeur: str):
        """Enregistre ou met à jour un paramètre"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO parametres (cle, valeur)
            VALUES (%s, %s)
        """, (cle, valeur))
        
        conn.commit()
        conn.close()
    
    def get_info_entreprise(self) -> Dict:
        """Récupère toutes les informations de l'entreprise"""
        return {
            'nom': self.get_parametre('nom_entreprise', 'WashAfrique Pro'),
            'description': self.get_parametre('description_entreprise', ''),
            'telephone': self.get_parametre('tel_entreprise', ''),
            'email': self.get_parametre('email_entreprise', ''),
            'adresse': self.get_parametre('adresse_entreprise', ''),
            'site_web': self.get_parametre('site_web_entreprise', '')
        }
    
    def set_info_entreprise(self, nom: str, description: str, telephone: str, 
                           email: str, adresse: str, site_web: str):
        """Enregistre les informations de l'entreprise"""
        self.set_parametre('nom_entreprise', nom)
        self.set_parametre('description_entreprise', description)
        self.set_parametre('tel_entreprise', telephone)
        self.set_parametre('email_entreprise', email)
        self.set_parametre('adresse_entreprise', adresse)
        self.set_parametre('site_web_entreprise', site_web)
    
    # ===== SUPPRESSION HISTORIQUE =====
    
    def supprimer_historique_services(self, date_avant: str = None):
        """Supprime l'historique des services (optionnel: avant une date)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if date_avant:
            # Supprimer services avant une date spécifique
            cursor.execute("DELETE FROM reservations WHERE date_reservation < %s", (date_avant,))
            cursor.execute("DELETE FROM paiements WHERE DATE(date_paiement) < %s", (date_avant,))
        else:
            # Supprimer TOUT l'historique
            cursor.execute("DELETE FROM reservations")
            cursor.execute("DELETE FROM paiements")
            cursor.execute("DELETE FROM photos_services")
            cursor.execute("DELETE FROM historique_fidelite")
        
        lignes_supprimees = cursor.rowcount
        conn.commit()
        conn.close()
        return lignes_supprimees
    
    def reinitialiser_ca(self):
        """Réinitialise le chiffre d'affaires (supprime tous les paiements)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM paiements")
        nb_paiements = cursor.rowcount
        
        # Réinitialiser montant_paye des réservations
        cursor.execute("UPDATE reservations SET montant_paye = 0, statut = 'en_attente'")
        
        conn.commit()
        conn.close()
        return nb_paiements
    
    def reinitialiser_clients(self):
        """Réinitialise points fidélité et total dépenses des clients"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE clients SET points_fidelite = 0, total_depense = 0")
        cursor.execute("DELETE FROM historique_fidelite")
        
        conn.commit()
        conn.close()
    
    def archiver_et_reinitialiser(self, nom_archive: str = None):
        """Archive les données actuelles puis réinitialise tout"""
        import shutil
        from datetime import datetime
        
        # Créer nom archive avec timestamp
        if not nom_archive:
            nom_archive = f"washafrique_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        # Copier la base actuelle vers archive
        shutil.copy2(self.db_name, nom_archive)
        
        # Réinitialiser
        self.reinitialiser_ca()
        self.supprimer_historique_services()
        self.reinitialiser_clients()
        
        return nom_archive
    
    # ===== SITE CLIENT - PARAMÈTRES =====
    def get_parametre_site_client(self, cle: str, defaut: str = "") -> str:
        """Récupère un paramètre du site client"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT valeur FROM parametres_site_client WHERE cle = %s", (cle,))
        result = cursor.fetchone()
        conn.close()
        return result['valeur'] if result else defaut
    
    def set_parametre_site_client(self, cle: str, valeur: str):
        """Met à jour un paramètre du site client"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE parametres_site_client SET valeur = %s, updated_at = CURRENT_TIMESTAMP WHERE cle = %s",
            (valeur, cle)
        )
        conn.commit()
        conn.close()
    
    def get_all_parametres_site_client(self) -> List[Dict]:
        """Récupère tous les paramètres site client"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parametres_site_client ORDER BY cle")
        parametres = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return parametres
    
    # ===== SITE CLIENT - CRÉNEAUX HORAIRES =====
    def get_creneaux_disponibles(self, jour_semaine: str = None) -> List[Dict]:
        """Récupère les créneaux horaires disponibles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if jour_semaine:
            cursor.execute(
                "SELECT * FROM creneaux_disponibles WHERE jour_semaine = %s AND actif = TRUE",
                (jour_semaine,)
            )
        else:
            cursor.execute("SELECT * FROM creneaux_disponibles")
        creneaux = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return creneaux
    
    def update_creneau(self, jour_semaine: str, heure_debut: str, heure_fin: str, 
                       intervalle: int, capacite: int, actif: int):
        """Met à jour un créneau horaire"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE creneaux_disponibles 
            SET heure_debut = %s, heure_fin = %s, intervalle_minutes = %s, 
                capacite_simultanee = %s, actif = %s
            WHERE jour_semaine = %s
        """, (heure_debut, heure_fin, intervalle, capacite, actif, jour_semaine))
        conn.commit()
        conn.close()
    
    # ===== SITE CLIENT - RÉSERVATIONS WEB =====
    def creer_reservation_web(self, nom: str, tel: str, email: str, service_id: int,
                              date: str, heure: str, notes: str = "") -> str:
        """Crée une réservation depuis le site client"""
        import random
        import string
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Générer code unique
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        cursor.execute("""
            INSERT INTO reservations_web 
            (code_reservation, nom_client, tel_client, email_client, service_id, 
             date_reservation, heure_reservation, notes_client)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (code, nom, tel, email, service_id, date, heure, notes))
        
        conn.commit()
        conn.close()
        return code
    
    def get_reservation_web_by_code(self, code: str) -> Optional[Dict]:
        """Récupère une réservation par son code"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, s.nom as service_nom, s.prix, s.duree
            FROM reservations_web r
            JOIN services s ON r.service_id = s.id
            WHERE r.code_reservation = %s
        """, (code,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_reservations_web_en_attente(self) -> List[Dict]:
        """Récupère toutes les réservations web en attente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, s.nom as service_nom, s.prix
            FROM reservations_web r
            JOIN services s ON r.service_id = s.id
            WHERE r.statut = 'en_attente'
            ORDER BY r.date_reservation, r.heure_reservation
        """)
        reservations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reservations
    
    def valider_reservation_web(self, code: str):
        """Valide une réservation web"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservations_web 
            SET statut = 'confirmee', confirmed_at = CURRENT_TIMESTAMP
            WHERE code_reservation = %s
        """, (code,))
        conn.commit()
        conn.close()
    
    def annuler_reservation_web(self, code: str):
        """Annule une réservation web"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservations_web 
            SET statut = 'annulee'
            WHERE code_reservation = %s
        """, (code,))
        conn.commit()
        conn.close()
    
    # ===== SITE CLIENT - AVIS =====
    def ajouter_avis_client(self, nom: str, note: int, commentaire: str = "", 
                            reservation_web_id: int = None) -> int:
        """Ajoute un avis client"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO avis_clients (reservation_web_id, nom_client, note, commentaire)
            VALUES (%s, %s, %s, %s)
        """, (reservation_web_id, nom, note, commentaire))
        avis_id = cursor.fetchone()['id']  # PostgreSQL: nécessite RETURNING id dans l'INSERT
        conn.commit()
        conn.close()
        return avis_id
    
    def get_avis_visibles(self, limit: int = 10) -> List[Dict]:
        """Récupère les avis visibles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM avis_clients 
            WHERE visible = TRUE 
            ORDER BY created_at DESC 
            LIMIT %s
        """, (limit,))
        avis = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return avis
    
    def toggle_visibilite_avis(self, avis_id: int):
        """Bascule la visibilité d'un avis"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE avis_clients 
            SET visible = NOT visible
            WHERE id = %s
        """, (avis_id,))
        conn.commit()
        conn.close()



    def get_all_users(self) -> List[Dict]:
        """Récupère tous les utilisateurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY created_at DESC")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def get_total_ca(self) -> float:
        """Calcule le chiffre d'affaires total"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(montant), 0) as total FROM paiements")
        result = cursor.fetchone()
        conn.close()
        return float(result['total']) if result and result['total'] else 0.0


# Alias pour compatibilité avec le code existant
Database = DatabasePostgres
