import _json
from typing import Annotated, Optional

from fastapi import FastAPI, Form, HTTPException, Request, Response, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from User import add_user, login, print_all, update, get_user, delete_all_data
from auth import AuthHandler, login_jwt
from Advertisement import add_advertisement, print_all_ad
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
def add_ad(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
    token = authorization_header.split("Bearer ")[1]
    username = auth_handler.decode_token(token)
    data = request.json()
    ad_id = add_advertisement(username, data)
    return {"id": ad_id}


if __name__ == '__main__':
    # add_user("esil@.com", "8705", "password", "Beka", "Astana")
    # add_user("hghg@.com", "+8842", "password", "Arman", "Pavlodar")
    # add_user("tora@.com", "9021", "password", "Maksat", "Almaty")
    # print(get_user("tora@.com"))
    # print_all()
    print_all_ad()



