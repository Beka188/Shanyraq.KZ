from fastapi import FastAPI, Form, HTTPException
from User import add_user, User, login, print_all
from pydantic import BaseModel
import hashlib

app = FastAPI()


class LoginRequest:
    username: str
    password: str


@app.post("/auth/users")
def sign_up(email: str = Form(...), phone: str = Form(...), password: str = Form(...), name: str = Form(...),
            city: str = Form(...)):
    status_code = add_user(email, phone, password, name, city)
    if status_code == 200:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")


@app.get("/auth/users/login", response_model=None)
def user_login(username: str, password: str):
    # username = request.username
    # password = request.username
    # return 200
    if login(username, password):
        return 200  # also jwt token
    else:
        raise HTTPException(status_code=401, detail="Wrong password or email")


if __name__ == '__main__':
    add_user("email", "ph", "pas", "name", "city")
    print_all()


