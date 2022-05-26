# ezlinkshortener

Let's build a link shortening service!

This is just a toy, I wanted to learn the nuts and bolts of [FastAPI](https://fastapi.tiangolo.com).

## How A Link Shortener Works

Very briefly:

```
url -> function(url) = shortened -> return shortened
shortened -> lookup(shortened) -> return url
```

## Testing

This uses `pipenv` but there's a requirements.txt for people who want to use plain `virtualenv`.

```
# Create pipenv

pipenv shell;
pipenv install -r requirements.txt;

# Create test database (some data included)
./create_db.sh

# Running
python3 main.py --port 5000
```

## API Documentation

FastAPI has built-in documentation, so once you're running this, go to [your docs](http://localhost:5000/docs)

## TODO

- Nicer frontend
- Add authentication to the API
- Extend data modelling so that we're not tied to sqlite (ie port to an ORM)
