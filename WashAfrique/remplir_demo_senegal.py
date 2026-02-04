#!/usr/bin/env python3
"""
Script pour remplir la base de données avec des données démo réalistes pour le Sénégal
"""

from database import Database
from datetime import datetime, timedelta
import random

db = Database()

print("🇸🇳 REMPLISSAGE BASE DE DONNÉES DÉMO - SÉNÉGAL")
print("=" * 60)

# 1. Créer des employés sénégalais
print("\n👥 Création employés...")
employes = [
    ("Mamadou Fall", "+221 77 234 56 78", "Laveur Principal", 120000),
    ("Aminata Sy", "+221 76 345 67 89", "Spécialiste Intérieur", 110000),
    ("Cheikh Ndiaye", "+221 78 456 78 90", "Polissage & Finitions", 115000),
    ("Fatou Sall", "+221 70 567 89 01", "Accueil & Coordination", 95000),
]

for nom, tel, poste, salaire in employes:
    try:
        # Créer compte user
        username = nom.lower().replace(" ", ".")
        user_id = db.ajouter_user(username, "employe123", "employe")
        # Créer fiche employé
        db.cursor.execute(
            "INSERT INTO employes (nom, tel, poste, salaire, user_id) VALUES (?, ?, ?, ?, ?)",
            (nom, tel, poste, salaire, user_id)
        )
        print(f"   ✅ {nom} - {tel}")
    except:
        print(f"   ⚠️  {nom} existe déjà")

db.conn.commit()

# 2. Mettre à jour les clients existants avec noms et tél sénégalais
print("\n👤 Mise à jour clients avec données sénégalaises...")
clients_senegalais = [
    ("Ousmane Diop", "+221 77 123 45 67", "ousmane.diop@gmail.com", "Renault Clio", "Plateau, Dakar"),
    ("Aissatou Ba", "+221 76 234 56 78", "aissatou.ba@yahoo.fr", "Peugeot 208", "Almadies, Dakar"),
    ("Ibrahima Sarr", "+221 78 345 67 89", "ibrahima.sarr@hotmail.com", "Toyota RAV4", "Mermoz, Dakar"),
    ("Mariama Diallo", "+221 70 456 78 90", "mariama.diallo@gmail.com", "Hyundai i10", "Ouakam, Dakar"),
    ("Moussa Kane", "+221 77 567 89 01", "moussa.kane@orange.sn", "Mercedes C-Class", "Fann, Dakar"),
    ("Khady Ndao", "+221 76 678 90 12", "khady.ndao@gmail.com", "Volkswagen Golf", "Point E, Dakar"),
    ("Abdoulaye Thiam", "+221 78 789 01 23", "abdoulaye.thiam@yahoo.fr", "Ford Focus", "Sacré-Cœur, Dakar"),
    ("Fatou Touré", "+221 70 890 12 34", "fatou.toure@hotmail.fr", "Nissan Qashqai", "Liberté 6, Dakar"),
    ("Alioune Cissé", "+221 77 901 23 45", "alioune.cisse@gmail.com", "Kia Sportage", "HLM, Dakar"),
    ("Binta Mbaye", "+221 76 012 34 56", "binta.mbaye@gmail.com", "Citroën C3", "Yoff, Dakar"),
    ("Modou Gueye", "+221 78 123 45 67", "modou.gueye@orange.sn", "BMW Série 3", "Ngor, Dakar"),
    ("Ndeye Seck", "+221 70 234 56 78", "ndeye.seck@yahoo.fr", "Audi A3", "Amitié, Dakar"),
    ("Papa Diagne", "+221 77 345 67 89", "papa.diagne@gmail.com", "Honda Civic", "Medina, Dakar"),
    ("Awa Niang", "+221 76 456 78 90", "awa.niang@hotmail.com", "Toyota Corolla", "Grand Yoff, Dakar"),
    ("Malick Faye", "+221 78 567 89 01", "malick.faye@gmail.com", "Mazda CX-5", "Parcelles Assainies, Dakar"),
    ("Seynabou Dieng", "+221 70 678 90 12", "seynabou.dieng@yahoo.fr", "Suzuki Swift", "Pikine, Dakar"),
    ("Lamine Sow", "+221 77 789 01 23", "lamine.sow@orange.sn", "Dacia Duster", "Guédiawaye, Dakar"),
    ("Adama Ba", "+221 76 890 12 34", "adama.ba@gmail.com", "Renault Megane", "Rufisque, Dakar"),
]

