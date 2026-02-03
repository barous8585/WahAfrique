"""
Script pour convertir database.py (SQLite) en database_postgres.py (PostgreSQL)
"""

import re

print("🔄 Conversion database.py → database_postgres.py...")

# Lire database.py
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacements SQLite → PostgreSQL
conversions = [
    # Types de colonnes
    (r'INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY'),
    (r'TEXT', 'TEXT'),
    (r'DATETIME DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
    (r'DATE DEFAULT CURRENT_DATE', 'DATE DEFAULT CURRENT_DATE'),
    
    # Connexions
    (r'sqlite3\.connect\(self\.db_path\)', 'self.get_connection()'),
    (r'sqlite3\.Row', 'RealDictCursor'),
    (r'conn\.row_factory = sqlite3\.Row', '# RealDictCursor déjà configuré'),
    
    # Fetchall
    (r'\[dict\(row\) for row in cursor\.fetchall\(\)\]', '[dict(row) for row in cursor.fetchall()]'),
    
    # Placeholders
    (r'\?', '%s'),  # Attention: peut affecter les commentaires
    
    # Imports
    (r'import sqlite3', 'import psycopg2\nfrom psycopg2.extras import RealDictCursor'),
]

for pattern, replacement in conversions:
    content = re.sub(pattern, replacement, content)

# Remplacer la classe Database
content = content.replace(
    'class Database:',
    '''class DatabasePostgres:
    """Classe Database adaptée pour PostgreSQL (Supabase)"""
    
    def __init__(self):
        """Initialise la connexion PostgreSQL"""
        self.config = self._get_config()
        self.init_database()
    
    def _get_config(self) -> dict:
        """Récupère configuration depuis st.secrets ou db_config.py"""
        try:
            # Priorité 1: Streamlit Secrets (pour Cloud)
            import streamlit as st
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
                "Configuration base de données manquante!\\n"
                "Créez db_config.py avec vos credentials Supabase"
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
            raise Exception(f"Erreur connexion PostgreSQL: {str(e)}")

class Database:
'''
)

print("✅ Conversion terminée !")
print("⚠️  ATTENTION: Vérifiez manuellement les requêtes SQL complexes")

# Note: Ce script fait une conversion basique
# Il faudra vérifier et ajuster manuellement certaines parties
