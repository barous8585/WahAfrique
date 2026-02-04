"""
Script de diagnostic connexion PostgreSQL pour Streamlit Cloud
Affiche des informations détaillées sur la tentative de connexion
"""

import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

st.title("🔍 Diagnostic Connexion PostgreSQL")

# Vérifier si Secrets existent
st.header("1️⃣ Vérification Secrets")

if hasattr(st, 'secrets'):
    st.success("✅ Module st.secrets accessible")
    
    if 'postgres' in st.secrets:
        st.success("✅ Section [postgres] trouvée dans Secrets")
        
        # Afficher les clés présentes (sans valeurs sensibles)
        keys = list(st.secrets.postgres.keys())
        st.info(f"Clés trouvées: {keys}")
        
        # Vérifier chaque clé requise
        required_keys = ['host', 'port', 'database', 'user', 'password']
        missing_keys = [k for k in required_keys if k not in keys]
        
        if missing_keys:
            st.error(f"❌ Clés manquantes: {missing_keys}")
        else:
            st.success("✅ Toutes les clés requises présentes")
            
            # Afficher les valeurs (masquer password)
            st.subheader("Configuration détectée:")
            st.code(f"""
host     = {st.secrets.postgres.host}
port     = {st.secrets.postgres.port} (type: {type(st.secrets.postgres.port).__name__})
database = {st.secrets.postgres.database}
user     = {st.secrets.postgres.user}
password = {'*' * len(st.secrets.postgres.password)} ({len(st.secrets.postgres.password)} caractères)
            """)
            
            # Test de connexion
            st.header("2️⃣ Test de connexion")
            
            try:
                st.info("Tentative de connexion...")
                
                conn = psycopg2.connect(
                    host=st.secrets.postgres.host,
                    port=int(st.secrets.postgres.port),
                    database=st.secrets.postgres.database,
                    user=st.secrets.postgres.user,
                    password=st.secrets.postgres.password,
                    cursor_factory=RealDictCursor,
                    connect_timeout=10
                )
                
                st.success("✅ CONNEXION RÉUSSIE!")
                
                # Test requête simple
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                st.success(f"✅ Version PostgreSQL: {version['version']}")
                
                # Compter les tables
                cursor.execute("""
                    SELECT COUNT(*) as nb_tables 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                nb_tables = cursor.fetchone()['nb_tables']
                st.success(f"✅ Nombre de tables: {nb_tables}")
                
                conn.close()
                
            except psycopg2.OperationalError as e:
                error_msg = str(e)
                st.error(f"❌ ERREUR DE CONNEXION")
                st.code(error_msg)
                
                # Diagnostic selon le type d'erreur
                if "timeout" in error_msg.lower():
                    st.warning("""
                    🔍 **Timeout détecté**
                    
                    Causes possibles:
                    - Supabase est en pause (projets gratuits se mettent en pause après inactivité)
                    - Firewall bloque la connexion
                    - Host incorrect
                    
                    Solutions:
                    1. Allez sur https://supabase.com/dashboard
                    2. Vérifiez que le projet est actif (vert)
                    3. Si "Paused", cliquez "Resume"
                    """)
                    
                elif "password" in error_msg.lower() or "authentication" in error_msg.lower():
                    st.warning("""
                    🔍 **Erreur d'authentification**
                    
                    Le mot de passe est incorrect.
                    
                    Solutions:
                    1. Allez sur Supabase Dashboard
                    2. Settings → Database → Connection string
                    3. Copiez le mot de passe (cliquez sur l'œil)
                    4. Mettez à jour les Secrets Streamlit
                    """)
                    
                elif "could not translate" in error_msg.lower() or "resolve" in error_msg.lower():
                    st.warning("""
                    🔍 **Host introuvable**
                    
                    Le hostname ne peut pas être résolu.
                    
                    Solutions:
                    1. Vérifiez l'orthographe du host dans Secrets
                    2. Format attendu: db.xxxxx.supabase.co
                    3. Ne pas inclure https:// ou postgres://
                    """)
                else:
                    st.warning("Erreur inconnue. Consultez le message ci-dessus.")
                    
            except Exception as e:
                st.error(f"❌ ERREUR INATTENDUE: {type(e).__name__}")
                st.code(str(e))
                
    else:
        st.error("❌ Section [postgres] introuvable dans Secrets")
        st.warning("""
        **Action requise:**
        
        1. Allez dans Settings → Secrets
        2. Ajoutez cette configuration:
        
        ```toml
        [postgres]
        host = "db.qstcskpamdnqssvcbana.supabase.co"
        port = 5432
        database = "postgres"
        user = "postgres"
        password = "Tobkesso.2006"
        ```
        
        3. Cliquez Save
        4. Attendez le redémarrage (30-60s)
        5. Rechargez cette page
        """)
else:
    st.error("❌ Module Streamlit Secrets non accessible")
    st.info("Ceci est normal en développement local.")
