# -*- coding: utf-8 -*-
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader
from models import BaseResponse, ErrorResponse, SuccessData, ErrorData
from movie_service import MovieService
from settings import AppSettings

_settings = AppSettings()

app = FastAPI(
    title="Rest Movies",
    description="Serviço destinado para consulta de filmes em cartaz em tempo real.",
    # summary="",
    version="0.0.1",
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
    docs_url="/",
    redoc_url=None,
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_scheme = APIKeyHeader(
    name="Authorization",
    scheme_name="Bearer",
    description="Por favor insira no campo o token JWT com Bearer.",   
    auto_error=False,
)

@app.get(
    "/v1/movies/getall", 
    summary="Retorna a lista de filmes em cartaz",
    tags=["movies"],
    responses={
        status.HTTP_200_OK: {
            "description": "Data returned with success",
            "model": BaseResponse
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Validation errors",
            "model": ErrorResponse
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticated",
            "model": ErrorResponse
        }
    }
)
async def get_games(token = Depends(auth_scheme)): 
    """
    Exemplo de requisição para obter os filmes.

        Request:
        GET /v1/movies/getall
    """
    if(token):
        print(token)

    print(_settings.url_scrapping_api)
    service = MovieService(_settings)
    result = service.get_movies()
    if(not result):
        return ErrorData("Erro ao consultar os filmes")
        
    return SuccessData(result)