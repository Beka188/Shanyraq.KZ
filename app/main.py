import _json
from typing import Annotated, Optional

from fastapi import FastAPI, Form, HTTPException, Response, Depends, Path, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from AdvertisementSearch import AdvertisementSearch
from User import add_user, update, get_user
from auth import AuthHandler, login_jwt, unauthorized
from Advertisement import add_advertisement, Addd, get_ad, delete_add, update_add, add_to_favorite, fav_list, \
    delete_fav, search_advertisements
from UpdateUser import UpdateUserInfo, UpdateAd
from comment import add_comment, com, get_comments, update_comment, delete_comment, total_comments

app = FastAPI()
auth_handler = AuthHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/auth/users/login")
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_jwt(form_data)


@app.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_jwt(form_data)


@app.post("/auth/users")
def sign_up(email: str = Form(...), phone: str = Form(...), password: str = Form(...), name: str = Form(...),
            city: str = Form(...)):
    status_code = add_user(email, phone, password, name, city)
    if status_code == 200:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")


@app.patch("/auth/users/me")
async def update_user_info(update_data: UpdateUserInfo, token: str = Depends(oauth2_scheme)):
    if not token:
        return Response(status_code=403, content="Token is missing")
    user_username = auth_handler.decode_token(token)
    data = update_data.dict(exclude_unset=True)
    update(user_username, data)
    return Response(status_code=200)


@app.get("/auth/users/me")
def user_info(token: Annotated[str, Depends(oauth2_scheme)]):
    username = auth_handler.decode_token(token)
    return get_user(username)


@app.post("/shanyraks")
def add_ad(token: Annotated[str, Depends(oauth2_scheme)], ad: Addd):
    username = auth_handler.decode_token(token)
    ad_id = add_advertisement(username, ad)
    return {"id": ad_id}


@app.get("/shanyraks/{id}")
def get_ad_by_id(ad_id: int):
    count = total_comments(ad_id)
    ad = get_ad(ad_id, count)
    if ad:
        return ad
    else:
        raise HTTPException(status_code=404, detail=f"The ad with id {ad_id} doesn't exist")


@app.patch("/shanyraks/{id}")
def update_ad_info(id: int, token: Annotated[str, Depends(oauth2_scheme)], update_data: UpdateAd):
    username = auth_handler.decode_token(token)
    data = update_data.dict(exclude_unset=True)
    updated = update_add(id, username, data)
    if updated == -1:
        return unauthorized()
    elif not updated:
        raise HTTPException(status_code=404, detail=f"The ad with id {id} doesn't exist")
    return Response(status_code=200)


@app.delete("/shanyraks/{id}")
def delete_ad(id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    username = auth_handler.decode_token(token)
    deleted = delete_add(id, username)
    if deleted == -1:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this advertisement")
    if not deleted:
        raise HTTPException(status_code=404, detail=f"The ad with id {id} doesn't exist")
    return Response(status_code=200)


@app.post("/shanyraks/{id}/comments")
def post_comment(ad_id: int, content: com, token: Annotated[str, Depends(oauth2_scheme)]):
    ad = get_ad_by_id(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail=f"The ad with id {id} doesn't exist")
    username = auth_handler.decode_token(token)
    user = get_user(username)
    data = content.dict()
    add_comment(data, user["id"], ad_id)
    return Response(status_code=200)


@app.get("/shanyraks/{id}/comments")
def get_comments_fastapi(ad_id: int):
    return {"comments": get_comments(ad_id)}


@app.patch("/shanyraks/{id}/comments/{comment_id}")
def update_com(id: int, comment_id: int, token: Annotated[str, Depends(oauth2_scheme)], content: com):
    username = auth_handler.decode_token(token)
    updated = update_comment(comment_id, username, id, content.content)
    if updated == -1:
        raise HTTPException(status_code=403, detail="You are not allowed to change this comment")
    elif updated == 0:
        raise HTTPException(status_code=404, detail=f"Doesn't exist")
    return Response(status_code=200)


@app.delete("/shanyraks/{id}/comments/{comment_id}")
def delete_com(id: int, comment_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    username = auth_handler.decode_token(token)
    deleted = delete_comment(id, comment_id, username)
    if deleted == -1:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this comment")
    elif deleted == 0:
        raise HTTPException(status_code=404, detail=f"Doesn't exist")
    return Response(status_code=200)


@app.post("/auth/users/favorites/shanyraks/{id}")
def add_favorite(token: Annotated[str, Depends(oauth2_scheme)],
                 id: int = Path(..., description="The ID of the advertisement to add to favorites")):
    username = auth_handler.decode_token(token)
    user_id = get_user(username)["id"]
    if get_ad(id):
        added = add_to_favorite(user_id, id)
        if added:
            return {"message": "Advertisement added to favorites"}
    else:
        raise HTTPException(status_code=404, detail=f"Ad with id: {id} doesn't exist")


@app.get("/auth/users/favorites/shanyraks")
def get_favorite_list(token: Annotated[str, Depends(oauth2_scheme)]):
    username = auth_handler.decode_token(token)
    return {"shanyraks": fav_list(username)}


@app.delete("/auth/users/favorites/shanyraks/{id}")
def delete_from_fav_list(token: Annotated[str, Depends(oauth2_scheme)], id: int = Path(...,
                                                                                       description="Id of the ad that you want to delete from the favorite list")):
    username = auth_handler.decode_token(token)
    if delete_fav(username, id):
        return {"message": "Successfully deleted!"}
    else:
        raise HTTPException(status_code=404, detail=f"Ad with such id and/or user_id doesn't exist")


@app.get("/shanyraks")
def search(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), type: Optional[str] = None,
           rooms_count: Optional[int] = None, price_from: Optional[int] = None, price_until: Optional[int] = None):
    search_parameters = AdvertisementSearch(limit=limit, offset=offset, type=type, rooms_count=rooms_count,
                                            price_from=price_from, price_until=price_until)
    return search_advertisements(search_parameters)


if __name__ == '__main__':
    # add_user("esil@.com", "8705", "password", "Beka", "Astana")
    # add_user("hghg@.com", "+8842", "password", "Arman", "Pavlodar")
    # add_user("tora@.com", "9021", "password", "Maksat", "Almaty")
    # print(get_user("tora@.com"))
    # print_all()
    # print_all_ad()
    # print_all_fav()
    # print_all_comments()
    # get_comments(1)
    # print(fav_list("esil@.com"))
    search = AdvertisementSearch()
    search.type = "sell"
    search.rooms_count = 2
    print(search_advertisements(search))
