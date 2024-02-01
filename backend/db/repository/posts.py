from fastapi import Depends,Body,HTTPException,Query
from fastapi.encoders import jsonable_encoder
from db.conexion import get_database
from db.models.posts import PostCreate,PostEdit,PostFilter
from bson import ObjectId
from .helpers import post_helper,get_post_query
import datetime




# new post
async def create_post(data: PostCreate = Body(...), db = Depends(get_database)):
    """
    Create a new post
    """
    data = jsonable_encoder(data)
    data['author'] = ObjectId(data['author'])
    date = datetime.datetime.now()
    data['date'] = date
    data['last_modified'] = date
    result = await db['posts'].insert_one(data)
    return {"message": "Post created successfully", "post_id": str(result.inserted_id)}



# Obtener posts con autores y comentarios paginados
async def get_posts(f:PostFilter, db = Depends(get_database)):
    # pagination
    start_index = (f.page - 1) * f.page_size
    # query
    query = get_post_query(f) # get pipeline!!!!
    #
    posts_with_details = []
    async for post in db['posts'].find(query).skip(start_index).limit(f.page_size):
        author = await db['users'].find_one({"_id": ObjectId(post['author'])})
        post_with_details = post_helper(post,author)
        posts_with_details.append(post_with_details)
    return posts_with_details



# get post by id
async def retrieve_post(post_id: str, db = Depends(get_database)) -> dict:
    post = await db['posts'].find_one({"_id": ObjectId(post_id)})
    author = await db['users'].find_one({"_id": ObjectId(post['author'])})
    if post:
        return post_helper(post,author)



# update post by id
async def edit_post(post_id: str, data : PostEdit, db = Depends(get_database)): 
    post = await db["posts"].find_one({"_id": ObjectId(post_id)})
    # un post sólo lo puede editar el que lo creó (lo valido dsp. a partir del token)
    if post:
        # armo los datos
        data = jsonable_encoder(data)
        data['last_modified'] = datetime.datetime.now()
        # last_modified date
        updated_post = await db['posts'].update_one(
            {"_id": ObjectId(post_id)}, {"$set": data}
        )
        if updated_post:
            return 'ok'
        return 'Error'
    



# delete post by id
async def delete_post(post_id: str, db = Depends(get_database)):
    """
    Delete post by id
    """
    collection = db["posts"]
    user = await collection.find_one({"_id": ObjectId(post_id)})
    if user:
        await collection.delete_one({"_id": ObjectId(post_id)})
        return 'ok'
    else:
        return 'Error'
    



# para las consultas con lookups puedo hacer pipelines
    
"""
pipeline = [
        {"$match": {"author.username": author_username}},
        {"$skip": skip_count},
        {"$limit": page_size},
        {"$lookup": {
            "from": "users",  # Nombre de la colección de usuarios
            "localField": "author",
            "foreignField": "_id",
            "as": "author_details"
        }},
        {"$unwind": "$author_details"},
        {"$project": {
            "_id": 1,
            "title": 1,
            "content": 1,
            "author": {
                "id": "$author_details._id",
                "name": "$author_details.name",
                "email": "$author_details.email"
            },
            "comments": 1
        }}
    ]

    posts_with_details = await posts_collection.aggregate(pipeline).to_list(None)
    return posts_with_details
"""