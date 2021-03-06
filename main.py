import os
import argparse
import hashlib
import logging
import sqlite3
import functools

import fastapi
import fastapi.responses
import fastapi.staticfiles
import fastapi.templating
import uvicorn
import pydantic

import db
from config import Settings

logging.getLogger(__name__)

app = fastapi.FastAPI()
templates = fastapi.templating.Jinja2Templates(directory='templates')

@functools.lru_cache()
def get_settings():
    return Settings()

class Link(pydantic.BaseModel):
    url: str

def search_hash(hash, store):
    args = {
        'hash' : hash
    }
    sql = '''
        SELECT hash, url
        FROM link
        WHERE hash=:hash
        LIMIT 1;
    '''
    conn, cur = db.connect(store)
    cur.execute(sql, args)
    res = cur.fetchall()
    conn.close()

    return res

def insert_link(hash, url, store):
    args = {
        'hash' : hash,
        'url'  : url
    }
    sql = '''
        INSERT INTO link (hash, url)
        VALUES (:hash, :url)
        RETURNING *;
    '''
    conn, cur = db.connect(store)

    try:
        cur.execute(sql, args)
        res = cur.fetchall()
        conn.commit()
    except sqlite3.IntegrityError:
        res =  None

    conn.close()
    return res

def sanitise(url):
    sanitised = url
    if 'https://' in url:
        sanitised = str.replace(url, 'https://', '')
    elif 'http://' in url:
        sanitised = str.replace(url, 'http://', '')
    return sanitised

def shorten(url):
    md5 = hashlib.md5(url.encode()).hexdigest()
    return md5[0:10]

def expand(hash, request):
    return 'http://' + str(request.url).split("/")[2:-1][0] + '/' + hash

@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def serve_index(request: fastapi.Request, settings: Settings = fastapi.Depends(get_settings)):
    params = {'request' : request, 'title' : settings.app_name}
    return templates.TemplateResponse('index.html', params)

@app.post("/make", response_class=fastapi.responses.HTMLResponse)
async def make_url_form(request: fastapi.Request, settings: Settings = fastapi.Depends(get_settings), url:str = fastapi.Form()):
    url = sanitise(url)
    hash = shorten(url)

    insert_link(hash, url, settings.datastore)

    vars = {
        'request' : request,
        'title' : settings.app_name,
        'long_url' : "http://" + sanitise(url),
        'short_url' : expand(shorten(sanitise(url)), request)
    }
    return templates.TemplateResponse('link.html', vars)

@app.put("/api/make/")
async def make_url(link: Link, request: fastapi.Request, settings: Settings = fastapi.Depends(get_settings)):
    url = sanitise(link.url)
    hash = shorten(url)

    insert = insert_link(hash, url, settings.datastore)

    if insert is None:
        raise fastapi.HTTPException(409, detail="Conflict")

    return { "url" : expand(hash, request) }

@app.get("/{hash}")
async def go_to_url(hash: str, settings: Settings = fastapi.Depends(get_settings)):
    url = search_hash(hash, settings.datastore)

    if len(url) == 0:
        raise fastapi.HTTPException(404, detail="Item not found")

    url = url[0].get('url')
    return fastapi.responses.RedirectResponse('http://' + url)

@app.get("/api/resolve/{hash}")
async def get_url(hash: str, settings: Settings = fastapi.Depends(get_settings)):
    url = search_hash(hash, settings.datastore)

    if len(url) == 0:
        raise fastapi.HTTPException(404, detail="Item not found")

    url = url[0].get('url')
    return { "url" : 'http://' + url }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ezlinkshortener - world\'s easiest link shortener'
    )
    parser.add_argument(
        '--port', '-p',
        metavar='N',
        type=int,
        default=5000,
        help='Specify port, defaults to 5000.'
    )
    args = vars(parser.parse_args())

    uvicorn.run("main:app", host="127.0.0.1", port=args['port'], log_level="info")
