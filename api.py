import aiohttp
from aiohttp import web
import async_timeout
import jsonpath_rw # pip install jsonpath-rw
import traceback

class URLTooLarge(Exception):
    """The content-length headers was too large to reasonably download"""
    
class NoContentLengthHeader(Exception):
    """Due to download restrictions a content-length header is required"""
    
def check_headers(headers):
    if "content-length" not in headers:
        raise NoContentLengthHeader
    elif headers["content-length"] > 104857600:
        raise URLTooLarge

async def root_handled(request):
    try:
        async with async_timeout.timeout(15):
            return await root(request)
    except asyncio.TimeoutError:
        return web.Response(body="Either the request URL or the image URL was unresponive")
    except NoContentLengthHeader:
        return web.Response(body=NoContentLengthHeader.__doc__)
    except URLTooLarge:
        return web.Response(body=URLTooLarge.__doc__)
    except:
        traceback.print_exc()
        return web.Response(body=traceback.format_exc())

async def root(request):
    url = request.query["url"]
    expression = jsonpath_rw.parse(request.query["query"])

    async with aiohttp.ClientSession() as session:
        async with session.head(_url) as resp:
            check_headers(resp.headers)

        async with session.get(url) as resp:
            json = await resp.json()

        image_url = expression.find(json)[0].value

        suffix = request.query.get("suffix")
        prefix = request.query.get("prefix")
        replace = request.query.get("replace")
        if replace:
            be_replaced, to_replace = replace.split(",")[:2]
            image_url = image_url.replace(be_replaced, to_replace)

        if prefix:
            image_url = prefix + image_url

        if suffix:
            image_url += suffix

        async with session.head(image_url) as resp:
            check_headers(resp.headers)
            
        async with session.get(image_url) as resp:
            body = await resp.read()

    return web.Response(body=body, content_type="image/png")

async def app():
    app = web.Application()
    app.router.add_get("/", root_handled)
    return app

if __name__ == "__main__":
    web.run_app(app())
