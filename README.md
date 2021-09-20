![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)

![alt text](https://github.com/jpvincent1980/P9/blob/main/Screenshot.png)

# Gestionnaire de tournois d'échecs (Projet P4)

Cette application va vous permettre de gérer les résultats d'un tournoi d'échecs organisé selon le système Suisse. 

Il vous permettra de suivre les différentes étapes d'un tournoi (de sa création à la génération de son classement final) de manière décorrélée, c'est-à-dire que vous pourrez créer un tournoi, fermer l'application, puis rouvrir l'application afin d'inscrire un ou plusieurs joueurs au tournoi, fermer l'application, rouvrir l'application et entrer les résultats d'un match, etc.)

Chaque tournoi se joue en quatre rounds et doit avoir huit joueurs pour démarrer. Les rounds et les matchs associés sont automatiquement générés par l'application selon le système Suisse.

## Pré-requis

Une version de Python >= 3.0 doit être installée sur votre poste.

## Installation

Depuis un terminal de type GitBash, déplacez-vous dans le répertoire dans lequel vous souhaitez récupérer le script ainsi que les fichiers *readme.md* et *requirements.txt*  et saisissez la commande ci-dessous:

``git clone https://github.com/jpvincent1980/P4``

Une fois les fichiers téléchargés sur votre poste de travail, vous devez au préalable créer et activer un environnement virtuel sur votre poste.
Pour se faire, suivez les étapes suivantes :
1. Depuis votre terminal et toujours dans le même répertoire que précédemment, créer un environnement virtuel en saisissant la commande suivante:
  `` python -m venv env`` (``env`` sera le nom de votre environnement virtuel)
  

2. Activez votre environnement virtuel en saisissant la commande suivante:
   
   *sous Windows* -> ``env/Scripts/activate.bat``
   
   *sous Mac/Linux* -> ``source/env/bin/activate``
   

Lorsque votre environnement virtuel est activé, installez les modules Python nécessaires à la bonne exécution du script grâce au fichier *requirements.txt* précédemment téléchargé en saisissant la commande ci-dessous toujours depuis le terminal:

``pip install -r requirements.txt``


Flake8:

Flake8 faisant partie des modules du fichier ``requirements.txt``, 
celui-ci sera installé dans votre environnement virtuel. Vous pourrez 
générer un nouveau rapport flake8 en saisissant la commande ``flake8`` dans votre terminal depuis le répertoire où vous avez enregistré le 
projet.

## Démarrage

Depuis votre terminal de commande et toujours depuis le répertoire dans lequel les fichiers ont été téléchargés, saisissez la commande suivante:

``python main.py``

Le menu principal vous permettra de choisir entre la gestion d'un tournoi et l'affichage ou l'export de listes d'informations.

**Gestion d'un tournoi**:

La gestion d'un tournoi se décompose selon les étapes suivantes:

1) Création d'un tournoi
2) Inscription de huit joueurs au tournoi
    - si un joueur ne figure pas dans la base de données, il est nécessaire de le créer au préalable afin de pouvoir l'inscrire au tournoi;
    - lorsque le huitième et dernier joueur est inscrit, l'application crée automatiquement le premier round du tournoi et génère ses matchs selon le système de tournoi Suisse.
    
3) Entrée des résultats des matchs du tournoi
    - lorsque les résultats du dernier match d'un round sont rentrés, l'application génère automatiquement un nouveau round, et ceci jusqu'au quatrième round du tournoi;
    - lorsque les résultats du dernier match du quatrième round sont rentrés, le tournoi est terminé.

**Affichage/Export d'une liste**:

Vous pouvez choisir d'afficher ou d'exporter une liste parmi les suivantes:
1) *Liste de tous les joueurs*
2) *Liste de tous les joueurs d'un tournoi*, 
3) *Liste de tous les tournois*,
4) *Liste de tous les tours d'un tournoi*,
5) *Liste de tous les matchs d'un tournoi*,
6) *Classement d'un tournoi*

Si vous choisissez d'exporter une liste, celle-ci sera exportée dans un fichier "export.csv" située à la racine du projet.


## IDE utilisé

[PyCharm Community Edition](https://www.jetbrains.com/fr-fr/pycharm/)

## Auteur

[Jean-Philippe Vincent](https://twitter.com/JeanPhilippeV15)