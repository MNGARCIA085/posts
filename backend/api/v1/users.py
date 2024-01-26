# En app/api/user_api.py

from fastapi import APIRouter, Depends, HTTPException,Body
from db.conexion import get_database
from bson import ObjectId


from db.repository import users

from db.models.users import UserCreate,UserFilter






router = APIRouter()




# create new user
@router.post("/")
async def create_user(user: UserCreate = Body(...), db = Depends(get_database)):
    """
    Crea un nuevo usuario.
    """
    return await users.create_user(user,db)







# get all users
@router.get("/")
async def read_users(f: UserFilter = Depends(),db = Depends(get_database)):
    """
    Retrieve all users.
    """
    return await users.read_users(f,db)






# get user by id
@router.get("/{user_id}")
async def retrieve_user(user_id:str,db = Depends(get_database)):
    """
    Retrieve an user by id
    """
    return await users.retrieve_user(user_id,db)



# delete user by id
@router.delete("/{user_id}")
async def delete_user(user_id: str, db = Depends(get_database)):
    """
    Delete a user by ID
    """
    result = await users.delete_user(user_id,db)
    if result == 'ok':
        return {"message": f"User with ID {user_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")



# update user by id
@router.put("/{user_id}")
async def edit_user(user_id: str, user: UserCreate = Body(...), db = Depends(get_database)):
    """
    Edit an user by ID
    """
    result = await users.edit_user(user_id,user,db)
    if result == 'ok':
        return {"message": f"User with ID {user_id} edited"}
    else:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
























