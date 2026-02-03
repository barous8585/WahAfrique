#!/bin/bash

# Script de lancement WashAfrique Pro
# Utilisation: ./start.sh

echo "🚗 Démarrage de WashAfrique Pro v3.0..."
echo "=========================================="
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 n'est pas installé !"
    echo "Installez Python 3.8+ depuis https://www.python.org/"
    exit 1
fi

# Vérifier si Streamlit est installé
if ! python3 -c "import streamlit" &> /dev/null
then
    echo "📦 Installation des dépendances..."
    pip3 install -r requirements.txt
    echo "✅ Installation terminée !"
    echo ""
fi

# Vérifier si la base existe
if [ ! -f "washafrique.db" ]; then
    echo "🔧 Première utilisation détectée !"
    echo "Initialisation des données d'exemple..."
    python3 init_data.py
    echo ""
fi

# Lancer l'application
echo "🚀 Lancement de l'application..."
echo "📱 L'application va s'ouvrir dans votre navigateur"
echo "🔐 Identifiants par défaut:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  Pour arrêter l'application, pressez CTRL+C"
echo "=========================================="
echo ""

streamlit run app.py
