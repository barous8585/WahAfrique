# 🐘 Guide Migration PostgreSQL (Supabase)

## 📋 Vue d'ensemble

Ce guide vous aide à migrer votre application WashAfrique de SQLite vers PostgreSQL (Supabase) pour synchroniser vos apps admin et client sur Streamlit Cloud.

---

## 🎯 Étape 1 : Créer Compte Supabase

### 1.1 Inscription

1. Allez sur : **https://supabase.com**
2. Cliquez **"Start your project"**
3. Connectez-vous avec **GitHub** (compte `barous8585`)

### 1.2 Créer un Projet

1. Cliquez **"New Project"**
2. Remplissez :
   - **Name** : `washafrique`
   - **Database Password** : Choisissez un mot de passe fort (ex: `WashAfr1que!2026`)
     - ⚠️ **NOTEZ CE MOT DE PASSE** - Vous en aurez besoin !
   - **Region** : `Frankfurt` (plus proche de l'Afrique)
   - **Pricing Plan** : Free (gratuit)

3. Cliquez **"Create new project"**
4. **Attendez 2-3 minutes** (création de la base de données)

### 1.3 Récupérer les Credentials

Une fois le projet créé :

1. Dans le menu gauche, cliquez **Settings** (⚙️)
2. Cliquez **Database**
3. Descendez jusqu'à **Connection string**
4. Copiez les informations :

```
Host: db.xxxxxxxxxxxxxxxxxxxxx.supabase.co
Database name: postgres
Port: 5432
User: postgres
Password: [le mot de passe que vous avez choisi]
```

**⚠️ GARDEZ CES INFORMATIONS PRÉCIEUSEMENT**

---

## 🔧 Étape 2 : Configuration Locale

### 2.1 Installer psycopg2

```bash
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
pip3 install psycopg2-binary
```

### 2.2 Configurer les Credentials

1. Ouvrez le fichier `db_config.py`
2. Remplacez les valeurs par vos credentials Supabase :

```python
DB_CONFIG = {
    "host": "db.xxxxxxxxxxxxxxxxxxxxx.supabase.co",  # Votre host
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "WashAfr1que!2026"  # Votre mot de passe
}
```

3. **Sauvegardez** le fichier

⚠️ **NE COMMITEZ PAS** ce fichier sur GitHub (déjà dans .gitignore)

---

## 🚀 Étape 3 : Migration des Données

### 3.1 Script de Migration

Je vais créer un script qui :
- Lit toutes vos données SQLite actuelles
- Les transfère vers PostgreSQL Supabase

**Attendez que je finalise le script...**

### 3.2 Exécuter la Migration

```bash
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
python3 migrate_to_postgres.py
```

Le script affichera :
- ✅ Services migrés : X
- ✅ Clients migrés : Y
- ✅ Réservations migrées : Z
- etc.

---

## ☁️ Étape 4 : Configuration Streamlit Cloud

### 4.1 Ajouter les Secrets

Pour chaque app (Admin + Client) sur Streamlit Cloud :

1. Ouvrez l'app sur https://share.streamlit.io
2. Cliquez **⋮ → Settings**
3. Cliquez **Secrets**
4. Ajoutez :

```toml
[postgres]
host = "db.xxxxxxxxxxxxxxxxxxxxx.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "WashAfr1que!2026"
```

5. Cliquez **Save**

### 4.2 Redémarrer les Apps

1. Cliquez **⋮ → Reboot app**
2. Attendez 2-3 minutes
3. Les apps se reconnectent à PostgreSQL automatiquement

---

## ✅ Étape 5 : Vérification

### 5.1 Test App Admin

1. Connectez-vous : `admin` / `admin123`
2. Allez dans **Services & Prix**
3. Ajoutez un nouveau service test
4. Notez son nom

### 5.2 Test App Client

1. Ouvrez le **site client**
2. Onglet **Services**
3. **Le service que vous venez de créer devrait apparaître !** ✅

### 5.3 Test Réservation

1. Sur le **site client** : Faites une réservation
2. Sur l'**app admin** : Onglet **🌐 Site Client** → **Réservations Web**
3. **La réservation devrait apparaître !** ✅

---

## 🎉 Résultat Final

```
┌─────────────────────────────────────────────────┐
│           AVANT (SQLite)                        │
├─────────────────────────────────────────────────┤
│  App Admin → washafrique.db (local)             │
│  App Client → washafrique.db (local, différent) │
│  ❌ PAS DE SYNCHRONISATION                      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│          APRÈS (PostgreSQL)                     │
├─────────────────────────────────────────────────┤
│  App Admin ──┐                                  │
│             ├──→ PostgreSQL Supabase (cloud)    │
│  App Client ─┘                                  │
│  ✅ SYNCHRONISATION EN TEMPS RÉEL               │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Dépannage

### Erreur : "OperationalError: FATAL: password authentication failed"

✅ **Solution** : Vérifiez le mot de passe dans `db_config.py` ou les Secrets Streamlit

### Erreur : "relation 'services' does not exist"

✅ **Solution** : Les tables ne sont pas créées. Redémarrez l'app, `init_database()` les créera automatiquement.

### App admin et client toujours désynchronisés

✅ **Solution** : 
1. Vérifiez que les **deux apps** utilisent bien les mêmes credentials Supabase (Settings → Secrets)
2. Redémarrez les deux apps
3. Testez en créant un service dans l'admin

---

## 📞 Support

Si vous rencontrez un problème :
1. Vérifiez les logs Streamlit (cliquez **⋮ → View logs**)
2. Cherchez les lignes rouges avec "Error"
3. Copiez-moi l'erreur complète

---

## 🔐 Sécurité

✅ **Bonnes pratiques** :
- ✅ Mot de passe fort (12+ caractères, majuscules, chiffres, symboles)
- ✅ Ne jamais commiter `db_config.py` sur GitHub
- ✅ Utiliser Streamlit Secrets pour le cloud
- ✅ Sauvegarder vos credentials dans un endroit sûr

---

## ⏭️ Prochaines Étapes

Une fois la migration terminée, dites-moi et je vous aiderai à :
1. Optimiser les performances PostgreSQL
2. Ajouter des backups automatiques
3. Configurer des alertes email pour les réservations

**🎯 Dites-moi quand vous avez créé votre compte Supabase et récupéré vos credentials !**
