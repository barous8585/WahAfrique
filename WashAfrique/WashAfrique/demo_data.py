#!/usr/bin/env python3
"""
Script de création de données de démonstration pour WashAfrique Pro
Exécuter: python3 demo_data.py
"""

from database import Database
from datetime import datetime, timedelta
import random

def create_demo_data():
    print("🚀 Création des données de démonstration WashAfrique Pro...\n")
    
    db = Database()
    
    # === 1. CLIENTS ===
    print("👥 Création de 10 clients...")
    clients_demo = [
        ("Mamadou Traoré", "+225 07 12 34 56", "mamadou@email.com", "Toyota Corolla 2020"),
        ("Fatou Koné", "+225 05 23 45 67", "fatou@email.com", "Honda Civic 2019"),
        ("Abdoul Diallo", "+225 07 34 56 78", "abdoul@email.com", "Mercedes Classe C"),
        ("Aïcha Touré", "+225 01 45 67 89", "aicha@email.com", "Peugeot 3008"),
        ("Youssouf Camara", "+225 07 56 78 90", "youssouf@email.com", "BMW Série 3"),
        ("Mariam Sylla", "+225 05 67 89 01", "mariam@email.com", "Renault Clio"),
        ("Ibrahim Sanogo", "+225 07 78 90 12", "ibrahim@email.com", "Volkswagen Golf"),
        ("Kadiatou Barry", "+225 01 89 01 23", "kadiatou@email.com", "Audi A4"),
        ("Oumar Coulibaly", "+225 07 90 12 34", "oumar@email.com", "Nissan Qashqai"),
        ("Aminata Keita", "+225 05 01 23 45", "aminata@email.com", "Ford Focus")
    ]
    
    client_ids = []
    for nom, tel, email, vehicule in clients_demo:
        # Vérifier si client existe déjà
        client_existant = db.get_client_by_tel(tel)
        if client_existant:
            client_ids.append(client_existant['id'])
            print(f"  ℹ️  {nom} - Déjà existant")
        else:
            client_id = db.ajouter_client(nom, tel, email, vehicule)
            client_ids.append(client_id)
            print(f"  ✅ {nom} - {vehicule}")
    
    print(f"✅ {len(client_ids)} clients créés\n")
    
    # === 2. SERVICES (variés pour les stats) ===
    print("🔧 Vérification des services...")
    services = db.get_all_services(actif_only=True)
    if services:
        print(f"✅ {len(services)} services disponibles\n")
        service_ids = [s['id'] for s in services]
    else:
        print("⚠️ Aucun service trouvé. Création de services de base...")
        service_ids = []
        services_base = [
            ("Lavage Express", 3000, 15, 10, "Lavage extérieur rapide"),
            ("Lavage Standard", 5000, 30, 20, "Lavage ext + int complet"),
            ("Lavage Premium", 8000, 45, 30, "Lavage complet + cirage"),
            ("Nettoyage Intérieur", 4000, 25, 15, "Aspirateur + nettoyage sièges"),
            ("Polissage", 12000, 60, 50, "Polissage carrosserie complète")
        ]
        for nom, prix, duree, points, desc in services_base:
            service_id = db.ajouter_service(nom, desc, prix, duree, points)
            service_ids.append(service_id)
            print(f"  ✅ {nom} - {prix} FCFA")
        print()
    
    # === 3. RÉSERVATIONS & PAIEMENTS (7 derniers jours) ===
    print("📅 Création de 20 réservations sur les 7 derniers jours...")
    
    postes = db.get_all_postes()
    poste_id = postes[0]['id'] if postes else 1
    
    today = datetime.now()
    reservations_creees = 0
    paiements_total = 0
    
    for i in range(20):
        # Répartir sur 7 jours
        jour_offset = random.randint(0, 6)
        date_service = (today - timedelta(days=jour_offset)).strftime("%Y-%m-%d")
        heure_service = f"{random.randint(8, 17)}:{random.choice(['00', '15', '30', '45'])}"
        
        # Client et service aléatoires
        client_id = random.choice(client_ids)
        service = random.choice(services)
        
        # Créer réservation
        reservation_id = db.ajouter_reservation(
            client_id=client_id,
            service_id=service['id'],
            date=date_service,
            heure=heure_service,
            montant=service['prix'],
            poste_id=poste_id,
            employe_id=None,
            notes=""
        )
        
        # Simuler workflow: 80% des services sont payés et validés
        if random.random() < 0.8:
            # Changer statut à payé
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reservations SET statut = 'paye', montant_paye = ? WHERE id = ?",
                (service['prix'], reservation_id)
            )
            conn.commit()
            conn.close()
            
            # Ajouter paiement
            methode = random.choice(["Espèces", "Carte", "Mobile Money", "Espèces", "Espèces"])  # 60% espèces
            db.ajouter_paiement(reservation_id, service['prix'], methode, "")
            paiements_total += service['prix']
            
            # 70% sont validés
            if random.random() < 0.7:
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE reservations SET statut = 'valide' WHERE id = ?",
                    (reservation_id,)
                )
                conn.commit()
                conn.close()
            
            # Ajouter points fidélité
            db.update_client_points(client_id, service['points'], "add")
        
        reservations_creees += 1
    
    print(f"✅ {reservations_creees} réservations créées")
    print(f"💰 CA Total simulé: {paiements_total:,.0f} FCFA\n")
    
    # === 4. POINTAGES (Skip - méthode non disponible) ===
    print("⏰ Pointages: À créer manuellement via l'interface employé\n")
    
    # === 5. STATISTIQUES FINALES ===
    print("=" * 60)
    print("📊 RÉSUMÉ DES DONNÉES DE DÉMONSTRATION")
    print("=" * 60)
    
    stats = db.get_stats_dashboard()
    employes = db.get_all_employes(actif_only=True)
    
    print(f"👥 Clients:           {len(db.get_all_clients())}")
    print(f"🔧 Services:          {len(db.get_all_services(actif_only=True))}")
    print(f"📅 Réservations:      {len(db.get_all_reservations())}")
    print(f"💰 CA Aujourd'hui:    {stats.get('ca_jour', 0):,.0f} FCFA")
    print(f"💰 CA Total:          {stats.get('ca_total', 0):,.0f} FCFA")
    print(f"💳 Paiements:         {len(db.get_all_paiements())}")
    print(f"👨‍💼 Employés:          {len(employes)}")
    
    print("\n✅ Données de démonstration créées avec succès!")
    print("\n🚀 Vous pouvez maintenant tester l'application:")
    print("   1. Lancez: streamlit run app.py")
    print("   2. Connectez-vous: admin / admin123")
    print("   3. Explorez toutes les fonctionnalités!\n")

if __name__ == "__main__":
    try:
        create_demo_data()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
