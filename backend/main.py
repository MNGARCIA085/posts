from fastapi import FastAPI,APIRouter, Depends
from db.conexion import get_database
from api.base import api_router




def include_router(app):
    app.include_router(api_router)

def start_application():
    #app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    #cors(app)
    app = FastAPI()
    include_router(app)
    return app


app = start_application()




