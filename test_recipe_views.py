from unittest import TestCase
from app import app
from models import User,Recipes, db
from flask import session 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lets_eat_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config["WTF_CSRF_ENABLED"]=False
app.config['TESTING'] = True
db.drop_all()
db.create_all()


class RecipeTest(TestCase):

    def setUp(self):
        
        User.query.delete()
        u1 = User.register("tester1", "email1@test.com","testman", "password")
        u1.id = 1111
        db.session.commit()

        u1 = User.query.get(u1.id)
        self.u1 = u1


        Recipes.query.delete()
        recipe1 = Recipes(user_id = self.u1.id, recipe_id= 654857, title="Pasta On The Border")
        recipe1.id = 22
        db.session.add(recipe1)
        db.session.commit()
        
        recipe1 = Recipes.query.get(22)
        self.recipe1 = recipe1

    def tearDown(self):
        db.session.rollback()            

    def test_show_favorite_recipes(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["user_id"] = self.u1.id
            resp = client.get("/users/profile/favorites")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Saved recipes</h1>",html)

    def test_favorite_recipe(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                    sess["user_id"] = self.u1.id
            resp = client.post("/users/favorites/add/654857", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["user_id"], self.u1.id)
            self.assertIn("<span>No fuss</span>",html)
    
    def test_show_recipe_details(self):
        with app.test_client() as client:
            resp= client.get(f"/recipes/{self.recipe1.recipe_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h2 style="text-align: center">{self.recipe1.title}</h2>',html) 

    def test_filter_recipes_cuisines(self):
        with app.test_client() as client:
            resp= client.get("/filter/cuisine")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<b>Check out other cuisines :</b>",html) 

    def test_filter_recipes_diets(self):
        with app.test_client() as client:
            resp= client.get("/filter/diet")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<b>Check out other diets :</b>",html) 

    def test_filter_recipes_quick(self):
        with app.test_client() as client:
            resp= client.get("/filter/quick")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3 style="text-align: center">Meals ready in 30 minutes or less</h3>',html)

    def test_search_recipes(self):
        with app.test_client() as client:
            resp= client.get("/recipes/search?search=apples")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>"Apples" recipes</h2>',html) 



  