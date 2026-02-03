# 🚀 Guide de Déploiement sur Streamlit Cloud

## ✅ VOTRE CODE EST MAINTENANT SUR GITHUB !

Repository : https://github.com/barous8585/WashAfrique

---

## 📋 ÉTAPES DE DÉPLOIEMENT

### 1️⃣ Aller sur Streamlit Cloud

Ouvrez votre navigateur et allez sur :
👉 **https://share.streamlit.io**

### 2️⃣ Se Connecter

- Cliquez sur **"Sign up"** ou **"Sign in"**
- Choisissez **"Continue with GitHub"**
- Autorisez l'accès à votre compte GitHub

### 3️⃣ Créer une Nouvelle App

1. Cliquez sur **"New app"**
2. Remplissez les informations :

   **Repository :**
   ```
   barous8585/WashAfrique
   ```

   **Branch :**
   ```
   main
   ```

   **Main file path :**
   ```
   app.py
   ```

   **App URL (optionnel) :**
   ```
   washafrique
   ```
   (L'URL sera : washafrique.streamlit.app)

3. Cliquez sur **"Deploy!"**

### 4️⃣ Attendre le Déploiement

- ⏳ Le déploiement prend **2-5 minutes**
- Vous verrez les logs d'installation en temps réel
- Attendez le message : **"Your app is live!"**

### 5️⃣ Tester l'Application

Une fois déployée, l'URL sera :
👉 **https://washafrique.streamlit.app** (ou votre URL personnalisée)

**Connexion :**
- Username : `admin`
- Password : `admin123`

---

## ⚙️ CONFIGURATION AVANCÉE (Optionnel)

### Variables d'Environnement

Si vous voulez configurer des secrets (API keys, etc.) :

1. Dans Streamlit Cloud, allez dans **App settings** (⚙️)
2. Cliquez sur **"Secrets"**
3. Ajoutez vos variables :

```toml
# Exemple
DB_NAME = "washafrique.db"
ENTREPRISE_NOM = "WashAfrique Pro"
ENTREPRISE_TEL = "+225 XX XX XX XX"
```

### Domaine Personnalisé

Pour utiliser votre propre domaine (ex: app.washafrique.com) :

1. Allez dans **App settings** → **General**
2. Section **"Custom domain"**
3. Suivez les instructions pour configurer votre DNS

---

## 🔄 MISES À JOUR AUTOMATIQUES

**Bonne nouvelle !** Chaque fois que vous faites un `git push` sur GitHub, Streamlit Cloud **redéploie automatiquement** votre application.

### Workflow :

```bash
# 1. Modifier votre code localement
nano app.py

# 2. Commit
git add .
git commit -m "Nouvelle fonctionnalité"

# 3. Push
git push origin main

# 4. Streamlit Cloud redéploie automatiquement (2-3 min)
```

---

## 🐛 DÉPANNAGE

### Erreur : "Requirements file not found"

**Solution :**
Vérifiez que `requirements.txt` est bien à la racine du projet.

```bash
ls requirements.txt
```

### Erreur : "Module not found"

**Solution :**
Ajoutez la dépendance manquante dans `requirements.txt` et push.

### Erreur : "Database locked"

**Solution :**
La base SQLite est créée automatiquement. Si problème persiste :

1. Allez dans App settings → **Reboot app**
2. Ou supprimez `washafrique.db` du repo (elle sera recréée)

### Erreur : "Memory exceeded"

**Solution :**
Streamlit Cloud gratuit a une limite de 1GB RAM.

Pour plus de ressources :
- Passez à Streamlit Cloud Teams (payant)
- Ou hébergez sur votre propre serveur

### Application Lente

**Solutions :**
- Activez le cache Streamlit (`@st.cache_data`)
- Optimisez les requêtes base de données
- Réduisez les graphiques lourds

---

## 📊 MONITORING

### Voir les Logs

1. Dans votre app Streamlit Cloud
2. Cliquez sur **"Manage app"** (en bas à droite)
3. Onglet **"Logs"**

Vous verrez tous les logs en temps réel.

### Voir les Métriques

- **Onglet "Analytics"** : Nombre de visiteurs, utilisation CPU/RAM
- **Onglet "Settings"** : Configuration app

---

## 🔒 SÉCURITÉ

### ⚠️ IMPORTANT : Changer le Mot de Passe Admin

Après le premier déploiement :

1. Connectez-vous à l'app
2. Allez dans **Paramètres** → **Utilisateurs**
3. Changez le mot de passe `admin123`

**Ou** modifiez directement dans `database.py` :

```python
# Ligne ~47
password_hash = hashlib.sha256("VOTRE_NOUVEAU_MOT_DE_PASSE".encode()).hexdigest()
```

### Protéger l'Accès

Pour restreindre l'accès uniquement à certaines personnes :

1. Utilisez l'authentification de l'app (déjà implémentée)
2. Ou configurez l'authentification Streamlit Cloud (Teams uniquement)

---

## 💰 COÛTS

### Plan Gratuit (Community)
- ✅ 1 app publique
- ✅ Redéploiement automatique
- ✅ 1 GB RAM / 1 CPU
- ✅ Suffisant pour commencer

### Plan Teams (Payant)
- ✅ Apps privées
- ✅ Plus de ressources (4GB RAM)
- ✅ Support prioritaire
- ✅ Domaine personnalisé
- 💰 **$250-500/mois**

**Recommandation :** Commencez avec le plan gratuit !

---

## 📱 PARTAGER VOTRE APP

Une fois déployée, partagez simplement l'URL :

```
https://washafrique.streamlit.app
```

**Marketing :**
- 📱 WhatsApp : "Testez notre app : [URL]"
- 📘 Facebook : Post avec lien
- 📧 Email : Newsletters aux prospects
- 🖨️ Flyers : QR Code vers l'app

---

## 🎯 CHECKLIST POST-DÉPLOIEMENT

- [ ] App déployée et accessible
- [ ] Connexion admin fonctionne
- [ ] Créer une réservation de test
- [ ] Tester sur mobile
- [ ] Changer le mot de passe admin
- [ ] Supprimer les données d'exemple (si production)
- [ ] Personnaliser les horaires
- [ ] Configurer infos entreprise
- [ ] Tester tous les modules
- [ ] Partager l'URL avec 5 personnes test

---

## 🆘 SUPPORT STREAMLIT

**Documentation officielle :**
- 📖 https://docs.streamlit.io/streamlit-community-cloud

**Community Forum :**
- 💬 https://discuss.streamlit.io/

**Support Email :**
- 📧 support@streamlit.io

---

## 🎉 FÉLICITATIONS !

Votre application **WashAfrique Pro** est maintenant **EN LIGNE** et accessible au monde entier ! 🌍

**URL Publique :**
👉 **https://washafrique.streamlit.app**

**Prochaines Étapes :**
1. ✅ Testez l'application en ligne
2. ✅ Partagez l'URL à vos prospects
3. ✅ Commencez la commercialisation
4. ✅ Collectez les feedbacks
5. ✅ Améliorez et mettez à jour (git push)

---

## 📞 BESOIN D'AIDE ?

Si vous rencontrez des problèmes de déploiement :

📧 Email : verdent@ai.com  
💬 Réponse sous 24h

---

<p align="center">
  <strong>🚀 BONNE COMMERCIALISATION ! 💰</strong><br>
  <em>Votre app est maintenant accessible 24/7 depuis n'importe où dans le monde</em>
</p>

---

**Mis à jour le** : 28 Janvier 2026  
**Version** : 3.0 Pro  
**Status** : ✅ Déployé sur GitHub, prêt pour Streamlit Cloud
