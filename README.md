
# SoftDesk API


## Présentation
Bienvenue dans l'API SoftDesk. Ce projet est une plateforme de gestion de projets permettant aux utilisateurs de créer des projets, des problèmes (issues), des commentaires, et de collaborer avec des contributeurs.

## Table des matières

- [Installation](#installation)
- [Accès API](#accès-api)
- [Authentification](#authentification)
- [Principaux Endpoints](#principaux-endpoints)
- [Documentation API](#documentation-api)
- [Tests](#tests)
- [Contribuer](#contribuer)


## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre système :
- [Version Python 3.12.6 (ou compatible)](https://www.python.org/downloads/release/python-3126/)
- [Pipenv (pour la gestion des dépendances)](https://pipenv.pypa.io/en/latest/)


## Installation

Pour installer et configurer ce projet sur votre machine locale :

1. Clonez le dépôt GitHub :

```bash
git clone <url_du_repository>
cd SoftDesk_DjangoRestfulAPI
   ```

2. Installez les dépendances avec pipenv :


```bash
pipenv install --dev
```

3. Activez l'environnement virtuel :

```bash
pipenv shell
```

## Démarrage

1. **Modifier le fichier `.env`**

Aller dans la racine du projet : 

```bash
cd src/ApiSoftDesk/
```

- Renommer le fichier : Renommez le fichier `.env.sample` en `.env` dans le répertoire de votre projet.

- Ouvrir le fichier `.env` : Ouvrez le fichier `.env` avec un éditeur de texte.

- Configurer la clé secrète : Remplacez <your_secret_key_here> par une clé secrète Django forte et unique.


2. **Générer une clé secrète Django** : 
    

    - Vous pouvez utiliser des outils en ligne tels que [Djecrety](https://djecrety.ir/). 
    Ce site génère une clé secrète Django sécurisée que vous pouvez simplement copier et coller dans votre fichier `.env`.


    - Assurez-vous que les valeurs des autres variables, comme <DEBUG> et <ALLOWED_HOSTS>, sont appropriées pour votre environnement de développement.

    - Sauvegarder les modifications : Enregistrez le fichier `.env` après avoir effectué les modifications nécessaires.

    - Ce fichier ne doit pas être ajouté à votre dépôt Git. Assurez-vous qu'il est bien listé dans votre .gitignore pour éviter toute exposition accidentelle de vos configurations.


4. Démarrez le serveur de développement local :

Dans src : 

```bash

python manage.py runserver
```

Votre application devrait maintenant être disponible à l'adresse : http://127.0.0.1:8000/


## Accès API

L'API SoftDesk est disponible à l'adresse `/api/v1/`. L'accès à certains endpoints nécessite un token d'authentification (JWT).
Obtenir un token d'authentification

### Outil de test recommandé

Pour tester les requêtes et interactions avec l'API, Postman est recommandé. Vous pouvez télécharger et configurer Postman ici : 
[Postman](https://www.postman.com/downloads/)

### Accès administrateur préconfiguré

Pour tester l'API avec des privilèges d'administrateur, vous pouvez utiliser les identifiants suivants :

- **Nom d'utilisateur** : `opc-admin`
- **Mot de passe** : `opc-password`

Ces identifiants vous permettront d'accéder à toutes les fonctionnalités administratives de l'API sans avoir à créer un superuser.

---

### Obtention d'un Token JWT

#### 1. Obtenir un Token JWT

Utilisez le endpoint suivant pour obtenir un token JWT après vous être authentifié avec vos identifiants :

- **URL** : `/api/v1/token/`
- **Méthode** : `POST`
- **Données** :

```json
{
    "username": "votre_nom_utilisateur",
    "password": "votre_mot_de_passe"
}
```

La réponse vous fournira deux tokens : un access token et un refresh token.

### 2. Rafraîchir votre Token

 
 Utilisez le endpoint suivant pour rafraîchir votre token JWT en utilisant le refresh token obtenu précédemment :

- **URL** : `/api/v1/token/refresh/`
- **Données** :

{
 "refresh": "votre_refresh_token"
}


La réponse vous fournira un nouveau access token.

## Principaux Endpoints

Voici une liste des principaux endpoints de l'API SoftDesk :

### Projets

- **Liste des projets**
  - **URL** : `/api/v1/projects/`
  - **Méthode** : `GET`
  - **Description** : Récupère la liste de tous les projets.

- **Créer un projet**
  - **URL** : `/api/v1/projects/`
  - **Méthode** : `POST`
  - **Description** : Crée un nouveau projet.
  - **Données** :

  ```json
  {
      "title": "Nom du projet",
      "description": "Description du projet",
      "type": "ios"
  }
  ```

### Issues

- **Liste des issues**
  - **URL** : `/api/v1/projects/{project_id}/issues/`
  - **Méthode** : `GET`
  - **Description** : Récupère la liste de toutes les issues pour un projet donné.

- **Créer une issue**
  - **URL** : `/api/v1/projects/{project_id}/issues/`
  - **Méthode** : `POST`
  - **Description** : Crée une nouvelle issue pour un projet donné.
  - **Données** :

  ```json
    {
    "title": "Nouvelle Issue",
    "description": "Description de l'issue",
    "tag": "bug",
    "priority": "high",
    "status": "todo",
    "assigned_to": 23,
    "author":22,
    "project":25
    }
  ```

### Commentaires

- **Liste des commentaires**
  - **URL** : `/api/v1/issues/{issue_id}/comments/`
  - **Méthode** : `GET`
  - **Description** : Récupère la liste de tous les commentaires pour une issue donnée.

- **Créer un commentaire**
  - **URL** : `/api/v1/issues/{issue_id}/comments/`
  - **Méthode** : `POST`
  - **Description** : Crée un nouveau commentaire pour une issue donnée.
  - **Données** :

  ```json
  {
      "description": "Contenu du commentaire"
  }
  ```




## Utilisation et Documentation

La documentation complète de l'API est disponible via les interfaces Swagger et Redoc :

- Swagger UI : Swagger | http://127.0.0.1:8000/swagger/
- Redoc : Redoc  | http://127.0.0.1:8000/redoc/




Ces interfaces vous permettent d'explorer tous les endpoints disponibles et de tester les différentes fonctionnalités directement via une interface interactive.

## Contributions

Indiquez comment d'autres peuvent contribuer à votre projet.

## License

Indiquez la licence sous laquelle le projet est distribué.