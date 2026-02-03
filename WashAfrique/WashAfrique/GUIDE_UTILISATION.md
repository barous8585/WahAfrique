# 📚 Guide d'Utilisation - WashAfrique Pro v3.0

## 🚀 Démarrage Rapide

### Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

### Première Connexion

**Identifiants par défaut :**
- Username : `admin`
- Password : `admin123`

⚠️ **IMPORTANT** : Changez le mot de passe après la première connexion !

---

## 📖 Guide des Fonctionnalités

### 🏠 Tableau de Bord

**Vue d'ensemble de votre activité :**
- Statistiques en temps réel (RDV du jour, revenus, clients)
- Alertes stock automatiques
- Graphiques de performance (30 derniers jours)
- Top services populaires
- Prochains rendez-vous avec statuts

### ➕ Nouvelle Réservation

**Créer une réservation en 3 étapes :**

1. **Informations Client**
   - Recherche automatique par téléphone
   - Création automatique si nouveau client
   - Affichage des points fidélité

2. **Détails du Service**
   - Sélection date/heure avec disponibilité en temps réel
   - Choix du poste de lavage
   - Affectation employé (optionnel)
   - Durée calculée automatiquement

3. **Promotions & Paiement**
   - Application code promo
   - Utilisation points fidélité
   - Calcul automatique du prix final
   - Génération facture PDF avec QR code

**💡 Astuce :** La gestion multi-postes permet de bloquer uniquement les créneaux nécessaires selon la durée du service.

### 📅 Planning

**Visualisation et gestion des réservations :**

- Vue calendrier avec créneaux colorés (libre/occupé/pause)
- Filtrage par poste de lavage
- Actions rapides : Confirmer / Terminer / Annuler
- Gestion automatique des points fidélité à la fin du service

**Statuts disponibles :**
- 🟡 **En attente** : Réservation créée
- 🟢 **Confirmé** : Client a confirmé
- 🔵 **Payé** : Paiement effectué
- ✅ **Terminé** : Service complété (points ajoutés)
- 🔴 **Annulé** : Réservation annulée

### 👥 Clients

**Base de données clients complète :**

- Recherche rapide par nom/téléphone
- Historique détaillé des réservations
- Suivi des dépenses totales
- Points fidélité accumulés
- Récompenses disponibles

**Programme Fidélité Automatique :**
- Points gagnés selon le service
- Utilisation des points lors d'une réservation
- 4 paliers de récompenses (Bronze, Silver, Gold, Platinum)

### 🔧 Services

**Gestion du catalogue :**

- Création illimitée de services personnalisés
- Prix, durée, points fidélité configurables
- Descriptions détaillées
- Activation/désactivation sans suppression

**💡 Conseil :** Créez des packages (Ex: Lavage + Polissage) pour maximiser les revenus.

### 👨‍💼 Employés

**Gestion du personnel :**

- Ajout employés avec coordonnées
- Définition des postes et salaires
- Affectation aux réservations
- Suivi des performances (à venir)

### 💰 Paiements

**Système de paiement complet :**

- Vue des réservations non payées
- Paiements partiels acceptés
- Méthodes : Espèces, Mobile Money, Carte, Virement
- Historique des transactions
- Mise à jour automatique des statuts

### 🎁 Promotions

**Codes promo avancés :**

**Types de réductions :**
- Pourcentage (Ex: 20% OFF)
- Montant fixe (Ex: 5000 FCFA OFF)

**Configuration :**
- Dates de validité (début/fin)
- Limite d'utilisations
- Codes illimités possibles

**Exemples :**
```
SUMMER2024 : 15% de réduction
NOUVEAU500 : 5000 FCFA pour nouveaux clients
VIP : 25% sans limite
```

### ⭐ Fidélité

**Programme automatisé :**

**Classement TOP 10 :**
- Meilleurs clients par points
- Total dépensé par client

**Récompenses par défaut :**
- Bronze (10 pts) : 5% OFF
- Silver (25 pts) : 10% OFF
- Gold (50 pts) : 15% OFF
- Platinum (100 pts) : 20% OFF

**💡 Personnalisable :** Créez vos propres paliers dans la base de données.

### 📦 Stock

**Gestion des produits :**

- Inventaire en temps réel
- Alertes automatiques (stock bas)
- Mouvements d'entrée/sortie
- Calcul des coûts
- Valorisation du stock

**Produits recommandés :**
- Shampooing auto
- Cire de protection
- Nettoyant intérieur
- Chiffons microfibres
- Produits vitres

### 📊 Statistiques

**Analyse de performance :**

**KPIs :**
- Chiffre d'affaires (total, journalier)
- Nombre de réservations
- Nombre de clients

**Graphiques :**
- Évolution CA sur 60 jours
- Répartition des services (pie chart)
- Heures de pointe (à venir)

**Export :**
- Données brutes pour Excel
- Rapports PDF (à venir)

### ⚙️ Paramètres

**Configuration :**

1. **Entreprise**
   - Horaires d'ouverture/fermeture
   - Gestion des postes de lavage
   - Informations légales

2. **Sauvegarde**
   - Export JSON automatique
   - Backup base SQLite
   - Import/export données

3. **Utilisateurs**
   - Gestion des accès
   - Rôles et permissions

---

## 🌍 Multilingue

**3 langues disponibles :**
- 🇫🇷 Français
- 🇬🇧 English
- 🇸🇦 العربية (Arabe)

Changement instantané via les boutons en haut de la sidebar.

---

## 🔒 Sécurité

**Protection des données :**

✅ Authentification obligatoire  
✅ Mots de passe hashés (SHA-256)  
✅ Session sécurisée  
✅ Données clients protégées  
✅ Backup automatique  

**Recommandations :**
1. Changez le mot de passe admin immédiatement
2. Effectuez des sauvegardes régulières
3. Limitez l'accès au fichier `.db`
4. Utilisez HTTPS en production

---

## 📱 Responsive Design

L'application s'adapte automatiquement :
- 💻 Desktop
- 📱 Tablette
- 📱 Mobile

Testé sur :
- Chrome, Firefox, Safari
- iOS et Android

---

## 🆘 Support & Assistance

**Problèmes courants :**

### "Base de données verrouillée"
```bash
# Fermer toutes les instances Streamlit
# Relancer l'application
streamlit run app.py
```

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Erreur de connexion"
Vérifiez que le fichier `washafrique.db` est bien créé dans le même dossier.

---

## 🚀 Améliorations Futures

**Roadmap v4.0 :**

- [ ] Notifications SMS automatiques
- [ ] Intégration Mobile Money API
- [ ] Application mobile native
- [ ] Système de réservation en ligne (client)
- [ ] Rapport PDF automatique
- [ ] Gestion multi-sites
- [ ] Intégration WhatsApp Business
- [ ] Scanner QR code pour check-in
- [ ] Système de notation/avis clients
- [ ] Programme de parrainage

---

## 📞 Contact

**Support Technique :**  
📧 Email : support@washafrique.com  
📱 WhatsApp : +225 XX XX XX XX  

**Développeur :**  
🧑‍💻 Verdent AI Assistant  
🌐 Version : 3.0 Pro  
📅 Date : 2026  

---

## 📄 Licence

© 2026 WashAfrique Pro - Tous droits réservés

**Utilisation Commerciale Autorisée**

---

## 🙏 Remerciements

Merci d'avoir choisi **WashAfrique Pro** pour gérer votre entreprise de lavage automobile !

💪 **Bonne commercialisation !** 🚀
