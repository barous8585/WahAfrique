# 🌐 Guide du Site Client WashAfrique

## 📋 Vue d'ensemble

Le site client est une application web séparée qui permet à vos clients de :
- 📱 Consulter vos services et tarifs 24/7
- 📅 Réserver en ligne depuis leur téléphone
- 🔍 Suivre l'état de leur réservation
- ⭐ Laisser des avis après le service

Vous contrôlez **tout depuis votre espace admin** !

---

## 🚀 Démarrage Rapide

### 1. Lancer le Site Client (en local)

```bash
# Dans un terminal
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
streamlit run app_client.py --server.port 8502
```

**📱 URL locale** : http://localhost:8502

### 2. Lancer l'App Admin (en parallèle)

```bash
# Dans un autre terminal
cd /Users/thiernoousmanebarry/Desktop/WashAfrique/WashAfrique
streamlit run app.py --server.port 8501
```

**💼 URL admin** : http://localhost:8501

---

## ⚙️ Configuration (Espace Admin)

### Étape 1 : Activer le Site Client

1. Connectez-vous à l'app admin (`admin` / `admin123`)
2. Allez dans l'onglet **🌐 Site Client**
3. Sous-onglet **⚙️ Paramètres**
4. Cochez :
   - ✅ **Site client activé**
   - ✅ **Autoriser réservations en ligne**
5. Remplissez les informations :
   - Nom entreprise
   - Slogan
   - Téléphone / Email / Adresse
   - Couleur principale du site
6. Cliquez **💾 Enregistrer**

### Étape 2 : Configurer les Horaires

1. Sous-onglet **⏰ Horaires**
2. Pour chaque jour de la semaine :
   - Cochez **Ouvert** si disponible
   - Définissez **Heure début** et **Heure fin**
   - Choisissez **Intervalle** (ex: 30 min = créneaux toutes les 30 min)
   - Définissez **Capacité simultanée** (ex: 2 = 2 clients peuvent réserver en même temps)
3. Cliquez **💾 Enregistrer** pour chaque jour

### Étape 3 : Vérifier les Services

1. Allez dans l'onglet **🔧 Services & Prix**
2. Assurez-vous que vos services sont :
   - ✅ Activés (bouton vert)
   - 💰 Prix corrects
   - 📝 Descriptions claires
3. Ces services apparaîtront automatiquement sur le site client

---

## 📱 Workflow Client → Admin

### Scénario 1 : Réservation en Ligne

**Côté Client (app_client.py)** :
1. Client va sur http://localhost:8502
2. Onglet **📅 Réserver**
3. Remplit le formulaire :
   - Nom, téléphone, email
   - Service choisi
   - Date et heure
4. Clique **✅ Confirmer la Réservation**
5. Reçoit un **code de réservation** (ex: `ABC12345`)

**Côté Admin (app.py)** :
1. Propriétaire voit une notification dans l'onglet **🌐 Site Client**
2. Sous-onglet **📋 Réservations Web**
3. Liste les réservations en attente
4. Peut :
   - ✅ **Valider** → Passe à "confirmée"
   - ❌ **Annuler** → Passe à "annulée"

### Scénario 2 : Suivi de Réservation

**Côté Client** :
1. Client va dans l'onglet **🔍 Suivi Réservation**
2. Entre son code (`ABC12345`)
3. Voit le statut :
   - ⏳ **EN_ATTENTE** : Admin n'a pas encore validé
   - ✅ **CONFIRMEE** : RDV confirmé
   - ❌ **ANNULEE** : RDV annulé
   - 🏁 **TERMINEE** : Service effectué

### Scénario 3 : Avis Clients

**Côté Client** :
1. Après le service, client va dans l'onglet **⭐ Avis**
2. Laisse une note (1-5 étoiles) et un commentaire
3. L'avis est envoyé

**Côté Admin** :
1. Onglet **🌐 Site Client** → **⭐ Avis Clients**
2. Voit tous les avis
3. Peut **masquer** les avis inappropriés
4. Les avis visibles apparaissent sur la page d'accueil du site client

---

## 🌍 Déploiement en Ligne (Streamlit Cloud)

### Pour rendre le site accessible partout :

1. **Créer un compte Streamlit Cloud** : https://streamlit.io/cloud
2. **Connecter votre repo GitHub** `WashAfrique`
3. **Créer 2 apps** :
   - **App 1 (Admin)** : `app.py` → URL privée pour vous
   - **App 2 (Client)** : `app_client.py` → URL publique pour vos clients
4. **Partager l'URL client** avec vos clients (ex: `https://washafrique.streamlit.app`)

### Avantages :
- ✅ Accessible 24/7 depuis n'importe quel téléphone
- ✅ Pas besoin de serveur physique
- ✅ Gratuit pour 1 app publique
- ✅ Mise à jour automatique depuis GitHub

---

## 🔧 Paramètres Avancés

### Délai Minimum de Réservation

Dans **⚙️ Paramètres** → **⏱️ Délai min réservation** :
- **2 heures** (défaut) : Client ne peut pas réserver dans moins de 2h
- Utile pour éviter les réservations de dernière minute

### Capacité Simultanée

Dans **⏰ Horaires** → **Capacité simultanée** :
- **2** (défaut) : 2 clients peuvent réserver le même créneau
- Si vous avez 2 postes de lavage en parallèle

### Désactiver Temporairement

Pour fermer le site sans perdre les données :
1. Décochez **🌐 Site client activé**
2. Le site affichera "Site temporairement fermé pour maintenance"

---

## 📊 Statistiques

### Dans l'espace Admin :

**Tableau de Bord** :
- Nombre de réservations web en attente
- CA généré par réservations web

**Site Client → Réservations Web** :
- Liste complète avec filtres
- Export CSV possible

**Rapports** :
- Statistiques sur taux de conversion
- Services les plus demandés

---

## ❓ FAQ

**Q: Les clients doivent-ils créer un compte ?**
R: Non ! Réservation sans inscription, uniquement nom/téléphone.

**Q: Les réservations web sont-elles payées en ligne ?**
R: Non, paiement sur place. Le site ne gère que la prise de RDV.

**Q: Puis-je modifier les services visibles sur le site ?**
R: Oui ! Depuis **Services & Prix**, désactivez un service pour qu'il disparaisse du site client.

**Q: Comment supprimer une réservation ?**
R: Depuis **Site Client → Réservations Web**, cliquez **❌ Annuler**.

**Q: Les modifications sont-elles instantanées ?**
R: Oui ! Admin et site client partagent la même base de données. Changements visibles immédiatement après refresh.

---

## 🎨 Personnalisation

### Couleurs

Changez la couleur principale depuis **⚙️ Paramètres** → **🎨 Couleur principale**.
Le site client s'adapte automatiquement.

### Textes

Modifiez :
- **Nom entreprise** : Titre en haut du site
- **Slogan** : Sous-titre page d'accueil
- **Texte accueil** : Message principal
- **Contact** : Téléphone, email, adresse affichés en footer

---

## 🚨 Support

Pour toute question ou bug, contactez votre développeur ou consultez la documentation Streamlit : https://docs.streamlit.io

---

✅ **Votre site client est maintenant opérationnel !**

📱 Testez le workflow complet pour vous assurer que tout fonctionne avant de le partager à vos clients.
