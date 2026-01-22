# ☁️ VidP : Pipeline Hybride de Traitement Vidéo

### Groupe 8 - Architecture Cloud & Edge

VidP est un pipeline automatisé conçu pour le traitement, l'analyse et la gestion de flux vidéos. Ce système repose sur une architecture hybride : le traitement lourd et l'extraction de métadonnées s'effectuent via des micro-services conteneurisés, tandis que le stockage et la diffusion sont centralisés sur AWS (S3 & DynamoDB).

## Fonctionnalités

* **Downscaling** : Compression et redimensionnement automatique des vidéos pour optimiser le stockage.
* **Analyse de contenu** : Détection automatique de la langue parlée.
* **Sous-titrage** : Génération de fichiers de sous-titres basés sur l'audio.
* **Dashboard Analytics** : Interface web v1.4 permettant de visualiser l'historique des traitements et de lire les vidéos directement depuis le Cloud.

## Architecture des Composants

### 1. Pipeline de Traitement (Local/Edge)

Le pipeline est orchestré par Docker Compose et comprend les modules suivants :

* **Downscale Pod** : Réduit la résolution des fichiers .mp4.
* **LangIdent Pod** : Identifie la langue pour la segmentation.
* **Subtitle Pod** : Produit les fichiers de transcription.
* **Animal Detect Pod** : (En cours de développement) - Détection d'objets et d'animaux.

### 2. Infrastructure Cloud (AWS)

* **Amazon EC2** : Serveur virtuel qui héberge le site web.
* **Amazon S3** : Espace de stockage en ligne pour les vidéos.
* **Amazon DynamoDB** : Base de données pour les informations textuelles (langue, transcription).

## Guide d'Exécution

### Partie 1 : Traitement Local (Docker)

1. Placer une vidéo .mp4 dans le dossier `/videos`.
2. Lancer le pipeline avec la commande :
`docker-compose up -d --build`
3. Les résultats sont générés dans le dossier partagé `/data`.

### Partie 2 : Accès au Dashboard (Cloud sur AWS)

Pour administrer le serveur à distance, nous utilisons le protocole SSH.

1. **Préparer la clé de sécurité** :
Le fichier `notreprojet.pem` est votre "clé numérique" privée. Sans elle, l'accès au serveur est impossible. Avant de l'utiliser, il faut limiter ses droits pour que le système l'accepte :
`chmod 400 notreprojet.pem`
2. **Se connecter au serveur (SSH)** :
Utilisez la commande suivante en remplaçant `<IP_INSTANCE_EC2>` par l'adresse IP publique de votre serveur (ex: 54.12.34.56) :
`ssh -i "notreprojet.pem" ubuntu@<IP_INSTANCE_EC2>`
*Note : `ubuntu` est l'identifiant par défaut de la machine, et `-i` indique au terminal d'utiliser votre fichier de clé pour s'identifier.*
3. **Lancer le site web sur le serveur** :
Une fois connecté, entrez dans le dossier du projet et démarrez le conteneur :
`cd ~/VidP-Pipeline-Hybride-Groupe8`
`docker-compose up -d --build website`
4. **Consulter les résultats** :
Ouvrez votre navigateur et tapez l'adresse IP du serveur suivie du port 5000 (ex: `http://54.12.34.56:5000`).

## Équipe - Groupe 8

* TENG KANA Arielle
* TEDOU ZANDJIO William
* ESSOMBA OLAMA Sévérin
* NDADEM Donald
