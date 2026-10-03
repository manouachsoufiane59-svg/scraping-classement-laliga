# Classement de La Liga — Projet de web scraping

## Présentation

Ce projet utilise Python pour récupérer des données de classement de football sur le site `mercato.fr`, puis générer une page HTML avec les équipes, leur position et leur logo.

Le fichier `index.html` joint est un exemple du résultat produit par le script.

## Fonctionnement

1. Le script envoie une requête à la page de classement de Girona FC.
2. Il analyse le tableau HTML avec BeautifulSoup.
3. Il extrait la position, le nom des équipes et l’adresse de leur logo.
4. Il génère un fichier `index.html` présentant le classement et des éléments visuels complémentaires.

## Technologies

- Python
- `requests`
- BeautifulSoup (`beautifulsoup4`)
- HTML
- CSS

## Utilisation

Installer les dépendances :

```bash
pip install requests beautifulsoup4
```

Lancer le script :

```bash
python "Projet Web.py"
```

Le fichier `index.html` est créé dans le dossier depuis lequel le script est exécuté. Ouvre-le ensuite dans un navigateur pour consulter le résultat.

## Fichiers

- `Projet Web.py` — script de collecte et de génération HTML
- `index.html` — exemple de page générée

## Limites et améliorations possibles

Le script dépend de la structure HTML du site source, qui peut changer. Les images et certains médias sont chargés depuis des sites externes. Le fichier vidéo attendu par la page n’est pas inclus dans les fichiers fournis.
