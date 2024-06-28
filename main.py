from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse, ORJSONResponse
from hltb import HLTB
from starlette.middleware.cors import CORSMiddleware

description="Simple endpoint for HLTB. Microservice is required as HLTB doesn't allow CORS requests"


app = FastAPI(
    title="Python MicroService for HowLongToBeat API consultation",
    description=description,
    contact={'email': 'martin.antelo.jallas@gmail.com'}
)


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
async def HLTBquery(query:str):
    hltb = HLTB()
    result = hltb.search(query)
    return result
    
app.include_router(router)