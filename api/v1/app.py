from pydantic import BaseModel
from fastapi import FastAPI, Response, Query, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Callable
from models import storage
from models.exercise import Exercise
from models.session import Session
from models.review import Review
from models.user import User
from hashlib import md5

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class BodyRequest(BaseModel):
    exercise_name: str
    text: str
    stars: int
    user_id: str = None

app = FastAPI()

app.mount("/static/css", StaticFiles(directory="CSS"), name="css")
app.mount("/static/img", StaticFiles(directory="IMG"), name="img")
app.mount("/static/js", StaticFiles(directory="JS"), name="js")

templates = Jinja2Templates(directory="HTML")

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
    height_in_meters = h / 100
    bmi = w / (height_in_meters ** 2)
    return {"bmi": bmi}


@app.get('/logout')
def logout(response:Response, request:Request):
    session_id = request.cookies.get('session')
    sessions = storage.all(Session)
    for thissession in sessions:
        if thissession.id == session_id:
            storage.delete(thissession)
            storage.save()
            response = RedirectResponse(url='/')
            response.delete_cookie(key='session')
            return response
    return {'Error': 'User must be logged in'}

@app.get('/')
def all_users(request: Request):
    reviews_data = []
    reviews = storage.all(Review)
    for review in reviews:
        data = {}
        data['user'] = storage.get(User, review.user_id).email
        data['exercise'] = storage.get(Exercise, review.exercise_id).name
        data['text'] = review.text
        data['stars'] = review.stars
        reviews_data.append(data)
    return templates.TemplateResponse(name='Home.html', context={"request": request, "reviews": reviews_data})

@app.get('/contact')
def nothing(request: Request):
    return templates.TemplateResponse(name='Contact.html', context={"request": request})

@app.get('/workout')
def exercises(request: Request):
    exercises_formatted = []
    exercises = storage.all(Exercise)
    for muscle, muscle_exercises in exercises.items():
        for muscle_exercise in muscle_exercises:
            data = {
                "target_muscle": muscle,
                "name": muscle_exercise.name,
                "sets": muscle_exercise.sets,
                "description": muscle_exercise.description,
                "rest_period_in_seconds": muscle_exercise.rest_period_in_seconds
            }
            exercises_formatted.append(data)
    return templates.TemplateResponse(name='Workouts.html', context={"request": request, "exercises":exercises_formatted})


@app.post('/register')
def register(request:Request,
             response:Response,
             first_name: str=Form(...),
             last_name: str=Form(...),
             email: str=Form(...),
             password: str=Form(...)):
    if not email:
        return {'Error': 'Email is required field'}
    elif not password:
        return {'Error': 'Password is required field'}
    users = storage.all(User)
    for user in users:
        if user.email.lower() == email.lower():
            return {'Error': 'Email already in use'}
    newUser = User(email=email, password=password, last_name=last_name, first_name=first_name)
    storage.new(newUser)
    storage.save()
    session = Session(user_id=newUser.id)
    storage.new(session)
    storage.save()
    response = RedirectResponse(url='/', status_code=303)
    response.set_cookie(key='session', value=str(session.id))
    return response

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post('/login')
def login(response: Response, request:Request,
          email:str=Form(...),
          password:str=Form(...)):
    if not email:
        return {'Error': 'Email is required field'}
    elif not password:
        return {'Error': 'Password is required field'}
    hashed_password = md5(password.encode()).hexdigest()
    users = storage.all(User)
    for user in users:
        if user.password == hashed_password and user.email.lower() == email.lower():
            session = Session(user_id=user.id)
            storage.new(session)
            storage.save()
            response = RedirectResponse(url='/', status_code=303)
            response.set_cookie(key='session', value=str(session.id))
            return response
    return {'error': 'user password and email did not match any user in our database'}

@app.post('/feedback')
def review(
    request: Request,
    exercise_name: str = Form(...),
    text: str = Form(...),
    stars: int = Form(...)):
    id = ""
    exercises = storage.all(Exercise)
    for key, value in exercises.items():
        for exercise in value:
            if exercise.name.lower() == exercise_name.lower():
                id = exercise.id
    if id == "":
        return {"failed": 'Cannot find this exercise in our database'}
    session = None
    session_id = request.cookies.get('session')
    sessions = storage.all(Session)
    for thissession in sessions:
        if thissession.id == session_id:
            session = thissession
            break
    else:
        return {'Error': 'User must be logged in'}
    user_id = session.user_id
    if datetime.now() > session.expires_at:
        storage.delete(session)
        storage.save()
        return {'Error': 'Session expired, Please log in again'}
    review = Review(user_id=user_id, exercise_id=id, stars=stars, text=text)
    storage.new(review)
    storage.save()
    return RedirectResponse(url='/', status_code=303)

@app.get('/feedback')
def review(request: Request):
    return templates.TemplateResponse(name='Feedback.html', context={"request": request})

@app.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse(name='Login.html', context={"request":request})
