from fastapi import status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class Movie(BaseModel):
    name: str | None = None
    poster: str | None = None
    synopsis: str | None = None
    date: str | None = None

class Error(BaseModel):
    code: str | None = None
    message: str | None = None

class BaseResponse(BaseModel):
    data: list[Movie]
    success: bool = False

class ErrorResponse(BaseModel):
    errors: list[Error]
    success: bool = False

def ErrorData(error: str) -> ErrorResponse:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={ 
        "errors": [
            { "code": "400", "message": error }
        ],
        "success": False
    })

def SuccessData(data: list[Movie]) -> BaseResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={ 
        "data": data,
        "success": True
    })