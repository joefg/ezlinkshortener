import argparse
import hashlib
import logging

import fastapi
import fastapi.responses
import fastapi.staticfiles
import fastapi.templating
import uvicorn
import pydantic

logging.getLogger(__name__)

store = {}

app = fastapi.FastAPI()
templates = fastapi.templating.Jinja2Templates(directory='templates')

class Link(pydantic.BaseModel):
    url: str

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
async def serve_index(request: fastapi.Request):
    return templates.TemplateResponse('index.html', {'request' : request, 'title' : 'ezlinkshortener'})

@app.post("/make", response_class=fastapi.responses.HTMLResponse)
async def make_url_form(request: fastapi.Request, url:str = fastapi.Form()):
    store[shorten(sanitise(url))] = sanitise(url)
    vars = {
        'request' : request,
        'title' : "ezlinkshortener",
        'long_url' : "http://" + sanitise(url),
        'short_url' : expand(shorten(sanitise(url)), request)
    }
    return templates.TemplateResponse('link.html', vars)

@app.put("/api/make/")
async def make_url(link: Link, request: fastapi.Request):
    store[shorten(sanitise(link.url))] = link.url
    return { "url" : expand(shorten(sanitise(link.url)), request) }

@app.get("/{hash}")
async def go_to_url(hash: str):
    if store.get(hash) is None:
        raise fastapi.HTTPException(404, detail="Item not found")
    return fastapi.responses.RedirectResponse('http://' + store[hash])

@app.get("/api/resolve/{hash}")
async def get_url(hash: str):
    if store.get(hash) is None:
        raise fastapi.HTTPException(404, detail="Item not found")
    return { "url" : 'http://' + store[hash] }

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
