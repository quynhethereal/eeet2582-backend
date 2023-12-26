# Setup Instructions

## Prerequisites
- Python 3.6 or higher

## Environment variables setup
1. Copy .env.example to .env
```bash
cd eeet2582_backend && cp .env.example .env
```

## Database setup (Mac)
1. Install openssl
```bash
brew install openssl
```

2. Add path to openssl to bash profile
- For M1: https://stackoverflow.com/a/69871441

3. Install required packages
```bash 
pip3 install virtualenv
```
```bash
pip3 install psycopg
```
4. Create new database (required that postgres is installed)
- Open psql shell
```bash
psql
```

- Create new database
```sql
CREATE DATABASE eeet2582_backend;
```

5. Go back to project directory and run migrations
```bash
poetry install && poetry run manage.py migrate
```

6. Finally, run the server
```bash
poetry run manage.py runserver
```

## Superuser setup
1. Create superuser (I'm using admin as username and password)
```bash
poetry run manage.py createsuperuser
```
2. Go to http://localhost:8000/admin/ and login with the superuser credentials


## Run server in virtual environment using poetry

```bash 
poetry run manage.py runserver
```


## Database setup (Win 11 & 10)
1. Download & install choco package manager by following instruction from this [link](https://chocolatey.org/install).
2. Use choco to install OpenSSL. Please open the powershell in administration mode
```bash
choco install openssl
```

2. Add path to openssl to win environment path (if the path is not added automaticly)
- create new variable named as "OPENSSL_CONF" and add this path C:\Program Files\OpenSSL-Win64\bin\openssl.cfg  as the its value.

3. Install required packages
```bash
pip3 install virtualenv
```
```bash
pip3 install psycopg
```
4. Create new database (required that postgres is installed)
- Open psql shell
```bash
psql -U postgres
```
- if the command isn't recognized, please add C:\Program Files\PostgreSQL\16\bin to the systen environemnt path

- Create new database
```sql
CREATE DATABASE eeet2582_backend;
```

- check if the database is created successfully
```
\l
```
5. Go back to project directory and run migrations

- install poetry dependecy management (if not)

```bash
pip3 install poetry
```
- install the project && migrating the database
```bash
poetry install && poetry run python manage.py migrate
```

6. Finally, run the server
```bash
poetry run python manage.py runserver
```

## Superuser setup
1. Create superuser (I'm using admin as username and password)
```bash
poetry run python manage.py createsuperuser
```
2. Go to http://localhost:8000/admin/ and login with the superuser credentials


## Run server in virtual environment using poetry

```bash 
poetry run python manage.py runserver
```

## run ngrok for Stripe webhook call
1. After runing the server locally on port 8000
2. download the ngrok.exe
3. add authenticated token
```bash
ngrok config add-authtoken 2a1bssHACk98o1MV40hwaWna3TS_NpUqCqMpqfookK7DJaxb
```
4. run ngrok at reserved domain
```bash
 ngrok http --domain smiling-narwhal-remotely.ngrok-free.app 8000
```