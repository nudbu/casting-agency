# Casting Agency

This is the Udacity Capstone Project for the Full Stack Program.

The project is a casting agency API, that simplifies the process of matching actors and movies.

## Getting Started

The API is implemented with Python 3.8. and the Flask framework.
It  follows REST principles, data is formatted in JSON

To test the API, it is deployed on Heroku at: https://casting-agency-7492.herokuapp.com

Authentication is realized, using RBAC, with the third party service _Auth0_.

### Installing Dependencies

Create a virtual environment in the project directory, and activate it

```bash
python -m venv venv
venv\Scripts\activate
```
Next, install python dependencies with:
```
pip install -r requirements.txt
```

To run the backend set the FLASK_APP environment variable, and activate development mode
```bash
$env:FLASK_APP = ".\backend\entrypoint.py"

$env:FLASK_ENV = "development"

flask run
```


## Testing

Tests are implemented with the Python Unit testing framework _Unittest_

Each endpoint is tested for correct behaviour with each role.

Run the tests with:
```
python .\test_casting_api.py
```


## Deployment

The Project is deployed on Heroku at: https://casting-agency-7492.herokuapp.com

A Procfile is included, that is used to specify the entrypoint to heroku.

To deploy the application on heroku:

Login:
```
heroku login
```

create an app:
```
heroku create my-new-app
```

deploy code:
```
git push heroku master
```


## API Reference

### Getting Started
- Base URL: 
  - For local development Flask default URL is `http://127.0.0.1:5000/`
  - On Heroku: https://casting-agency-7492.herokuapp.com


- Authentication

Authentication is implemented with a third party service: Auth0.

JWT (Bearer) Tokens are used after logging in with Auth0.

There are 3 roles with different permission sets:

  - Assistant
    - get:actors
    - get:movies

  - Director
    - assistant permissions +
    - add:actors
    - delete:actors
    - patch:actors
    - patch:movies

  - Producer
    - director permissions +
    - add:movies
    - delete:movies
    

Test Tokens for each role are in the `setup.sh` file.
    
## Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "description": "Resource Not Found",
  "status code": 404,
  "success": false
}
```
The API will return these error types when requests fail:
- 404 Resource Not Found
- 422 Unprocessable
- 401 Unauthenicated
- 403 Forbidden
- 500 Internal Server Error


## Endpoints

### Actors

#### GET /actors

Get all actors paginated. Requires permission get:actors (at least Assistant status)

URL:
- GET https://casting-agency-7492.herokuapp.com/actors

Response:
```json
{
    "actors": [
        {
            "age": 18,
            "gender": "female",
            "id": 18,
            "name": "sandra"
        }
    ],
    "success": true,
    "total_actors": 17
}
```

#### POST /actors

Add a new actor. Requires permission post:actors (at least Director status)

URL:
- POST https://casting-agency-7492.herokuapp.com/actors

Request requires json body with parameters:

```json
{
    "name": "sandra",
    "birthdate": "2001-12-30",
    "gender": "female"
}
```

Response:
```json
{
    "added_actor": {
        "age": 18,
        "gender": "female",
        "id": 19,
        "name": "sandra"
    },
    "success": true
}
```

#### PATCH /actors

Modify existing actor. Requires permission patch:actors (at least Director status)

URL:
- PATCH https://casting-agency-7492.herokuapp.com/actors/1

Request requires json body with at least one of these parameters:

```json
{
    "name": "sue",
    "birthdate": "1995-12-30",
    "gender": "female"
}
```

Response:
```json
{
    "success": true,
    "updated_actor": {
        "age": 24,
        "gender": "female",
        "id": 1,
        "name": "sue"
    }
}
```


#### DELETE /actors

Delete an actor. Requires permission delete:actors (at least Director status)

URL:
- DELETE https://casting-agency-7492.herokuapp.com/actors/1

Response:
```json
{
    "deleted_actor": {
        "age": 18,
        "gender": "female",
        "id": 6,
        "name": "sandra"
    },
    "success": true,
    "total_actors": 17
}
```


### Movies


#### GET /movies

Get all movies paginated. Requires permission get:movies (at least Assistant status)

URL:
- GET https://casting-agency-7492.herokuapp.com/movies

Response:
```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 30 Dec 2005 00:00:00 GMT",
            "title": "Fight Club"
        }
    ],
    "success": true,
    "total_movies": 1
}
```

#### POST /movies

Add a new movie. Requires permission post:movies (Producer status)

URL:
- POST https://casting-agency-7492.herokuapp.com/movies

Request requires json body with parameters:

```json
{
    "title": "harry potter chamber",
    "release_date": "2022-12-30"
}
```

Response:
```json
{
    "added_movie": {
        "id": 3,
        "release_date": "Fri, 30 Dec 2022 00:00:00 GMT",
        "title": "harry potter chamber"
    },
    "success": true
}
```

#### PATCH /movies

Modify existing movie. Requires permission patch:movie (at least Director status)

URL:
- PATCH https://casting-agency-7492.herokuapp.com/movies/1

Request requires json body with at least one of these parameters:

```json
{
    "title": "Harry Potter and the Chamber of Secrets",
    "release_date": "2005-12-30"
}
```

Response:
```json
{
    "success": true,
    "updated_movie": {
        "id": 1,
        "release_date": "Fri, 30 Dec 2005 00:00:00 GMT",
        "title": "Fight Club"
    }
}
```


#### DELETE /movies

Delete a movie. Requires permission delete:movies (Producer status)

URL:
- DELETE https://casting-agency-7492.herokuapp.com/movies/1

Response:
```json
{
    "deleted_movie": {
        "id": 3,
        "release_date": "Fri, 30 Dec 2022 00:00:00 GMT",
        "title": "harry potter chamber"
    },
    "success": true,
    "total_movies": 1
}
```


### Contracts


#### POST /contracts

Add a new contract. Requires permission add:contracts (Producer status)

URL:
- POST https://casting-agency-7492.herokuapp.com/contracts

Request requires json body with parameters:

```json
{
    "actor_id": 1,
    "movie_id": 1
}
```

Response:
```json
{
    "added_contract": {
        "actor_id": 1,
        "id": 2,
        "movie_id": 1
    },
    "success": true
}
```

## Authors

* Juliane 
