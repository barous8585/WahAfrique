import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Lavage Esthétique Pro+",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des données en session state
if 'reservations' not in st.session_state:
    st.session_state.reservations = []
if 'clients' not in st.session_state:
    st.session_state.clients = []
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []
if 'avis' not in st.session_state:
    st.session_state.avis = []
if 'codes_promo' not in st.session_state:
    st.session_state.codes_promo = [
        {'code': 'FIRST10', 'reduction': 10, 'type': 'pourcentage', 'actif': True},
        {'code': 'FIDELE5000', 'reduction': 5000, 'type': 'fcfa', 'actif': True}
    ]
if 'paiements' not in st.session_state:
    st.session_state.paiements = []

# Services disponibles (PRIX EN FCFA)
SERVICES = {
    1: {"nom": "Lavage Extérieur Standard", "prix": 5000, "duree": 30, "points": 1},
    2: {"nom": "Lavage Complet (Int + Ext)", "prix": 15000, "duree": 90, "points": 2},
    3: {"nom": "Polissage & Céramique", "prix": 60000, "duree": 180, "points": 5},
    4: {"nom": "Détailing Complet", "prix": 100000, "duree": 300, "points": 8},
    5: {"nom": "Nettoyage Intérieur Premium", "prix": 20000, "duree": 120, "points": 3}
}

# Horaires d'ouverture
HORAIRES = {
    'debut': '08:00',
    'fin': '18:00',
    'pause_debut': '12:00',
    'pause_fin': '13:00'
}

