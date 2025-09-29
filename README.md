# SearchHub – Script d’archivage Discord (analyse technique)

> ⚠️ Avertissement : Ce script est un **selfbot Discord**.  
> Les selfbots sont contraires aux règles d’utilisation de Discord et peuvent entraîner des sanctions (ban du compte).  
> Ce document a uniquement pour but **d’expliquer le fonctionnement du code**.  
> Ce n’est **pas un guide d’utilisation**.

---

## Présentation

Ce script utilise la librairie **discord.py** en mode `self_bot=True` pour :
- Initialiser un dossier par utilisateur rencontré.
- Sauvegarder les messages envoyés dans les serveurs.
- Télécharger les fichiers joints aux messages.
- Suivre l’activité vocale (connexion, déconnexion, mute, etc.).
- Extraire des informations utilisateur via l’API [discordlookup.mesalytic.moe](https://discordlookup.mesalytic.moe).

Les données sont stockées localement dans le dossier `scrap/` sous forme de fichiers **JSON** et de dossiers.

---

## Dépendances

- Python 3.x
- [discord.py-self](https://pypi.org/project/discord.py-self/) (version modifiée de discord.py)
- requests
- asyncio

---

## Structure des données

Lorsqu’un utilisateur apparaît, le script crée :

scrap/
└── <user_id>/
├── files/ # Fichiers joints téléchargés
├── user/ # Avatar et infos utilisateur
├── messages.json # Historique textuel
└── voice.json # Historique vocal


---

## Événements principaux

- **on_message** :  
  - Sauvegarde du message (serveur, salon, contenu, timestamp).  
  - Téléchargement des pièces jointes.

- **on_voice_state_update** :  
  - Détection des connexions/déconnexions vocales.  
  - Ajout d’entrées (mute, unmute, déplacement).

- **on_ready** :  
  - Nettoyage de la console au lancement.

- **on_disconnect** :  
  - Relance automatique du script en cas de coupure.

---

## Points importants

- Chaque utilisateur est identifié par son **ID Discord**.  
- Le script télécharge automatiquement les **avatars** lorsqu’ils changent.  
- Les fichiers JSON sont mis à jour en continu avec l’historique.  

---

## Remarque

Ce code n’est **pas destiné à un usage en production**.  
Il sert surtout à comprendre comment un selfbot peut intercepter et organiser les données des utilisateurs via l’API Discord (de manière non autorisée).
