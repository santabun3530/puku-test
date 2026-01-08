# Postgres install if postgress is not present
```
sudo apt install -y postgresql postgresql-contrib
sudo systemctl status postgresql
```

## create database
```
sudo -u postgres psql
CREATE DATABASE recipe_db;
CREATE USER admin WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE recipe_db TO admin;
ALTER USER admin CREATEDB;
\q
```
## Bydefault we can access postgres with localhost
Just like 
```
psql -h localhost -U admin -d recipe_db
```

## But if we are access postgres with host ip 
we have to changes two separate places

### 1.1 One is postgresql.config for Server configuration
we have to change of listen_addresses 'localhost' to '*'
```
sudo vim /etc/postgresql/*/main/postgresql.conf
```
### 1.2 Two is pg_hba.conf for client authentication 
we have to added host ip into pg_hba.conf
```
sudo vim /etc/postgresql/*/main/pg_hba.conf

host    all             all             hostIP/32      md5
```
After two file changes then we have to used this command. 
```
sudo systemctl restart postgresql@*-main.service
```
### Create table 
1. Go to database directory.
2. Then table create with command
```
psql -h 192.168.121.195 -U admin -d recipe_db -f init.sql

\dt
```
# OS dependencies 
```
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx nodejs npm
```

## Now create .env.linux 
```
# Database Configuration
POSTGRES_DB=recipe_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_HOST=192.168.121.195
POSTGRES_PORT=5432

# Service URLs (for inter-service communication)
USER_SERVICE_URL=http://192.168.121.195:8001
RECIPE_SERVICE_URL=http://192.168.121.195:8002
RATING_SERVICE_URL=http://192.168.121.195:8003

# Database URL
DATABASE_URL=postgresql://admin:password@192.168.121.195:5432/recipe_db
```
# Service deploy 

## User service
```
cd user-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
### Now set up for background process with systemd
Create a file user.service
```
sudo vim /etc/systemd/system/user.service
```
Now set up configuration 
```
[Unit]
Description=User Service
After=network.target postgresql.service

[Service]
User=vagrant
WorkingDirectory=/home/vagrant/recipe-app-linux/puku-app/user-service
EnvironmentFile=/home/vagrant/recipe-app-linux/puku-app/.env.linux
ExecStart=/home/vagrant/recipe-app-linux/puku-app/user-service/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```
After that enable that service
```
sudo systemctl enable user.service
sudo systemctl restart user.service
sudo systemctl status user.service
```

## Recipe service
```
cd recipe-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
### Now set up for background process with systemd
Create a file recipe.service
```
sudo vim /etc/systemd/system/recipe.service
```
Now set up configure file
```
[Unit]
Description=Recipe Service
After=network.target postgresql.service

[Service]
User=vagrant
WorkingDirectory=/home/vagrant/recipe-app-linux/puku-app/recipe-service
EnvironmentFile=/home/vagrant/recipe-app-linux/puku-app/.env.linux
ExecStart=/home/vagrant/recipe-app-linux/puku-app/recipe-service/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8002
Restart=always

[Install]
WantedBy=multi-user.target
```
After that enable that service
```
sudo systemctl enable recipe.service
sudo systemctl restart recipe.service
sudo systemctl status recipe.service
```

## Rating service
```
cd rating-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
### Now set up for background process with systemd
Create a file rating.service
```
sudo vim /etc/systemd/system/rating.service
```
Now set up configure file
```
[Unit]
Description=Rating Service
After=network.target postgresql.service

[Service]
User=vagrant
WorkingDirectory=/home/vagrant/recipe-app-linux/puku-app/rating-service
EnvironmentFile=/home/vagrant/recipe-app-linux/puku-app/.env.linux
ExecStart=/home/vagrant/recipe-app-linux/puku-app/rating-service/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8003
Restart=always

[Install]
WantedBy=multi-user.target
```

After that enable that service
```
sudo systemctl enable rating.service
sudo systemctl restart rating.service
sudo systemctl status rating.service
```
## Frontend Service
```
cd frontend
npm install
npm run build
sudo cp -r build/* /var/www/frontend/

```
### Set up nginx as LB 
```
sudo vim /etc/nginx/sites-available/recipe-app.conf
```
Configuration file 
```
server{
listen 80;    
server_name _;

    # Frontend (React)
    root /var/www/frontend;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    # User service
    location /api/users/ {
        proxy_pass http://192.168.121.195:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Recipe service
    location /api/recipes/ {
        proxy_pass http://192.168.121.195:8002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Rating service
    location /api/ratings/ {
        proxy_pass http://192.168.121.195:8003/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
### After nginx configuration we need to restart nginx
```
sudo ln -s /etc/nginx/sites-available/recipe-app.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
