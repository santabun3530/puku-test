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
### Create table 
1. Go to database directory.
2. Then table create with command
```
psql -h localhost -U admin -d recipe_db -f init.sql
```

