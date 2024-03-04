from fastapi import FastAPI, Form, HTTPException, Request
from User import add_user, login, print_all


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


@app.post("/auth/users/login")
def user_login(username: str = Form(...), password: str = Form(...)):
    if login(username, password):
        return 200  # also jwt token
    else:
        raise HTTPException(status_code=401, detail="Wrong password or email")


if __name__ == '__main__':
    print_all()



