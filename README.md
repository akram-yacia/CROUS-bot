# Alertes CROUS Lille sur Telegram

Ce watcher vérifie la recherche CROUS de Lille toutes les 10 minutes avec GitHub Actions et envoie un message Telegram pour chaque nouvelle URL de logement repérée. Le premier lancement crée une référence des annonces déjà visibles; les alertes concernent les annonces repérées ensuite.

## Mise en place

1. Crée un bot Telegram avec [@BotFather](https://t.me/BotFather), envoie `/newbot` et garde le token privé.
2. Ouvre ton nouveau bot et appuie sur **Démarrer**.
3. Envoie un message au bot. Ouvre ensuite `https://api.telegram.org/bot<TON_TOKEN>/getUpdates` dans ton navigateur et relève `message.chat.id`. Ne partage pas cette URL : elle contient ton token.
4. Crée un dépôt GitHub privé et ajoute les fichiers de ce dossier, en conservant le chemin `.github/workflows/watch.yml`.
5. Dans **Settings → Secrets and variables → Actions**, ajoute `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID` comme secrets.
6. Dans **Settings → Actions → General → Workflow permissions**, active **Read and write permissions** pour sauvegarder les annonces déjà vues.
7. Dans **Actions**, lance **CROUS Lille watcher → Run workflow**. La première exécution établit la référence; les suivantes détectent les nouvelles annonces.

GitHub peut décaler les exécutions planifiées. Les secrets ne sont pas enregistrés dans le code.
