from db.models.users import UserFilter
from db.models.posts import PostFilter
from bson import ObjectId

# renderizar correctamente
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


# consulta
def get_query(f:UserFilter):
    query = {}
    
    # username, lista dsp-.
    if f.username:
        query["username"] = f.username

    if f.username__contains: # gana si pongo ambos
        query['username'] = {"$regex": f".*{f.username__contains}.*", "$options": "i"}
    
    if f.email:
        query["email"] = f.email
    
    if f.email__contains:
        query["email"] = {"$regex": f".*{f.email__contains}.*", "$options": "i"}

    if f.first_name:
        query["first_name"] = f.first_name
    
    if f.first_name__contains: 
        query['first_name'] = {"$regex": f".*{f.first_name__contains}.*", "$options": "i"}

    if f.last_name:
        query["last_name"] = f.last_name
    
    if f.last_name__contains: 
        query['last_name'] = {"$regex": f".*{f.last_name__contains}.*", "$options": "i"}

    #if username: si fuese lista
    #    query["$or"] = [{"username": user} for user in username]
    return query



#########################  2. POSTS ################################

# renderizar post
def post_helper(post,author) -> dict:
    return {
            "id": str(post['_id']),
            "title": post['title'],
            "content": post['content'],
            "date": post['date'],
            "last_modified": post['last_modified'],
            "author": {
                "id": str(author['_id']),
                "first_name": author['first_name'],
                "last_name": author['last_name'],
                "username": author['username'],
                "email": author['email']
            },
            "comments" : post.get('comments', [])
        }



def get_post_query(f:PostFilter):
    query = {}
    
    if f.title:
        query["title"] = f.title
    if f.title__contains: # gana si pongo ambos
        query['title'] = {"$regex": f".*{f.title__contains}.*", "$options": "i"}

    if f.content:
        query["content"] = f.content
    if f.content__contains: # gana si pongo ambos
        query['content'] = {"$regex": f".*{f.content__contains}.*", "$options": "i"}


    if f.author:
        query["author"] = ObjectId(f.author)

    if f.author__username:
        query["author.username"] = f.author__username    
    

    return query