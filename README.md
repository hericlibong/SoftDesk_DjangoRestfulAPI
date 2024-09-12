# SoftDesk API

## Présentation
(A compléter)

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre système :

- Version `Python` >= [Python 3.10](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/) (pour la gestion des dépendances)

## Installation

Suivez les étapes ci-dessous pour configurer le projet sur votre machine locale.

1. **Clonez le dépôt** :

   ```bash
   git clone <URL_DU_DEPOT>
   cd nom_du_dossier_du_projet
   ```

2. **Créez un environnement virtuel avec Pipenv :**

    ```bash
    pipenv --python <your version>
    ```

3. **Installez les dépendances:**

    Utilisez la commande suivante pour installer toutes les dépendances nécessaires définies dans le Pipfile :

    ```shell
    pipenv install
    ```

## Démarrage


1. **Activez l'environnement virtuel :**

    Avant de démarrer le projet, vous devez activer l'environnement virtuel :

    ```
    pipenv shell
    ```

2. **Lancez le serveur Django :**

    Une fois l'environnement activé, vous pouvez démarrer le serveur de développement :

    ```
    python manage.py runserver
    ```

Le serveur sera accessible à l'adresse http://127.0.0.1:8000/.


## Utilisation et Documentation

Description de l'utilisation de l'API

## Contributions

Indiquez comment d'autres peuvent contribuer à votre projet.

## License

Indiquez la licence sous laquelle le projet est distribué.