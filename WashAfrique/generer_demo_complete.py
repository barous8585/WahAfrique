#!/usr/bin/env python3
"""
Script pour générer une base de données démo COMPLÈTE et ACTIVE
avec CA, services, réservations, paiements, pointages, etc.
"""

from database import Database
from datetime import datetime, timedelta, date
import random
import hashlib

print("🇸🇳 GÉNÉRATION BASE DÉMO COMPLÈTE - ENTREPRISE ACTIVE")
print("=" * 70)

db = Database()

# 1. Nettoyer les données existantes (sauf admin)
print("\n🧹 Nettoyage des données existantes...")
conn = db.get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM pointages")
cursor.execute("DELETE FROM paiements")
cursor.execute("DELETE FROM photos_services")
cursor.execute("DELETE FROM reservations")
cursor.execute("DELETE FROM employes")
cursor.execute("DELETE FROM clients")
cursor.execute("DELETE FROM users WHERE role != 'admin'")

conn.commit()
print("   ✅ Données nettoyées")

# 2. Créer 3 employés sénégalais
print("\n👥 Création employés...")
employes_data = [
    ("Yao Kouadio", "+225 07 11 22 33 44", "Laveur Senior", 150000, "yao.k", "yao123"),
    ("Marie Bamba", "+225 05 22 33 44 55", "Détaileuse", 180000, "marie.b", "marie123"),
    ("Jean-Claude Touré", "+225 01 33 44 55 66", "Polisseur Expert", 200000, "jean.t", "jean123"),
]

employes_ids = []
for nom, tel, poste, salaire, username, password in employes_data:
    # Créer compte user
    user_id = db.creer_compte_employe(username, password, "")
    # Créer fiche employé
    emp_id = db.ajouter_employe(nom, tel, poste, salaire)
    db.lier_employe_user(emp_id, user_id)
    employes_ids.append({'user_id': user_id, 'emp_id': emp_id, 'nom': nom})
    print(f"   ✅ {nom} - {username}/{password}")

# 3. Créer 18 clients sénégalais
print("\n👤 Création clients...")
clients_data = [
    ("Ousmane Diop", "+221 77 123 45 67", "ousmane.diop@gmail.com", "Renault Clio Blanc"),
    ("Aissatou Ba", "+221 76 234 56 78", "aissatou.ba@orange.sn", "Peugeot 208 Gris"),
    ("Ibrahima Sarr", "+221 78 345 67 89", "ibrahima.sarr@hotmail.com", "Toyota RAV4 Noir"),
    ("Mariama Diallo", "+221 70 456 78 90", "mariama.diallo@gmail.com", "Hyundai i10 Rouge"),
    ("Moussa Kane", "+221 77 567 89 01", "moussa.kane@orange.sn", "Mercedes C-Class Argenté"),
    ("Khady Ndao", "+221 76 678 90 12", "khady.ndao@gmail.com", "Volkswagen Golf Bleu"),
    ("Abdoulaye Thiam", "+221 78 789 01 23", "abdoulaye.thiam@yahoo.fr", "Ford Focus Noir"),
    ("Fatou Touré", "+221 70 890 12 34", "fatou.toure@gmail.com", "Nissan Qashqai Blanc"),
    ("Alioune Cissé", "+221 77 901 23 45", "alioune.cisse@gmail.com", "Kia Sportage Gris"),
    ("Binta Mbaye", "+221 76 012 34 56", "binta.mbaye@gmail.com", "Citroën C3 Rouge"),
    ("Modou Gueye", "+221 78 123 45 67", "modou.gueye@orange.sn", "BMW Série 3 Noir"),
    ("Ndeye Seck", "+221 70 234 56 78", "ndeye.seck@yahoo.fr", "Audi A3 Blanc"),
    ("Papa Diagne", "+221 77 345 67 89", "papa.diagne@gmail.com", "Honda Civic Gris"),
    ("Awa Niang", "+221 76 456 78 90", "awa.niang@hotmail.com", "Toyota Corolla Argent"),
    ("Malick Faye", "+221 78 567 89 01", "malick.faye@gmail.com", "Mazda CX-5 Bleu"),
    ("Seynabou Dieng", "+221 70 678 90 12", "seynabou.dieng@yahoo.fr", "Suzuki Swift Rouge"),
    ("Lamine Sow", "+221 77 789 01 23", "lamine.sow@orange.sn", "Dacia Duster Noir"),
    ("Adama Ba", "+221 76 890 12 34", "adama.ba@gmail.com", "Renault Megane Blanc"),
]

clients_ids = []
for nom, tel, email, vehicule in clients_data:
    client_id = db.ajouter_client(nom, tel, email, vehicule)
    clients_ids.append(client_id)
    print(f"   ✅ {nom} - {tel}")

