import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go
from database import Database
import hashlib
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import qrcode

# Configuration de la page
st.set_page_config(
    page_title="🚗 WashAfrique Pro",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# WashAfrique Pro\nVersion 3.0 - Édition Professionnelle\n\nSolution complète de gestion pour lavage automobile"
    }
)

# Initialisation de la base de données
if 'db' not in st.session_state:
    st.session_state.db = Database()

# Dictionnaire multilingue
TRANSLATIONS = {
    'fr': {
        'title': '🚗 WashAfrique Pro',
        'login': 'Connexion',
        'username': "Nom d'utilisateur",
        'password': 'Mot de passe',
        'login_btn': 'Se connecter',
        'logout': 'Déconnexion',
        'dashboard': '🏠 Tableau de Bord',
        'new_reservation': '➕ Nouvelle Réservation',
        'planning': '📅 Planning',
        'clients': '👥 Clients',
        'services': '🔧 Services',
        'employees': '👨💼 Employés',
        'payments': '💰 Paiements',
        'promotions': '🎁 Promotions',
        'loyalty': '⭐ Fidélité',
        'stock': '📦 Stock',
        'analytics': '📊 Statistiques',
        'settings': '⚙️ Paramètres',
    },
    'en': {
        'title': '🚗 WashAfrique Pro',
        'login': 'Login',
        'username': 'Username',
        'password': 'Password',
        'login_btn': 'Sign In',
        'logout': 'Logout',
        'dashboard': '🏠 Dashboard',
        'new_reservation': '➕ New Booking',
        'planning': '📅 Schedule',
        'clients': '👥 Clients',
        'services': '🔧 Services',
        'employees': '👨💼 Employees',
        'payments': '💰 Payments',
        'promotions': '🎁 Promotions',
        'loyalty': '⭐ Loyalty',
        'stock': '📦 Inventory',
        'analytics': '📊 Analytics',
        'settings': '⚙️ Settings',
    },
    'ar': {
        'title': '🚗 WashAfrique Pro',
        'login': 'تسجيل الدخول',
        'username': 'اسم المستخدم',
        'password': 'كلمة المرور',
        'login_btn': 'دخول',
        'logout': 'خروج',
        'dashboard': '🏠 لوحة التحكم',
        'new_reservation': '➕ حجز جديد',
        'planning': '📅 الجدول',
        'clients': '👥 العملاء',
        'services': '🔧 الخدمات',
        'employees': '👨💼 الموظفون',
        'payments': '💰 المدفوعات',
        'promotions': '🎁 العروض',
        'loyalty': '⭐ الولاء',
        'stock': '📦 المخزون',
        'analytics': '📊 الإحصائيات',
        'settings': '⚙️ الإعدادات',
    }
}

# Initialisation de la langue
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

def t(key):
    """Fonction de traduction"""
    return TRANSLATIONS[st.session_state.lang].get(key, key)

