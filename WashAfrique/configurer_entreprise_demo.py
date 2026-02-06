#!/usr/bin/env python3
"""
Script pour remplir les informations de l'entreprise démo - SÉNÉGAL
"""

from database import Database

print("🇸🇳 CONFIGURATION ENTREPRISE DÉMO - SÉNÉGAL")
print("=" * 70)

db = Database()

# Informations entreprise
print("\n📋 Enregistrement informations entreprise...")
db.set_info_entreprise(
    nom="WashAfrique Pro",
    description="Service de lavage automobile premium à Dakar. Nous offrons un service rapide, écologique et professionnel pour tous types de véhicules.",
    telephone="+221 33 825 40 50",
    email="contact@washafrique.sn",
    adresse="Avenue Cheikh Anta Diop, Almadies, Dakar",
    site_web="www.washafrique.sn"
)
print("   ✅ Informations entreprise enregistrées")

# Paramètres site client - Format Sénégal
print("\n🌐 Configuration site client...")
db.set_parametre('couleur_principale', '#1E88E5')
db.set_parametre('texte_accueil', 'Bienvenue chez WashAfrique Pro ! Le meilleur service de lavage automobile à Dakar.')
db.set_parametre('slogan', '✨ Votre voiture mérite le meilleur ✨')
db.set_parametre('email_notifications', 'notifications@washafrique.sn')
db.set_parametre('telephone_contact', '+221 33 825 40 50')
db.set_parametre('email_contact', 'contact@washafrique.sn')
db.set_parametre('adresse', 'Almadies, Dakar, Sénégal')
print("   ✅ Site client configuré (Format Sénégal +221)")

# Horaires (Lundi à Samedi 8h-19h, Dimanche fermé)
print("\n⏰ Configuration horaires...")
horaires = {
    "Lundi": {"ouverture": "08:00", "fermeture": "19:00"},
    "Mardi": {"ouverture": "08:00", "fermeture": "19:00"},
    "Mercredi": {"ouverture": "08:00", "fermeture": "19:00"},
    "Jeudi": {"ouverture": "08:00", "fermeture": "19:00"},
    "Vendredi": {"ouverture": "08:00", "fermeture": "19:00"},
    "Samedi": {"ouverture": "09:00", "fermeture": "18:00"},
    "Dimanche": {"ouverture": "Fermé", "fermeture": "Fermé"}
}

for jour, heures in horaires.items():
    db.set_parametre(f"horaire_{jour.lower()}_ouverture", heures["ouverture"])
    db.set_parametre(f"horaire_{jour.lower()}_fermeture", heures["fermeture"])

print("   ✅ Horaires configurés (Lun-Sam 8h-19h)")

# Profil propriétaire (user_id = 1 pour admin)
print("\n👤 Configuration profil propriétaire...")
db.set_profil_proprietaire(
    user_id=1,
    nom_complet="Thierno Ousmane Barry",
    telephone="+221 77 555 12 34",
    email="thierno.barry@washafrique.sn",
    adresse="Almadies, Dakar, Sénégal"
)
print("   ✅ Profil propriétaire enregistré")

print("\n" + "=" * 70)
print("✅ CONFIGURATION ENTREPRISE SÉNÉGAL TERMINÉE")
print("=" * 70)
print("\n📊 Récapitulatif:")
print("   🇸🇳 Pays: SÉNÉGAL")
print("   🏢 Nom: WashAfrique Pro")
print("   📍 Adresse: Almadies, Dakar")
print("   ☎️  Téléphone: +221 33 825 40 50")
print("   📧 Email: contact@washafrique.sn")
print("   ⏰ Horaires: Lun-Sam 8h-19h")
print("   👤 Propriétaire: Thierno Ousmane Barry")
print("\n🚀 Entreprise prête pour démonstration !")
