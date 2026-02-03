# 🧪 GUIDE DE TEST DÉMO COMPLET - WashAfrique Pro

**Date:** 02 Février 2026  
**Version:** 3.0 Enterprise  
**Durée estimée:** 20 minutes

---

## 📋 PRÉPARATION

### Étape 1 : Créer les données de démonstration

```bash
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
python3 demo_data.py
```

**Résultat attendu:**
- ✅ 10 clients créés
- ✅ 5+ services disponibles
- ✅ 20 réservations sur 7 jours
- ✅ CA Total: 80 000 - 150 000 FCFA
- ✅ Pointages employés (5 derniers jours)

### Étape 2 : Lancer l'application

```bash
streamlit run app.py
```

**URL:** http://localhost:8503

---

## 🔐 PARTIE 1 : TEST COMPTE PROPRIÉTAIRE (admin)

### Connexion
- **Username:** `admin`
- **Password:** `admin123`

---

### 🏠 ONGLET 1 : Tableau de Bord

**Tests à effectuer:**

✅ **KPIs Affichés:**
- [ ] CA Jour (devrait afficher montant > 0)
- [ ] CA Total (80 000 - 150 000 FCFA)
- [ ] Nombre RDV Aujourd'hui
- [ ] Nombre Total Clients (10+)

✅ **Graphique Évolution CA:**
- [ ] Line chart visible avec données 7 derniers jours
- [ ] Courbe avec variations

✅ **Services Populaires:**
- [ ] Camembert (pie chart) visible
- [ ] Top 3-5 services affichés

✅ **Pointages du Jour:**
- [ ] Liste employés présents
- [ ] Heures arrivée/départ affichées

**Note:** Si CA Jour = 0, c'est normal (pas de paiement aujourd'hui). Vérifier CA Total.

---

### 👥 ONGLET 2 : Employés

#### Sous-onglet : Liste Employés

✅ **Tests:**
- [ ] Au moins 1 employé affiché (Abdoul par défaut)
- [ ] Informations complètes (Nom, Tel, Poste, Salaire)
- [ ] Boutons "✏️ Modifier" et "🗑️ Supprimer" présents

✅ **Test Modification:**
1. Cliquer "✏️ Modifier" sur un employé
2. Changer le téléphone
3. Sauvegarder
4. ✅ Vérifier changement appliqué

✅ **Test Suppression:**
1. Créer un employé test: "Test Demo" / "test" / "test123"
2. Cliquer "🗑️ Supprimer"
3. ✅ Vérifier disparition immédiate

#### Sous-onglet : Ajouter Employé

✅ **Test Création:**
1. Nom: "Jean Dupont"
2. Téléphone: "+225 07 99 88 77"
3. Poste: "Laveur"
4. Salaire: 150000
5. Username: "jean"
6. Password: "jean123"
7. Cliquer "Créer Employé"
8. ✅ Message succès + employé dans liste

#### Sous-onglet : Pointages