# Style CSS professionnel
st.markdown("""
    <style>
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: white;
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.9) !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2em !important;
        font-weight: bold !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin: 10px 0;
        color: white;
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #00d4ff;
        margin: 15px 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff6b6b;
        margin: 15px 0;
    }
    
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    @media (max-width: 768px) {
        .stMetric {
            font-size: 0.85em;
            padding: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Horaires
HEURE_OUVERTURE = "08:00"
HEURE_FERMETURE = "19:00"
HEURE_PAUSE_DEBUT = "12:00"
HEURE_PAUSE_FIN = "13:00"

def format_fcfa(montant):
    """Formate en FCFA"""
    return f"{int(montant):,} FCFA".replace(',', ' ')

def generer_creneaux(date_sel, poste_id=None):
    """Génère les créneaux horaires avec gestion multi-postes et durée réelle"""
    creneaux = []
    debut = datetime.strptime(HEURE_OUVERTURE, '%H:%M')
    fin = datetime.strptime(HEURE_FERMETURE, '%H:%M')
    pause_d = datetime.strptime(HEURE_PAUSE_DEBUT, '%H:%M')
    pause_f = datetime.strptime(HEURE_PAUSE_FIN, '%H:%M')
    
    reservations = st.session_state.db.get_reservations_by_date(date_sel)
    if poste_id:
        reservations = [r for r in reservations if r['poste_id'] == poste_id]
    
    current = debut
    while current < fin:
        heure_str = current.strftime('%H:%M')
        
        if pause_d <= current < pause_f:
            statut = 'pause'
        else:
            est_occupe = False
            for res in reservations:
                heure_res = datetime.strptime(res['heure'], '%H:%M')
                duree = res.get('duree', 30)
                fin_res = heure_res + timedelta(minutes=duree)
                
                if heure_res <= current < fin_res:
                    est_occupe = True
                    break
            
            statut = 'occupe' if est_occupe else 'libre'
        
        creneaux.append({'heure': heure_str, 'statut': statut})
        current += timedelta(minutes=30)
    
    return creneaux

def generer_pdf_facture(reservation, client, service):
    """Génère une facture PDF professionnelle"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("🚗 WASHAFRIQUE PRO", title_style))
    story.append(Paragraph("Lavage Automobile Premium", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(f"<b>FACTURE #{reservation['id']:05d}</b>", styles['Heading2']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    client_info = [
        ["<b>CLIENT</b>", ""],
        ["Nom:", client['nom']],
        ["Téléphone:", client['tel']],
        ["Véhicule:", client['vehicule']],
        ["Points fidélité:", str(client['points_fidelite'])]
    ]
    
    table = Table(client_info, colWidths=[4*cm, 10*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))
    
    service_info = [
        ["<b>SERVICE</b>", "<b>DATE/HEURE</b>", "<b>MONTANT</b>"],
        [
            service['nom'],
            f"{reservation['date']} à {reservation['heure']}",
            format_fcfa(service['prix'])
        ]
    ]
    
    if reservation.get('code_promo'):
        service_info.append([
            f"Code promo: {reservation['code_promo']}",
            "Réduction",
            f"- {format_fcfa(reservation['reduction'])}"
        ])
    
    if reservation.get('points_utilises', 0) > 0:
        service_info.append([
            f"Points utilisés: {reservation['points_utilises']}",
            "Réduction fidélité",
            f"- {format_fcfa(reservation['points_utilises'] * 100)}"
        ])
    
    service_info.append(["", "<b>TOTAL À PAYER</b>", f"<b>{format_fcfa(reservation['montant'])}</b>"])
    
    table = Table(service_info, colWidths=[7*cm, 5*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(table)
    story.append(Spacer(1, 1*cm))
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"WASHAFRIQUE-{reservation['id']:05d}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    story.append(Paragraph("<b>Code de confirmation:</b>", styles['Normal']))
    img = RLImage(qr_buffer, width=3*cm, height=3*cm)
    story.append(img)
    
    story.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    story.append(Paragraph("Merci de votre confiance ! | WashAfrique Pro - Solution de gestion professionnelle", footer_style))
    story.append(Paragraph("📞 Contact: +225 XX XX XX XX | 📧 contact@washafrique.com", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ===== AUTHENTIFICATION =====
def check_authentication():
    """Vérifie si l'utilisateur est connecté"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title(t('login'))
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🚗 WashAfrique Pro")
            st.markdown("---")
            
            username = st.text_input(t('username'), placeholder="admin")
            password = st.text_input(t('password'), type="password", placeholder="admin123")
            
            if st.button(t('login_btn'), use_container_width=True, type="primary"):
                user = st.session_state.db.verify_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success("✅ Connexion réussie !")
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
            
            st.markdown("---")
            st.info("💡 **Par défaut:** admin / admin123")
        
        return False
    
    return True

# Vérifier l'authentification
if not check_authentication():
    st.stop()

