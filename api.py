import aiohttp
from aiohttp import web
import jsonpath_rw # pip install jsonpath-rw

async def root(request):
    try:
        session = aiohttp.ClientSession()

        url = request.query["url"]
        expression = jsonpath_rw.parse(request.query["query"])
        async with session.get(url) as resp:
            json = await resp.json()

        image_url: str = expression.find(json)[0].value

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

        async with session.get(image_url) as resp:
            body = await resp.read()

        return web.Response(body=body, content_type="image/png")
    except:
        import traceback
        traceback.print_exc()
        return web.Response(body="fail")

async def run_app():
    app = web.Application()
    app.router.add_get("/", root)
    return app

if __name__ == "__main__":
    web.run_app(run_app())
