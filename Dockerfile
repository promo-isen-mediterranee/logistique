FROM python:3.12


###############################
#  Variables d'environnement  #
###############################

# Base de donnée
ENV DB_HOST=logistisen_db
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=logistisen_db

ENV API_EVENT=http://10.89.0.21:5000/event
ENV API_STOCK=http://10.89.0.22:8000/stock
ENV API_USER=http://10.89.0.23:5050/auth

ENV BYPASS_TOKEN=v2Fq5EoogcM0F7L2dtvZ9KZNaYpdfdx7

###############################
#  Configuration de l'image   #
###############################

# Création du répertoire de travail
WORKDIR /Service_Logistique

# Copie des fichiers de configuration
COPY ./requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Expose le port 5200
EXPOSE 5200

# Spécifie la commande à exécuter
CMD ["python3", "main.py"]