from fastapi import FastAPI
from models import User


#  calling fastapi library through variable 'app'
app = FastAPI()


users = {
    '1': {
        'name': 'Tom',
        'age': 45
    },
    '2': {
        'name': 'Alice',
        'age': 32
    }
}

#  decorators add more functionalities to functions
#  .get is the method
#  '/' is the route, the address to the webpage that will give us answer

@app.get('/users')


def root():
    return users


@app.get('/users/{user_id}')  # Another decorator. The {} expects parameter.
def get_user(user_id: str):  # Here we define that the parameter should be a string.
    return users[user_id]

#  On the browser running http://127.0.0.1:8000/users/1 returns user 1
