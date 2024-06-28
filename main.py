from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse, ORJSONResponse
from hltb import HLTB
from starlette.middleware.cors import CORSMiddleware
import os

description = "Simple endpoint for HLTB. Microservice is required as HLTB doesn't allow CORS requests"

app = FastAPI(
    title="Python MicroService for HowLongToBeat API consultation",
    description=description,
    contact={'email': 'martin.antelo.jallas@gmail.com'}
)

# Uncomment this for API Key support.
# Be sure to have an .env file with 
# a parameter API_KEY 
""" @app.middleware("http")
async def check_api_key(request: Request, call_next):
    expected_api_key = os.getenv("API_KEY")
    if request.url.path in ["/docs", "/redoc"]:
        api_key = request.query_params.get("api_key")
        if not api_key:
            return JSONResponse(
                status_code=401, 
                content={"detail": "API Key required, la cual hay que pasarla como parámetro 'api_key' en la URL. Ejemplo: api_key=API"}
            )
        if api_key != expected_api_key:
            return JSONResponse(
                status_code=401, 
                content={"detail": "Wrong API Key."}
            )
    response = await call_next(request)
    return response """

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"Unexpected Error: {exc.__class__.__name__}.",
            "description": str(exc)
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(
    tags=["Files"],
    default_response_class=ORJSONResponse
)

@router.get("/searchHLTB/{query}")
async def HLTBquery(query: str):
    hltb = HLTB()
    result = hltb.search(query)
    return result

app.include_router(router)