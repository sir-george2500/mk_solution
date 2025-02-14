# MK Solution

MK Solution is a logistics management system that helps users transport goods seamlessly from one location to another, including international shipments. With MK Solution, users can efficiently move their goods from one country to another.

## Tech Stack
The project is built using the following technologies:
- **Python** (FastAPI) for the backend API.
- **SQLAlchemy** as the Object-Relational Mapper (ORM).
- **PostgreSQL** as the database.
- **Alembic** for database migrations.

## Getting Started

### Clone the Repository
To get started, clone the repository to your local machine:
```bash
git clone git@github.com:sir-george2500/mk_solution.git
```

### Install the dependencies 

```python
pip install -r requirements.txt
```

### Create your Virtual Environment
```
python3 -m venv venv
```

#### Make sure to ask your project Lead for the .env
```bash
 .env
```

### Run Database Migrations
Navigate to the project directory and run the database migrations using Alembic:

```python 
alembic upgrade head
```


### Run the testcases 
```python 
pytest
```
### Start the Server
Start the project using Uvicorn, the ASGI server:


```python
uvicorn app.main:app --reload
```

