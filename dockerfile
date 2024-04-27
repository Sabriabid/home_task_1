# Définir l'image de base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les autres fichiers du projet dans le conteneur
COPY . .
RUN chmod +x start.sh  # Assurez-vous que le script est exécutable
# Exposer le port utilisé par l'API
EXPOSE 5000

# Commande pour démarrer l'application (modifiez cela selon vos besoins)
CMD ["./start.sh"]


