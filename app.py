from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import urllib.request
import html
import json
import os

app = flask(__name__)

@app.route('/filmes', methods=['GET'])
def filmes():
    html_doc = urllib.request.urlopen("http://www.adorocinema.com/filmes/numero-cinemas/").read()
    soup = BeautifulSoup(html_doc, "html.parser")

    data = []
    for dataBox in soup.find_all("li",class_="mdl"): 
        nomeObj = dataBox.find("h2", class_="meta-litle").find("a", class_="meta-litle-link")
        imgObj = 'imagem'
        sinopseObj = 'sinopse'
        dataObj = 'data'

        data.append({ 'nome': nomeObj.strip(),
                    'poster' : imgObj.strip(),
                    'sinopse' : sinopseObj.strip(),
                    'data' :  dataObj.strip()})
              
return jsonify({'filmes': data})

app.run(debug=True)