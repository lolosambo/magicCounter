# Guide de Déploiement Local - Magic Counter

Ce guide vous explique comment déployer et exécuter le projet Magic Counter sur votre machine locale.

## Prérequis

- Python 3.8 ou supérieur (testé avec Python 3.11)
- pip (gestionnaire de paquets Python)
- Git

## Étapes d'installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd magicCounter
```

### 2. Créer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet :

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales installées sont :
- Django 4.0.6
- BeautifulSoup4 (pour le parsing HTML)
- django-livereload-server (pour le rechargement automatique en développement)

### 4. Configurer les variables d'environnement

Créez un fichier `.env` dans le répertoire `magicCounter/magicCounter/` :

```bash
cd magicCounter
mkdir -p magicCounter
touch magicCounter/.env
```

Ajoutez le contenu suivant dans le fichier `.env` :

```env
SECRET_KEY=votre-cle-secrete-django-ici-changez-la
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Important** : Pour générer une SECRET_KEY sécurisée, vous pouvez utiliser :

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Créer la base de données

Le projet utilise SQLite par défaut. Créez les tables de la base de données :

```bash
# Depuis le répertoire magicCounter (où se trouve manage.py)
cd magicCounter
python3 manage.py migrate
```

### 6. Créer un super utilisateur (optionnel)

Pour accéder à l'interface d'administration Django :

```bash
python3 manage.py createsuperuser
```

Suivez les instructions pour créer votre compte administrateur.

### 7. Collecter les fichiers statiques

```bash
python3 manage.py collectstatic --noinput
```

### 8. Lancer le serveur de développement

```bash
python3 manage.py runserver
```

Le serveur sera accessible à l'adresse : **http://127.0.0.1:8000/**

L'interface d'administration sera disponible à : **http://127.0.0.1:8000/admin/**

## Structure du projet

```
magicCounter/
├── magicCounter/          # Répertoire principal du projet Django
│   ├── magicCounter/      # Configuration Django
│   │   ├── settings.py    # Paramètres du projet
│   │   ├── urls.py        # Configuration des URLs
│   │   └── .env           # Variables d'environnement (à créer)
│   ├── cards/             # Application de gestion des cartes
│   ├── user/              # Application de gestion des utilisateurs
│   ├── manage.py          # Script de gestion Django
│   ├── staticfiles/       # Fichiers statiques collectés
│   └── mediafiles/        # Fichiers média uploadés
├── requirements.txt       # Dépendances Python
└── README.md
```

## Commandes utiles

### Lancer le serveur avec live reload
```bash
python3 manage.py livereload
```

### Créer de nouvelles migrations
```bash
python3 manage.py makemigrations
```

### Appliquer les migrations
```bash
python3 manage.py migrate
```

### Lancer le shell Django
```bash
python3 manage.py shell
```

## Dépannage

### Erreur "SECRET_KEY" non définie
Assurez-vous que le fichier `.env` existe dans `magicCounter/magicCounter/.env` et contient une valeur pour SECRET_KEY.

### Erreur d'import Django
Vérifiez que votre environnement virtuel est activé et que les dépendances sont installées :
```bash
pip install -r requirements.txt
```

### Port déjà utilisé
Si le port 8000 est déjà utilisé, spécifiez un autre port :
```bash
python3 manage.py runserver 8080
```

## Configuration pour la production

Pour un déploiement en production, modifiez le fichier `.env` :

```env
SECRET_KEY=cle-secrete-tres-complexe-et-unique
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

**Important** : Ne jamais commiter le fichier `.env` dans Git. Il est déjà dans `.gitignore`.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur le dépôt du projet.
