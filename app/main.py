from fastapi import FastAPI, Form
from User import add_user, User

app = FastAPI()


@app.post("/auth/users")
def sign_up(email: str = Form(...), phone: str = Form(...), password: str = Form(...), name: str = Form(...),
            city: str = Form(...)):
    add_user(email, phone, password, name, city)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
