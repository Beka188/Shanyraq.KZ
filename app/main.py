from fastapi import FastAPI, Form, HTTPException, Request
from User import add_user, login, print_all
from auth import AuthHandler

app = FastAPI()
auth_handler = AuthHandler()

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


@app.post("/auth/users/login")
def user_login(username: str = Form(...), password: str = Form(...)):
    if login(username, password):
        jwt_token = auth_handler.encode_token(username)
        return {"access_token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Wrong password or email")


if __name__ == '__main__':
    print_all()



