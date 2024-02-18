import os
from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Recipes
from forms import RegistrationForm, loginForm
from sqlalchemy.exc import IntegrityError
from helpers import Spoonacular_api
from search_options import diets, cuisines


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///lets_eat_test'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "ihavesecret321")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

    

@app.route("/")
def show_homepage():

    top_recipe = Spoonacular_api.get_recipe(660493)
    pasta_recipes = Spoonacular_api.get_by_type("pasta")
    steak_recipes =  Spoonacular_api.get_by_type("steak")
    chicken_recipes =  Spoonacular_api.get_by_type("chicken")

    if "user_id" in session:
        user_favorites = Recipes.query.filter_by(user_id=session["user_id"]).all()
     

        def get_favorited_ids(fav):
            return fav.recipe_id
            
        fav_recipes = list(map(get_favorited_ids,user_favorites)) 
      
    else:    
        fav_recipes = []

    return render_template("homepage.html",  pasta = pasta_recipes, steak = steak_recipes, chicken = chicken_recipes, favorites=fav_recipes,top_recipe=top_recipe)

@app.route("/users/register", methods=["GET", "POST"])
def handle_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.register(name, email, username, password)
        
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken, Please try again")
            return render_template("registration.html", form=form)

        session["user_id"] = user.id
        flash("Account created successfully", "success")
        return redirect("/")

    return render_template("registration.html", form=form)


@app.route("/users/login", methods=["GET", "POST"])
def handle_login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome, {user.username}!","success")
            session["user_id"] = user.id
            return redirect("/")
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)


  
@app.route("/users/profile/<int:user_id>")
def show_user_profile(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", user=user)


@app.route("/users/profile/favorites")
def show_favorite_recipes():
    user = User.query.get(session["user_id"])
    favorites = user.recipes
    return render_template("favorited_recipes.html", favorites=favorites)


@app.route("/users/favorites/add/<int:recipe_id>", methods=["POST"])
def favorite_recipe(recipe_id):
    if "user_id" in session:
        recipe = Spoonacular_api.get_recipe(recipe_id)
        favorited = Recipes.query.filter_by(
            user_id=session["user_id"], recipe_id = recipe_id).first()

        if favorited:
            db.session.delete(favorited)
            db.session.commit()
        else:
            new_Favorite = Recipes(user_id = session["user_id"], recipe_id=recipe_id, title= recipe["title"] , image = recipe["image"])
            db.session.add(new_Favorite)
            db.session.commit()
            return redirect("/users/profile/favorites")
    
    flash("Must be logged in", "danger")
    return redirect("/users/login")


@app.route("/recipes/search")
def search_recipes():
    search = request.args.get("search").lower()
  
    if (search in cuisines):
        search_res = Spoonacular_api.search("cuisine",search)
    elif (search in diets):
        search_res = Spoonacular_api.search("diet",search)
    
    else:
        search_res = Spoonacular_api.get_by_ingredient(search)
    return render_template("search.html", search=search, results=search_res)

@app.route("/filter/<filter>")
def filter_recipes(filter):
    if (filter == "cuisine"):
        chinese = Spoonacular_api.filter(filter,"Chinese")
        mexican = Spoonacular_api.filter(filter,"Mexican")
        italian = Spoonacular_api.filter(filter,"Italian")
        american = Spoonacular_api.filter(filter,"American")
        
        options = [[{"type":"Chinese"},*chinese],[{"type":"Mexican"},*mexican],[{"type":"Italian"},*italian],[{"type":"American"},*american]]
        return render_template("filters.html", options=options, filter=filter, others=cuisines)
    
    if (filter == "diet"):
        veg = Spoonacular_api.filter(filter,"vegetarian")
        vegan = Spoonacular_api.filter(filter,"vegan")
        gf = Spoonacular_api.filter(filter,"glutenfree")
        ketogenic= Spoonacular_api.filter(filter,"ketogenic")

        options= [[{"type":"Vegetarian"},*veg],[{"type":"Vegan"},*vegan],[{"type":"Gluten Free"},*gf],[{"type":"Ketogenic"},*ketogenic]]
        return render_template("filters.html",options=options, filter=filter,others=diets)
    
    if(filter == "quick"):
        in20= Spoonacular_api.search("maxReadyTime", 30)
        return render_template("quick.html", in20=in20 )
     
    return redirect("/")
    

@app.route("/recipes/<int:recipe_id>")
def show_recipe_details(recipe_id):
    search_res = Spoonacular_api.get_recipe(recipe_id)
    return render_template("recipe_details.html",results=search_res)


@app.route("/users/logout")
def handle_logout():
    session.pop("user_id")
    flash("Logged out successfully", "success")
    return redirect("/users/login")