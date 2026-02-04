# 🎯 COMPTES DÉMO - WashAfrique

## 🌐 URLs des Applications (Local)

| Application | URL | Description |
|------------|-----|-------------|
| **App Propriétaire/Admin** | http://localhost:8503 | Interface complète de gestion |
| **Site Client** | http://localhost:8502 | Interface de réservation publique |

---

## 🔐 COMPTES DE TEST

### 👤 Compte Propriétaire/Admin

**Username :** `admin`  
**Password :** `admin123`

**Accès :**
- ✅ Tableau de bord complet
- ✅ Gestion des services (créer, modifier, supprimer)
- ✅ Gestion des employés
- ✅ Gestion des clients
- ✅ Photos avant/après
- ✅ Pointage des employés
- ✅ Rapports et statistiques
- ✅ Paramètres du site client
- ✅ Export PDF/CSV
- ✅ Historique complet

---

### 👨‍💼 Compte Employé (Exemple)

**Username :** `employe1`  
**Password :** `employe123`

**Accès :**
- ✅ Pointage arrivée/départ
- ✅ Liste des services en attente
- ✅ Lancer un service client
- ✅ Prendre photos avant/après
- ✅ Valider service terminé
- ❌ Pas d'accès aux statistiques
- ❌ Pas d'accès à la gestion

**Note :** Pour créer d'autres employés, connectez-vous avec le compte admin → Gestion Employés → Ajouter Employé

---

## 🧪 SCÉNARIOS DE TEST

### Test 1 : Créer un service (Admin)
1. Connectez-vous sur http://localhost:8503 avec `admin` / `admin123`
2. Allez dans **Gestion Services**
3. Cliquez **➕ Ajouter un service**
4. Remplissez :
   - Nom : `Test Lavage VIP`
   - Prix : `50000`
   - Durée : `60`
   - Description : `Service test`
5. Validez
6. **Vérification** : Le service apparaît immédiatement sur http://localhost:8502

---

### Test 2 : Réservation client → Admin
1. Ouvrez http://localhost:8502 (Site Client)
2. Cliquez sur un service disponible
3. Cliquez **Réserver**
4. Remplissez le formulaire :
   - Nom : `Test Client`
   - Téléphone : `628123456`
   - Véhicule : `Toyota Corolla`
   - Immatriculation : `DK-1234-AB`
   - Date : Aujourd'hui
   - Heure : 14:00
5. Validez la réservation
6. **Vérification** : 
   - Ouvrez http://localhost:8503 avec compte admin
   - Allez dans **Services** ou **Gestion Clients**
   - La réservation apparaît instantanément

---

### Test 3 : Pointage employé
1. Connectez-vous avec `employe1` / `employe123` sur http://localhost:8503
2. Cliquez **☀️ Pointer Arrivée**
3. **Vérification** :
   - Message de confirmation
   - Bouton devient **🌙 Pointer Départ**
