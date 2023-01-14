import secrets
from aiohttp import web
from aiohttp_session import get_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import bcrypt
import datetime

async def handler_logout(request):

    session = await get_session(request)

    if "connected" in session.keys():
        session["connected"] = False
    return web.Response(status=200)


async def handler_logged(request):

    session = await get_session(request)

    if "connected" in session.keys() and session["connected"] == True:
        return web.Response(status=200)
    return web.Response(status=401)


async def handler(request):

    data = await request.post()
    session = await get_session(request)

    if "connected" in session.keys() and session["connected"] == True:
        return web.HTTPFound("/")

    try:
        login = data["username"]
        password = data["password"]
        otp = data["otp"]

        # Change this block to add your own auth method
        h = b"$2b$1xxxx3qhK"
        if (
            (bcrypt.hashpw(password.encode(), h) == h)
            and login == ""
            and str(otp) == str(datetime.datetime.today().day)
        ):
            session["connected"] = True
            return web.HTTPFound("/")

    except:
        return web.Response(status=401)

    return web.Response(status=401)


def init():
    app = web.Application()
    setup(app, EncryptedCookieStorage(secrets.token_bytes(32)))
    app.router.add_route("GET", "/", handler_logged)
    app.router.add_route("POST", "/api/login", handler)
    app.router.add_route("GET", "/api/logout", handler_logout)

    return app


web.run_app(init(), host="127.0.0.1", port=8080)