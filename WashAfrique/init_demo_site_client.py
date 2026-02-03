#!/usr/bin/env python3
"""
Script d'initialisation des données de démonstration pour le site client
À exécuter une seule fois après déploiement Streamlit Cloud
"""

from database import Database

def init_demo_data():
    """Initialise services et paramètres de démonstration"""
    db = Database()
    
    print("🔧 Initialisation des données de démonstration...")
    
    # Services de base
    services_demo = [
        {
            "nom": "Lavage Extérieur Simple",
            "prix": 3000,
            "duree": 20,
            "description": "Lavage extérieur complet + séchage",
            "actif": 1
        },
        {
            "nom": "Lavage Intérieur + Extérieur",
            "prix": 6000,
            "duree": 40,
            "description": "Lavage complet intérieur et extérieur + aspirateur",
            "actif": 1
        },
        {
            "nom": "Lavage Premium",
            "prix": 10000,
            "duree": 60,
            "description": "Lavage complet + lustrage + nettoyage moteur",
            "actif": 1
        },
        {
            "nom": "Nettoyage Intérieur Seul",
            "prix": 4000,
            "duree": 30,
            "description": "Aspirateur + nettoyage sièges + tableau de bord",
            "actif": 1
        }
    ]
    
    print("📋 Ajout des services...")
    for service in services_demo:
        try:
            service_id = db.add_service(
                nom=service["nom"],
                prix=service["prix"],
                duree=service["duree"],
                description=service.get("description", "")
            )
            print(f"  ✅ {service['nom']} ajouté (ID: {service_id})")
        except Exception as e:
            print(f"  ⚠️ {service['nom']} existe déjà ou erreur: {e}")
    
    # Paramètres site client
    print("\n⚙️ Configuration site client...")
    parametres = {
        "nom_entreprise_site": "WashAfrique Pro",
        "slogan": "Votre voiture mérite le meilleur",
        "telephone_contact": "+225 07 XX XX XX XX",
        "email_contact": "contact@washafrique.com",
        "adresse": "Abidjan, Cocody, Côte d'Ivoire",
        "texte_accueil": "Réservez votre lavage en ligne 24/7. Service professionnel garanti !",
        "couleur_principale": "#667eea",
        "site_actif": "1",
        "reservation_active": "1",
        "delai_min_reservation": "2"
    }
    
    for cle, valeur in parametres.items():
        try:
            db.set_parametre_site_client(cle, valeur)
            print(f"  ✅ {cle} configuré")
        except Exception as e:
            print(f"  ⚠️ Erreur {cle}: {e}")
    
    print("\n🎉 Initialisation terminée !")
    print("\n📱 Prochaines étapes:")
    print("1. Rafraîchissez votre site client")
    print("2. Les 4 services devraient apparaître")
    print("3. Testez une réservation")
    print("4. Validez-la depuis l'app admin")
    
    # Afficher les services créés
    print("\n📊 Services disponibles:")
    services = db.get_all_services()
    for s in services:
        if s['actif']:
            print(f"  • {s['nom']} - {s['prix']:,} FCFA - {s['duree']} min")

if __name__ == "__main__":
    init_demo_data()
