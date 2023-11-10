# udacity-capstone Overview
This is final project for Udacity Full stack development nanodegree.
Deployment url:
https://manhvgt-udacity-capstone.onrender.com

## Project directory overview;
| udacity-capstone
| -- main.py: main module
| -- main_test.py: local testing module
| -- error.py: for error handling
| -- README.md: this file
| -- README_API.md: Detail for API (including API testing information)
| -- requirements.txt: requirement package to be install
| -- auth
| ---- __init__.py
| ---- auth.py: define and functional for authentication handling
| -- database
| ---- __init__.py
| ---- models.py: define and functional for database handling
| -- others related file for environtent


## Database design : Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models:
Movies with attributes title and release date
Actors with attributes name, age and gender

### Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

### Roles:
- Casting Assistant
    Can view actors and movies
- Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies
- Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database

# Code check-in and Evironment setup
## Code checkin
Github repo:
https://github.com/manhvgt/udacity-capstone

## Setup Database and Installing Dependencies (For Local)
### Python 3.11.6
Follow instructions to install the version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### PIP Dependencies

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server (Local)
From within the `udacity-capstone` directory first ensure you are working using your created virtual environment.
Create an `.env` file for environement variable. See detail in `sample_env.txt` file.

Each time you open a new terminal session, run:

```bash
python3 main.py
```
or

```bash
gunicorn main:app
```

# API document
Check `README_API.md`


# Live server testing method

!! NOTE: Currently manual testing method only be provided

## Requirement software
- Postman: Follow instruction in the website to download and install: https://www.postman.com/downloads/
- Web browser: Any web browser. (Not require) 

## Testing method
- Download `capstone.postman_collection.json` file and inport to Postman
- Sample HTTP request and data is provided in collection
- Authentication tokens are preset based on Roles for RBAC. Tokens are valid for 24h from latest update of file `capstone.postman_collection.json`.
  Please request for updating if tokens are expired.
- Proceeding test by manual runing each request in Postman collection
  !! NOTE: There is some test with failed result base on RBAC. Please refer to Roles section in this document for details
