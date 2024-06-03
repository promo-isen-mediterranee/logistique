# Base image
FROM python:3.12

###############################
#  Environment Variables      #
###############################

# Database
ENV DB_HOST=logistisen_db
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=logistisen_db

ENV API_EVENT=http://api_event:5000/event
ENV API_STOCK=http://api_stock:8000/stock
ENV API_USER=http://api_auth:5050/auth

###############################
#  Image Configuration        #
###############################

# Create working directory
WORKDIR /Service_Logistique

# Copy configuration files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy scripts
COPY check_deadline.sh check_deadline.sh

# Give necessary permissions
RUN chmod +x check_deadline.sh

# Make sure cron is started in the background
RUN touch /var/log/cron.log

# Add crontab file
COPY cron_task /etc/cron.d/cron_task
RUN chmod 0644 /etc/cron.d/cron_task
RUN crontab /etc/cron.d/cron_task

# Copy the code
COPY . .

# Expose port 5200
EXPOSE 5200

# Start cron and your application
CMD cron && tail -f /var/log/cron.log & python3 main.py