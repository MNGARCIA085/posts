# En app/api/user_api.py
from fastapi import APIRouter, Depends, HTTPException,Body,Query
from db.conexion import get_database
from bson import ObjectId
from db.repository import posts
from db.models.posts import PostCreate,PostFilter,PostEdit


router = APIRouter()


# create new user
@router.post("/")
async def create_post(post: PostCreate = Body(...), db = Depends(get_database)):
    """
    Create new post
    """
    return await posts.create_post(post,db)



# Endpoint para obtener detalles de todos los posts con sus autores y comentarios
@router.get("/")
async def get_all_posts(f:PostFilter=Depends(), db = Depends(get_database)):
    return await posts.get_posts(f,db)


# get post by id
@router.get("/{post_id}")
async def retrieve_post(post_id:str,db = Depends(get_database)):
    """
    Retrieve a post by id
    """
    return await posts.retrieve_post(post_id,db)

    

@router.put("/{user_id}")
async def edit_post(post_id: str, post: PostEdit = Body(...), db = Depends(get_database)):
    """
    Edit a post by ID
    """
    result = await posts.edit_post(post_id,post,db)
    if result == 'ok':
        return {"message": f"Post with ID {post_id} edited"}
    else:
        raise HTTPException(status_code=404, detail=f"User with ID {post_id} not found")
    

# delete user by id
@router.delete("/{post_id}")
async def delete_post(post_id: str, db = Depends(get_database)):
    """
    Delete a post by ID
    """
    result = await posts.delete_post(post_id,db)
    if result == 'ok':
        return {"message": f"Post with ID {post_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")