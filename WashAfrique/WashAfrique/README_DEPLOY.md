# 🚗 WashAfrique Pro - Système de Gestion de Nettoyage Esthétique

Application professionnelle de gestion complète pour entreprise de nettoyage automobile.

## 🚀 Déploiement sur Streamlit Cloud

### Étape 1 : Préparer le repository
Le repository est déjà prêt avec tous les fichiers nécessaires :
- ✅ `app.py` - Application principale
- ✅ `database.py` - Gestion base de données SQLite
- ✅ `init_data.py` - Données d'exemple
- ✅ `requirements.txt` - Dépendances Python
- ✅ `.streamlit/config.toml` - Configuration Streamlit

### Étape 2 : Déployer sur Streamlit Cloud

1. **Allez sur https://share.streamlit.io**

2. **Connectez-vous avec votre compte GitHub**

3. **Cliquez sur "New app"**

4. **Remplissez les informations :**
   - Repository : `barous8585/WashAfrique`
   - Branch : `main`
   - Main file path : `WashAfrique/app.py`

5. **Cliquez sur "Deploy!"**

6. **Attendez 2-3 minutes** - L'application va :
   - Installer les dépendances
   - Créer la base de données automatiquement
   - Initialiser avec les données d'exemple

### Étape 3 : Premier lancement

Une fois déployé, l'application sera accessible via une URL comme :
```
https://washafrique-xxxxx.streamlit.app
```

**Identifiants par défaut :**
- Username : `admin`
- Password : `admin123`

⚠️ **IMPORTANT :** Changez le mot de passe dès la première connexion !

## 📋 Fonctionnalités Principales

### 👨‍💼 Propriétaire
- ✅ Tableau de bord avec statistiques en temps réel
- ✅ Gestion complète des employés (création comptes, pointage)
- ✅ Création et modification des services et prix
- ✅ Validation qualité des services
- ✅ Gestion clients et fidélité
- ✅ Rapports et statistiques
- ✅ Configuration entreprise

### 👔 Employé
- ✅ Pointage arrivée/départ automatique
- ✅ Lancement de services pour clients
- ✅ Workflow complet : Démarrer → Terminer → Encaisser
- ✅ Suivi des services en cours
- ✅ Dashboard personnel avec stats

## 🔄 Workflow des Services

```
1. 🔵 EN ATTENTE → Employé démarre le service
2. 🟡 EN COURS → Employé marque comme terminé
3. 🟢 TERMINÉ → Employé encaisse
4. 💰 PAYÉ → Propriétaire valide la qualité
5. ✅ VALIDÉ → Service complet !
```

## 💾 Base de Données

L'application utilise SQLite avec 16 tables :
- users (comptes utilisateurs)
- employes (informations employés)
- pointages (présences)
- clients (base clients)
- services (catalogue)
- reservations (services en cours/terminés)
- paiements (historique)
- Et plus...

La base de données est créée automatiquement au premier lancement.

## 🛠️ Technologies

- **Frontend/Backend :** Streamlit 1.28+
- **Base de données :** SQLite
- **Graphiques :** Plotly
- **PDF :** ReportLab
- **Authentification :** SHA-256

## 📱 Interface

- ✅ Navigation horizontale (SANS sidebar)
- ✅ Design moderne avec dégradés
- ✅ Responsive pour mobile/tablette
- ✅ Badges colorés par statut
- ✅ Interface intuitive

## 🔐 Sécurité

- Mots de passe hashés (SHA-256)
- Authentification multi-rôles (admin/employé)
- Sessions sécurisées
- Protection CSRF intégrée

## 📊 Données d'Exemple

L'application inclut des données de démonstration :
- 7 services pré-configurés
- 5 clients exemple
- 3 employés
- 3 codes promo
- 6 produits en stock

## 🆘 Support

Pour toute question ou assistance :
- Repository : https://github.com/barous8585/WashAfrique
- Issues : https://github.com/barous8585/WashAfrique/issues

## 📜 Licence

© 2026 WashAfrique Pro - Tous droits réservés

---

**Version :** 3.0 Enterprise  
**Dernière mise à jour :** Janvier 2026  
**Statut :** ✅ Production Ready