# Style CSS amélioré
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stMetric {background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .success-box {background: #d4edda; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745;}
    .warning-box {background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107;}
    .info-box {background: #d1ecf1; padding: 20px; border-radius: 10px; border-left: 5px solid #17a2b8;}
    .calendar-slot {padding: 10px; margin: 5px; border-radius: 5px; text-align: center; cursor: pointer;}
    .slot-libre {background: #d4edda; border: 2px solid #28a745;}
    .slot-occupe {background: #f8d7da; border: 2px solid #dc3545;}
    .slot-pause {background: #e2e3e5; border: 2px solid #6c757d;}
    </style>
""", unsafe_allow_html=True)


# Fonctions utilitaires
def format_fcfa(montant):
    """Formate un montant en FCFA"""
    return f"{montant:,.0f} FCFA".replace(',', ' ')


def calculer_points_fidelite(client_tel):
    """Calcule les points de fidélité d'un client"""
    reservations_client = [r for r in st.session_state.reservations if r['client_tel'] == client_tel]
    total_points = sum([SERVICES[r['service_id']]['points'] for r in reservations_client])
    return total_points


def appliquer_code_promo(prix, code):
    """Applique un code promo au prix"""
    promo = next((p for p in st.session_state.codes_promo if p['code'] == code and p['actif']), None)
    if promo:
        if promo['type'] == 'pourcentage':
            return prix * (1 - promo['reduction'] / 100)
        else:  # type FCFA
            return max(0, prix - promo['reduction'])
    return prix


def generer_creneaux_disponibles(date_selectionnee):
    """Génère les créneaux disponibles pour une date"""
    creneaux = []
    heure_debut = datetime.strptime(HORAIRES['debut'], '%H:%M')
    heure_fin = datetime.strptime(HORAIRES['fin'], '%H:%M')
    pause_debut = datetime.strptime(HORAIRES['pause_debut'], '%H:%M')
    pause_fin = datetime.strptime(HORAIRES['pause_fin'], '%H:%M')

    current = heure_debut
    while current < heure_fin:
        heure_str = current.strftime('%H:%M')

        # Vérifier si c'est la pause
        if pause_debut <= current < pause_fin:
            statut = 'pause'
        else:
            # Vérifier si le créneau est déjà réservé
            est_reserve = any(
                r['date'] == date_selectionnee.isoformat() and r['heure'] == heure_str
                for r in st.session_state.reservations
            )
            statut = 'occupe' if est_reserve else 'libre'

        creneaux.append({'heure': heure_str, 'statut': statut})
        current += timedelta(minutes=30)

    return creneaux


def generer_facture_pdf(reservation_id):
    """Génère une facture en PDF (simulé ici en texte)"""
    res = next((r for r in st.session_state.reservations if r['id'] == reservation_id), None)
    if res:
        service = SERVICES[res['service_id']]
        facture = f"""
        ═══════════════════════════════════════
                    FACTURE N°{reservation_id}
        ═══════════════════════════════════════

        Client: {res['client_nom']}
        Téléphone: {res['client_tel']}
        Véhicule: {res['vehicule']}

        Date: {res['date']}
        Heure: {res['heure']}

        Service: {service['nom']}
        Prix: {format_fcfa(service['prix'])}

        Statut paiement: {res.get('statut_paiement', 'Non payé')}

        ═══════════════════════════════════════
                Merci de votre confiance !
        ═══════════════════════════════════════
        """
        return facture
    return None


# Sidebar pour navigation
st.sidebar.title("🚗 Lavage Pro+")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Menu",
    ["🏠 Tableau de Bord", "📅 Planning Visuel", "✨ Nouvelle Réservation",
     "💰 Devis & Promos", "👥 Clients & Fidélité", "📸 Portfolio",
     "📊 Statistiques", "⚙️ Paramètres"]
)

# ====== PAGE TABLEAU DE BORD ======
if page == "🏠 Tableau de Bord":
    st.title("🏠 Tableau de Bord")

    # KPIs
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    reservations_today = [r for r in st.session_state.reservations if r['date'] == today]
    reservations_tomorrow = [r for r in st.session_state.reservations if r['date'] == tomorrow]

    revenus_jour = sum([SERVICES[r['service_id']]['prix'] for r in reservations_today])
    revenus_total = sum([SERVICES[r['service_id']]['prix'] for r in st.session_state.reservations])
    revenus_mois = sum([SERVICES[r['service_id']]['prix'] for r in st.session_state.reservations
                        if r['date'].startswith(date.today().strftime('%Y-%m'))])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📅 RDV Aujourd'hui", len(reservations_today), delta=f"{len(reservations_tomorrow)} demain")
    with col2:
        st.metric("💰 Revenus Jour", format_fcfa(revenus_jour))
    with col3:
        st.metric("📈 Revenus Mois", format_fcfa(revenus_mois))
    with col4:
        st.metric("👥 Total Clients", len(st.session_state.clients))

    st.markdown("---")

    # Prochaines réservations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏰ Prochains RDV")
        upcoming = sorted(
            [r for r in st.session_state.reservations if r['date'] >= today],
            key=lambda x: (x['date'], x['heure'])
        )[:5]

        if upcoming:
            for res in upcoming:
                service = SERVICES[res['service_id']]
                with st.container():
                    st.markdown(f"""
                    <div class="info-box">
                    <strong>🚗 {res['client_nom']}</strong><br>
                    📅 {res['date']} à {res['heure']}<br>
                    🔧 {service['nom']}<br>
                    💰 {format_fcfa(service['prix'])} - {res.get('statut_paiement', '❌ Non payé')}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("")
        else:
            st.info("Aucun RDV à venir")

    with col2:
        st.subheader("⭐ Derniers Avis")
        if st.session_state.avis:
            for avis in st.session_state.avis[-3:]:
                st.markdown(f"""
                <div class="success-box">
                <strong>{avis['client_nom']}</strong> - {'⭐' * avis['note']}<br>
                "{avis['commentaire']}"
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")
        else:
            st.info("Aucun avis pour le moment")

    # Graphique rapide
    st.markdown("---")
    st.subheader("📊 Aperçu Revenus (7 derniers jours)")

    dates_7j = [(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    revenus_7j = [sum([SERVICES[r['service_id']]['prix'] for r in st.session_state.reservations if r['date'] == d]) for
                  d in dates_7j]

    fig = px.bar(x=dates_7j, y=revenus_7j, labels={'x': 'Date', 'y': 'Revenus (FCFA)'})
    fig.update_traces(marker_color='#667eea')
    st.plotly_chart(fig, use_container_width=True)

# ====== PAGE PLANNING VISUEL ======
elif page == "📅 Planning Visuel":
    st.title("📅 Planning Visuel des Réservations")

    # Sélection de la date
    col1, col2 = st.columns([2, 1])
    with col1:
        date_selectionnee = st.date_input("Choisir une date", value=date.today(), min_value=date.today())
    with col2:
        st.metric("RDV ce jour",
                  len([r for r in st.session_state.reservations if r['date'] == date_selectionnee.isoformat()]))

    st.markdown("---")

    # Affichage du calendrier
    creneaux = generer_creneaux_disponibles(date_selectionnee)

    st.subheader(f"Créneaux pour le {date_selectionnee.strftime('%d/%m/%Y')}")

    # Légende
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="slot-libre">🟢 Disponible</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="slot-occupe">🔴 Réservé</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="slot-pause">⏸️ Pause</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Grille de créneaux
    cols = st.columns(4)
    for idx, creneau in enumerate(creneaux):
        with cols[idx % 4]:
            if creneau['statut'] == 'libre':
                st.markdown(f'<div class="calendar-slot slot-libre">✅ {creneau["heure"]}<br>Disponible</div>',
                            unsafe_allow_html=True)
            elif creneau['statut'] == 'occupe':
                res = next((r for r in st.session_state.reservations
                            if r['date'] == date_selectionnee.isoformat() and r['heure'] == creneau['heure']), None)
                if res:
                    st.markdown(
                        f'<div class="calendar-slot slot-occupe">🚗 {creneau["heure"]}<br>{res["client_nom"]}</div>',
                        unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="calendar-slot slot-pause">⏸️ {creneau["heure"]}<br>Pause</div>',
                            unsafe_allow_html=True)

    # Détails des réservations du jour
    st.markdown("---")
    st.subheader("📋 Détails des réservations")

    reservations_jour = [r for r in st.session_state.reservations if r['date'] == date_selectionnee.isoformat()]

    if reservations_jour:
        for res in sorted(reservations_jour, key=lambda x: x['heure']):
            service = SERVICES[res['service_id']]
            with st.expander(f"🕐 {res['heure']} - {res['client_nom']} ({res['vehicule']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Service:** {service['nom']}")
                    st.write(f"**Prix:** {format_fcfa(service['prix'])}")
                    st.write(f"**Durée:** {service['duree']}min")
                    st.write(f"**Téléphone:** {res['client_tel']}")
                with col2:
                    st.write(f"**Paiement:** {res.get('statut_paiement', '❌ Non payé')}")
                    st.write(f"**Points fidélité:** +{service['points']} points")
                    if res.get('notes'):
                        st.write(f"**Notes:** {res['notes']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📄 Générer Facture", key=f"facture_{res['id']}"):
                        facture = generer_facture_pdf(res['id'])
                        st.code(facture)
                with col2:
                    if st.button("✅ Marquer payé", key=f"payer_{res['id']}"):
                        for r in st.session_state.reservations:
                            if r['id'] == res['id']:
                                r['statut_paiement'] = '✅ Payé'
                        st.success("Paiement enregistré !")
                        st.rerun()

# ====== PAGE NOUVELLE RÉSERVATION ======
elif page == "✨ Nouvelle Réservation":
    st.title("✨ Nouvelle Réservation")

    col1, col2 = st.columns(2)

    with col1:
        client_nom = st.text_input("👤 Nom du client *", placeholder="Amadou Diallo")
        vehicule = st.text_input("🚗 Véhicule *", placeholder="Toyota Corolla 2020")
        date_res = st.date_input("📅 Date *", min_value=date.today())

        # Afficher les créneaux disponibles
        creneaux_dispo = [c['heure'] for c in generer_creneaux_disponibles(date_res) if c['statut'] == 'libre']
        heure = st.selectbox("🕐 Heure *", options=creneaux_dispo if creneaux_dispo else ["Aucun créneau disponible"])

    with col2:
        client_tel = st.text_input("📞 Téléphone *", placeholder="+225 07 12 34 56 78")
        client_email = st.text_input("📧 Email", placeholder="client@email.com")
        service_id = st.selectbox(
            "🔧 Service *",
            options=list(SERVICES.keys()),
            format_func=lambda
                x: f"{SERVICES[x]['nom']} - {format_fcfa(SERVICES[x]['prix'])} ({SERVICES[x]['duree']}min) +{SERVICES[x]['points']}pts"
        )

        # Code promo
        code_promo = st.text_input("🎁 Code promo (optionnel)", placeholder="FIRST10")

    notes = st.text_area("📝 Notes/Instructions spéciales")

    # Options avancées
    with st.expander("⚙️ Options avancées"):
        photo_avant = st.text_input("📸 URL Photo AVANT (optionnel)")
        envoi_email = st.checkbox("📧 Envoyer email de confirmation", value=True)
        acompte = st.number_input("💳 Acompte reçu (FCFA)", min_value=0, value=0, step=1000)

    # Aperçu du prix
    prix_base = SERVICES[service_id]['prix']
    prix_final = appliquer_code_promo(prix_base, code_promo) if code_promo else prix_base

    if code_promo and prix_final < prix_base:
        st.success(f"🎉 Code promo appliqué ! Prix: ~~{format_fcfa(prix_base)}~~ → **{format_fcfa(prix_final)}**")
    else:
        st.info(f"💰 Prix total: **{format_fcfa(prix_final)}**")

    if st.button("✅ Confirmer la réservation", use_container_width=True, type="primary"):
        if client_nom and client_tel and vehicule and creneaux_dispo:
            # Créer la réservation
            nouvelle_res = {
                'id': len(st.session_state.reservations) + 1,
                'client_nom': client_nom,
                'client_tel': client_tel,
                'client_email': client_email,
                'vehicule': vehicule,
                'date': date_res.isoformat(),
                'heure': heure,
                'service_id': service_id,
                'notes': notes,
                'code_promo': code_promo,
                'prix_final': prix_final,
                'photo_avant': photo_avant,
                'statut_paiement': '✅ Payé' if acompte >= prix_final else f'💳 Acompte {format_fcfa(acompte)}' if acompte > 0 else '❌ Non payé',
                'created_at': datetime.now().isoformat()
            }
            st.session_state.reservations.append(nouvelle_res)

            # Ajouter/mettre à jour le client
            client_existant = next((c for c in st.session_state.clients if c['tel'] == client_tel), None)
            if not client_existant:
                nouveau_client = {
                    'id': len(st.session_state.clients) + 1,
                    'nom': client_nom,
                    'tel': client_tel,
                    'email': client_email,
                    'vehicule': vehicule,
                    'points_fidelite': SERVICES[service_id]['points'],
                    'date_ajout': datetime.now().isoformat()
                }
                st.session_state.clients.append(nouveau_client)
            else:
                client_existant['points_fidelite'] = client_existant.get('points_fidelite', 0) + SERVICES[service_id][
                    'points']

            st.success("✅ Réservation confirmée avec succès !")
            st.balloons()

            if envoi_email and client_email:
                st.info(f"📧 Email de confirmation envoyé à {client_email}")

            st.markdown(f"""
            <div class="success-box">
            <h3>📋 Récapitulatif</h3>
            Client: {client_nom}<br>
            Date: {date_res.strftime('%d/%m/%Y')} à {heure}<br>
            Service: {SERVICES[service_id]['nom']}<br>
            Prix: {format_fcfa(prix_final)}<br>
            Points gagnés: +{SERVICES[service_id]['points']} points
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Veuillez remplir tous les champs obligatoires et choisir un créneau disponible")

# ====== PAGE DEVIS & PROMOS ======
elif page == "💰 Devis & Promos":
    st.title("💰 Calculateur de Devis & Codes Promo")

    tab1, tab2 = st.tabs(["💵 Devis", "🎁 Codes Promo"])

    with tab1:
        st.subheader("Sélectionnez les services")

        services_selectionnes = []
        for service_id, service in SERVICES.items():
            if st.checkbox(
                    f"{service['nom']} - {format_fcfa(service['prix'])} (⏱️ {service['duree']}min, +{service['points']} points)",
                    key=f"devis_service_{service_id}"
            ):
                services_selectionnes.append(service_id)

        if services_selectionnes:
            total_prix = sum([SERVICES[s]['prix'] for s in services_selectionnes])
            total_duree = sum([SERVICES[s]['duree'] for s in services_selectionnes])
            total_points = sum([SERVICES[s]['points'] for s in services_selectionnes])

            code_promo_devis = st.text_input("🎁 Appliquer un code promo")
            prix_final = appliquer_code_promo(total_prix, code_promo_devis) if code_promo_devis else total_prix

            col1, col2, col3 = st.columns(3)
            with col1:
                reduction = total_prix - prix_final
                st.metric("💰 Total", format_fcfa(prix_final),
                          delta=f"-{format_fcfa(reduction)}" if reduction > 0 else None)
            with col2:
                st.metric("⏱️ Durée", f"{total_duree // 60}h{total_duree % 60}min")
            with col3:
                st.metric("⭐ Points", f"+{total_points}")

    with tab2:
        st.subheader("🎁 Gérer les codes promo")

        # Afficher codes existants
        for idx, promo in enumerate(st.session_state.codes_promo):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{promo['code']}**")
            with col2:
                if promo['type'] == 'pourcentage':
                    st.write(f"-{promo['reduction']}%")
                else:
                    st.write(f"-{format_fcfa(promo['reduction'])}")
            with col3:
                st.write("✅ Actif" if promo['actif'] else "❌ Inactif")

        st.markdown("---")

        # Ajouter nouveau code
        st.write("**Créer un nouveau code**")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_code = st.text_input("Code", key="new_promo_code")
        with col2:
            reduction = st.number_input("Réduction", min_value=1, key="new_promo_reduction")
        with col3:
            type_reduction = st.selectbox("Type", ["pourcentage", "fcfa"], key="new_promo_type")

        if st.button("➕ Ajouter"):
            st.session_state.codes_promo.append({
                'code': new_code,
                'reduction': reduction,
                'type': type_reduction,
                'actif': True
            })
            st.success(f"Code {new_code} ajouté !")
            st.rerun()

# ====== PAGE CLIENTS & FIDÉLITÉ ======
elif page == "👥 Clients & Fidélité":
    st.title("👥 Base Clients & Programme Fidélité")

    st.info("🎁 Programme fidélité: 10 points = 1 lavage gratuit !")

    if st.session_state.clients:
        # Statistiques clients
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total clients", len(st.session_state.clients))
        with col2:
            clients_fideles = len([c for c in st.session_state.clients if c.get('points_fidelite', 0) >= 10])
            st.metric("Clients fidèles (10+ pts)", clients_fideles)
        with col3:
            revenus_total = sum([
                sum([SERVICES[r['service_id']]['prix'] for r in st.session_state.reservations if
                     r['client_tel'] == c['tel']])
                for c in st.session_state.clients
            ])
            st.metric("CA Total clients", format_fcfa(revenus_total))

        st.markdown("---")

        # Liste des clients avec détails
        for client in sorted(st.session_state.clients, key=lambda x: x.get('points_fidelite', 0), reverse=True):
            reservations_client = [r for r in st.session_state.reservations if r['client_tel'] == client['tel']]
            nb_reservations = len(reservations_client)
            total_depense = sum([SERVICES[r['service_id']]['prix'] for r in reservations_client])
            points = client.get('points_fidelite', 0)

            # Badge fidélité
            badge = "🏆 VIP" if points >= 20 else "⭐ Fidèle" if points >= 10 else "👤 Client"

            with st.expander(f"{badge} {client['nom']} - {points} points"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**📞 Téléphone:** {client['tel']}")
                    st.write(f"**📧 Email:** {client.get('email', 'Non renseigné')}")
                    st.write(f"**🚗 Véhicule:** {client['vehicule']}")
                    st.write(f"**📅 Client depuis:** {client['date_ajout'][:10]}")

                with col2:
                    st.metric("Réservations", nb_reservations)
                    st.metric("Dépenses totales", format_fcfa(total_depense))
                    st.metric("Points fidélité", f"{points}/10")

                    if points >= 10:
                        if st.button(f"🎁 Utiliser 10 points (lavage gratuit)", key=f"fidelite_{client['id']}"):
                            client['points_fidelite'] -= 10
                            st.success("10 points utilisés ! Lavage gratuit accordé 🎉")
                            st.rerun()
    else:
        st.info("Aucun client enregistré")

# ====== PAGE PORTFOLIO ======
elif page == "📸 Portfolio":
    st.title("📸 Portfolio - Nos Réalisations")

    tab1, tab2 = st.tabs(["🖼️ Galerie", "➕ Ajouter"])

    with tab1:
        if st.session_state.portfolio:
            cols = st.columns(3)
            for idx, photo in enumerate(st.session_state.portfolio):
                with cols[idx % 3]:
                    st.image(photo['image_url'], use_container_width=True)
                    st.markdown(f"**{photo['titre']}**")
                    if photo.get('description'):
                        st.write(photo['description'])
                    if photo.get('note'):
                        st.write(f"⭐ Note: {photo['note']}/5")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️", key=f"del_portfolio_{idx}"):
                            st.session_state.portfolio.pop(idx)
                            st.rerun()
                    with col2:
                        if st.button("👍", key=f"like_portfolio_{idx}"):
                            st.success("Ajouté aux favoris !")
                    st.markdown("---")
        else:
            st.info("Aucune photo dans le portfolio")

    with tab2:
        st.subheader("Ajouter une réalisation")
        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input("Titre *", placeholder="Toyota Hilux - Détailing Complet")
            image_url = st.text_input("URL de l'image *", placeholder="https://...")
        with col2:
            note_client = st.slider("Note du client", 1, 5, 5)
            description = st.text_input("Description", placeholder="Polissage + céramique + intérieur")

        if st.button("➕ Ajouter au portfolio", use_container_width=True):
            if titre and image_url:
                nouvelle_photo = {
                    'id': len(st.session_state.portfolio) + 1,
                    'titre': titre,
                    'description': description,
                    'image_url': image_url,
                    'note': note_client,
                    'date': datetime.now().isoformat()
                }
                st.session_state.portfolio.append(nouvelle_photo)
                st.success("✅ Photo ajoutée !")
                st.rerun()

# ====== PAGE STATISTIQUES ======
elif page == "📊 Statistiques":
    st.title("📊 Statistiques & Analytics")

    if not st.session_state.reservations:
        st.info("Pas encore de données pour les statistiques. Créez des réservations d'abord !")
    else:
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            periode = st.selectbox("Période", ["7 derniers jours", "30 derniers jours", "Tout"])
        with col2:
            st.metric("Total réservations", len(st.session_state.reservations))

        # Graphiques
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Revenus", "📈 Services", "👥 Clients", "⏰ Planning"])

        with tab1:
            # Revenus par jour
            df_res = pd.DataFrame([
                {
                    'date': r['date'],
                    'revenus': SERVICES[r['service_id']]['prix']
                }
                for r in st.session_state.reservations
            ])

            if not df_res.empty:
                df_grouped = df_res.groupby('date')['revenus'].sum().reset_index()
                fig = px.line(df_grouped, x='date', y='revenus', title='Évolution des revenus (FCFA)')
                fig.update_traces(line_color='#667eea', line_width=3)
                st.plotly_chart(fig, use_container_width=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("CA Total", format_fcfa(df_grouped['revenus'].sum()))
                with col2:
                    st.metric("CA Moyen/Jour", format_fcfa(df_grouped['revenus'].mean()))

        with tab2:
            # Services les plus demandés
            services_count = {}
            for r in st.session_state.reservations:
                service_nom = SERVICES[r['service_id']]['nom']
                services_count[service_nom] = services_count.get(service_nom, 0) + 1

            if services_count:
                fig = px.pie(
                    values=list(services_count.values()),
                    names=list(services_count.keys()),
                    title='Répartition des services'
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            # Top clients
            st.subheader("🏆 Top 5 Clients")
            clients_stats = []
            for client in st.session_state.clients:
                reservations_client = [r for r in st.session_state.reservations if r['client_tel'] == client['tel']]
                total_depense = sum([SERVICES[r['service_id']]['prix'] for r in reservations_client])
                clients_stats.append({
                    'nom': client['nom'],
                    'reservations': len(reservations_client),
                    'depense_fcfa': total_depense,
                    'points': client.get('points_fidelite', 0)
                })

            df_clients = pd.DataFrame(clients_stats).sort_values('depense_fcfa', ascending=False).head(5)
            if not df_clients.empty:
                st.dataframe(df_clients, use_container_width=True)

        with tab4:
            # Créneaux les plus demandés
            creneaux_count = {}
            for r in st.session_state.reservations:
                creneaux_count[r['heure']] = creneaux_count.get(r['heure'], 0) + 1

            if creneaux_count:
                fig = px.bar(
                    x=list(creneaux_count.keys()),
                    y=list(creneaux_count.values()),
                    title='Créneaux horaires les plus demandés'
                )
                fig.update_traces(marker_color='#667eea')
                st.plotly_chart(fig, use_container_width=True)

# ====== PAGE PARAMÈTRES ======
elif page == "⚙️ Paramètres":
    st.title("⚙️ Paramètres & Configuration")

    tab1, tab2, tab3 = st.tabs(["🏢 Entreprise", "💾 Données", "🔔 Notifications"])

    with tab1:
        st.subheader("Informations de l'entreprise")
        nom_entreprise = st.text_input("Nom", value="Lavage Esthétique Pro")
        adresse = st.text_input("Adresse", value="Abidjan, Cocody")
        telephone = st.text_input("Téléphone", value="+225 07 12 34 56 78")
        email = st.text_input("Email", value="contact@lavagepro.ci")

        st.subheader("⏰ Horaires d'ouverture")
        col1, col2 = st.columns(2)
        with col1:
            heure_ouverture = st.time_input("Ouverture", value=datetime.strptime("08:00", "%H:%M").time())
            pause_debut = st.time_input("Début pause", value=datetime.strptime("12:00", "%H:%M").time())
        with col2:
            heure_fermeture = st.time_input("Fermeture", value=datetime.strptime("18:00", "%H:%M").time())
            pause_fin = st.time_input("Fin pause", value=datetime.strptime("13:00", "%H:%M").time())

        if st.button("💾 Sauvegarder les paramètres"):
            st.success("✅ Paramètres sauvegardés !")

    with tab2:
        st.subheader("💾 Gestion des données")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"**Réservations:** {len(st.session_state.reservations)}")
            st.write(f"**Clients:** {len(st.session_state.clients)}")
            st.write(f"**Portfolio:** {len(st.session_state.portfolio)}")

        with col2:
            if st.button("📥 Exporter tout (JSON)"):
                data_export = {
                    'reservations': st.session_state.reservations,
                    'clients': st.session_state.clients,
                    'portfolio': st.session_state.portfolio,
                    'avis': st.session_state.avis,
                    'export_date': datetime.now().isoformat()
                }
                st.download_button(
                    "💾 Télécharger",
                    data=json.dumps(data_export, indent=2, ensure_ascii=False),
                    file_name=f"backup_{date.today()}.json",
                    mime="application/json"
                )

        with col3:
            if st.button("🗑️ Réinitialiser", type="secondary"):
                if st.checkbox("Je confirme la réinitialisation"):
                    st.session_state.reservations = []
                    st.session_state.clients = []
                    st.session_state.portfolio = []
                    st.session_state.avis = []
                    st.success("Données réinitialisées")
                    st.rerun()

        st.markdown("---")
        st.info("💡 Astuce: Pour sauvegarder définitivement vos données, utilisez Google Sheets (voir documentation)")

    with tab3:
        st.subheader("🔔 Paramètres de notifications")

        email_confirmation = st.checkbox("Email de confirmation client", value=True)
        email_rappel = st.checkbox("Email de rappel 24h avant", value=True)
        sms_confirmation = st.checkbox("SMS de confirmation", value=False)

        email_admin = st.text_input("Email admin pour notifications", value="admin@lavagepro.ci")

        st.info("📧 Configuration SMTP nécessaire pour l'envoi d'emails réels")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
💰 **Devise:** FCFA (Franc CFA)  
💾 **Mode:** Session  
📚 **Version:** Pro+ 2.0 (Afrique)  
🚀 **Mise à jour:** Janvier 2025
""")

# Boutons d'action rapide dans la sidebar
st.sidebar.markdown("### ⚡ Actions rapides")
if st.sidebar.button("🆕 Nouvelle réservation", use_container_width=True):
    st.session_state.page_override = "✨ Nouvelle Réservation"
if st.sidebar.button("📊 Voir stats", use_container_width=True):
    st.session_state.page_override = "📊 Statistiques"