from fastapi import Depends,Body,HTTPException,Query
from utils.password_utils import Hasher
from fastapi.encoders import jsonable_encoder
from db.conexion import get_database
from db.models.users import UserCreate,UserFilter
from bson import ObjectId
from .helpers import user_helper,get_query





# new user
async def create_user(user_data: UserCreate = Body(...), db = Depends(get_database)):
    """
    Create a new user
    """
    collection = db["users"]
    user_data = jsonable_encoder(user_data)
    # valido password ....
    # quito el segundo password
    user_data.pop('password2')
    hash_password = Hasher.get_password_hash(user_data['password'])
    user_data['password'] = hash_password
    # hash del password
    result = await collection.insert_one(user_data)
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}






# all users
async def read_users(f:UserFilter,db = Depends(get_database)) -> dict:
    users = []
    # pagination
    start_index = (f.page - 1) * f.page_size
    # query
    query = get_query(f)
    async for user in db['users'].find(query).skip(start_index).limit(f.page_size):
        users.append(user_helper(user))
    return users





# edit user
async def edit_user(user_id: str, user_data : UserCreate, db = Depends(get_database)): #async def update_student(id: str, data: dict):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        # armo los datos
        user_data = jsonable_encoder(user_data)
        user_data.pop('password2')
        hash_password = Hasher.get_password_hash(user_data['password'])
        user_data['password'] = hash_password
        updated_user = await db['users'].update_one(
            {"_id": ObjectId(user_id)}, {"$set": user_data}
        )
        if updated_user:
            return 'ok'
        return 'Error'



# delete user
async def delete_user(user_id: str, db = Depends(get_database)):
    """
    Delete user by id
    """
    collection = db["users"]
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        await collection.delete_one({"_id": ObjectId(user_id)})
        return 'ok'
    else:
        return 'Error'



# get user by id
async def retrieve_user(user_id: str, db = Depends(get_database)) -> dict:
    user = await db['users'].find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)





##https://testdriven.io/blog/fastapi-mongo/