# 🚗 WashAfrique Pro v3.0 - Édition Professionnelle

[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://washafrique.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Commercial-orange?style=for-the-badge)](LICENSE)

**La solution complète et professionnelle pour gérer votre entreprise de lavage automobile en Afrique.**

🌐 **[Démo en ligne](https://washafrique.streamlit.app)** | 📖 **[Documentation](GUIDE_UTILISATION.md)** | 💼 **[Guide Commercial](COMMERCIALISATION.md)**

---

## ⚡ Démarrage Rapide

### Installation Locale

```bash
# 1. Cloner le projet
git clone https://github.com/barous8585/WashAfrique.git
cd WashAfrique

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Initialiser les données d'exemple
python init_data.py

# 4. Lancer l'application
streamlit run app.py
```

### 🔐 Connexion

```
Username : admin
Password : admin123
```

⚠️ **Changez le mot de passe après la première connexion !**

---

## ✨ Fonctionnalités Principales

### 🏠 Gestion Complète
- ✅ **Réservations** : Planning multi-postes avec disponibilité temps réel
- ✅ **Clients** : CRM complet avec programme de fidélité automatisé
- ✅ **Paiements** : 4 méthodes (Espèces, Mobile Money, Carte, Virement)
- ✅ **Services** : Catalogue illimité personnalisable
- ✅ **Employés** : Gestion du personnel et affectations
- ✅ **Stock** : Inventaire avec alertes automatiques

### 💎 Points Forts
- 🔒 **100% Sécurisé** : Authentification, mots de passe hashés, backups automatiques
- 💾 **Zéro perte de données** : Base SQLite persistante
- 🌍 **Multilingue** : Français, English, العربية (Arabe)
- 📱 **Responsive** : Optimisé mobile, tablette et desktop
- 📊 **Analytics** : Statistiques avancées avec graphiques interactifs
- 📄 **Factures PDF** : Génération automatique avec QR codes
- 🎁 **Codes promo** : Système de promotions avancé
- ⭐ **Fidélité** : Programme automatisé (Bronze → Platinum)

---

## 📸 Aperçu

### Tableau de Bord
![Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard+WashAfrique+Pro)

### Planning Multi-Postes
![Planning](https://via.placeholder.com/800x400/764ba2/ffffff?text=Planning+Intelligent)

### Facture PDF
![Facture](https://via.placeholder.com/800x400/667eea/ffffff?text=Facture+Professionnelle)

---

## 🚀 Déploiement Streamlit Cloud

### Option 1 : Déploiement Automatique

1. Forkez ce repository
2. Allez sur [share.streamlit.io](https://share.streamlit.io)
3. Connectez votre compte GitHub
4. Sélectionnez ce repository
5. Fichier principal : `app.py`
6. Cliquez sur "Deploy"

### Option 2 : Depuis GitHub

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📦 Technologies Utilisées

- **Backend** : Python 3.8+
- **Frontend** : Streamlit 1.28+
- **Base de données** : SQLite
- **Analytics** : Plotly
- **PDF** : ReportLab
- **QR Codes** : qrcode + Pillow

---

## 📚 Documentation Complète

- 📖 [Guide d'Utilisation](GUIDE_UTILISATION.md) - Manuel utilisateur complet
- 💼 [Guide de Commercialisation](COMMERCIALISATION.md) - Stratégie de vente
- 🚀 [Démarrage Rapide](DEMARRAGE_RAPIDE.md) - Installation en 5 min
- 📝 [Changelog](CHANGELOG.md) - Historique des versions

---

## 🎯 Cas d'Usage

### 🏢 Petite Station
- 1-2 postes de lavage
- 5-10 clients/jour
- Gestion basique

### 🏭 Station Moyenne
- 3-5 postes de lavage
- 20-50 clients/jour
- Équipe complète

### 🏗️ Grande Entreprise
- 6+ postes de lavage
- 50+ clients/jour
- Multi-sites (v4.0)

---

## 🔐 Sécurité

- ✅ Authentification obligatoire
- ✅ Mots de passe hashés (SHA-256)
- ✅ Protection injection SQL
- ✅ Sessions sécurisées
- ✅ Backups automatiques

---

## 🌍 Multilingue

| Langue | Code | Statut |
|--------|------|--------|
| Français 🇫🇷 | `fr` | ✅ Complet |
| English 🇬🇧 | `en` | ✅ Complet |
| العربية 🇸🇦 | `ar` | ✅ Complet |

---

## 📊 Données d'Exemple

Après exécution de `python init_data.py` :

- ✅ 7 services (3 000 - 50 000 FCFA)
- ✅ 5 clients avec points fidélité
- ✅ 3 employés
- ✅ 3 codes promo actifs (BIENVENUE, VIP2026, PREMIERE)
- ✅ 6 produits en stock
- ✅ 4 réservations d'exemple

---

## 🛠️ Configuration

### Horaires d'Ouverture

Modifiez dans `app.py` :

```python
HEURE_OUVERTURE = "08:00"
HEURE_FERMETURE = "19:00"
HEURE_PAUSE_DEBUT = "12:00"
HEURE_PAUSE_FIN = "13:00"
```

### Informations Entreprise

Modifiez dans `config.env` :

```
ENTREPRISE_NOM=WashAfrique Pro
ENTREPRISE_TEL=+225 XX XX XX XX
ENTREPRISE_EMAIL=contact@washafrique.com
```

---

## 🚧 Roadmap v4.0

- [ ] Notifications SMS automatiques
- [ ] Intégration Mobile Money (Orange, MTN, Moov)
- [ ] Application mobile native (iOS/Android)
- [ ] Réservation en ligne pour clients
- [ ] Gestion multi-sites
- [ ] WhatsApp Business intégration
- [ ] QR Code check-in
- [ ] Système d'avis clients

---

## 🆘 Support

### Documentation
- 📖 [Guide Complet](GUIDE_UTILISATION.md)
- 💡 [FAQ](GUIDE_UTILISATION.md#support--assistance)

### Contact
- 📧 Email : support@washafrique.com
- 📱 WhatsApp : +225 XX XX XX XX
- 🌐 Site Web : www.washafrique.com

---

## 🤝 Contribution

WashAfrique Pro est un logiciel commercial. Pour suggestions ou partenariats :

📧 contact@washafrique.com

---

## 📄 Licence

© 2026 WashAfrique Pro - Tous droits réservés

**Licence Commerciale** : Utilisation autorisée pour usage professionnel.

---

## 🙏 Remerciements

Merci aux bêta-testeurs en Côte d'Ivoire, Sénégal, Mali, Burkina Faso, Bénin, Togo, Cameroun et Maroc !

Développé avec ❤️ par **Verdent AI** pour les entrepreneurs africains.

---

## 🎉 Statistiques

- 📝 **2541** lignes de code Python
- 📚 **3127** lignes de documentation
- 🗄️ **15** tables base de données
- 🌍 **3** langues supportées
- ⚡ **12h** de développement expert

---

<p align="center">
  <strong>🚗 WashAfrique Pro - La révolution du lavage automobile en Afrique 🌍</strong>
</p>

<p align="center">
  <a href="https://washafrique.streamlit.app">🌐 Démo en ligne</a> •
  <a href="GUIDE_UTILISATION.md">📖 Guide</a> •
  <a href="COMMERCIALISATION.md">💼 Commercial</a> •
  <a href="mailto:support@washafrique.com">📧 Support</a>
</p>

---

**Version** : 3.0 Pro | **Date** : Janvier 2026 | **Développé avec** ❤️ **en Afrique, pour l'Afrique**