# 4. Récupérer les services existants
services = db.get_all_services()
print(f"\n🔧 {len(services)} services disponibles")

# 5. Créer des réservations + paiements sur 30 derniers jours
print("\n📅 Création réservations et paiements...")

total_ca = 0
nb_reservations_creees = 0
nb_paiements = 0

# Répartition: 80% payés, 15% terminés, 5% en cours/attente
for jour in range(30):
    date_res = (datetime.now() - timedelta(days=jour)).date()
    
    # 4-8 réservations par jour
    nb_res_jour = random.randint(4, 8)
    
    for _ in range(nb_res_jour):
        client_id = random.choice(clients_ids)
        service = random.choice(services)
        employe = random.choice(employes_ids)
        
        heure = f"{random.randint(9, 17):02d}:{random.choice(['00', '30'])}"
        
        # 80% payé, 15% terminé, 5% en_cours/attente
        rand = random.random()
        if rand < 0.80:
            statut = 'valide'  # Payé et validé
        elif rand < 0.95:
            statut = 'termine'  # Terminé mais pas payé
        else:
            statut = random.choice(['en_cours', 'en_attente'])
        
        # Créer réservation
        cursor.execute("""
            INSERT INTO reservations (
                client_id, service_id, employe_id, date, heure, 
                statut, montant, montant_paye, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            client_id, service['id'], employe['emp_id'], 
            date_res.isoformat(), heure, 
            statut, service['prix'], 
            service['prix'] if statut == 'valide' else 0,
            f"{date_res.isoformat()} {heure}:00"
        ))
        
        reservation_id = cursor.lastrowid
        nb_reservations_creees += 1
        
        # Si payé, créer paiement
        if statut == 'valide':
            methode = random.choice(['Espèces', 'Espèces', 'Orange Money', 'Wave', 'Carte Bancaire'])
            cursor.execute("""
                INSERT INTO paiements (
                    reservation_id, montant, methode, date_paiement
                ) VALUES (?, ?, ?, ?)
            """, (
                reservation_id, service['prix'], methode,
                f"{date_res.isoformat()} {heure}:30"
            ))
            nb_paiements += 1
            total_ca += service['prix']
            
            # Mettre à jour dépense client
            cursor.execute("""
                UPDATE clients 
                SET total_depense = total_depense + ?
                WHERE id = ?
            """, (service['prix'], client_id))
    
    if jour % 5 == 0:
        print(f"   📆 Jour -{jour}: {nb_res_jour} réservations")

conn.commit()

# 6. Créer pointages employés (30 derniers jours)
print("\n⏰ Création pointages employés...")
nb_pointages = 0

for jour in range(30):
    date_pointage = (datetime.now() - timedelta(days=jour)).date()
    
    # Skip dimanches
    if date_pointage.weekday() == 6:
        continue
    
    for emp in employes_ids:
        # 90% de présence
        if random.random() < 0.90:
            # Arrivée 8h-9h30
            h_arr = random.randint(8, 9)
            m_arr = random.randint(0, 59)
            heure_arrivee = f"{h_arr:02d}:{m_arr:02d}"
            
            cursor.execute("""
                INSERT INTO pointages (user_id, type, date, heure)
                VALUES (?, 'arrivee', ?, ?)
            """, (emp['user_id'], date_pointage.isoformat(), heure_arrivee))
            nb_pointages += 1
            
            # Départ 17h-19h
            h_dep = random.randint(17, 18)
            m_dep = random.randint(0, 59)
            heure_depart = f"{h_dep:02d}:{m_dep:02d}"
            
            cursor.execute("""
                INSERT INTO pointages (user_id, type, date, heure)
                VALUES (?, 'depart', ?, ?)
            """, (emp['user_id'], date_pointage.isoformat(), heure_depart))
            nb_pointages += 1

conn.commit()
conn.close()

# 7. Afficher résumé
print("\n" + "=" * 70)
print("📊 RÉSUMÉ ENTREPRISE ACTIVE")
print("=" * 70)
print(f"   👥 Employés:          {len(employes_data)}")
print(f"   👤 Clients:           {len(clients_data)}")
print(f"   🔧 Services:          {len(services)}")
print(f"   📅 Réservations:      {nb_reservations_creees}")
print(f"   💰 Paiements:         {nb_paiements}")
print(f"   💵 CA Total:          {total_ca:,} FCFA".replace(',', ' '))
print(f"   ⏰ Pointages:         {nb_pointages}")
print("=" * 70)
print("\n✅ BASE DE DONNÉES COMPLÈTE ET ACTIVE !")
print("🎯 Données réparties sur 30 jours")
print("📈 CA réaliste avec historique complet")
print("\n👤 Identifiants employés créés:")
for emp in employes_data:
    print(f"   - {emp[3]} / {emp[4]}")
print("\n🚀 Prêt pour démo professionnelle!")
