#!/bin/bash
# Script de configuration automatique pour Magic Counter
# Génère le fichier .env avec les paramètres nécessaires

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================================"
echo "Configuration automatique de Magic Counter"
echo "============================================================"
echo ""

# Chemin du fichier .env
ENV_PATH="magicCounter/magicCounter/.env"

# Vérifier si le fichier existe déjà
if [ -f "$ENV_PATH" ]; then
    echo -e "${YELLOW}⚠️  Le fichier .env existe déjà à l'emplacement :${NC}"
    echo "   $ENV_PATH"
    echo ""
    read -p "Voulez-vous le remplacer ? (o/N) : " response
    response=${response,,} # Convertir en minuscules
    if [[ ! "$response" =~ ^(o|oui|y|yes)$ ]]; then
        echo -e "${RED}❌ Opération annulée.${NC}"
        exit 0
    fi
    echo ""
fi

# Créer le répertoire si nécessaire
mkdir -p "$(dirname "$ENV_PATH")"

# Générer la SECRET_KEY
echo -e "${BLUE}🔐 Génération d'une SECRET_KEY sécurisée...${NC}"

# Vérifier si Python et Django sont disponibles
if command -v python3 &> /dev/null; then
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null || \
                 python3 -c "import secrets; chars='abcdefghijklmnopqrstuvwxyz0123456789!@#\$%^&*(-_=+)'; print(''.join(secrets.choice(chars) for _ in range(50)))")
else
    echo -e "${RED}❌ Python 3 n'est pas installé !${NC}"
    exit 1
fi

# Créer le fichier .env
cat > "$ENV_PATH" << EOF
# Configuration Django - Magic Counter
# Généré automatiquement par setup_env.sh

# Clé secrète Django (ATTENTION : Ne jamais commiter ce fichier !)
SECRET_KEY=$SECRET_KEY

# Mode debug (True pour développement, False pour production)
DEBUG=True

# Hôtes autorisés (séparés par des virgules)
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

echo -e "${GREEN}✅ Fichier .env créé avec succès !${NC}"
echo "   Emplacement : $ENV_PATH"
echo ""
echo "📋 Configuration créée :"
echo "   - SECRET_KEY : ******************** (générée)"
echo "   - DEBUG : True"
echo "   - ALLOWED_HOSTS : localhost,127.0.0.1"
echo ""
echo "============================================================"
echo "Prochaines étapes :"
echo "============================================================"
echo ""
echo "1. Appliquer les migrations :"
echo "   cd magicCounter"
echo "   python3 manage.py migrate"
echo ""
echo "2. Créer un super utilisateur (optionnel) :"
echo "   python3 manage.py createsuperuser"
echo ""
echo "3. Lancer le serveur :"
echo "   python3 manage.py runserver"
echo ""
echo -e "${GREEN}🎉 Le serveur sera accessible sur http://127.0.0.1:8000/${NC}"
echo ""
