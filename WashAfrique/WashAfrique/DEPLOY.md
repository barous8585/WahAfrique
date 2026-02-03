# 🚀 GUIDE DE DÉPLOIEMENT STREAMLIT CLOUD

## Étapes pour déployer WashAfrique Pro

### 1. Préparation (✅ DÉJÀ FAIT)
- ✅ Code poussé sur GitHub
- ✅ requirements.txt configuré
- ✅ .gitignore créé
- ✅ Configuration Streamlit

### 2. Déploiement sur Streamlit Cloud

#### A. Accéder à Streamlit Cloud
1. Allez sur : **https://share.streamlit.io**
2. Connectez-vous avec votre compte GitHub

#### B. Créer une nouvelle application
1. Cliquez sur **"New app"** (en haut à droite)

2. Remplissez le formulaire :
   ```
   Repository : barous8585/WashAfrique
   Branch : main
   Main file path : WashAfrique/app.py
   ```

3. **Advanced settings** (optionnel mais recommandé) :
   - Python version : 3.11
   - Secrets : (aucun nécessaire pour le moment)

4. Cliquez sur **"Deploy!"**

#### C. Attendre le déploiement
L'application va :
- ⏱️ Installer les dépendances (~2 min)
- 🗄️ Créer la base de données automatiquement
- 📊 Initialiser les données d'exemple
- ✅ Démarrer l'application

Vous verrez les logs en temps réel.

### 3. Premier accès

Une fois déployé, vous recevrez une URL comme :
```
https://washafrique-xxxxx.streamlit.app
```

**🔐 Identifiants par défaut :**
- Username : `admin`
- Password : `admin123`

⚠️ **ACTION IMMÉDIATE :** Changez le mot de passe dès la première connexion !

### 4. Initialiser les données (optionnel)

Si vous voulez réinitialiser les données d'exemple :

1. Connectez-vous en SSH à votre app (via Streamlit Cloud)
2. Exécutez : `python init_data.py`

Ou bien, l'initialisation se fait automatiquement au premier lancement.

### 5. Configuration post-déploiement

#### A. Changer le mot de passe admin
1. Connectez-vous avec `admin` / `admin123`
2. Allez dans **⚙️ Mon Profil** → **🔐 Sécurité**
3. Changez le mot de passe

#### B. Personnaliser l'entreprise
1. Allez dans **⚙️ Mon Profil** → **🏢 Entreprise**
2. Remplissez :
   - Nom de votre entreprise
   - Adresse
   - Téléphone
   - Email

#### C. Créer vos services
1. Allez dans **🔧 Services & Prix**
2. Supprimez les services d'exemple si besoin
3. Créez vos vrais services avec vos prix

#### D. Créer vos employés
1. Allez dans **👥 Employés** → **➕ Ajouter Employé**
2. Créez un compte pour chaque employé
3. Notez bien les identifiants

### 6. Partager l'application

Votre URL Streamlit Cloud peut être partagée directement :
- Avec vos employés (ils se connectent avec leurs identifiants)
- Sur votre site web
- Sur vos réseaux sociaux

### 7. Maintenance et mises à jour

Pour mettre à jour l'application :
1. Modifiez le code localement
2. Committez et poussez sur GitHub :
   ```bash
   git add .
   git commit -m "Description de la mise à jour"
   git push origin main
   ```
3. Streamlit Cloud redéploiera automatiquement en 1-2 minutes

### 8. Surveillance

Dans Streamlit Cloud, vous pouvez :
- 📊 Voir les logs en temps réel
- 👥 Voir le nombre d'utilisateurs connectés
- 🔄 Redémarrer l'application si besoin
- ⚙️ Modifier la configuration

### 9. Limites du plan gratuit

**Streamlit Cloud Gratuit :**
- ✅ 1 application publique
- ✅ 1 GB RAM
- ✅ 1 GB stockage
- ✅ Redémarrage automatique si inactif 7 jours

**Suffisant pour :**
- 10-20 utilisateurs simultanés
- Base SQLite jusqu'à 100 000 réservations
- Fonctionnement 24/7

**Si vous avez besoin de plus :**
- Passez au plan Team ($20/mois)
- Plus de ressources et d'applications

### 10. Backup des données

⚠️ **IMPORTANT :** Sur Streamlit Cloud gratuit, les données peuvent être perdues si l'app est inactive trop longtemps.

**Solution :**
1. Téléchargez régulièrement la base de données :
   - Ajoutez un bouton dans l'interface propriétaire
   - Export SQLite → téléchargement
2. Ou passez à une base PostgreSQL (plan payant)

### 🆘 Problèmes courants

#### Erreur lors du déploiement
- Vérifiez que le chemin est bien `WashAfrique/app.py`
- Vérifiez requirements.txt

#### Application lente
- Normal au premier démarrage (création BDD)
- Si persistant : vérifiez les logs

#### Base de données vide
- Exécutez `python init_data.py` manuellement
- Ou attendez le premier lancement

### ✅ Checklist finale

Avant de commercialiser :
- [ ] Application déployée et accessible
- [ ] Mot de passe admin changé
- [ ] Informations entreprise remplies
- [ ] Services personnalisés créés
- [ ] Au moins 1 employé créé et testé
- [ ] Workflow complet testé (de la réservation à la validation)
- [ ] URL partagée aux employés

---

**🎉 Votre application est maintenant en ligne et prête pour la commercialisation !**

**URL de déploiement :** https://share.streamlit.io
**Repository GitHub :** https://github.com/barous8585/WashAfrique
**Documentation complète :** README_DEPLOY.md
