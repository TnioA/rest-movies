from bs4 import BeautifulSoup
from app.settings.app_settings import AppSettings
import requests

class MovieService:
    def __init__(self, settins: AppSettings):
        self._settings = settins
        pass

    def get_movies(self):
        try:
            html_doc = requests.get(self._settings.url_scrapping_api)
            soup = BeautifulSoup(html_doc.text, "html.parser")
            data = []
            for dataBox in soup.find_all("li", class_="mdl"):
                if dataBox.find("div", class_="card entity-card entity-card-list cf"):
                    nomeObj = dataBox.find("h2", class_="meta-title").find("a", class_="meta-title-link")
                    imgObj = dataBox.find("figure").find("img", class_="thumbnail-img")
                    sinopseObj = dataBox.find("div", class_="synopsis").find("div", class_="content-txt")
                    dataObj = dataBox.find("div", class_="meta-body-item meta-body-info").find("span", class_="date")
                    if imgObj.has_attr("data-src"):
                        imagem = imgObj["data-src"]
                    else:
                        imagem = imgObj["src"]
                        
                    data.append({ 
                        "name" : nomeObj.text.strip(),
                        "poster" : imagem,
                        "synopsis" : sinopseObj.text.strip(),
                        "date" :  dataObj.text.strip()
                    })

            return data
        except ZeroDivisionError as error:
            print(error)
            return None