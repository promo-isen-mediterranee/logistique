#!/bin/bash

python3 /Service_Logistique/scrypt_bot_alert.py

# Fichier à vérifier
file_path="/tmp/dead_line.tmp"

# Lire la valeur du fichier
if [ -f "$file_path" ]; then
  value=$(cat "$file_path")
else
  echo "Fichier $file_path non trouvé. Utilisation de la valeur par défaut 'F'."
  value="F"
fi

crontab_file="cron_task"

# Définir le crontab en fonction de la valeur lue
if [ "$value" == "F" ]; then
  echo "0 10 * * * /Service_Logistique/check_deadline.sh" >  $crontab_file
else if [ "$value" == "T" ]; then
  echo "0 */2 * * * /Service_Logistique/check_deadline.sh" >  $crontab_file
fi

# Appliquer la crontab
crontab  $crontab_file
