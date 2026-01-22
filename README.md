![Logo du projet](cloud.png)


![Logo du projet](architecture-projet.jpeg)



# ☁️ VidP : Pipeline Hybride de Traitement Vidéo

### **Groupe 8 - Architecture Cloud & Edge**

**VidP** est un pipeline automatisé conçu pour le traitement, l'analyse et la gestion de flux vidéos. Ce système repose sur une architecture **hybride** : le traitement lourd et l'extraction de métadonnées s'effectuent via des micro-services conteneurisés, tandis que le stockage et la diffusion sont centralisés sur AWS (S3 & DynamoDB).

---

## 🚀 Fonctionnalités

* **Downscaling** : Compression et redimensionnement automatique des vidéos pour optimiser le stockage.
* **Analyse de contenu** : Détection automatique de la langue parlée.
* **Sous-titrage** : Génération de fichiers de sous-titres basés sur l'audio.
* **Dashboard Analytics** : Interface web v1.1 permettant de visualiser l'historique des traitements et de lire les vidéos directement depuis le Cloud.

---

## 🏗️ Architecture des Composants

### 1. Pipeline de Traitement (Local/Edge)

Le pipeline est orchestré par **Docker Compose** et comprend les modules suivants :

* **Downscale Pod** : Réduit la résolution des fichiers `.mp4`.
* **LangIdent Pod** : Identifie la langue pour la segmentation.
* **Subtitle Pod** : Produit les fichiers de transcription.
* **Animal Detect Pod** : (En cours de développement) - Détection d'objets et d'animaux.

### 2. Infrastructure Cloud (AWS)

* **Amazon EC2** : Héberge le serveur web Flask et l'interface utilisateur.
* **Amazon S3** : Stockage persistant des vidéos traitées et des fichiers originaux.
* **Amazon DynamoDB** : Base de données NoSQL stockant les métadonnées (ID, Langue, Transcription, URL S3).

---

## 🛠️ Guide d'Exécution

### Partie 1 : Traitement Local (Docker)

1. Placer une vidéo `.mp4` dans le dossier `/videos`.
2. Lancer le pipeline :
```bash
docker-compose up -d --build

```


3. Les résultats (vidéos compressées et logs) sont générés dans le dossier partagé `/data`.

### Partie 2 : Accès au Dashboard (Cloud)

Le dashboard est configuré pour afficher les analyses consolidées sans permettre l'upload direct par l'utilisateur final (sécurisation du pipeline).

1. **Connexion à l'instance EC2** :
```bash
cd ACCES_EC2
chmod 400 notreprojet.pem
ssh -i "notreprojet.pem" ubuntu@<IP_INSTANCE_EC2>

```


2. **Lancement du service Web (v1.1)** :
```bash
cd ~/VidP-Pipeline-Hybride-Groupe8
docker-compose up -d --build website

```


3. **Consultation** : Accéder à l'interface via `http://<IP_EC2>:5000` (Utiliser le mode navigation privée pour éviter le cache).

## 👥 Équipe - Groupe 8

* TENG KANA Arielle
* TEDOU ZANDJIO William
* ESSOMBA OLAMA Sévérin
* NDADEM Donald
