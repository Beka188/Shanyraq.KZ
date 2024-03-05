import _json
from typing import Annotated, Optional

from fastapi import FastAPI, Form, HTTPException, Request, Response, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from User import add_user, print_all, update, get_user, delete_all_data
from auth import AuthHandler, login_jwt
from Advertisement import add_advertisement, print_all_ad, Addd, get_ad, delete_add
from UpdateUser import UpdateUserInfo

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
    ad = get_ad(ad_id)
    if ad:
        return ad
    else:
        raise HTTPException(status_code=404, detail=f"The ad with id {ad_id} doesn't exist")


@app.delete("/shanyraks/{id}")
def delete_ad(id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    username = auth_handler.decode_token(token)
    deleted = delete_add(id, username)
    if deleted == -1:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this advertisement")
    if not deleted:
        raise HTTPException(status_code=404, detail=f"The ad with id {id} doesn't exist")
    return 200


if __name__ == '__main__':
    # add_user("esil@.com", "8705", "password", "Beka", "Astana")
    # add_user("hghg@.com", "+8842", "password", "Arman", "Pavlodar")
    # add_user("tora@.com", "9021", "password", "Maksat", "Almaty")
    # print(get_user("tora@.com"))
    print_all()
    print_all_ad()
