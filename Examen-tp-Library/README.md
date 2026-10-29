# Examen pratique Docker — Mini bibliothèque

## Sujet
Vous devez conteneuriser une petite application de gestion de livres appelée **Mini Bibliothèque**. L'application contient un frontend Nginx et trois microservices backend Python, qui partagent une base de données MySQL.

### Architecture
- **Nginx / Frontend** : sert l'interface web et distribue les requêtes API.
- **Books API** : affiche la liste des livres.
- **Members API** : ajoute et liste les membres.
- **Loans API** : enregistre et liste les emprunts.
- **MySQL** : stocke les livres, membres et emprunts.

## Travail demandé
1. Compléter les Dockerfiles fournis dans `frontend/`, `books/`, `members/`, `loans/` et `database/`.
2. Construire les images Docker.
3. Créer le réseau `library-network`.
4. Démarrer les conteneurs sur ce réseau tel que  
Env DB: 
MYSQL_ROOT_PASSWORD='RootPass123!'   MYSQL_DATABASE='librarydb'  
MYSQL_USER='libraryuser'  
MYSQL_PASSWORD='LibraryPass123!'  
Env books, loans, members:  
DB_HOST=database  
DB_PORT=3306  
DB_NAME=librarydb  
DB_USER=libraryuser  
DB_PASSWORD='LibraryPass123!'  
5. Publier uniquement le frontend sur le port `8080` de l'hôte.
6. Tester l'application et les API graphiquement
7. Challenge final — Dépannage
Une API devient indisponible à la suite d'une erreur de configuration.
Votre mission :
Diagnostiquer l'incident à l'aide de l'interface et des commandes Docker et des logs.  
Identifier et corriger la cause du problème.  
Rétablir le service sans reconstruire inutilement toutes les images.  
Vérifier le bon fonctionnement de l'application.