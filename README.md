Finance Tracker - Dockerized Flask App on AWS EC2

Project Overview
  This project is a Finance Tracker application built using Python Flask and SQLite3. 
  It is designed to help users track their income and expenses through a dynamic web dashboard. 
  The application is fully containerized using Docker and deployed on an AWS EC2 (Ubuntu) instance to ensure scalability, consistency, and high availability.

Key Features
  Full-Stack Integration: Combined HTML/CSS/JS frontend with a Flask backend.
  Containerized Environment: Packaged with all dependencies using Docker for seamless deployment.
  Data Persistence: Implemented Docker Volumes to ensure financial records in finance.db are not lost when containers restart.
  Cloud Deployment: Hosted on AWS EC2, making the tracker accessible via a public IP.

  Tech Stack
    Language: Python 3.9 
    Framework: Flask 
    Database: SQLite3 
    Platform: Docker 
    Cloud: AWS EC2 (Ubuntu)

Project Structure
my-project/
├── app.py              # Main Flask Application
├── finance.db          # SQLite Database (Persistent)
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
└── templates/
    └── index.html      # Web Dashboard

Deployment Commands
1. Build the Docker Image
Run this command in the project root to build the image using the Dockerfile:
  docker build -t finance-tracker-app .

2. Run the Container (With Volume & Port Mapping)
This command launches the app on port 8080 and links the database file to the host for persistence:
  docker run -d -p 8080:5000 --name my-finance-container -v "$(pwd):/app" finance-tracker-app

3. Check Logs (For Debugging)
To see the real-time activity of your Flask app:
  docker logs -f my-finance-container

4. Verify Database Records
To view stored transactions directly from the terminal:
  sqlite3 finance.db "SELECT * FROM transactions;"

How to Access
Once the container is running on AWS, access the app at:
  http://<YOUR-EC2-PUBLIC-IP>:8080

1. Docker Installation (AWS EC2 - Ubuntu)
EC2 var Docker install karnyasaathi ya commands vapra:

# Update the package database
sudo apt-get update

# Install Docker
sudo apt-get install docker.io -y

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Check Docker status
sudo systemctl status docker

2. Project Directory and File Creation
Project sathi folder ani files banvanyasathi ya commands vapra:

# Create project directory
mkdir my-project
cd my-project

# Create Flask app file
nano app.py

# Create requirements file
nano requirements.txt

# Create Dockerfile
nano Dockerfile

# Create templates folder and HTML file
mkdir templates
nano templates/index.html

3. Managing Permissions
Docker la file access deny hou naye mhanun ya permissions garjechya aahet:

# Give ownership to the current user
sudo chown ubuntu:ubuntu finance.db

# Provide read/write permissions
sudo chmod 666 finance.db

4. Useful Docker Management Commands
Container manage karnyasaathi ya commands kaamala yetil:

Bash
# List all running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# Stop the container
docker stop my-finance-container

# Remove the container
docker rm my-finance-container

# Remove the Docker image
docker rmi finance-tracker-app

Task            Command
Start Docker:-  sudo systemctl start docker 
Check Status:-  sudo systemctl status docker 
Build Image:-   docker build -t finance-tracker-app . 
Run App:-       docker run -d -p 8080:5000 --name my-finance-container -v "$(pwd):/app" finance-tracker-app 
View Logs:-     docker logs -f my-finance-container

1. Troubleshooting Section
  Port 8080 Access: Ensure that Port 8080 is added to the Inbound Rules of your AWS Security Group.
  Permission Denied: If Docker commands fail, use sudo or add the user to the docker group: sudo usermod -aG docker $USER.
  Database Locked: If the database is locked, restart the container using docker restart my-finance-container

2. Future Scope
  User Authentication: Adding Login/Signup for multiple users.
  Data Visualization: Integrating Chart.js to show spending patterns in graphs.
  Advanced Database: Migrating from SQLite to AWS RDS (MySQL/PostgreSQL) for better scalability.

Final Checklist:
  Public IP Check: Udya presentation chya veli EC2 cha Public IP badalla asu shakto (jar instance stop karun start kela tar). Ekda IP verify kara.
  Screenshot: Tujhya PPT madhe docker ps ani docker logs che screenshots naki dakhva, te proof mhanun kaam kartat.
  Kachra Saaf: Folder madhle te vichtra navache temporary files (085da63...) delete kelet ka te ekda check kara.

CI/CD Pipeline: Implementing GitHub Actions or Jenkins for automated deployment.

Author
Samarth Computer Engineering Student at SPPU
