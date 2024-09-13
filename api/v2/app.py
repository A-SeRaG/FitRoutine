from fastapi import FastAPI, Response, Query, Request, Form
from functools import wraps
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from models import storage
from models.exercise import Exercise
from models.session import Session
from models.review import Review
from models.user import User
from hashlib import md5
import inspect

app = FastAPI()

app.mount("/static/css", StaticFiles(directory="CSS"), name="css")
app.mount("/static/img", StaticFiles(directory="IMG"), name="img")
app.mount("/static/js", StaticFiles(directory="JS"), name="js")

templates = Jinja2Templates(directory=".")


def logged(func):
    @wraps(func)
    def ensure_logged_in(*args, **kwargs):
        signature = inspect.signature(func)
        bound_args = signature.bind(*args, **kwargs)
        bound_args.apply_defaults()
        request = bound_args.arguments.get("request", None)
        if request:
            session_id = request.cookies.get("session_id", None)
            user_id = request.cookies.get("user_id", None)
            if session_id is None or user_id is None:
                return RedirectResponse(url="/login?login_error User must log in first", status_code=303)
            session = storage.get(Session, session_id)  
            if session.user_id == user_id:
                if session.expires_at < datetime.now():
                    return RedirectResponse(url="/login?login_error Session expired", status_code=303)
                return func(*args, **kwargs)
        return RedirectResponse(url="/login?login_error session does not exist", status_code=303)
    return ensure_logged_in


@app.post("/register")
def register(
        response: Response,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        gender: str = Form("Male")):
    existing_users = storage.all(User)
    for user in existing_users:
        if user.email.lower() == email.lower():
            return RedirectResponse(url="/login?register_error Email already exist", status_code=303)
    newUser = User(email=email, password=password,
                   last_name=last_name, first_name=first_name, gender=gender)
    storage.new(newUser)
    session = Session(user_id=newUser.id)
    storage.new(session)
    storage.save()
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="session_id", value=str(session.id))
    response.set_cookie(key="user_id", value=str(newUser.id))
    return response


@app.get("/login")
def login_page(request: Request):
    register_error = request.query_params.get("register_error", None)
    login_error = request.query_params.get("login_error", None)
    return templates.TemplateResponse(name="Login.html", context={"request": request, "register_error": register_error, "login_error": login_error})


@app.post("/login")
def login(response: Response,
          email: str = Form(...),
          password: str = Form(...)):
    hashed_password = md5(password.encode()).hexdigest()
    existing_users = storage.all(User)
    for user in existing_users:
        if user.password == hashed_password and user.email.lower() == email.lower():
            session = Session(user_id=user.id)
            storage.new(session)
            storage.save()
            response = RedirectResponse(url="/", status_code=303)
            response.set_cookie(key="session_id", value=str(session.id))
            response.set_cookie(key="user_id", value=str(user.id))
            return response
    return RedirectResponse("/login?login_error Wrong password or email", status_code=303)


@app.get("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    sessions = storage.all(Session)
    for session in sessions:
        if session.id == session_id:
            storage.delete(session)
            storage.save()
            response = RedirectResponse(url="/")
            response.delete_cookie(key="session_id")
            response.delete_cookie(key="user_id")
            return response
    return RedirectResponse("/login?login_error User must log in first")


@app.get('/')
def home(request: Request):
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
    return templates.TemplateResponse(name='Workouts.html', context={"request": request, "exercises": exercises_formatted})


@app.get('/contact')
def contact(request: Request):
    return templates.TemplateResponse(name='Contact.html', context={"request": request})


@app.get('/feedback')
@logged
def review(request: Request):
    feedback_error = request.query_params.get('feedback_error', None)
    return templates.TemplateResponse(name='Feedback.html', context={"request": request, "feedback_error": feedback_error})


@app.post('/feedback')
@logged
def review(
        request: Request,
        exercise_name: str = Form(...),
        text: str = Form(...),
        stars: int = Form(...)):
    id = None
    exercises = storage.all(Exercise)
    for value in exercises.values():
        for exercise in value:
            if exercise.name.lower() == exercise_name.lower():
                id = exercise.id
                break
    if id is None:
        return RedirectResponse(url='/feedback?feedback_error=Exercise does not exist', status_code=303)
    user_id = request.cookies.get('user_id')
    review = Review(user_id=user_id, exercise_id=id, stars=stars, text=text)
    storage.new(review)
    storage.save()
    return RedirectResponse(url='/', status_code=303)