✅ **Tests:**
- [ ] Sélectionner date (aujourd'hui ou jour avec pointages)
- [ ] **Cartes visuelles par employé** (fond coloré)
- [ ] **3 colonnes:** Arrivées | Départs | Durée
- [ ] Statut visible: 🟢 PRÉSENT ou 🔴 PARTI
- [ ] Durée calculée affichée (ex: 8h30min)

---

### 🔧 ONGLET 3 : Services & Prix

#### Sous-onglet : Mes Services

✅ **Tests:**
- [ ] Au moins 5 services affichés
- [ ] Infos: Nom, Prix, Durée, Points, Description
- [ ] Boutons "✏️ Modifier" et "🗑️ Supprimer"

✅ **Test Modification:**
1. Modifier le prix d'un service
2. Sauvegarder
3. ✅ Vérifier prix mis à jour

✅ **Test Suppression:**
1. Créer service test
2. Supprimer
3. ✅ Disparaît immédiatement

#### Sous-onglet : Nouveau Service

✅ **Test Création Service:**
1. Nom: "Lavage VIP"
2. Prix: 25000
3. Durée: 90 min
4. Points: 100
5. Description: "Service ultra premium"
6. Cliquer "Créer"
7. ✅ Service créé et visible dans liste

---

### 📅 ONGLET 4 : Réservations

#### Sous-onglet : Planning

✅ **Tests:**
- [ ] Sélectionner date avec réservations
- [ ] Liste services affichée avec badges colorés:
  - 🔵 EN ATTENTE
  - 🟡 EN COURS
  - 🟢 TERMINÉ
  - 💰 PAYÉ
  - ✅ VALIDÉ
- [ ] Infos: Client, Service, Heure, Montant

#### Sous-onglet : À Valider

✅ **Tests:**
- [ ] Liste services avec statut 💰 PAYÉ
- [ ] Bouton "✅ Valider" visible
- [ ] Cliquer Valider
- [ ] ✅ Statut passe à ✅ VALIDÉ
- [ ] Service disparaît de l'onglet "À Valider"

---

### 💼 ONGLET 5 : Clients

✅ **Tests:**
- [ ] 10 clients minimum affichés
- [ ] Infos: Nom, Tel, Véhicule, Points, Total dépenses
- [ ] Système fidélité visible (⭐ points)
- [ ] Historique achats accessible

✅ **Test Recherche Client:**
1. Taper "Mamadou" dans recherche
2. ✅ Clients correspondants filtrés

---

### 💰 ONGLET 6 : Paiements

#### Sous-onglet : Historique

✅ **Tests:**
- [ ] Liste 20 derniers paiements
- [ ] Infos: Client, Service, Montant, Date, Heure, Méthode
- [ ] Emojis méthodes: 💵 Espèces / 💳 Carte / 📱 Mobile
- [ ] Total affiché en haut

#### Sous-onglet : Statistiques

✅ **Tests KPIs:**
- [ ] Total Encaissé affiché
- [ ] Nombre Paiements
- [ ] Montant Moyen calculé

✅ **Répartition Méthodes:**
- [ ] Liste méthodes avec compteurs
- [ ] Montants par méthode
- [ ] Pourcentages affichés

#### Sous-onglet : Recherche

✅ **Tests:**
1. Rechercher client: "Fatou"
2. ✅ Paiements filtrés
3. Filtrer par méthode: "Espèces"
4. ✅ Résultats filtrés
5. Total filtré affiché

---

### 📦 ONGLET 7 : Stock

✅ **Tests:**
- [ ] Message placeholder affiché
- [ ] Liste fonctionnalités prévues visible
- [ ] Note claire pour l'utilisateur

---

### 📊 ONGLET 8 : Rapports

#### Sous-onglet : Statistiques Générales

✅ **Sélection Période:**
1. Date début: 7 jours avant
2. Date fin: Aujourd'hui
3. ✅ KPIs mis à jour

✅ **KPIs Période:**
- [ ] CA Total période
- [ ] Nombre services
- [ ] Clients uniques
- [ ] Taux validation

✅ **Graphique Évolution CA:**
- [ ] Line chart affiché
- [ ] Données période visible

✅ **Top 5 Services:**
- [ ] Classement affiché
- [ ] Compteurs corrects

✅ **Méthodes Paiement:**
- [ ] Répartition affichée
- [ ] Montants par méthode

#### Sous-onglet : Galerie Photos

✅ **Tests:**
- [ ] Message info qualité affiché
- [ ] Si photos existantes: affichées
- [ ] Boutons téléchargement/suppression

#### Sous-onglet : Exports

✅ **Test Export Paiements:**
1. Cliquer "📥 Export Paiements (CSV)"
2. Cliquer "💾 Télécharger"
3. ✅ Fichier `paiements_2026-02-02.csv` téléchargé
4. Ouvrir dans Excel/LibreOffice
5. ✅ Données correctes

✅ **Test Export Services:**
1. Cliquer "📥 Export Services (CSV)"
2. Télécharger
3. ✅ Fichier téléchargé et lisible

✅ **Test Export Clients:**
1. Cliquer "📥 Export Clients (CSV)"
2. Télécharger
3. ✅ 10 clients dans le fichier

✅ **Test Export Pointages:**
1. Cliquer "📥 Export Pointages (CSV)"
2. Télécharger
3. ✅ Pointages 30 derniers jours

✅ **Test Rapport Mensuel:**
1. Cliquer "📊 Générer Rapport Mensuel"
2. Prévisualiser
3. ✅ Rapport formaté ASCII
4. Télécharger `.txt`
5. ✅ Lisible dans éditeur texte

---

### ⚙️ ONGLET 9 : Mon Profil

#### Sous-onglet : Informations

✅ **Tests:**
- [ ] Nom admin affiché
- [ ] Possibilité modifier email
- [ ] Sauvegarder fonctionne

#### Sous-onglet : Entreprise

✅ **Test Modification:**
1. Changer nom entreprise: "Ma Super Station"
2. Ajouter description
3. Téléphone: "+225 27 XX XX XX"
4. Sauvegarder
5. ✅ Message confirmation
6. Recharger page
7. ✅ Header affiche "Ma Super Station"

#### Sous-onglet : Gestion Données

✅ **Test Réinitialisation CA:**
1. Noter CA actuel
2. Cliquer "🔄 Réinitialiser CA"
3. ✅ Message confirmation
4. Vérifier Tableau de Bord
5. ✅ CA remis à 0

⚠️ **Ne pas tester "TOUT Réinitialiser"** sauf si vous voulez tout effacer !

---

## 👨‍💼 PARTIE 2 : TEST COMPTE EMPLOYÉ

### Se déconnecter et reconnecter

- **Username:** `abdoul` (ou employé créé)
- **Password:** `abdoul123`

---

### 🏠 ONGLET 1 : Mon Espace

✅ **Tests:**
- [ ] Date du jour affichée
- [ ] Si pointé: Heures affichées
- [ ] Heures travaillées calculées

---

### ⏰ ONGLET 2 : Pointage

✅ **Test Arrivée:**
1. Cliquer "⏰ Pointer Arrivée"
2. ✅ Message succès
3. ✅ Heure d'arrivée affichée

✅ **Attendre 1 minute**

✅ **Test Départ:**
1. Cliquer "🏁 Pointer Départ"
2. ✅ Message succès
3. ✅ Heure de départ affichée
4. ✅ Durée calculée (1-2 min)

✅ **Historique:**
- [ ] Pointages du mois affichés
- [ ] Tableau avec Date | Arrivée | Départ | Heures

---

### 🚗 ONGLET 3 : Lancer un Service

✅ **Test Recherche Client Existant:**
1. Taper "Mamadou" dans recherche
2. ✅ Client Mamadou Traoré apparaît
3. Cliquer bouton "✅"
4. ✅ Client sélectionné (encadré vert)
5. Infos pré-remplies

✅ **Test Création Service Rapide:**
1. Sélectionner service: "Lavage Standard"
2. Poste de lavage: Premier disponible
3. Cliquer "✅ Démarrer le Service"
4. ✅ Message succès avec balloons 🎈
5. ✅ Récapitulatif affiché

✅ **Test Nouveau Client:**
1. Cocher "➕ Nouveau client"
2. Nom: "Client Test"
3. Téléphone: "+225 07 88 77 66"
4. Véhicule: "Test Car"
5. Sélectionner service
6. Démarrer
7. ✅ Client créé + service lancé

---

### 📸 ONGLET 4 : Mes Services en Cours

✅ **Test Workflow Photos:**

**Étape 1: Démarrer**
1. Trouver le service créé
2. Cliquer "▶️ Démarrer"
3. ✅ Statut → 🟡 EN COURS

**Étape 2: Photos AVANT**
1. Mode: "📁 Upload"
2. Sélectionner 2-3 images test de votre galerie
3. ✅ Compteur: "📤 3 photo(s) sélectionnée(s)"
4. Cliquer "💾 Sauvegarder TOUTES les photos AVANT"
5. ✅ Message: "3 photo(s) AVANT ajoutée(s) !"
6. ✅ Miniatures affichées

**Étape 3: Photos APRÈS**
1. Même processus
2. Sélectionner 2-3 autres images
3. Sauvegarder
4. ✅ Photos APRÈS ajoutées

**Étape 4: Terminer**
1. Cliquer "✅ Terminer le Service"
2. ✅ Statut → 🟢 TERMINÉ

**Étape 5: Encaisser**
1. Sélectionner méthode: "Espèces"
2. Cliquer "💰 Encaisser"
3. ✅ Statut → 💰 PAYÉ
4. ✅ Paiement enregistré

---

### 👤 ONGLET 5 : Mon Profil

✅ **Tests:**
- [ ] Infos employé affichées
- [ ] Possibilité modifier téléphone
- [ ] Sauvegarder fonctionne

---

## ✅ CHECKLIST FINALE

### Fonctionnalités Principales

- [ ] Connexion admin/employé fonctionne
- [ ] Tableau de bord affiche CA réel
- [ ] Recherche rapide clients opérationnelle
- [ ] Création service en 5 secondes
- [ ] Upload photos multiples fonctionne
- [ ] Workflow complet service OK
- [ ] Pointages visuels clairs
- [ ] Statistiques affichées correctement
- [ ] Exports CSV fonctionnels
- [ ] Module Paiements complet

### Performance

- [ ] Application réactive (< 2s chargement page)
- [ ] Pas d'erreurs dans console
- [ ] Rechargements automatiques (`st.rerun()`) fluides

### UX/UI

- [ ] Interface claire et intuitive
- [ ] Couleurs et badges lisibles
- [ ] Messages de confirmation présents
- [ ] Navigation facile entre onglets

---

## 🎯 SCÉNARIOS MÉTIER COMPLETS

### Scénario 1 : Journée Type Propriétaire

**Matin (9h):**
1. Se connecter
2. Vérifier CA jour (Tableau de Bord)
3. Vérifier présence employés (Pointages)
4. Consulter réservations du jour

**Midi (12h):**
5. Valider services payés (À Valider)
6. Vérifier galerie photos pour réseaux sociaux

**Soir (18h):**
7. Consulter statistiques journée
8. Exporter rapport pour comptable

### Scénario 2 : Journée Type Employé

**Matin (8h):**
1. Se connecter
2. Pointer arrivée

**Toute la journée:**
3. Client arrive → Recherche rapide → Service démarré (30 sec)
4. Photos AVANT (caméra ou upload)
5. Lavage véhicule
6. Photos APRÈS
7. Terminer + Encaisser
8. Répéter pour chaque client

**Soir (18h):**
9. Pointer départ

---

## 📊 RÉSULTATS ATTENDUS

Après ce test complet, vous devriez avoir:

✅ **Base de données enrichie:**
- 10-15 clients
- 20+ réservations
- 15+ paiements
- CA Total: 100 000 - 200 000 FCFA
- 10+ pointages

✅ **Fichiers exportés:**
- `paiements_2026-02-02.csv`
- `services_2026-02-02.csv`
- `clients_2026-02-02.csv`
- `pointages_2026-02-02.csv`
- `rapport_mensuel_2026_02.txt`

✅ **Fonctionnalités validées:**
- Tous les modules opérationnels
- Workflow complet testé
- Performance satisfaisante

---

## 🐛 PROBLÈMES CONNUS (Non bloquants)

⚠️ **Warnings Streamlit:**
```
Please replace `use_container_width` with `width`
```
→ **Impact:** Aucun, juste dépréciation future

⚠️ **Base SQLite:**
- Limite pratique: ~10 000 enregistrements
- Pour production intensive: migrer vers PostgreSQL

---

## 📞 SUPPORT

**Questions/Problèmes:**
- Vérifier `washafrique.db` existe
- Relancer: `streamlit run app.py`
- Vérifier logs terminal

**Réinitialisation complète:**
```bash
rm washafrique.db
python3 app.py  # Recrée la base
python3 demo_data.py  # Recrée les données
```

---

**Bon test ! 🚀**
