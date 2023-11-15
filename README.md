# Setup Instructions

## Prerequisites
- Python 3.6 or higher

## Environment variables setup
1. Copy .env.example to .env
```bash
cd eeet2582_backend && cp .env.example .env
```

## Database setup 
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
poetry manage.py runserver
```

## Superuser setup
1. Create superuser (I'm using admin as username and password)
```bash
poetry manage.py createsuperuser
```
2. Go to http://localhost:8000/admin/ and login with the superuser credentials


## Run server in virtual environment using poetry

```bash 
poetry manage.py runserver
```