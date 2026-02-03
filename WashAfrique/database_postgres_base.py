"""
Adaptateur PostgreSQL pour WashAfrique
Remplace SQLite par PostgreSQL (Supabase)
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any
import streamlit as st
from datetime import datetime

class DatabasePostgres:
    """Classe Database adaptée pour PostgreSQL"""
    
    def __init__(self):
        """Initialise la connexion PostgreSQL"""
        self.config = self._get_config()
        self.init_database()
    
    def _get_config(self) -> dict:
        """Récupère configuration depuis st.secrets ou db_config.py"""
        try:
            # Priorité 1: Streamlit Secrets (pour Cloud)
            if hasattr(st, 'secrets') and 'postgres' in st.secrets:
                return {
                    'host': st.secrets.postgres.host,
                    'port': st.secrets.postgres.port,
                    'database': st.secrets.postgres.database,
                    'user': st.secrets.postgres.user,
                    'password': st.secrets.postgres.password
                }
        except:
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
                "2. Ajoutez section [postgres] avec credentials"
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
                cursor_factory=RealDictCursor
            )
            return conn
        except psycopg2.OperationalError as e:
            raise Exception(f"❌ Erreur connexion PostgreSQL: {str(e)}")
    
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

# Pour compatibilité avec le code existant, créer un alias
Database = DatabasePostgres
