# CAPSTONE API DOCUMENTATION

## Description

This is an document for API in CAPSTONE app

## Base URL

`https://manhvgt-udacity-capstone.onrender.com`

## Endpoints

### `'/index'`

- Return status of server

```json
{
    "message": "working",
    "success": true
}
```

### `'/login'`

- Redirect to login page by Auth0


### `'/movies', methods=['GET']'`

- Fetches all movies from DB. Required RBAC
- Request Arguments: None
- Returns: An object containt result and list of movies overview infomation

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 24 Oct 2023 00:00:00 GMT",
            "title": "movie title"
        },
        {
            "id": 2,
            "release_date": "Tue, 24 Oct 2023 00:00:00 GMT",
            "title": "pirates of the caribbean"
        }
    ],
    "success": true
}
```

---

### `'/movies/<int:movie_id>', methods=['GET']`

- Get movies details (including involved actor) by movie_id. Required RBAC
- Request Arguments: int:movie_id
- Returns: An object containt result and movie details

```json
{
    "actors_involvement": [1, 2],
    "movie_details": {
        "casting_site": "casting_site",
        "id": 1,
        "release_date": "Tue, 24 Oct 2023 00:00:00 GMT",
        "revenue": 12345,
        "title": "title"
    },
    "success": true
}
```


### `'/movies', methods=['POST']`

- Create a new movie. Required RBAC
- Request Arguments: A json object containts Movies information
- Returns: An object containt result and movie details

```json
{
    "message": "Movie created successfully",
    "movie_details": {
        "casting_site": "Hanoi",
        "id": 2,
        "release_date": "Tue, 24 Oct 2023 00:00:00 GMT",
        "revenue": 123456,
        "title": "a new movie"
    },
    "success": true
}
```


### `'/movies/<int:movie_id>', methods=['PATCH']`

- Update movie details by movie_id. Required RBAC
- Request Arguments: A json object containts Movies information
- Returns: An object containt result and movie details

```json
{
    "message": "Movie details updated successfully",
    "movie_details": {
        "casting_site": "Caribbean",
        "id": 1,
        "release_date": "Sat, 24 Oct 2020 00:00:00 GMT",
        "revenue": 123456,
        "title": "Pirates of the Caribbean"
    },
    "success": true
}
```

### `'/movies/<int:movie_id>', methods=['DELETE']`

- Delete a movie by movie_id. Required RBAC
- Request Arguments: int:movie_id
- Returns: An object containt result and movie iD

```json
{
    "deleted_movie_id": 2,
    "message": "Movie deleted successfully",
    "success": true,
    "title": "a new movie"
}
```


### `'/actors', methods=['GET']`

- Get all actors in short form. Required RBAC
- Request Arguments: None
- Returns: An object containt result and list of actors overview infomation

```json
{
    "actors": [
        {
            "id": 1,
            "name": "Amber Heard"
        },
        {
            "id": 2,
            "name": "Johnny Depp"
        }
    ],
    "success": true
}
```


### `'/actors/<int:actor_id>', methods=['GET']`

- Get actors details (including involving movies if any) by actor_id. Required RBAC
- Request Arguments: int:actor_id
- Returns: An object containt result and actors details (including involving movies)

```json
{
    "actor_details": {
        "age": 43,
        "gender": "male",
        "id": 2,
        "name": "Johnny Depp"
    },
    "movies_involvement": [
        {
            "id": 1,
            "title": "Pirates of the Caribbean"
        }
    ],
    "success": true
}
```

### `'/actors', methods=['POST']`

- Create a new actor. Required RBAC
- Request Arguments: None
- Returns: An object containt result and actor details

```json
{
    "actor_details": {
        "age": 43,
        "gender": "male",
        "id": 2,
        "name": "Johnny Depp"
    },
    "message": "actor created successfully",
    "success": true
}
```


### `'/actors/<int:actor_id>', methods=['PATCH']`

- Update actor details by actor_id. Required RBAC
- Request Arguments: int:actor_id
- Returns: An object containt result and actors details 

```json
{
    "actor_details": {
        "age": 45,
        "gender": "male",
        "id": 2,
        "name": "Johnny Depp"
    },
    "message": "actor details updated successfully",
    "success": true
}
```

### `'/actors/<int:actor_id>', methods=['DELETE']`

- Delete a actor by actor_id. Required RBAC
- Request Arguments: int:actor_id
- Returns: An object containt result and actor ID

```json
{
    "deleted_actor_id": 2,
    "deleted_actor_name": "Johnny Depp",
    "message": "actor deleted successfully",
    "success": true
}
```
