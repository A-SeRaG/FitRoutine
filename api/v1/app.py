from pydantic import BaseModel
from fastapi import FastAPI, Response, Query
from pydantic import BaseModel, EmailStr
from models import storage
from models.exercise import Exercise
from models.session import Session
from models.user import User
from hashlib import md5

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

app = FastAPI()


@app.get('/api/v1/exercise')
def all_exercises():
    return storage.all(Exercise)

@app.get('/api/v1/muscle={target_muscle}')
def get_muscle_exercise(target_muscle:str):
    target_muscle = target_muscle.lower()
    if target_muscle in storage.all(Exercise):
        return storage.all(Exercise)[target_muscle]
    return []

@app.get('/api/v1/name={exercise_name}')
def get_exercise(exercise_name: str):
    exercises = []
    all_exercises = storage.all(Exercise)
    for key, values in all_exercises.items():
        index = 0
        for value in values:
            if value.name.lower() == exercise_name.lower():
                exercises.append(all_exercises[key][index])
            index = index + 1
    return exercises


@app.get('/api/v1/bmi')
def calculate_bmi(w: float = Query(..., description="Weight in kilograms"), h: float = Query(..., description="Height in centimeters")):
    if h <= 0:
        return {"Error": "Height must be greater than 0"}
    height_in_meters = h / 100  # Convert height to meters
    bmi = w / (height_in_meters ** 2)
    return {"bmi": bmi}


@app.get('/')
def all_users():
    return storage.all(User)

@app.post('/register')
def register(body: RegisterRequest, response:Response):
    if not body.email:
        return {'Error': 'Email is required field'}
    elif not body.password:
        return {'Error': 'Password is required field'}
    users = storage.all(User)
    for user in users:
        if user.email == body.email:
            return {'Error': 'Email already in use'}
    newUser = User(email=body.email, password=body.password, last_name=body.last_name, first_name=body.first_name)
    storage.new(newUser)
    storage.save()
    session = Session(user_id=newUser.id)
    storage.new(session)
    storage.save()
    response.set_cookie(key='session', value=str(session.id))
    return {'message': 'User registered successfully', 'session_id': str(session.id)}

@app.post('/login')
def login(email, password, response: Response):
    hashed_password = md5(password.encode()).hexdigest()
    users = storage.all(User)
    for user in users:
        if user.password == hashed_password and user.email.lower() == email.lower():
            session = Session(user_id=user.id)
            storage.new(session)
            storage.save()
            response.set_cookie(key='session', value=str(session.id))
            return {'message': 'User logged in successfully', 'new_session_id': str(session.id)}
    return {'error': 'user password and email did not match any user in our database'}
