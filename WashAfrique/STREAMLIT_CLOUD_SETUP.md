# 🚀 Configuration Streamlit Cloud - WashAfrique

## 📱 Main File Paths (Chemins principaux)

### App Propriétaire/Admin
**Main file path:** `app.py`
- Interface complète pour le propriétaire
- Gestion des employés, services, clients
- Tableaux de bord, rapports, statistiques
- Pointage employés
- Photos avant/après

### Site Client (Réservations)
**Main file path:** `app_client.py`
- Interface publique pour les clients
- Réservation de services en ligne
- Visualisation des services disponibles
- Confirmation par email/SMS
- Synchronisé en temps réel avec l'app admin

---

## 🔐 Configuration Secrets PostgreSQL

Pour **chaque application** sur Streamlit Cloud, configurez les Secrets identiques :

### Étapes :
1. Allez sur https://share.streamlit.io
2. Ouvrez votre app
3. Cliquez sur **Settings** → **Secrets**
4. Copiez-collez exactement ceci :

```toml
[postgres]
host = "db.qstcskpamdnqssvcbana.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "Tobkesso.2006"
```

5. Cliquez sur **Save**
6. L'app redémarrera automatiquement (30-60 secondes)

---

## ✅ Vérifications après déploiement

### App Admin (`app.py`)
- [ ] Connexion avec username `admin` / password `admin123`
- [ ] Tableau de bord affiche CA
- [ ] Liste des services visible
- [ ] Création d'employés fonctionne

### Site Client (`app_client.py`)
- [ ] Page d'accueil s'affiche
- [ ] Services créés par admin sont visibles
- [ ] Bouton "Réserver" fonctionne
- [ ] Formulaire de réservation s'ouvre

### Synchronisation
- [ ] Service créé sur admin apparaît instantanément sur site client
- [ ] Réservation faite sur site client apparaît dans admin

---

## 🐛 Résolution des problèmes courants

### Erreur "Configuration base de données manquante"
➡️ **Solution :** Les Secrets ne sont pas configurés
1. Settings → Secrets
2. Vérifiez le format `[postgres]` (entre crochets)
3. Pas d'espaces avant `[postgres]`
4. Utilisez `=` (pas `:`)

### Erreur "Timeout connexion à Supabase"
➡️ **Solution :** Problème réseau ou host incorrect
1. Vérifiez l'orthographe du host dans Secrets
2. Assurez-vous que Supabase est actif
3. Testez depuis : https://supabase.com/dashboard

### Erreur "Authentification échouée"
➡️ **Solution :** Mot de passe incorrect
1. Vérifiez le password dans Secrets
2. Pas de guillemets dans le mot de passe
3. Password actuel : `Tobkesso.2006`

### Page blanche après connexion
➡️ **Solution :** Problème de session Streamlit
1. Videz le cache : Menu ⋮ → Clear cache
2. Rechargez la page (F5)
3. Reconnectez-vous

---

## 📊 URLs de déploiement

| Application | URL | Main Path |
|------------|-----|-----------|
| **App Propriétaire** | https://wahafrique-xxx.streamlit.app | `app.py` |
| **Site Client** | https://wahafrique-client-xxx.streamlit.app | `app_client.py` |

*(Remplacez `xxx` par votre identifiant unique Streamlit)*

---

## 🎯 Fonctionnalités disponibles

### App Propriétaire (`app.py`)
✅ Tableau de bord avec KPIs  
✅ Gestion services (créer, modifier, supprimer)  
✅ Gestion employés (ajouter, désactiver)  
✅ Pointage employés (arrivée/départ + retards)  
✅ Photos avant/après pour TikTok/Instagram  
✅ Rapports & Exports (PDF, CSV)  
✅ Statistiques période personnalisée  
✅ Gestion réservations web  

### Site Client (`app_client.py`)
✅ Catalogue services en temps réel  
✅ Réservation en ligne  
✅ Choix date & heure  
✅ Informations véhicule  
✅ Confirmation instantanée  
✅ Synchronisation admin ↔ client  

---

## 📝 Notes importantes

1. **Une seule base PostgreSQL** : Les deux apps partagent la même base Supabase
2. **Synchronisation automatique** : Modifications visibles instantanément
3. **Secrets identiques** : Les deux apps doivent avoir les mêmes Secrets
4. **Thème light forcé** : Pour meilleure lisibilité sur mobile
5. **Limite Supabase gratuit** : 500 MB de stockage (largement suffisant)

---

## 🔄 Mise à jour du code

Après modification locale :

```bash
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
git add .
git commit -m "Description des modifications"
git push origin main
```

Streamlit Cloud détecte automatiquement les changements et redémarre les apps (1-2 minutes).

---

## 📞 Support

En cas de problème :
1. Consultez les logs : **Manage app** → **Logs**
2. Vérifiez les Secrets sont corrects
3. Testez la connexion Supabase : https://supabase.com/dashboard
4. Comparez avec les captures d'écran de ce guide

---

**Dernière mise à jour :** 2026-02-04  
**Version PostgreSQL :** psycopg2-binary 2.9.0  
**Version Streamlit :** 1.28.0+
