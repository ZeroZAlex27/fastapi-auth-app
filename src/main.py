from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .lifespan import lifespan

from .auth.router import auth_router
from .users.router import user_router
from .access_control.access_roles.router import access_role_router
from .access_control.business_elements.router import business_element_router
from .access_control.access_rules.router import access_rule_router
from .mock.router import mock_router


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

routers = [
    auth_router,
    user_router,
    access_role_router,
    business_element_router,
    access_rule_router,
    mock_router,
]

for router in routers:
    app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs">Documentation</a><br>
    <a href="http://127.0.0.1:8000/redoc">ReDoc</a>
    """
