<h1>Installation</h1>

<h3>Setting Up Database </h3>
<details><summary><b>Instructions</b></summary>

1. Install <a url=https://www.postgresql.org/download/>PostgreSQL</a> if not already installed.
2. Open a terminal and type 
```sh 
sudo -u postgres psql
```
3. Create database called: cinema_db: 
```sh
CREATE DATABASE cinema_db;
```
4. Enter the database:
```sh 
\c cinema_db
```
5. Create a user called db_manager with a password: 
```sh
CREATE USER db_manager WITH PASSWORD '123456';
```
6. Create priviliges to user: 
```sh
GRANT ALL PRIVILEGES ON DATABASE cinema_db TO db_manager;
```
7. If Postgres permission denied for schema public. Input into terminal: 
```sh
GRANT ALL ON SCHEMA public TO db_manager;
```

EXTRA: 
- To remove database: 
```sh
DROP DATABASE cinema_db;
```
- To remove user: 
```sh
DROP USER db_manager;
```
</details>

<h3>Setting Up Flask</h3>
<details><summary><b>Instructions</b></summary>

1. Check for Python 3.10 or above via the terminal with: 
```sh
python --version
```
If not install <a url=https://www.python.org/downloads/>Python</a>

2. Clone repository in the terminal: 
```sh
git clone ...
```
3. Activate the virtual environment inside the cloned repository: 
```sh
source .venv/bin/activate
```
4. Install requirements: 
```sh
pip install -r requirements.txt
```
5. Place details of database in ```.env.sample``` and rename it to ```.env```:
```sh
DATABASE_URI= ...
JWT_SECRET_KEY= ...
```
6. To create tables: 
```sh
flask db create
```
7. To seed tables: 
```sh
flask db seed
```
8. To drop tables:
```sh
flask db drop
```
9. To run server:
```sh
flask run
```

</details>


<h2>R7	Detail any third party services that your app will use</h2>

- SQLAlchemy:
SQLAlchemy is a Python library that acts as an object-relational mapping (ORM) tool. It enables interaction with the API's database without the necessity of using direct SQL queries. By defining models as Python classes, SQLAlchemy facilitates tasks such as table creation, population, modification, and deletion within the database. It also supports 

- Marshmallow:
Marshmallow is a Python library designed for the serialization and deserialization of data within the API. It allows for the conversion of complex data types, such as Python objects, to and from formats like JSON which is suitable for transmission over networks. Marshmallow employs schemas containing fields that define the structure of data during serialization or deserialization. These fields may include validation rules to ensure that the data meets specified criteria, ensuring data integrity and consistency in the API.

- JWT (Bearer):
JSON Web Tokens (JWT) is used for customer identification within the API. JWT generates a token from customer information that uniquely identifies the customer without the need to store their session information.
