#!/usr/bin/env python3
"""
Script de configuration automatique pour Magic Counter
Génère le fichier .env avec les paramètres nécessaires
"""

import os
import sys
from pathlib import Path

def generate_secret_key():
    """Génère une SECRET_KEY Django sécurisée"""
    try:
        from django.core.management.utils import get_random_secret_key
        return get_random_secret_key()
    except ImportError:
        # Fallback si Django n'est pas encore installé
        import secrets
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return ''.join(secrets.choice(chars) for _ in range(50))

def create_env_file():
    """Crée le fichier .env avec la configuration de développement"""

    # Déterminer le chemin du fichier .env
    base_dir = Path(__file__).resolve().parent
    env_path = base_dir / 'magicCounter' / 'magicCounter' / '.env'

    print("=" * 60)
    print("Configuration automatique de Magic Counter")
    print("=" * 60)
    print()

    # Vérifier si le fichier existe déjà
    if env_path.exists():
        print(f"⚠️  Le fichier .env existe déjà à l'emplacement :")
        print(f"   {env_path}")
        print()
        response = input("Voulez-vous le remplacer ? (o/N) : ").lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Opération annulée.")
            return False
        print()

    # Créer le répertoire si nécessaire
    env_path.parent.mkdir(parents=True, exist_ok=True)

    # Générer la SECRET_KEY
    print("🔐 Génération d'une SECRET_KEY sécurisée...")
    secret_key = generate_secret_key()

    # Contenu du fichier .env
    env_content = f"""# Configuration Django - Magic Counter
# Généré automatiquement par setup_env.py

# Clé secrète Django (ATTENTION : Ne jamais commiter ce fichier !)
SECRET_KEY={secret_key}

# Mode debug (True pour développement, False pour production)
DEBUG=True

# Hôtes autorisés (séparés par des virgules)
ALLOWED_HOSTS=localhost,127.0.0.1
"""

    # Écrire le fichier
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)

        print(f"✅ Fichier .env créé avec succès !")
        print(f"   Emplacement : {env_path}")
        print()
        print("📋 Configuration créée :")
        print("   - SECRET_KEY : ******************** (générée)")
        print("   - DEBUG : True")
        print("   - ALLOWED_HOSTS : localhost,127.0.0.1")
        print()
        print("=" * 60)
        print("Prochaines étapes :")
        print("=" * 60)
        print()
        print("1. Appliquer les migrations :")
        print("   cd magicCounter")
        print("   python3 manage.py migrate")
        print()
        print("2. Créer un super utilisateur (optionnel) :")
        print("   python3 manage.py createsuperuser")
        print()
        print("3. Lancer le serveur :")
        print("   python3 manage.py runserver")
        print()
        print("🎉 Le serveur sera accessible sur http://127.0.0.1:8000/")
        print()

        return True

    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier .env :")
        print(f"   {e}")
        return False

def main():
    """Point d'entrée principal"""
    try:
        success = create_env_file()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Opération interrompue par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
