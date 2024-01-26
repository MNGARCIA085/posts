
from db.models.users import UserFilter


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