4. Reconnectez-vous avec `admin` / `admin123`
5. Allez dans **Rapports** → **Pointages**
6. **Vérification** : Le pointage apparaît avec :
   - Nom employé
   - Heure d'arrivée
   - Statut (À l'heure / En retard)

---

### Test 4 : Service complet avec photos
1. Connectez-vous avec `employe1` sur http://localhost:8503
2. Allez dans **Services**
3. Trouvez un service en attente
4. Cliquez **▶️ Lancer**
5. Cliquez **📷 Prendre Photos Avant**
6. Prenez 2-3 photos (ou uploadez)
7. Cliquez **✅ Terminer les photos avant**
8. Une fois le service fait, cliquez **📷 Prendre Photos Après**
9. Prenez 2-3 photos
10. Cliquez **✅ Valider Service Terminé**
11. **Vérification Admin** :
    - Reconnectez-vous avec `admin`
    - Tableau de bord : CA augmente
    - Historique : Service apparaît comme "Terminé"
    - Photos avant/après visibles

---

### Test 5 : Synchronisation Admin ↔ Client
1. **Fenêtre 1** : http://localhost:8503 (connecté admin)
2. **Fenêtre 2** : http://localhost:8502 (site client)
3. Sur admin : Créez un nouveau service "Test Sync"
4. **Sans recharger**, allez sur le site client
5. Rechargez la page du site client (F5)
6. **Vérification** : Le service "Test Sync" apparaît immédiatement

**C'est la preuve que les 2 apps partagent la même base PostgreSQL !** ✅

---

### Test 6 : Modifier prix (Admin) → Client
1. Admin : Modifiez le prix d'un service (ex: 15000 → 20000)
2. Sauvegardez
3. Site Client : Rechargez (F5)
4. **Vérification** : Le nouveau prix s'affiche

---

### Test 7 : Supprimer service (Admin) → Client
1. Admin : Supprimez un service
2. Confirmez
3. Site Client : Rechargez (F5)
4. **Vérification** : Le service n'apparaît plus

---

## 📊 DONNÉES DÉMO DISPONIBLES

### Services (9 disponibles)
- Lavage Extérieur Express (10000 FCFA, 15 min)
- Lavage Standard Complet (15000 FCFA, 30 min)
- Lavage Premium (25000 FCFA, 45 min)
- Nettoyage Intérieur Complet (20000 FCFA, 40 min)
- Lavage + Aspirateur (18000 FCFA, 35 min)
- Polish et Lustrage (30000 FCFA, 60 min)
- Traitement Cuir (15000 FCFA, 30 min)
- Désinfection Complète (12000 FCFA, 20 min)
- Lavage Moteur (18000 FCFA, 25 min)

### Clients (18 enregistrés)
- Divers clients avec différents véhicules
- Historique de services
- Coordonnées complètes

### Employés
- 1 admin (username: `admin`)
- Possibilité de créer plusieurs employés via interface admin

---

## 🎯 CHECKLIST FONCTIONNALITÉS À TESTER

### Interface Admin
- [ ] Connexion / Déconnexion
- [ ] Tableau de bord (KPIs)
- [ ] Créer / Modifier / Supprimer service
- [ ] Ajouter / Désactiver employé
- [ ] Voir liste clients
- [ ] Consulter historique services
- [ ] Voir pointages employés
- [ ] Exporter rapports PDF
- [ ] Paramètres site client
- [ ] Changer nom entreprise
- [ ] Définir horaires ouverture

### Interface Employé
- [ ] Connexion
- [ ] Pointer arrivée
- [ ] Voir services en attente
- [ ] Lancer un service
- [ ] Prendre photos avant (caméra + upload)
- [ ] Prendre photos après
- [ ] Supprimer une photo mal prise
- [ ] Valider service terminé
- [ ] Pointer départ

### Site Client
- [ ] Voir liste des services
- [ ] Voir détails d'un service
- [ ] Formulaire de réservation
- [ ] Choisir date/heure
- [ ] Confirmation réservation
- [ ] Voir horaires d'ouverture
- [ ] Interface responsive (mobile)

### Synchronisation
- [ ] Service créé admin → visible client
- [ ] Prix modifié admin → mis à jour client
- [ ] Service supprimé admin → disparu client
- [ ] Réservation client → visible admin
- [ ] CA mis à jour après service terminé

---

## 🐛 En cas de problème

### App ne se charge pas
```bash
# Redémarrer les apps
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
pkill -f streamlit
streamlit run app.py --server.port 8503 &
streamlit run app_client.py --server.port 8502 &
```

### Erreur de connexion base de données
```bash
# Tester la connexion
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
python3 -c "from database import Database; db = Database(); print('✅ OK')"
```

### Reset base de données démo
```bash
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
python3 init_demo_site_client.py
```

---

## 📱 URLS STREAMLIT CLOUD (Une fois déployé)

| Application | URL | Main Path | Secrets |
|-------------|-----|-----------|---------|
| **Admin** | https://wahafrique-admin.streamlit.app | `app.py` | [postgres] |
| **Client** | https://wahafrique-client.streamlit.app | `app_client.py` | [postgres] |

**Note :** Les URLs exactes dépendront de votre configuration Streamlit Cloud.

---

**Dernière mise à jour :** 2026-02-04 12:15  
**Base de données :** PostgreSQL Supabase (12 tables)  
**Données démo :** 9 services, 18 clients, 1 admin
