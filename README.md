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