clients_db = db.get_all_clients()
for i, client_db in enumerate(clients_db[:len(clients_senegalais)]):
    nom, tel, email, vehicule, quartier = clients_senegalais[i]
    db.cursor.execute("""
        UPDATE clients 
        SET nom = ?, tel = ?, email = ?, vehicule = ?, adresse = ?, points_fidelite = ?
        WHERE id = ?
    """, (nom, tel, email, vehicule, quartier, random.randint(0, 50), client_db['id']))
    print(f"   ✅ {nom} - {quartier}")

db.conn.commit()

# 3. Créer des réservations réalistes
print("\n📅 Création réservations...")
services = db.get_all_services()
clients = db.get_all_clients()

# Réservations des 7 derniers jours
for jour in range(7):
    date_res = (datetime.now() - timedelta(days=jour)).strftime("%Y-%m-%d")
    nb_reservations = random.randint(3, 8)
    
    for _ in range(nb_reservations):
        client = random.choice(clients)
        service = random.choice(services)
        heure = f"{random.randint(8, 17)}:{random.choice(['00', '30'])}"
        
        db.cursor.execute("""
            INSERT INTO reservations (client_id, service_id, date, heure, statut)
            VALUES (?, ?, ?, ?, ?)
        """, (client['id'], service['id'], date_res, heure, random.choice(['termine', 'termine', 'annule'])))

db.conn.commit()
print(f"   ✅ {nb_reservations * 7} réservations créées")

# 4. Créer des paiements pour les réservations terminées
print("\n💰 Création paiements...")
reservations = db.get_all_reservations()
nb_paiements = 0
for res in reservations:
    if res['statut'] == 'termine' and res.get('prix'):
        db.cursor.execute("""
            INSERT INTO paiements (reservation_id, montant, methode, date_paiement)
            VALUES (?, ?, ?, ?)
        """, (res['id'], res['prix'], random.choice(['Espèces', 'Wave', 'Orange Money']), 
              f"{res['date']} {res['heure']}:00"))
        nb_paiements += 1

db.conn.commit()
print(f"   ✅ {nb_paiements} paiements créés")

# 5. Créer des pointages pour les employés
print("\n⏰ Création pointages...")
db.cursor.execute("SELECT id FROM users WHERE role = 'employe'")
employes_users = [row['id'] for row in db.cursor.fetchall()]

for jour in range(7):
    date_pointage = (datetime.now() - timedelta(days=jour)).strftime("%Y-%m-%d")
    for emp_id in employes_users:
        # Arrivée
        heure_arrivee = f"0{random.randint(7, 9)}:{random.randint(0, 59):02d}"
        db.cursor.execute("""
            INSERT INTO pointages (user_id, type, date, heure)
            VALUES (?, 'arrivee', ?, ?)
        """, (emp_id, date_pointage, heure_arrivee))
        
        # Départ
        heure_depart = f"{random.randint(17, 19)}:{random.randint(0, 59):02d}"
        db.cursor.execute("""
            INSERT INTO pointages (user_id, type, date, heure)
            VALUES (?, 'depart', ?, ?)
        """, (emp_id, date_pointage, heure_depart))

db.conn.commit()
print(f"   ✅ {len(employes_users) * 7 * 2} pointages créés")

# 6. Statistiques finales
print("\n" + "=" * 60)
print("📊 RÉSUMÉ BASE DE DONNÉES")
print("=" * 60)
print(f"   Employés: {len(employes)}")
print(f"   Clients: {len(clients_senegalais)}")
print(f"   Services: {len(services)}")
print(f"   Réservations: {len(reservations)}")
print(f"   Paiements: {nb_paiements}")
print(f"   Pointages: {len(employes_users) * 7 * 2}")
print()
print("✅ Base de données remplie avec succès!")
print("🎯 Prête pour des tests réalistes")
