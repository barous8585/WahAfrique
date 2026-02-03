"""
Script d'initialisation de données d'exemple pour WashAfrique Pro
Exécutez ce script une seule fois pour peupler la base avec des données de test
"""

from database import Database
from datetime import date, timedelta

def initialiser_donnees_exemple():
    db = Database()
    
    print("🚀 Initialisation des données d'exemple...")
    
    # Services par défaut (si pas déjà créés)
    print("📋 Création des services...")
    services_defaut = [
        {
            "nom": "Lavage Extérieur Express",
            "prix": 3000,
            "duree": 20,
            "points": 1,
            "description": "Lavage rapide extérieur uniquement"
        },
        {
            "nom": "Lavage Standard (Ext + Int)",
            "prix": 8000,
            "duree": 45,
            "points": 2,
            "description": "Lavage complet intérieur et extérieur"
        },
        {
            "nom": "Lavage Premium",
            "prix": 15000,
            "duree": 90,
            "points": 3,
            "description": "Lavage complet + nettoyage tapis + vitres"
        },
        {
            "nom": "Polissage & Cire",
            "prix": 25000,
            "duree": 120,
            "points": 5,
            "description": "Polissage carrosserie + application cire protectrice"
        },
        {
            "nom": "Détailing Complet VIP",
            "prix": 50000,
            "duree": 180,
            "points": 10,
            "description": "Service premium : lavage complet, polissage, céramique, nettoyage moteur"
        },
        {
            "nom": "Nettoyage Intérieur Cuir",
            "prix": 12000,
            "duree": 60,
            "points": 3,
            "description": "Nettoyage et traitement sièges cuir"
        },
        {
            "nom": "Rénovation Phares",
            "prix": 8000,
            "duree": 30,
            "points": 2,
            "description": "Polissage et rénovation des phares ternis"
        }
    ]
    
    services_existants = db.get_all_services()
    if len(services_existants) < 5:
        for service in services_defaut:
            db.ajouter_service(
                service['nom'],
                service['prix'],
                service['duree'],
                service['points'],
                service['description']
            )
        print(f"✅ {len(services_defaut)} services créés")
    else:
        print("ℹ️  Services déjà existants")
    
    # Clients d'exemple
    print("👥 Création de clients d'exemple...")
    clients_exemple = [
        {
            "nom": "Amadou Diallo",
            "tel": "+225 07 12 34 56 78",
            "email": "amadou.diallo@email.com",
            "vehicule": "Toyota Corolla 2020"
        },
        {
            "nom": "Fatou Traoré",
            "tel": "+225 05 98 76 54 32",
            "email": "fatou.traore@email.com",
            "vehicule": "Mercedes Classe C 2019"
        },
        {
            "nom": "Kouassi N'Guessan",
            "tel": "+225 01 11 22 33 44",
            "email": "kouassi@email.com",
            "vehicule": "Range Rover Sport 2021"
        },
        {
            "nom": "Aïcha Koné",
            "tel": "+225 07 55 66 77 88",
            "email": "aicha.kone@email.com",
            "vehicule": "Peugeot 3008 2022"
        },
        {
            "nom": "Ibrahim Sow",
            "tel": "+225 05 44 33 22 11",
            "email": "ibrahim.sow@email.com",
            "vehicule": "BMW X5 2020"
        }
    ]
    
    clients_existants = db.get_all_clients()
    if len(clients_existants) < 3:
        for client in clients_exemple:
            if not db.get_client_by_tel(client['tel']):
                client_id = db.ajouter_client(
                    client['nom'],
                    client['tel'],
                    client['email'],
                    client['vehicule']
                )
                # Ajouter quelques points fidélité
                db.update_client_points(client_id, 15, "add")
        print(f"✅ {len(clients_exemple)} clients créés")
    else:
        print("ℹ️  Clients déjà existants")
    
    # Employés
    print("👨‍💼 Création des employés...")
    employes_exemple = [
        {
            "nom": "Yao Kouadio",
            "tel": "+225 07 11 22 33 44",
            "poste": "Laveur Senior",
            "salaire": 150000
        },
        {
            "nom": "Marie Bamba",
            "tel": "+225 05 22 33 44 55",
            "poste": "Détaileuse",
            "salaire": 180000
        },
        {
            "nom": "Jean-Claude Touré",
            "tel": "+225 01 33 44 55 66",
            "poste": "Polisseur Expert",
            "salaire": 200000
        }
    ]
    
    employes_existants = db.get_all_employes()
    if len(employes_existants) < 2:
        for emp in employes_exemple:
            db.ajouter_employe(emp['nom'], emp['tel'], emp['poste'], emp['salaire'])
        print(f"✅ {len(employes_exemple)} employés créés")
    else:
        print("ℹ️  Employés déjà existants")
    
    # Codes promo
    print("🎁 Création des codes promo...")
    promos_exemple = [
        {
            "code": "BIENVENUE",
            "type": "pourcentage",
            "valeur": 10,
            "date_debut": None,
            "date_fin": None,
            "utilisations_max": 100
        },
        {
            "code": "VIP2026",
            "type": "pourcentage",
            "valeur": 20,
            "date_debut": None,
            "date_fin": (date.today() + timedelta(days=60)).isoformat(),
            "utilisations_max": 50
        },
        {
            "code": "PREMIERE",
            "type": "montant_fixe",
            "valeur": 5000,
            "date_debut": None,
            "date_fin": None,
            "utilisations_max": -1
        }
    ]
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM codes_promo")
    nb_promos = cursor.fetchone()['count']
    conn.close()
    
    if nb_promos < 2:
        for promo in promos_exemple:
            try:
                db.ajouter_code_promo(
                    promo['code'],
                    promo['type'],
                    promo['valeur'],
                    promo['date_debut'],
                    promo['date_fin'],
                    promo['utilisations_max']
                )
            except:
                pass  # Code déjà existant
        print(f"✅ {len(promos_exemple)} codes promo créés")
    else:
        print("ℹ️  Codes promo déjà existants")
    
    # Produits stock
    print("📦 Création des produits en stock...")
    produits_exemple = [
        {
            "nom": "Shampooing Auto Premium",
            "quantite": 25,
            "seuil_alerte": 5,
            "unite": "L",
            "prix_unitaire": 5000
        },
        {
            "nom": "Cire de Protection",
            "quantite": 15,
            "seuil_alerte": 3,
            "unite": "L",
            "prix_unitaire": 12000
        },
        {
            "nom": "Nettoyant Intérieur",
            "quantite": 20,
            "seuil_alerte": 5,
            "unite": "L",
            "prix_unitaire": 4000
        },
        {
            "nom": "Polish Carrosserie",
            "quantite": 10,
            "seuil_alerte": 2,
            "unite": "L",
            "prix_unitaire": 15000
        },
        {
            "nom": "Chiffons Microfibres",
            "quantite": 50,
            "seuil_alerte": 10,
            "unite": "pièce",
            "prix_unitaire": 500
        },
        {
            "nom": "Produit Vitres",
            "quantite": 18,
            "seuil_alerte": 4,
            "unite": "L",
            "prix_unitaire": 3000
        }
    ]
    
    produits_existants = db.get_all_produits()
    if len(produits_existants) < 3:
        for prod in produits_exemple:
            db.ajouter_produit(
                prod['nom'],
                prod['quantite'],
                prod['seuil_alerte'],
                prod['unite'],
                prod['prix_unitaire']
            )
        print(f"✅ {len(produits_exemple)} produits ajoutés au stock")
    else:
        print("ℹ️  Produits déjà existants")
    
    # Créer quelques réservations d'exemple pour aujourd'hui et demain
    print("📅 Création de réservations d'exemple...")
    clients = db.get_all_clients()
    services = db.get_all_services()
    postes = db.get_all_postes()
    
    if clients and services and postes:
        reservations_exemple = [
            {
                "client_idx": 0,
                "service_idx": 1,
                "date": date.today().isoformat(),
                "heure": "09:00",
                "poste_id": postes[0]['id']
            },
            {
                "client_idx": 1,
                "service_idx": 0,
                "date": date.today().isoformat(),
                "heure": "10:30",
                "poste_id": postes[1]['id'] if len(postes) > 1 else postes[0]['id']
            },
            {
                "client_idx": 2,
                "service_idx": 3,
                "date": date.today().isoformat(),
                "heure": "14:00",
                "poste_id": postes[0]['id']
            },
            {
                "client_idx": 3,
                "service_idx": 2,
                "date": (date.today() + timedelta(days=1)).isoformat(),
                "heure": "09:30",
                "poste_id": postes[0]['id']
            }
        ]
        
        reservations_existantes = db.get_all_reservations()
        if len(reservations_existantes) < 2:
            for res in reservations_exemple:
                if res['client_idx'] < len(clients) and res['service_idx'] < len(services):
                    client = clients[res['client_idx']]
                    service = services[res['service_idx']]
                    
                    db.ajouter_reservation(
                        client_id=client['id'],
                        service_id=service['id'],
                        date=res['date'],
                        heure=res['heure'],
                        montant=service['prix'],
                        poste_id=res['poste_id'],
                        notes="Réservation d'exemple"
                    )
            print(f"✅ {len(reservations_exemple)} réservations créées")
        else:
            print("ℹ️  Réservations déjà existantes")
    
    print("\n✅ Initialisation terminée avec succès !")
    print("\n" + "="*60)
    print("🚗 WASHAFRIQUE PRO - PRÊT À L'EMPLOI")
    print("="*60)
    print("\n📌 IDENTIFIANTS DE CONNEXION :")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n⚠️  IMPORTANT : Changez le mot de passe après la première connexion !")
    print("\n💡 CODES PROMO DISPONIBLES :")
    print("   - BIENVENUE : 10% de réduction")
    print("   - VIP2026 : 20% de réduction")
    print("   - PREMIERE : 5000 FCFA de réduction")
    print("\n🎯 Lancez l'application avec : streamlit run app.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    initialiser_donnees_exemple()
