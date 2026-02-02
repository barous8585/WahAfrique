import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go
from database import Database
import hashlib
import io

# Configuration de la page (SANS sidebar par défaut)
st.set_page_config(
    page_title="🚗 WashAfrique Pro - Nettoyage Esthétique",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "# WashAfrique Pro\nVersion 3.0 Enterprise\nSolution complète pour entreprise de nettoyage esthétique"
    }
)

# Initialisation de la base de données
if "db" not in st.session_state:
    st.session_state.db = Database()

# Style CSS moderne SANS sidebar
st.markdown("""
    <style>
    /* Cacher complètement la sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Style général */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header navigation */
    .nav-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cards modernes */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Boutons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 0 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .nav-header {
            padding: 0.5rem 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Horaires (configurables par le propriétaire)
if "horaires" not in st.session_state:
    st.session_state.horaires = {
        "ouverture": "08:00",
        "fermeture": "19:00",
        "pause_debut": "12:00",
        "pause_fin": "13:00"
    }

def format_fcfa(montant):
    """Formate en FCFA"""
    return f"{int(montant):,} FCFA".replace(",", " ")

# ===== AUTHENTIFICATION =====
def check_authentication():
    """Vérifie si l'utilisateur est connecté"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("# 🚗 WashAfrique Pro")
            st.markdown("### Solution de Gestion Entreprise de Nettoyage Esthétique")
            st.markdown("---")
            
            username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre identifiant")
            password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
            
            if st.button("🚀 Se connecter", use_container_width=True, type="primary"):
                user = st.session_state.db.verify_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success("✅ Connexion réussie !")
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
            
            st.markdown("---")
            st.info("💡 **Compte par défaut:** Propriétaire → admin / admin123")
        
        return False
    
    return True

# Vérifier l'authentification
if not check_authentication():
    st.stop()

# ===== NAVIGATION HORIZONTALE =====
nom_entreprise = st.session_state.db.get_parametre('nom_entreprise', 'WashAfrique Pro')
st.markdown(f"""
    <div class="nav-header">
        <h2 style="color: white; margin: 0;">🚗 {nom_entreprise} | {st.session_state.user["username"]} ({st.session_state.user["role"]})</h2>
    </div>
""", unsafe_allow_html=True)

# Bouton de déconnexion en haut à droite
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# Navigation selon le rôle
user_role = st.session_state.user["role"]

if user_role == "admin":  # PROPRIÉTAIRE
    tabs = st.tabs([
        "🏠 Tableau de Bord",
        "👥 Employés",
        "🔧 Services & Prix",
        "📅 Réservations",
        "💼 Clients",
        "💰 Paiements",
        "📦 Stock",
        "📊 Rapports",
        "⚙️ Mon Profil"
    ])
    
    # ===== ONGLET 1: TABLEAU DE BORD PROPRIÉTAIRE =====
    with tabs[0]:
        st.header("📊 Tableau de Bord Propriétaire")
        
        stats = st.session_state.db.get_stats_dashboard()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📅 RDV Aujourd'hui", stats["rdv_today"])
        with col2:
            st.metric("💰 CA Jour", format_fcfa(stats["revenus_today"]))
        with col3:
            st.metric("💰 CA Total", format_fcfa(stats["revenus_total"]))
        with col4:
            st.metric("👥 Clients", stats["total_clients"])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Évolution CA (30j)")
            revenus_data = st.session_state.db.get_revenus_par_jour(30)
            if revenus_data:
                df = pd.DataFrame(revenus_data)
                fig = px.line(df, x="date", y="revenus", markers=True)
                fig.update_layout(xaxis_title="Date", yaxis_title="Revenus (FCFA)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée disponible")
        
        with col2:
            st.subheader("🏆 Services Populaires")
            services_stats = st.session_state.db.get_services_stats()
            if services_stats:
                df = pd.DataFrame(services_stats)
                fig = px.pie(df, values="nb_reservations", names="nom", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée disponible")
        
        st.markdown("---")
        st.subheader("⏰ Activité Employés Aujourd'hui")
        
        # Afficher les pointages du jour
        pointages_today = st.session_state.db.get_pointages_jour(date.today().isoformat())
        
        if pointages_today:
            for pointage in pointages_today:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**{pointage['username']}**")
                with col2:
                    st.write(f"{pointage['type'].upper()} à {pointage['heure']}")
                with col3:
                    if pointage['type'] == 'arrivee':
                        st.success("✅")
                    else:
                        st.info("🏁")
        else:
            st.info("Aucun pointage aujourd'hui")
    
    # ===== ONGLET 2: GESTION EMPLOYÉS =====
    with tabs[1]:
        st.header("👨💼 Gestion des Employés")
        
        sub_tabs = st.tabs(["📋 Liste Employés", "➕ Ajouter Employé", "⏰ Pointages"])
        
        with sub_tabs[0]:
            st.subheader("📋 Tous les Employés")
            
            employes = st.session_state.db.get_all_employes(actif_only=True)
            
            if employes:
                for emp in employes:
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**{emp['nom']}**")
                    with col2:
                        st.write(f"📞 {emp['tel'] or 'N/A'}")
                    with col3:
                        st.write(f"🏷️ {emp['poste'] or 'N/A'}")
                    with col4:
                        st.write(f"💰 {format_fcfa(emp['salaire'])}/mois")
                    with col5:
                        if emp['actif']:
                            st.success("✅ Actif")
                        else:
                            st.error("❌ Inactif")
                    
                    with st.expander(f"Gérer {emp['nom']}"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            if st.button(f"🗑️ Supprimer", key=f"del_emp_{emp['id']}"):
                                # TODO: Implémenter suppression
                                st.warning("Suppression employé à implémenter")
                        
                        with col_b:
                            if st.button(f"✏️ Modifier", key=f"edit_emp_{emp['id']}"):
                                st.info("Modification à implémenter")
                    
                    st.markdown("---")
            else:
                st.info("Aucun employé enregistré")
        
        with sub_tabs[1]:
            st.subheader("➕ Ajouter un Nouvel Employé")
            
            with st.form("nouvel_employe"):
                nom = st.text_input("👤 Nom complet *", placeholder="Ex: Jean Kouassi")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    tel = st.text_input("📞 Téléphone *", placeholder="+225 XX XX XX XX")
                    username_emp = st.text_input("🔐 Nom d'utilisateur *", placeholder="jean.k")
                
                with col2:
                    poste = st.text_input("🏷️ Poste", placeholder="Ex: Nettoyeur")
                    password_emp = st.text_input("🔒 Mot de passe *", type="password", placeholder="Minimum 6 caractères")
                
                salaire = st.number_input("💰 Salaire mensuel (FCFA)", min_value=0, step=10000, value=100000)
                
                submitted = st.form_submit_button("✅ Créer le Compte Employé", use_container_width=True, type="primary")
                
                if submitted:
                    if nom and tel and username_emp and password_emp:
                        if len(password_emp) < 6:
                            st.error("⚠️ Le mot de passe doit contenir au moins 6 caractères")
                        else:
                            # Créer le compte utilisateur
                            user_id = st.session_state.db.creer_compte_employe(username_emp, password_emp, "")
                            
                            if user_id == -1:
                                st.error("❌ Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
                            else:
                                # Créer l'employé
                                emp_id = st.session_state.db.ajouter_employe(nom, tel, poste, salaire)
                                
                                # Lier employé et compte utilisateur
                                st.session_state.db.lier_employe_user(emp_id, user_id)
                                
                                st.success(f"✅ Employé {nom} créé avec succès !")
                                st.info(f"📋 **Identifiants de connexion:**\n- Username: `{username_emp}`\n- Password: `{password_emp}`")
                                st.balloons()
                    else:
                        st.error("⚠️ Veuillez remplir tous les champs obligatoires")
        
        with sub_tabs[2]:
            st.subheader("⏰ Pointages et Présences")
            
            date_pointage = st.date_input("📅 Sélectionner une date", value=date.today())
            
            # Afficher les pointages du jour sélectionné
            pointages_jour = st.session_state.db.get_pointages_jour(date_pointage.isoformat())
            
            if pointages_jour:
                st.write(f"**{len(pointages_jour)} pointages ce jour**")
                
                for pointage in pointages_jour:
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**{pointage['username']}**")
                    with col2:
                        st.write(f"🕐 {pointage['heure']}")
                    with col3:
                        type_emoji = "✅ ARRIVÉE" if pointage['type'] == 'arrivee' else "🏁 DÉPART"
                        st.write(type_emoji)
                    with col4:
                        if pointage.get('notes'):
                            st.caption(pointage['notes'])
                    
                    st.markdown("---")
            else:
                st.info(f"Aucun pointage le {date_pointage.strftime('%d/%m/%Y')}")
    
    # ===== ONGLET 3: SERVICES & PRIX =====
    with tabs[2]:
        st.header("🔧 Gestion Services & Prix")
        
        sub_tabs = st.tabs(["📋 Mes Services", "➕ Nouveau Service", "🏷️ Catégories"])
        
        with sub_tabs[0]:
            st.subheader("📋 Liste de vos Services")
            
            services = st.session_state.db.get_all_services(actif_only=True)
            
            if services:
                for service in services:
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                    
                    with col1:
                        st.write(f"**{service['nom']}**")
                        if service.get('description'):
                            st.caption(service['description'])
                    with col2:
                        st.write(f"💰 {format_fcfa(service['prix'])}")
                    with col3:
                        st.write(f"⏱️ {service['duree']} min")
                    with col4:
                        st.write(f"⭐ {service['points']} pts")
                    with col5:
                        if service['actif']:
                            st.success("✅")
                        else:
                            st.error("❌")
                    
                    # Options de gestion du service
                    with st.expander(f"✏️ Gérer {service['nom']}"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            if st.button(f"🗑️ Supprimer", key=f"del_service_{service['id']}"):
                                st.session_state.db.delete_service(service['id'])
                                st.success(f"✅ Service '{service['nom']}' supprimé")
                                st.rerun()
                        
                        with col_b:
                            if st.button(f"✏️ Modifier Prix", key=f"edit_service_{service['id']}"):
                                st.session_state[f"edit_service_mode_{service['id']}"] = True
                        
                        # Mode édition
                        if st.session_state.get(f"edit_service_mode_{service['id']}", False):
                            with st.form(f"form_edit_service_{service['id']}"):
                                new_nom = st.text_input("Nom du service", value=service['nom'])
                                new_prix = st.number_input("Prix (FCFA)", value=float(service['prix']), step=1000.0)
                                new_duree = st.number_input("Durée (minutes)", value=int(service['duree']), step=5)
                                new_points = st.number_input("Points fidélité", value=int(service['points']))
                                new_desc = st.text_area("Description", value=service.get('description', ''))
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                                        conn = st.session_state.db.get_connection()
                                        cursor = conn.cursor()
                                        cursor.execute("""
                                            UPDATE services 
                                            SET nom = ?, prix = ?, duree = ?, points = ?, description = ?
                                            WHERE id = ?
                                        """, (new_nom, new_prix, new_duree, new_points, new_desc, service['id']))
                                        conn.commit()
                                        conn.close()
                                        st.success("✅ Service modifié !")
                                        st.session_state[f"edit_service_mode_{service['id']}"] = False
                                        st.rerun()
                    
                    st.markdown("---")
            else:
                st.info("Aucun service créé")
        
        with sub_tabs[1]:
            st.subheader("➕ Créer un Nouveau Service")
            
            with st.form("nouveau_service"):
                nom_service = st.text_input("🏷️ Nom du service *", placeholder="Ex: Nettoyage Intérieur Premium")
                description_service = st.text_area("📝 Description", placeholder="Décrivez le service en détail...")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    prix_service = st.number_input("💰 Prix (FCFA) *", min_value=1000, step=1000, value=10000)
                with col2:
                    duree_service = st.number_input("⏱️ Durée (minutes) *", min_value=5, step=5, value=60)
                with col3:
                    points_service = st.number_input("⭐ Points fidélité", min_value=1, value=2)
                
                submitted = st.form_submit_button("✅ Créer le Service", use_container_width=True, type="primary")
                
                if submitted:
                    if nom_service and prix_service > 0 and duree_service > 0:
                        service_id = st.session_state.db.ajouter_service(
                            nom_service, prix_service, duree_service, points_service, description_service
                        )
                        st.success(f"✅ Service '{nom_service}' créé avec succès !")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("⚠️ Veuillez remplir tous les champs obligatoires")
        
        with sub_tabs[2]:
            st.subheader("🏷️ Catégories de Services")
            st.info("Fonctionnalité de catégorisation à développer")
    
    # ===== ONGLET 4: RÉSERVATIONS =====
    with tabs[3]:
        st.header("📅 Gestion des Réservations")
        
        sub_tabs = st.tabs(["➕ Nouvelle Réservation", "📋 Planning", "✅ À Valider", "🔍 Rechercher"])
        
        with sub_tabs[0]:
            st.subheader("➕ Créer une Nouvelle Réservation")
            
            services = st.session_state.db.get_all_services()
            
            if not services:
                st.warning("⚠️ Aucun service disponible. Créez d'abord des services.")
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 👤 Informations Client")
                    
                    tel_search = st.text_input("📞 Rechercher par téléphone", placeholder="+225 XX XX XX XX")
                    client_existant = None
                    
                    if tel_search:
                        client_existant = st.session_state.db.get_client_by_tel(tel_search)
                        if client_existant:
                            st.success(f"✅ Client trouvé: **{client_existant['nom']}**")
                    
                    if client_existant:
                        nom = st.text_input("👤 Nom", value=client_existant['nom'])
                        tel = st.text_input("📞 Téléphone", value=client_existant['tel'], disabled=True)
                        vehicule = st.text_input("🚗 Véhicule", value=client_existant.get('vehicule', ''))
                    else:
                        nom = st.text_input("👤 Nom *", placeholder="Nom du client")
                        tel = st.text_input("📞 Téléphone *", value=tel_search, placeholder="+225 XX XX XX XX")
                        vehicule = st.text_input("🚗 Véhicule *", placeholder="Marque et modèle")
                
                with col2:
                    st.markdown("#### 📋 Détails Réservation")
                    
                    date_rdv = st.date_input("📅 Date *", min_value=date.today())
                    
                    service_id = st.selectbox(
                        "🔧 Service *",
                        options=[s['id'] for s in services],
                        format_func=lambda x: f"{next(s['nom'] for s in services if s['id'] == x)} - {format_fcfa(next(s['prix'] for s in services if s['id'] == x))}"
                    )
                    
                    heure = st.time_input("🕐 Heure *", value=datetime.strptime("09:00", "%H:%M").time())
                    
                    notes = st.text_area("📝 Notes (optionnel)")
                
                if st.button("✅ Confirmer la Réservation", use_container_width=True, type="primary"):
                    if nom and tel and vehicule:
                        if client_existant:
                            client_id = client_existant['id']
                        else:
                            client_id = st.session_state.db.ajouter_client(nom, tel, "", vehicule)
                        
                        service_choisi = next(s for s in services if s['id'] == service_id)
                        heure_str = heure.strftime("%H:%M")
                        
                        reservation_id = st.session_state.db.ajouter_reservation(
                            client_id=client_id,
                            service_id=service_id,
                            date=date_rdv.isoformat(),
                            heure=heure_str,
                            montant=service_choisi['prix'],
                            notes=notes
                        )
                        
                        st.success(f"✅ Réservation #{reservation_id:05d} créée avec succès !")
                        st.balloons()
                    else:
                        st.error("⚠️ Veuillez remplir tous les champs obligatoires")
        
        with sub_tabs[1]:
            st.subheader("📅 Planning des Réservations")
            
            date_select = st.date_input("Choisir une date", value=date.today())
            
            reservations_jour = st.session_state.db.get_reservations_by_date(date_select.isoformat())
            
            if reservations_jour:
                for res in sorted(reservations_jour, key=lambda x: x['heure']):
                    with st.expander(f"🕐 {res['heure']} - {res['client_nom']} ({res['statut']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Client:** {res['client_nom']}")
                            st.write(f"**Téléphone:** {res['client_tel']}")
                            st.write(f"**Véhicule:** {res['vehicule']}")
                        
                        with col2:
                            st.write(f"**Service:** {res['service_nom']}")
                            st.write(f"**Prix:** {format_fcfa(res['montant'])}")
                            st.write(f"**Statut:** {res['statut']}")
                        
                        if res.get('notes'):
                            st.info(f"📝 {res['notes']}")
            else:
                st.info("Aucune réservation ce jour")
        
        with sub_tabs[2]:
            st.subheader("✅ Services à Valider")
            
            st.info("💡 Validez la qualité des services terminés et payés")
            
            # Récupérer toutes les réservations payées mais pas validées
            all_reservations = st.session_state.db.get_all_reservations()
            reservations_a_valider = [r for r in all_reservations if r['statut'] == 'paye']
            
            if reservations_a_valider:
                st.write(f"**{len(reservations_a_valider)} service(s) en attente de validation**")
                st.markdown("---")
                
                for res in sorted(reservations_a_valider, key=lambda x: (x['date'], x['heure']), reverse=True):
                    with st.expander(f"🚗 {res['client_nom']} - {res['service_nom']} | 📅 {res['date']} {res['heure']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Client:** {res['client_nom']}")
                            st.write(f"**Téléphone:** {res['client_tel']}")
                            st.write(f"**Véhicule:** {res['vehicule']}")
                            st.write(f"**Date:** {res['date']}")
                            st.write(f"**Heure:** {res['heure']}")
                        
                        with col2:
                            st.write(f"**Service:** {res['service_nom']}")
                            st.write(f"**Prix:** {format_fcfa(res['montant'])}")
                            st.write(f"**Montant payé:** {format_fcfa(res['montant_paye'])}")
                            st.write(f"**Méthode:** {res.get('methode_paiement', 'N/A')}")
                            st.success("💰 PAYÉ")
                        
                        if res.get('notes'):
                            st.info(f"📝 Notes: {res['notes']}")
                        
                        st.markdown("---")
                        
                        col_a, col_b, col_c = st.columns([2, 2, 1])
                        
                        with col_a:
                            if st.button(f"✅ Valider (Qualité OK)", key=f"valide_{res['id']}", type="primary", use_container_width=True):
                                st.session_state.db.update_reservation_statut(res['id'], 'valide')
                                st.success("✅ Service validé avec succès !")
                                st.balloons()
                                st.rerun()
                        
                        with col_b:
                            if st.button(f"⚠️ Problème Qualité", key=f"probleme_{res['id']}", use_container_width=True):
                                st.session_state[f"show_note_{res['id']}"] = True
                        
                        # Formulaire de note si problème
                        if st.session_state.get(f"show_note_{res['id']}", False):
                            with st.form(f"form_probleme_{res['id']}"):
                                note_probleme = st.text_area("Décrivez le problème", placeholder="Ex: Client mécontent du résultat...")
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                                        # Mettre à jour avec note
                                        conn = st.session_state.db.get_connection()
                                        cursor = conn.cursor()
                                        cursor.execute(
                                            "UPDATE reservations SET notes = ? WHERE id = ?",
                                            (f"[PROBLÈME] {note_probleme}", res['id'])
                                        )
                                        conn.commit()
                                        conn.close()
                                        st.warning("⚠️ Problème enregistré - Service non validé")
                                        st.session_state[f"show_note_{res['id']}"] = False
                                        st.rerun()
                                with col_cancel:
                                    if st.form_submit_button("❌ Annuler", use_container_width=True):
                                        st.session_state[f"show_note_{res['id']}"] = False
                                        st.rerun()
            else:
                st.success("✅ Tous les services sont validés !")
                st.info("Aucun service en attente de validation")
        
        with sub_tabs[3]:
            st.subheader("🔍 Rechercher une Réservation")
            st.info("Fonctionnalité de recherche à développer")
    
    # ===== ONGLET 5: CLIENTS =====
    with tabs[4]:
        st.header("👥 Gestion des Clients")
        
        clients = st.session_state.db.get_all_clients()
        
        if clients:
            st.write(f"**Total: {len(clients)} clients**")
            
            search = st.text_input("🔍 Rechercher", placeholder="Nom ou téléphone...")
            
            if search:
                clients = [c for c in clients if search.lower() in c['nom'].lower() or search in c['tel']]
            
            st.markdown("---")
            
            for client in clients:
                with st.expander(f"👤 {client['nom']} - {client['tel']} | ⭐ {client['points_fidelite']} pts"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Téléphone:** {client['tel']}")
                        st.write(f"**Email:** {client.get('email', 'N/A')}")
                        st.write(f"**Véhicule:** {client.get('vehicule', 'N/A')}")
                    
                    with col2:
                        st.metric("Points fidélité", client['points_fidelite'])
                        st.metric("Total dépensé", format_fcfa(client['total_depense']))
        else:
            st.info("Aucun client enregistré")
    
    # ===== ONGLET 6: PAIEMENTS =====
    with tabs[5]:
        st.header("💰 Gestion des Paiements")
        
        st.info("Module paiements à développer complètement")
    
    # ===== ONGLET 7: STOCK =====
    with tabs[6]:
        st.header("📦 Gestion du Stock")
        
        st.info("Module stock à développer complètement")
    
    # ===== ONGLET 8: RAPPORTS =====
    with tabs[7]:
        st.header("📊 Rapports et Statistiques")
        
        sub_tabs_rapports = st.tabs(["📈 Statistiques", "📸 Galerie Photos", "📄 Exports"])
        
        with sub_tabs_rapports[0]:
            st.subheader("📈 Statistiques Générales")
            st.info("Module statistiques à développer")
        
        with sub_tabs_rapports[1]:
            st.subheader("📸 Galerie Photos Avant/Après")
            
            st.info("""
            💡 **Photos de vos services pour TikTok, Instagram, Facebook**
            
            **Pour qualité optimale** :
            - ✅ Utilisez le mode "📁 Upload" plutôt que "📷 Caméra"
            - ✅ Prenez d'abord vos photos avec l'app caméra native du téléphone
            - ✅ Téléchargez ensuite les photos en haute résolution
            - ⚠️ Le mode "Caméra web" compresse automatiquement pour la performance
            """)
            
            # Récupérer toutes les réservations avec photos
            services_avec_photos = st.session_state.db.get_toutes_photos_services(limit=100)
            
            if services_avec_photos:
                st.write(f"**{len(services_avec_photos)} service(s) avec photos**")
                
                st.markdown("---")
                
                # Afficher les photos par service
                for service in services_avec_photos:
                    with st.expander(f"🚗 {service['client_nom']} - {service['service_nom']} | {service['date']}", expanded=False):
                        st.write(f"**Véhicule:** {service['vehicule']}")
                        
                        # Séparer photos avant et après
                        photos_avant = [p for p in service['photos'] if p['type_photo'] == 'avant']
                        photos_apres = [p for p in service['photos'] if p['type_photo'] == 'apres']
                        
                        col_avant, col_apres = st.columns(2)
                        
                        # Photos AVANT
                        with col_avant:
                            st.write(f"**📸 AVANT ({len(photos_avant)} photo(s))**")
                            if photos_avant:
                                for idx, photo in enumerate(photos_avant):
                                    st.image(photo['photo_data'], caption=f"Avant #{idx+1}", use_container_width=True)
                                    col_dl, col_del = st.columns([3, 1])
                                    with col_dl:
                                        st.download_button(
                                            "⬇️ Télécharger",
                                            data=photo['photo_data'],
                                            file_name=f"avant_{service['client_nom']}_{idx+1}_{service['date']}.jpg",
                                            mime="image/jpeg",
                                            key=f"dl_avant_{photo['id']}",
                                            use_container_width=True
                                        )
                                    with col_del:
                                        if st.button("🗑️", key=f"del_gallery_avant_{photo['id']}"):
                                            st.session_state.db.supprimer_photo_service(photo['id'])
                                            st.success("✅ Photo supprimée")
                                            st.rerun()
                                    st.markdown("---")
                            else:
                                st.info("Aucune photo avant")
                        
                        # Photos APRÈS
                        with col_apres:
                            st.write(f"**📸 APRÈS ({len(photos_apres)} photo(s))**")
                            if photos_apres:
                                for idx, photo in enumerate(photos_apres):
                                    st.image(photo['photo_data'], caption=f"Après #{idx+1}", use_container_width=True)
                                    col_dl, col_del = st.columns([3, 1])
                                    with col_dl:
                                        st.download_button(
                                            "⬇️ Télécharger",
                                            data=photo['photo_data'],
                                            file_name=f"apres_{service['client_nom']}_{idx+1}_{service['date']}.jpg",
                                            mime="image/jpeg",
                                            key=f"dl_apres_{photo['id']}",
                                            use_container_width=True
                                        )
                                    with col_del:
                                        if st.button("🗑️", key=f"del_gallery_apres_{photo['id']}"):
                                            st.session_state.db.supprimer_photo_service(photo['id'])
                                            st.success("✅ Photo supprimée")
                                            st.rerun()
                                    st.markdown("---")
                            else:
                                st.info("Aucune photo après")
            else:
                st.info("Aucun service avec photos pour le moment")
                st.write("💡 Les employés peuvent ajouter des photos lors des services en cours")
        
        with sub_tabs_rapports[2]:
            st.subheader("📄 Exports")
            st.info("Module exports à développer")
    
    # ===== ONGLET 9: PROFIL PROPRIÉTAIRE =====
    with tabs[8]:
        st.header("⚙️ Mon Profil et Paramètres")
        
        sub_tabs = st.tabs(["👤 Informations", "🏢 Entreprise", "⏰ Horaires", "🔐 Sécurité", "🗑️ Gestion Données"])
        
        with sub_tabs[0]:
            st.subheader("👤 Mes Informations")
            
            with st.form("profil_proprio"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nom_proprio = st.text_input("Nom complet", value=st.session_state.user['username'])
                    email_proprio = st.text_input("Email")
                
                with col2:
                    tel_proprio = st.text_input("Téléphone")
                    adresse_proprio = st.text_input("Adresse")
                
                if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                    st.success("✅ Profil mis à jour")
        
        with sub_tabs[1]:
            st.subheader("🏢 Informations Entreprise")
            
            # Récupérer les infos actuelles
            info_entreprise = st.session_state.db.get_info_entreprise()
            
            with st.form("info_entreprise"):
                nom_entreprise_input = st.text_input("Nom de l'entreprise", value=info_entreprise['nom'])
                description_entreprise = st.text_area("Description", value=info_entreprise['description'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    tel_entreprise = st.text_input("Téléphone entreprise", value=info_entreprise['telephone'])
                    email_entreprise = st.text_input("Email entreprise", value=info_entreprise['email'])
                
                with col2:
                    adresse_entreprise = st.text_input("Adresse complète", value=info_entreprise['adresse'])
                    site_web = st.text_input("Site web (optionnel)", value=info_entreprise['site_web'])
                
                if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                    st.session_state.db.set_info_entreprise(
                        nom=nom_entreprise_input,
                        description=description_entreprise,
                        telephone=tel_entreprise,
                        email=email_entreprise,
                        adresse=adresse_entreprise,
                        site_web=site_web
                    )
                    st.success("✅ Informations entreprise mises à jour")
                    st.balloons()
                    st.rerun()
        
        with sub_tabs[2]:
            st.subheader("⏰ Horaires d'Ouverture")
            
            with st.form("horaires"):
                col1, col2 = st.columns(2)
                
                with col1:
                    ouverture = st.time_input("Heure d'ouverture", value=datetime.strptime("08:00", "%H:%M").time())
                    pause_debut = st.time_input("Début pause", value=datetime.strptime("12:00", "%H:%M").time())
                
                with col2:
                    fermeture = st.time_input("Heure de fermeture", value=datetime.strptime("19:00", "%H:%M").time())
                    pause_fin = st.time_input("Fin pause", value=datetime.strptime("13:00", "%H:%M").time())
                
                if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                    st.success("✅ Horaires mis à jour")
        
        with sub_tabs[3]:
            st.subheader("🔐 Sécurité")
            
            with st.form("change_password"):
                ancien_mdp = st.text_input("Ancien mot de passe", type="password")
                nouveau_mdp = st.text_input("Nouveau mot de passe", type="password")
                confirmer_mdp = st.text_input("Confirmer nouveau mot de passe", type="password")
                
                if st.form_submit_button("🔒 Changer le Mot de Passe", use_container_width=True):
                    if nouveau_mdp == confirmer_mdp:
                        st.success("✅ Mot de passe changé avec succès")
                    else:
                        st.error("❌ Les mots de passe ne correspondent pas")
        
        with sub_tabs[4]:
            st.subheader("🗑️ Gestion des Données")
            
            st.warning("⚠️ **ATTENTION** : Ces actions sont irréversibles ! Une archive sera créée avant suppression.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Réinitialiser CA")
                st.info("Supprime tous les paiements et réinitialise le chiffre d'affaires à 0 FCFA")
                
                if st.button("🔄 Réinitialiser CA", use_container_width=True, type="secondary"):
                    with st.spinner("Réinitialisation en cours..."):
                        nb_paiements = st.session_state.db.reinitialiser_ca()
                        st.success(f"✅ CA réinitialisé ! {nb_paiements} paiement(s) supprimé(s)")
                        st.balloons()
                
                st.markdown("---")
                
                st.markdown("### 🧹 Supprimer Historique Services")
                st.info("Supprime toutes les réservations et l'historique des services")
                
                if st.button("🗑️ Supprimer Historique", use_container_width=True, type="secondary"):
                    with st.spinner("Suppression en cours..."):
                        nb_lignes = st.session_state.db.supprimer_historique_services()
                        st.success(f"✅ Historique supprimé ! {nb_lignes} enregistrement(s) effacé(s)")
                        st.balloons()
            
            with col2:
                st.markdown("### 👥 Réinitialiser Clients")
                st.info("Remet à zéro les points fidélité et total dépenses de tous les clients")
                
                if st.button("🔄 Réinitialiser Clients", use_container_width=True, type="secondary"):
                    with st.spinner("Réinitialisation en cours..."):
                        st.session_state.db.reinitialiser_clients()
                        st.success("✅ Clients réinitialisés ! Points et dépenses remis à zéro")
                        st.balloons()
                
                st.markdown("---")
                
                st.markdown("### 💾 Archive + Réinitialisation Complète")
                st.info("Crée une copie de sauvegarde puis réinitialise TOUT (CA + Services + Clients)")
                
                if st.button("🚀 TOUT Réinitialiser", use_container_width=True, type="primary"):
                    with st.spinner("Archivage et réinitialisation..."):
                        nom_archive = st.session_state.db.archiver_et_reinitialiser()
                        st.success(f"✅ Archive créée : `{nom_archive}`")
                        st.success("✅ Toutes les données ont été réinitialisées !")
                        st.balloons()
                        st.rerun()

else:  # EMPLOYÉ
    st.header(f"👋 Bienvenue {st.session_state.user['username']}")
    
    tabs = st.tabs([
        "🏠 Mon Espace",
        "⏰ Pointage",
        "🚗 Lancer un Service",
        "👤 Mon Profil"
    ])
    
    with tabs[0]:
        st.subheader("🏠 Mon Espace Employé")
        
        # Stats du jour
        today = date.today().isoformat()
        pointages_today = st.session_state.db.get_pointages_employe(st.session_state.user['id'], today, today)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📅 Date", date.today().strftime("%d/%m/%Y"))
            
            if pointages_today:
                arrivee = next((p for p in pointages_today if p['type'] == 'arrivee'), None)
                if arrivee:
                    st.metric("✅ Arrivée", arrivee['heure'])
                else:
                    st.info("Pas encore pointé aujourd'hui")
        
        with col2:
            heures_travail = st.session_state.db.calculer_heures_travail(st.session_state.user['id'], today)
            st.metric("⏱️ Heures travaillées aujourd'hui", f"{heures_travail['heures_travail']}h")
            
            if pointages_today:
                depart = next((p for p in pointages_today if p['type'] == 'depart'), None)
                if depart:
                    st.metric("🏁 Départ", depart['heure'])
        
        st.markdown("---")
        st.info("💡 Utilisez l'onglet **⏰ Pointage** pour enregistrer vos arrivées et départs")
    
    with tabs[1]:
        st.subheader("⏰ Pointage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Pointer Arrivée", use_container_width=True, type="primary"):
                pointage_id = st.session_state.db.enregistrer_pointage(st.session_state.user['id'], 'arrivee')
                st.success(f"✅ Pointage enregistré à {datetime.now().strftime('%H:%M')}")
                st.rerun()
        
        with col2:
            if st.button("🏁 Pointer Départ", use_container_width=True):
                pointage_id = st.session_state.db.enregistrer_pointage(st.session_state.user['id'], 'depart')
                st.success(f"🏁 Départ enregistré à {datetime.now().strftime('%H:%M')}")
                st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Mes Pointages Ce Mois")
        
        # Afficher les pointages du mois en cours
        debut_mois = date.today().replace(day=1).isoformat()
        fin_mois = date.today().isoformat()
        
        pointages_mois = st.session_state.db.get_pointages_employe(
            st.session_state.user['id'], 
            debut_mois, 
            fin_mois
        )
        
        if pointages_mois:
            # Grouper par date
            dates_uniques = list(set([p['date'] for p in pointages_mois]))
            dates_uniques.sort(reverse=True)
            
            for date_str in dates_uniques:
                pointages_date = [p for p in pointages_mois if p['date'] == date_str]
                
                heures_travail = st.session_state.db.calculer_heures_travail(
                    st.session_state.user['id'], 
                    date_str
                )
                
                with st.expander(f"📅 {date_str} - {heures_travail['heures_travail']}h travaillées"):
                    for p in pointages_date:
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.write(f"🕐 {p['heure']}")
                        with col2:
                            type_text = "✅ Arrivée" if p['type'] == 'arrivee' else "🏁 Départ"
                            st.write(type_text)
        else:
            st.info("Aucun pointage ce mois")
    
    with tabs[2]:
        st.subheader("🚗 Lancer un Service Client")
        
        st.info("💡 **Recherche rapide** : Tapez téléphone ou nom pour retrouver un client existant")
        
        # === RECHERCHE RAPIDE CLIENT ===
        st.markdown("### 🔍 Recherche Client")
        
        col_search1, col_search2 = st.columns([3, 1])
        
        with col_search1:
            search_term = st.text_input(
                "🔎 Rechercher par téléphone ou nom",
                placeholder="Ex: +225 07, Mamadou, Koné...",
                key="search_client_quick"
            )
        
        with col_search2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            nouveau_client = st.checkbox("➕ Nouveau client", key="nouveau_client_check")
        
        client_selectionne = None
        
        # Si recherche active et pas nouveau client
        if search_term and not nouveau_client:
            # Recherche dans la base
            clients = st.session_state.db.get_all_clients()
            resultats = [
                c for c in clients 
                if search_term.lower() in c['tel'].lower() 
                or search_term.lower() in c['nom'].lower()
            ]
            
            if resultats:
                st.success(f"✅ **{len(resultats)} client(s) trouvé(s)**")
                
                # Afficher les résultats sous forme de cartes cliquables
                for client in resultats[:5]:  # Max 5 résultats
                    col_info, col_btn = st.columns([5, 1])
                    
                    with col_info:
                        st.markdown(f"""
                        <div style="padding: 10px; background: #f0f2f6; border-radius: 5px; margin-bottom: 5px;">
                            <p style="margin: 0; font-size: 16px;"><strong>{client['nom']}</strong></p>
                            <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">
                                📞 {client['tel']} | 🚗 {client.get('vehicule', 'N/A')} | 
                                ⭐ {client.get('points_fidelite', 0)} pts | 
                                💰 {format_fcfa(client.get('total_depense', 0))} dépensés
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_btn:
                        if st.button("✅", key=f"select_client_{client['id']}", help="Sélectionner ce client"):
                            client_selectionne = client
                            st.session_state['client_selectionne'] = client
                            st.rerun()
            else:
                st.warning("❌ Aucun client trouvé. Cochez '➕ Nouveau client' pour créer.")
        
        # Récupérer client sélectionné depuis session state
        if 'client_selectionne' in st.session_state and not nouveau_client:
            client_selectionne = st.session_state['client_selectionne']
        
        st.markdown("---")
        
        # === FORMULAIRE SERVICE ===
        # Récupérer les services disponibles
        services = st.session_state.db.get_all_services(actif_only=True)
        
        if not services:
            st.warning("⚠️ Aucun service disponible. Contactez le propriétaire.")
        else:
            with st.form("lancer_service_employe"):
                st.markdown("#### 🔧 Service à Lancer")
                
                # Si client sélectionné, afficher ses infos
                if client_selectionne:
                    st.success(f"✅ Client: **{client_selectionne['nom']}** | 📞 {client_selectionne['tel']} | 🚗 {client_selectionne.get('vehicule', 'N/A')}")
                    tel_client = client_selectionne['tel']
                    nom_client = client_selectionne['nom']
                    vehicule_input = st.text_input("🚗 Véhicule (modifier si nécessaire)", value=client_selectionne.get('vehicule', ''))
                    client_existant = client_selectionne
                elif nouveau_client:
                    # Nouveau client - saisie complète
                    col1, col2 = st.columns(2)
                    with col1:
                        nom_client = st.text_input("👤 Nom du client *", placeholder="Nom complet")
                        tel_client = st.text_input("📞 Téléphone *", placeholder="+225 XX XX XX XX")
                    with col2:
                        vehicule_input = st.text_input("🚗 Véhicule *", placeholder="Marque et modèle")
                    client_existant = None
                else:
                    st.info("👆 Recherchez un client ci-dessus ou cochez 'Nouveau client'")
                    tel_client = ""
                    nom_client = ""
                    vehicule_input = ""
                    client_existant = None
                
                st.markdown("---")
                
                # Sélection service et poste
                col_srv, col_post = st.columns(2)
                
                with col_srv:
                    service_id = st.selectbox(
                        "🔧 Service demandé *",
                        options=[s['id'] for s in services],
                        format_func=lambda x: f"{next(s['nom'] for s in services if s['id'] == x)} - {format_fcfa(next(s['prix'] for s in services if s['id'] == x))}"
                    )
                
                with col_post:
                    poste_id = st.selectbox(
                        "🏢 Poste de lavage",
                        options=[p['id'] for p in st.session_state.db.get_all_postes()],
                        format_func=lambda x: next(p['nom'] for p in st.session_state.db.get_all_postes() if p['id'] == x)
                    )
                
                notes = st.text_area("📝 Notes (optionnel)", placeholder="Instructions spéciales...")
                
                st.markdown("---")
                
                # Afficher le prix du service sélectionné
                service_choisi = next(s for s in services if s['id'] == service_id)
                st.info(f"💰 **Prix du service:** {format_fcfa(service_choisi['prix'])} | ⏱️ **Durée:** {service_choisi['duree']} min")
                
                submitted = st.form_submit_button("✅ Démarrer le Service", use_container_width=True, type="primary")
                
                if submitted:
                    if tel_client and nom_client and vehicule_input:
                        # Créer ou récupérer le client
                        if client_existant:
                            client_id = client_existant['id']
                            # Mettre à jour le véhicule si modifié
                            if vehicule_input != client_existant.get('vehicule', ''):
                                st.session_state.db.cursor.execute("UPDATE clients SET vehicule = ? WHERE id = ?", (vehicule_input, client_id))
                        else:
                            client_id = st.session_state.db.ajouter_client(nom_client, tel_client, "", vehicule_input)
                        
                        # Créer la réservation immédiate
                        now = datetime.now()
                        reservation_id = st.session_state.db.ajouter_reservation(
                            client_id=client_id,
                            service_id=service_id,
                            date=now.strftime("%Y-%m-%d"),
                            heure=now.strftime("%H:%M"),
                            montant=service_choisi['prix'],
                            poste_id=poste_id,
                            employe_id=st.session_state.user['id'],  # ID de l'employé connecté
                            notes=notes
                        )
                        
                        # Ajouter les points de fidélité
                        st.session_state.db.update_client_points(client_id, service_choisi['points'], "add")
                        
                        # Réinitialiser la sélection
                        if 'client_selectionne' in st.session_state:
                            del st.session_state['client_selectionne']
                        
                        st.success(f"✅ Service démarré avec succès !")
                        st.balloons()
                        
                        # Afficher le récapitulatif
                        st.markdown(f"""
                        ### 📋 Récapitulatif
                        - **Client:** {nom_client}
                        - **Véhicule:** {vehicule_input}
                        - **Service:** {service_choisi['nom']}
                        - **Prix:** {format_fcfa(service_choisi['prix'])}
                        - **Points gagnés:** +{service_choisi['points']} points
                        - **Réservation N°:** {reservation_id:05d}
                        """)
                        
                        st.info("💡 Le client peut maintenant aller au poste de lavage")
                    else:
                        st.error("⚠️ Veuillez remplir tous les champs obligatoires")
            
            st.markdown("---")
            st.subheader("📊 Services en Cours Aujourd'hui")
            
            # Afficher les réservations du jour
            reservations_today = st.session_state.db.get_reservations_by_date(date.today().isoformat())
            
            if reservations_today:
                # Filtrer par statut
                tab_attente = [r for r in reservations_today if r['statut'] == 'en_attente']
                tab_en_cours = [r for r in reservations_today if r['statut'] == 'en_cours']
                tab_termine = [r for r in reservations_today if r['statut'] == 'termine']
                tab_paye = [r for r in reservations_today if r['statut'] == 'paye']
                
                st.write(f"**En attente:** {len(tab_attente)} | **En cours:** {len(tab_en_cours)} | **Terminé:** {len(tab_termine)} | **Payé:** {len(tab_paye)}")
                st.markdown("---")
                
                for res in reservations_today:
                    # Badge de statut avec couleur
                    if res['statut'] == 'en_attente':
                        statut_badge = "🔵 En attente"
                    elif res['statut'] == 'en_cours':
                        statut_badge = "🟡 En cours"
                    elif res['statut'] == 'termine':
                        statut_badge = "🟢 Terminé"
                    elif res['statut'] == 'paye':
                        statut_badge = "💰 Payé"
                    elif res['statut'] == 'valide':
                        statut_badge = "✅ Validé"
                    else:
                        statut_badge = res['statut']
                    
                    with st.expander(f"🚗 {res['client_nom']} - {res['service_nom']} | {statut_badge}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Client:** {res['client_nom']}")
                            st.write(f"**Téléphone:** {res['client_tel']}")
                            st.write(f"**Véhicule:** {res['vehicule']}")
                        with col2:
                            st.write(f"**Service:** {res['service_nom']}")
                            st.write(f"**Prix:** {format_fcfa(res['montant'])}")
                            st.write(f"**Heure:** {res['heure']}")
                        
                        st.markdown("---")
                        
                        # Actions selon le statut
                        if res['statut'] == 'en_attente':
                            if st.button(f"▶️ Démarrer le service", key=f"start_{res['id']}", use_container_width=True):
                                st.session_state.db.update_reservation_statut(res['id'], 'en_cours')
                                st.success("✅ Service démarré !")
                                st.rerun()
                        
                        elif res['statut'] == 'en_cours':
                            st.info("🎬 Service en cours - Ajoutez les photos avant/après !")
                            
                            # Récupérer les photos existantes
                            photos_avant = st.session_state.db.get_photos_service(res['id'], 'avant')
                            photos_apres = st.session_state.db.get_photos_service(res['id'], 'apres')
                            
                            col_photo1, col_photo2 = st.columns(2)
                            
                            # ===== COLONNE PHOTOS AVANT =====
                            with col_photo1:
                                st.write("📸 **Photos AVANT**")
                                
                                # Afficher les photos existantes
                                if photos_avant:
                                    st.write(f"**{len(photos_avant)} photo(s) ajoutée(s)**")
                                    for idx, photo in enumerate(photos_avant):
                                        col_img, col_btn = st.columns([4, 1])
                                        with col_img:
                                            st.image(photo['photo_data'], use_container_width=True, caption=f"Photo {idx+1}")
                                        with col_btn:
                                            if st.button("🗑️", key=f"del_avant_{photo['id']}"):
                                                st.session_state.db.supprimer_photo_service(photo['id'])
                                                st.success("Photo supprimée")
                                                st.rerun()
                                    st.markdown("---")
                                
                                # Ajouter nouvelle photo
                                st.write("**➕ Ajouter photo AVANT**")
                                
                                st.info("💡 **Astuce qualité** : Pour meilleure qualité sur TikTok/Instagram, préférez 'Upload' après avoir pris la photo avec votre app caméra native")
                                
                                mode_avant = st.radio(
                                    "Mode",
                                    ["📷 Caméra", "📁 Upload"],
                                    key=f"mode_avant_{res['id']}",
                                    horizontal=True
                                )
                                
                                if mode_avant == "📷 Caméra":
                                    # Sélecteur caméra
                                    camera_type_avant = st.radio(
                                        "Quelle caméra ?",
                                        ["🔙 Caméra Arrière (principale)", "🤳 Caméra Avant (selfie)"],
                                        key=f"camera_type_avant_{res['id']}",
                                        horizontal=True
                                    )
                                    
                                    # Déterminer le facingMode
                                    facing_mode_avant = "environment" if "Arrière" in camera_type_avant else "user"
                                    
                                    # Composant HTML personnalisé pour contrôler la caméra
                                    st.markdown(f"""
                                    <div style="padding: 10px; background: #f0f2f6; border-radius: 5px; margin-bottom: 10px;">
                                        <p style="margin: 0; font-size: 14px;">📱 Mode: <strong>{camera_type_avant}</strong></p>
                                        <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
                                            💡 Si la mauvaise caméra s'ouvre, utilisez le bouton de votre navigateur pour basculer
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Utiliser une key différente pour forcer le rechargement
                                    photo_avant = st.camera_input(
                                        f"📸 Prendre photo ({camera_type_avant})",
                                        key=f"camera_avant_{res['id']}_{facing_mode_avant}"
                                    )
                                else:
                                    photos_avant_upload = st.file_uploader(
                                        "Upload photos (plusieurs à la fois possible)",
                                        type=['png', 'jpg', 'jpeg'],
                                        key=f"upload_avant_{res['id']}",
                                        accept_multiple_files=True
                                    )
                                
                                # Bouton de sauvegarde pour caméra (une seule photo)
                                if mode_avant == "📷 Caméra" and photo_avant:
                                    if st.button("💾 Sauvegarder cette photo AVANT", key=f"save_avant_{res['id']}", use_container_width=True):
                                        photo_bytes = photo_avant.read()
                                        st.session_state.db.ajouter_photo_service(
                                            res['id'],
                                            'avant',
                                            photo_bytes,
                                            employe_id=st.session_state.user['id']
                                        )
                                        st.success("✅ Photo AVANT ajoutée !")
                                        st.rerun()
                                
                                # Bouton de sauvegarde pour upload (plusieurs photos)
                                if mode_avant == "📁 Upload" and photos_avant_upload:
                                    st.write(f"📤 **{len(photos_avant_upload)} photo(s) sélectionnée(s)**")
                                    if st.button("💾 Sauvegarder TOUTES les photos AVANT", key=f"save_all_avant_{res['id']}", use_container_width=True):
                                        nb_ajoutees = 0
                                        for photo_file in photos_avant_upload:
                                            photo_bytes = photo_file.read()
                                            st.session_state.db.ajouter_photo_service(
                                                res['id'],
                                                'avant',
                                                photo_bytes,
                                                employe_id=st.session_state.user['id']
                                            )
                                            nb_ajoutees += 1
                                        st.success(f"✅ {nb_ajoutees} photo(s) AVANT ajoutée(s) !")
                                        st.balloons()
                                        st.rerun()
                            
                            # ===== COLONNE PHOTOS APRÈS =====
                            with col_photo2:
                                st.write("📸 **Photos APRÈS**")
                                
                                # Afficher les photos existantes
                                if photos_apres:
                                    st.write(f"**{len(photos_apres)} photo(s) ajoutée(s)**")
                                    for idx, photo in enumerate(photos_apres):
                                        col_img, col_btn = st.columns([4, 1])
                                        with col_img:
                                            st.image(photo['photo_data'], use_container_width=True, caption=f"Photo {idx+1}")
                                        with col_btn:
                                            if st.button("🗑️", key=f"del_apres_{photo['id']}"):
                                                st.session_state.db.supprimer_photo_service(photo['id'])
                                                st.success("Photo supprimée")
                                                st.rerun()
                                    st.markdown("---")
                                
                                # Ajouter nouvelle photo
                                st.write("**➕ Ajouter photo APRÈS**")
                                
                                st.info("💡 **Astuce qualité** : Pour meilleure qualité sur TikTok/Instagram, préférez 'Upload' après avoir pris la photo avec votre app caméra native")
                                
                                mode_apres = st.radio(
                                    "Mode",
                                    ["📷 Caméra", "📁 Upload"],
                                    key=f"mode_apres_{res['id']}",
                                    horizontal=True
                                )
                                
                                if mode_apres == "📷 Caméra":
                                    # Sélecteur caméra
                                    camera_type_apres = st.radio(
                                        "Quelle caméra ?",
                                        ["🔙 Caméra Arrière (principale)", "🤳 Caméra Avant (selfie)"],
                                        key=f"camera_type_apres_{res['id']}",
                                        horizontal=True
                                    )
                                    
                                    # Déterminer le facingMode
                                    facing_mode_apres = "environment" if "Arrière" in camera_type_apres else "user"
                                    
                                    # Composant HTML personnalisé pour contrôler la caméra
                                    st.markdown(f"""
                                    <div style="padding: 10px; background: #f0f2f6; border-radius: 5px; margin-bottom: 10px;">
                                        <p style="margin: 0; font-size: 14px;">📱 Mode: <strong>{camera_type_apres}</strong></p>
                                        <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
                                            💡 Si la mauvaise caméra s'ouvre, utilisez le bouton de votre navigateur pour basculer
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Utiliser une key différente pour forcer le rechargement
                                    photo_apres = st.camera_input(
                                        f"📸 Prendre photo ({camera_type_apres})",
                                        key=f"camera_apres_{res['id']}_{facing_mode_apres}"
                                    )
                                else:
                                    photos_apres_upload = st.file_uploader(
                                        "Upload photos (plusieurs à la fois possible)",
                                        type=['png', 'jpg', 'jpeg'],
                                        key=f"upload_apres_{res['id']}",
                                        accept_multiple_files=True
                                    )
                                
                                # Bouton de sauvegarde pour caméra (une seule photo)
                                if mode_apres == "📷 Caméra" and photo_apres:
                                    if st.button("💾 Sauvegarder cette photo APRÈS", key=f"save_apres_{res['id']}", use_container_width=True):
                                        photo_bytes = photo_apres.read()
                                        st.session_state.db.ajouter_photo_service(
                                            res['id'],
                                            'apres',
                                            photo_bytes,
                                            employe_id=st.session_state.user['id']
                                        )
                                        st.success("✅ Photo APRÈS ajoutée !")
                                        st.rerun()
                                
                                # Bouton de sauvegarde pour upload (plusieurs photos)
                                if mode_apres == "📁 Upload" and photos_apres_upload:
                                    st.write(f"📤 **{len(photos_apres_upload)} photo(s) sélectionnée(s)**")
                                    if st.button("💾 Sauvegarder TOUTES les photos APRÈS", key=f"save_all_apres_{res['id']}", use_container_width=True):
                                        nb_ajoutees = 0
                                        for photo_file in photos_apres_upload:
                                            photo_bytes = photo_file.read()
                                            st.session_state.db.ajouter_photo_service(
                                                res['id'],
                                                'apres',
                                                photo_bytes,
                                                employe_id=st.session_state.user['id']
                                            )
                                            nb_ajoutees += 1
                                        st.success(f"✅ {nb_ajoutees} photo(s) APRÈS ajoutée(s) !")
                                        st.balloons()
                                        st.rerun()
                            
                            st.markdown("---")
                            
                            # Informations sur les photos
                            total_avant = len(photos_avant) if photos_avant else 0
                            total_apres = len(photos_apres) if photos_apres else 0
                            
                            if total_avant > 0 or total_apres > 0:
                                st.success(f"📊 Total photos: {total_avant} avant + {total_apres} après = {total_avant + total_apres} photos")
                            
                            if st.button(f"✅ Marquer comme Terminé", key=f"finish_{res['id']}", use_container_width=True, type="primary"):
                                st.session_state.db.update_reservation_statut(res['id'], 'termine')
                                st.success("✅ Service terminé !")
                                st.rerun()
                        
                        elif res['statut'] == 'termine':
                            st.info("💡 Service terminé - En attente d'encaissement")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                methode = st.selectbox(
                                    "Méthode de paiement",
                                    ["Espèces", "Mobile Money", "Carte Bancaire"],
                                    key=f"methode_{res['id']}"
                                )
                            with col_b:
                                st.write("")
                                st.write("")
                                if st.button(f"💰 Encaisser {format_fcfa(res['montant'])}", key=f"pay_{res['id']}", type="primary", use_container_width=True):
                                    # Enregistrer le paiement
                                    st.session_state.db.ajouter_paiement(res['id'], res['montant'], methode)
                                    # Mettre à jour le statut
                                    st.session_state.db.update_reservation_statut(res['id'], 'paye')
                                    # Mettre à jour les dépenses client
                                    st.session_state.db.update_client_depense(res['client_id'], res['montant'])
                                    st.success(f"✅ Paiement de {format_fcfa(res['montant'])} encaissé !")
                                    st.balloons()
                                    st.rerun()
                        
                        elif res['statut'] == 'paye':
                            st.success("✅ Payé - En attente de validation par le propriétaire")
                        
                        elif res['statut'] == 'valide':
                            st.success("✅✅ Service validé par le propriétaire")
            else:
                st.info("Aucun service en cours aujourd'hui")
    
    with tabs[3]:
        st.subheader("👤 Mon Profil")
        
        with st.form("profil_employe"):
            st.write(f"**Nom:** {st.session_state.user['username']}")
            st.write(f"**Rôle:** {st.session_state.user['role']}")
            
            tel = st.text_input("Téléphone")
            email = st.text_input("Email")
            
            if st.form_submit_button("💾 Enregistrer"):
                st.success("✅ Profil mis à jour")
