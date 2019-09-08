# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def application(environ, start_response):
  if environ['REQUEST_METHOD'] == 'OPTIONS':
    start_response(
      '200 OK',
      [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', 'POST'),
      ]
    )
    return ''


@app.route('/api/filmes', methods=['GET'])
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






