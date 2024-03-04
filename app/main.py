from fastapi import FastAPI, Form, HTTPException, Request, Response
from User import add_user, login, print_all, update, get_user, delete_all_data
from auth import AuthHandler

app = FastAPI()
auth_handler = AuthHandler()


@app.post("/auth/users")
def sign_up(email: str = Form(...), phone: str = Form(...), password: str = Form(...), name: str = Form(...),
            city: str = Form(...)):
    status_code = add_user(email, phone, password, name, city)
    if status_code == 200:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")


@app.post("/auth/users/login")
def user_login(username: str = Form(...), password: str = Form(...)):
    if login(username, password):
        jwt_token = auth_handler.encode_token(username)
        return {"access_token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Wrong password or email")


@app.patch("/auth/users/me")
async def update_user_info(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
    token = authorization_header.split("Bearer ")[1]
    user_username = auth_handler.decode_token(token)
    data = await request.json()
    update(user_username, data)
    return Response(status_code=200)


@app.get("/auth/users/me")
def user_info(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
    token = authorization_header.split("Bearer ")[1]
    username = auth_handler.decode_token(token)
    return get_user(username)


if __name__ == '__main__':
    add_user("esil@.com", "8705", "password", "Beka", "Astana")
    add_user("hghg@.com", "+8842", "password", "Arman", "Pavlodar")
    add_user("tora@.com", "9021", "password", "Maksat", "Almaty")
    print(get_user("tora@.com"))
    print_all()

