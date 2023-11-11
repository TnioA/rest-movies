
# Rest Movies API

Service created for getting movies in theaters data in real time with all needed information to view pages.


## Autores

- [@TnioA](https://github.com/TnioA)


## API Documentation

#### Returns movies in theaters data in real time

```http
  GET /v1/movies/getall
```

| Parameter   | Type       | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `api_key` | `string` | **Mandatory**. JWT Bearer token |


## Instalation

Create an development environment

```bash
  py -m venv ./venv
```

Activate development environment

```bash
  venv/Scripts/activate.bat
```
    
Install application requirements

```bash
  pip install -r requirements.txt
```

Start application server with auto reload using uvicorn

```bash
  uvicorn main:app --reload
```