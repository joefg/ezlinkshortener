# ezlinkshortener

Let's build a link shortening service!

This is just a toy, I wanted to learn the nuts and bolts of [FastAPI](https://fastapi.tiangolo.com).

## How A Link Shortener Works

Very briefly:

```
url       -> shorten(url)      = shortened -> return shortened
shortened -> lookup(shortened) = url       -> return url
```

## Configuration

Bring your own `config.py`!

```python
import pydantic

class Settings(pydantic.BaseSettings):
    app_name: str = "ezlinkshortener"
    datastore: str = "data/service.db"

settings = Settings()
```

## Running

This uses `pipenv` but there's a requirements.txt for people who want to use plain `virtualenv`.

```bash
# Create pipenv
pipenv shell;
pipenv install -r requirements.txt;

# Create test database (some data included)
python3 db.py data/service.db --verbose --create --update

# Running
python3 main.py --port 5000
```

## Unit Tests

```bash
# Create pipenv
pipenv shell;
pipenv install -r requirements.txt;

# Run unit tests
python3 -m unittest test_main.py -vvv
```

## API Documentation

FastAPI has built-in documentation, so once you're running this, go to [your docs](http://localhost:5000/docs)

## TODO

- Nicer frontend
- Add authentication to the API
- Extend data modelling so that we're not tied to sqlite (ie port to an ORM)
- Much better sanitisation, at the moment it's horrible.
