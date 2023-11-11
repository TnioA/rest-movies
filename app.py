import datetime
from bs4 import BeautifulSoup
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import requests

app = FastAPI(
    title="TesteApp",
    description="Minha api de demonstração.",
    summary="",
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

class NumbersItem(BaseModel):
    date: datetime.datetime
    concurse: str | None = None
    winners: str
    value: str | None = None
    numbers: list[str]

class GamesResponse(BaseModel):
    results: list[NumbersItem]

class NumbersResponse(BaseModel):
    results: list[str]
    model_config = {
        "json_schema_extra": {
            "examples": [
                ["1", "2", "3", "4", "5", "6"]
            ]
        }
    }

@app.get(
    "/bets/numbers", 
    summary="Retorna a lista de jogos da mega-sena",
    tags=["bets"], 
    response_model=GamesResponse, 
    responses={
        status.HTTP_200_OK: {
            "description": "Data returned with success",
            "model": GamesResponse
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Validation errors",
            "content": {
                "application/json": {
                    "example": {}
                }
            },
        }
    }
)
async def get_games(token = Depends(auth_scheme)): 
    """
    Retorna a lista de jogos da mega-sena
    """
    if(token):
        print(token)
    html_doc = requests.get("http://www.resultadosmegasena.com.br/resultados-anteriores")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    data = []
    for dataBox in soup.find_all("tr", class_="rstable_td"):
        itens = dataBox.find_all("td")
        date = itens[0].text.strip()
        info = itens[1].text.strip().split("\t\t\t\t\t\t")
        concurse = info[0].replace("\n", "").strip()
        winners = info[1].replace("Ganhadores:", "").strip()
        #value = info[2].replace("Prêmio:", "").strip()
        value = ''
        numbers = [item.text for item in itens[2].find_all("div")]

        data.append({ 
            'date': date,
            'concurse': concurse,
            'winners': winners,
            'value': value,
            'numbers': numbers
        })      
        
    return JSONResponse(status_code=status.HTTP_200_OK, content={'results': data})

@app.get(
    "/bets/bestnumber", 
    summary="Retorna os 6 melhores números para jogo",
    tags=["bets"],
    response_model=NumbersResponse, 
    responses={
        status.HTTP_200_OK: {
            "description": "Data returned with success",
            "model": NumbersResponse
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Validation errors",
            "content": {
                "application/json": {
                    "example": {}
                }
            },
        }
    }
)
async def get_best_number():
    """
    Retorna os 6 melhores números para jogo
    """

    html_doc = requests.get("http://www.resultadosmegasena.com.br/resultados-anteriores")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    number_list = []
    object_list = {}
    final_list = []
    for dataBox in soup.find_all("tr", class_="rstable_td"):
        itens = dataBox.find_all("td")
        number = [int(item.text) for item in itens[2].find_all("div")]
        number_list.extend(number)

    for item in range(1, 60):
        object_list.update({
            str(item): number_list.count(item)
        })
        
    sorted_list = sorted(
        object_list.items(),
        key = lambda x: x[1],
        reverse = True
    )

    for i in range(0, 6):
        final_list.append(sorted_list[i][0])
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={'results': final_list})
























# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/movies', methods=['GET'])
def filmes():
    html_doc = requests.get("http://www.adorocinema.com/filmes/numero-cinemas/")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    data = []
    for dataBox in soup.find_all("li", class_="mdl"):

        if dataBox.find('div', class_='card entity-card entity-card-list cf'):
            nomeObj = dataBox.find("h2", class_="meta-title").find("a", class_="meta-title-link")
            imgObj = dataBox.find("figure").find("img", class_="thumbnail-img")
            sinopseObj = dataBox.find("div", class_="synopsis").find("div", class_="content-txt")
            dataObj = dataBox.find("div", class_="meta-body-item meta-body-info").find("span", class_="date")
            if imgObj.has_attr("data-src"):
                imagem = imgObj["data-src"]
            else:
                imagem = imgObj["src"]
                
            data.append({ 'nome' : nomeObj.text.strip(),
                        'poster' : imagem,
                        'sinopse' : sinopseObj.text.strip(),
                        'data' :  dataObj.text.strip()})

        else:
            pass
    
    return jsonify({'filmes': data})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)






