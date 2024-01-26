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




@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.get("/try")
async def read_items(db = Depends(get_database)):
    # Realizar operaciones con la base de datos
    collection = db["aux"]
    data = {'Estado':'ok'}
    result = await collection.insert_one(data)
    return {"message": "Operaciones realizadas"}


"""
router = APIRouter()

@router.get("/")
async def read_items(db = Depends(get_database)):
    # Realizar operaciones con la base de datos
    collection = db["aux"]
    data = {'Estado':'ok'}
    result = await collection.insert_one(data)
    return {"message": "Operaciones realizadas"}
"""