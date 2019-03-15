# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/filmes', methods=['GET'])
def filmes():
    html_doc = urlopen("http://www.adorocinema.com/filmes/numero-cinemas/").read()
    soup = BeautifulSoup(html_doc, "html.parser")

    data = []
    for dataBox in soup.find_all("li",class_="mdl"):
        nomeObj = dataBox.find("h2", class_="meta-title").find("a", class_="meta-title-link")
        imgObj = dataBox.find("figure", class_="thumbnail ").find("img", class_="thumbnail-img")
        sinopseObj = dataBox.find("div", class_="synopsis").find("div", class_="content-txt")
        dataObj = dataBox.find("div", class_="meta-body-item meta-body-info").find("span", class_="date")
        if imgObj.has_attr("data-src"):
            imagem = imgObj["data-src"]
        else:
            imagem = imgObj["src"]

        data.append({ 'nome': nomeObj.text.strip(),
                    'poster' : imagem,
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dataObj.text.strip()})

    
    return jsonify({'filmes': data})
if __name__=="__main__":
    app.run(debug=True)







