from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from User import add_user
# from requests import Request, Redi
app = FastAPI()


@app.post("/auth/users")
def sign_up(email: str = Form(...), phone: str = Form(...), password: str = Form(...), name: str = Form(...),
            city: str = Form(...)):
    adding_user = add_user(email, phone, password, name, phone)
    if adding_user == -1:
        return {"User already registered!"}
    return 'HTTP/1.1', 200, "OK"
