import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from database import Database
import locale

# Configuration de la page
st.set_page_config(
    page_title="🚗 WashAfrique - Réservation en ligne",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisation base de données
if "db" not in st.session_state:
    st.session_state.db = Database()

# Récupérer paramètres site
nom_entreprise = st.session_state.db.get_parametre_site_client('nom_entreprise_site', 'WashAfrique Pro')
slogan = st.session_state.db.get_parametre_site_client('slogan', 'Votre voiture mérite le meilleur')
couleur_principale = st.session_state.db.get_parametre_site_client('couleur_principale', '#667eea')
telephone = st.session_state.db.get_parametre_site_client('telephone_contact', '+225 XX XX XX XX')
email_contact = st.session_state.db.get_parametre_site_client('email_contact', 'contact@washafrique.com')
adresse = st.session_state.db.get_parametre_site_client('adresse', 'Abidjan, Côte d\'Ivoire')
texte_accueil = st.session_state.db.get_parametre_site_client('texte_accueil', 'Réservez votre lavage en ligne')
site_actif = st.session_state.db.get_parametre_site_client('site_actif', '1') == '1'
reservation_active = st.session_state.db.get_parametre_site_client('reservation_active', '1') == '1'

# Style CSS personnalisé
st.markdown(f"""
    <style>
    /* Header */
    .header-client {{
        background: linear-gradient(135deg, {couleur_principale} 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    
    .header-client h1 {{
        color: white;
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
    }}
    
    .header-client p {{
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        margin: 0.5rem 0 0 0;
    }}
    
    /* Cards services */
    .service-card {{
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid {couleur_principale};
        height: 100%;
    }}
    
    .service-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }}
    
    .service-nom {{
        font-size: 1.5rem;
        font-weight: 600;
        color: #262730;
        margin-bottom: 0.5rem;
    }}
    
    .service-prix {{
        font-size: 2rem;
        font-weight: 700;
        color: {couleur_principale};
        margin: 1rem 0;
    }}
    
    .service-duree {{
        color: #666;
        font-size: 1rem;
    }}
    
    /* Boutons */
    .stButton>button {{
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, {couleur_principale} 0%, #764ba2 100%) !important;
        color: white !important;
        border: none;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 15px;
        margin-top: 3rem;
    }}
    
    .footer-contact {{
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }}
    
    .contact-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Avis */
    .avis-card {{
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }}
    
    .avis-stars {{
        color: #ffc107;
        font-size: 1.2rem;
    }}
    </style>
""", unsafe_allow_html=True)

def format_fcfa(montant):
    """Formate en FCFA"""
    return f"{int(montant):,} FCFA".replace(",", " ")

# Vérifier si site actif
if not site_actif:
    st.error("🚧 Site temporairement fermé pour maintenance. Veuillez réessayer plus tard.")
    st.stop()

# ===== HEADER =====
st.markdown(f"""
    <div class="header-client">
        <h1>🚗 {nom_entreprise}</h1>
        <p>{slogan}</p>
    </div>
""", unsafe_allow_html=True)

# ===== NAVIGATION =====
tabs = st.tabs(["🏠 Accueil", "🧼 Services", "📅 Réserver", "🔍 Suivi Réservation", "⭐ Avis"])

# ===== ONGLET ACCUEIL =====
with tabs[0]:
    st.markdown(f"### {texte_accueil}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🕐 Rapide\nRéservez en 2 minutes")
    
    with col2:
        st.success("### ✅ Fiable\nQualité garantie")
    
    with col3:
        st.warning("### 💎 Pro\nÉquipe expérimentée")
    
    st.markdown("---")
    
    # Statistiques
    services = st.session_state.db.get_all_services()
    avis = st.session_state.db.get_avis_visibles(limit=5)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Services Disponibles", len([s for s in services if s['actif']]))
    with col2:
        if avis:
            note_moyenne = sum(a['note'] for a in avis) / len(avis)
            st.metric("Note Moyenne", f"{note_moyenne:.1f}/5 ⭐")
        else:
            st.metric("Note Moyenne", "N/A")
    with col3:
        st.metric("Clients Satisfaits", "500+")

# ===== ONGLET SERVICES =====
with tabs[1]:
    st.header("🧼 Nos Services")
    
    services = st.session_state.db.get_all_services()
    services_actifs = [s for s in services if s['actif']]
    
    if not services_actifs:
        st.info("Aucun service disponible pour le moment.")
    else:
        cols = st.columns(3)
        for idx, service in enumerate(services_actifs):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="service-card">
                        <div class="service-nom">{service['nom']}</div>
                        <div class="service-prix">{format_fcfa(service['prix'])}</div>
                        <div class="service-duree">⏱️ {service['duree']} minutes</div>
                        <p style="margin-top: 1rem; color: #666;">
                            {service.get('description', 'Service de qualité professionnelle')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

# ===== ONGLET RÉSERVATION =====
with tabs[2]:
    st.header("📅 Réserver un Service")
    
    if not reservation_active:
        st.warning("⚠️ Les réservations en ligne sont temporairement désactivées. Contactez-nous directement.")
    else:
        with st.form("formulaire_reservation"):
            st.subheader("Vos Informations")
            
            col1, col2 = st.columns(2)
            with col1:
                nom_client = st.text_input("👤 Nom complet *", placeholder="Ex: Jean Kouassi")
                tel_client = st.text_input("📱 Téléphone *", placeholder="Ex: +225 XX XX XX XX")
            
            with col2:
                email_client = st.text_input("📧 Email (optionnel)", placeholder="Ex: jean@email.com")
                vehicule = st.text_input("🚗 Véhicule", placeholder="Ex: Toyota Corolla")
            
            st.subheader("Détails de la Réservation")
            
            col1, col2 = st.columns(2)
            with col1:
                services_actifs = [s for s in st.session_state.db.get_all_services() if s['actif']]
                if services_actifs:
                    service_choisi = st.selectbox(
                        "🧼 Service *",
                        options=services_actifs,
                        format_func=lambda x: f"{x['nom']} - {format_fcfa(x['prix'])}"
                    )
                else:
                    st.error("Aucun service disponible")
                    st.stop()
                
                # Date minimum = demain
                delai_min = int(st.session_state.db.get_parametre_site_client('delai_min_reservation', '2'))
                date_min = date.today() + timedelta(hours=delai_min)
                date_max = date.today() + timedelta(days=30)
                
                date_reservation = st.date_input(
                    "📅 Date *",
                    min_value=date_min.date() if hasattr(date_min, 'date') else date_min,
                    max_value=date_max,
                    value=date_min.date() if hasattr(date_min, 'date') else date_min
                )
            
            with col2:
                # Récupérer créneaux pour le jour choisi
                jour_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'][date_reservation.weekday()]
                creneaux = st.session_state.db.get_creneaux_disponibles(jour_semaine)
                
                if creneaux and creneaux[0]['actif']:
                    # Générer heures disponibles
                    heure_debut = creneaux[0]['heure_debut']
                    heure_fin = creneaux[0]['heure_fin']
                    intervalle = creneaux[0]['intervalle_minutes']
                    
                    heures_dispo = []
                    h_debut = datetime.strptime(heure_debut, "%H:%M")
                    h_fin = datetime.strptime(heure_fin, "%H:%M")
                    
                    current = h_debut
                    while current < h_fin:
                        heures_dispo.append(current.strftime("%H:%M"))
                        current += timedelta(minutes=intervalle)
                    
                    heure_reservation = st.selectbox("⏰ Heure *", options=heures_dispo)
                else:
                    st.error(f"Fermé le {jour_semaine}")
                    heure_reservation = None
            
            notes_client = st.text_area("📝 Notes (optionnel)", placeholder="Informations supplémentaires...")
            
            submit = st.form_submit_button("✅ Confirmer la Réservation", use_container_width=True, type="primary")
            
            if submit:
                if not nom_client or not tel_client:
                    st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
                elif not heure_reservation:
                    st.error("❌ Aucun créneau disponible pour ce jour")
                else:
                    try:
                        code = st.session_state.db.creer_reservation_web(
                            nom=nom_client,
                            tel=tel_client,
                            email=email_client,
                            service_id=service_choisi['id'],
                            date=date_reservation.isoformat(),
                            heure=heure_reservation,
                            notes=notes_client
                        )
                        
                        st.success("🎉 **Réservation enregistrée avec succès !**")
                        st.info(f"""
                        **Code de réservation : `{code}`**
                        
                        📅 {date_reservation.strftime('%d/%m/%Y')} à {heure_reservation}
                        🧼 {service_choisi['nom']}
                        💰 {format_fcfa(service_choisi['prix'])}
                        
                        ⚠️ **Conservez ce code pour suivre votre réservation**
                        """)
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la réservation : {str(e)}")

# ===== ONGLET SUIVI =====
with tabs[3]:
    st.header("🔍 Suivre ma Réservation")
    
    code_recherche = st.text_input("Entrez votre code de réservation", placeholder="Ex: ABC12345")
    
    if st.button("🔍 Rechercher", use_container_width=True):
        if code_recherche:
            reservation = st.session_state.db.get_reservation_web_by_code(code_recherche.upper())
            
            if reservation:
                statut_emoji = {
                    'en_attente': '⏳',
                    'confirmee': '✅',
                    'annulee': '❌',
                    'terminee': '🏁'
                }
                statut_couleur = {
                    'en_attente': 'orange',
                    'confirmee': 'green',
                    'annulee': 'red',
                    'terminee': 'blue'
                }
                
                st.success("📋 Réservation trouvée !")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### Détails")
                    st.write(f"**Nom:** {reservation['nom_client']}")
                    st.write(f"**Téléphone:** {reservation['tel_client']}")
                    st.write(f"**Service:** {reservation['service_nom']}")
                    st.write(f"**Prix:** {format_fcfa(reservation['prix'])}")
                
                with col2:
                    st.markdown(f"### Date & Heure")
                    st.write(f"**📅 Date:** {reservation['date_reservation']}")
                    st.write(f"**⏰ Heure:** {reservation['heure_reservation']}")
                    st.write(f"**⏱️ Durée:** ~{reservation['duree']} min")
                
                statut = reservation['statut']
                st.markdown(f"### {statut_emoji.get(statut, '❓')} Statut: **:{statut_couleur.get(statut, 'gray')}[{statut.upper()}]**")
                
                if reservation.get('notes_client'):
                    st.info(f"📝 Notes: {reservation['notes_client']}")
            else:
                st.error("❌ Aucune réservation trouvée avec ce code")
        else:
            st.warning("⚠️ Veuillez entrer un code de réservation")

# ===== ONGLET AVIS =====
with tabs[4]:
    st.header("⭐ Avis Clients")
    
    avis_liste = st.session_state.db.get_avis_visibles(limit=20)
    
    if avis_liste:
        for avis in avis_liste:
            stars = "⭐" * avis['note']
            st.markdown(f"""
                <div class="avis-card">
                    <div class="avis-stars">{stars}</div>
                    <strong>{avis['nom_client']}</strong>
                    <p style="margin-top: 0.5rem;">{avis.get('commentaire', 'Très satisfait du service !')}</p>
                    <small style="color: #999;">{avis['created_at'][:10]}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun avis pour le moment. Soyez le premier à laisser un avis !")
    
    st.markdown("---")
    st.subheader("✍️ Laisser un Avis")
    
    with st.form("formulaire_avis"):
        nom_avis = st.text_input("👤 Votre nom", placeholder="Ex: Marie Diallo")
        note_avis = st.select_slider("⭐ Note", options=[1, 2, 3, 4, 5], value=5)
        commentaire_avis = st.text_area("💬 Commentaire", placeholder="Partagez votre expérience...")
        
        if st.form_submit_button("📤 Envoyer l'avis", use_container_width=True, type="primary"):
            if nom_avis:
                try:
                    st.session_state.db.ajouter_avis_client(
                        nom=nom_avis,
                        note=note_avis,
                        commentaire=commentaire_avis
                    )
                    st.success("✅ Merci pour votre avis !")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.error("❌ Veuillez entrer votre nom")

# ===== FOOTER =====
st.markdown(f"""
    <div class="footer">
        <h3>📞 Contactez-nous</h3>
        <div class="footer-contact">
            <div class="contact-item">📱 {telephone}</div>
            <div class="contact-item">📧 {email_contact}</div>
            <div class="contact-item">📍 {adresse}</div>
        </div>
        <p style="margin-top: 1.5rem; color: #999;">
            © 2026 {nom_entreprise}. Tous droits réservés.
        </p>
    </div>
""", unsafe_allow_html=True)
