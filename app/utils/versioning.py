from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple, TypeVar, cast
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html #, get_swagger_ui_html
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.routing import BaseRoute
from app.utils.custom_swagger import get_swagger_ui_html

CallableT = TypeVar("CallableT", bound=Callable[..., Any])

def version(major: int, minor: int = 0) -> Callable[[CallableT], CallableT]:
    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor)  # type: ignore
        return func

    return decorator

def version_to_route(route: BaseRoute, default_version: Tuple[int, int]) -> Tuple[Tuple[int, int], APIRoute]:
    api_route = cast(APIRoute, route)
    if(hasattr(api_route, 'endpoint')):
        version = getattr(api_route.endpoint, "_api_version", default_version)
        return version, api_route
    
    return default_version, api_route

def VersionedFastAPI(
    app: FastAPI,
    version_format: str = "{major}.{minor}",
    prefix_format: str = "/v{major}_{minor}",
    default_version: Tuple[int, int] = (1, 0),
    enable_latest: bool = False,
    **kwargs: Any,
) -> FastAPI:
    parent_app = FastAPI(
        title=app.title,
        description=app.description,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        openapi_url=None,
        **kwargs,
    )

    version_route_mapping: Dict[Tuple[int, int], List[APIRoute]] = defaultdict(
        list
    )

    version_routes = [
        version_to_route(route, default_version) for route in app.routes
    ]

    for version, route in version_routes:
        if (version != None):
            version_route_mapping[version].append(route)

    swagger_versions = []
    versions = sorted(version_route_mapping.keys())
    for version in versions:
        major, minor = version
        prefix = prefix_format.format(major=major, minor=minor)
        semver = version_format.format(major=major, minor=minor)
        openapi_url_path = "/swagger" + prefix + "/swagger.json"
        swagger_versions.append({ 
            "url": "/api" + openapi_url_path,
            "name": "V" + semver
        })

        versioned_app = FastAPI(
            prefix=prefix,
            title=app.title + f" {major}.{minor}",
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            version=f"{major}.{minor}",
            openapi_url=openapi_url_path,
            docs_url=None,
            redoc_url=None,
            servers=[
                {"url": "/api"}
            ],
        )

        unique_routes = {}
        # adding each route for each method
        for route in version_route_mapping[version]:          
            for method in route.methods:
                versioned_path = prefix + route.path
                route.path_format = versioned_path
                route.path = versioned_path

                versioned_app.router.routes.append(route)

        parent_app.include_router(versioned_app.router, prefix="/api")

    
    # adding_latest_routes
    if enable_latest:
        prefix = "/latest"
        major, minor = version
        semver = version_format.format(major=major, minor=minor)
        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )
        for route in unique_routes.values():
            versioned_app.router.routes.append(route)
        parent_app.mount(prefix, versioned_app)


    # adding_static_files_route
    parent_app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # adding_swagger_docs
    swagger = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Swagger - " + app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_js_standalone_url="/static/swagger-ui-standalone-preset.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.webp",
        swagger_ui_parameters={
            "layout": "StandaloneLayout",
            "urls": swagger_versions
        }
    )

    parent_app.add_route(path="/", route=swagger)

    # adding_redoc_docs
    for version in swagger_versions:
        redoc = get_redoc_html(
            openapi_url=version["url"],
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )
        parent_app.add_route(path= "/" + version["name"].lower() + "/redoc", route=redoc)

    return parent_app


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        openapi_version="3.0.1",
        title="Rest Movies 1.0",
        description="Serviço destinado para consulta de filmes em cartaz em tempo real.",
        # summary="",
        version="1.0",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Deadpoolio the Amazing",
            "url": "http://x-force.example.com/contact/",
            "email": "dp@x-force.example.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
