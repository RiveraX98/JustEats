
from app import app 
from unittest import TestCase
from models import db, User, Recipes

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lets_eat_test'
app.config['SQKAKCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        u1 = User.register("tester1", "email1@email.com","testman", "password")
        u1.id = 11
       
        db.session.commit()
        
        u1 = User.query.get(u1.id)
        self.u1 = u1
   

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):

        u2 = User.register("tester2", "email2@email.com","testwoman", "password")
        u2.id = 22
       
        db.session.commit()
        
        u2 = User.query.get(u2.id)
       
        users = User.query.all()
        self.assertEqual(u2.id, 22)
        self.assertEqual(u2.name, "tester2")
        self.assertEqual(len(users), 2)


class RecipesModelTestCase(TestCase):
    def setUp(self): 
        User.query.delete()
        u1 = User.register("tester1", "email1@email.com","testman", "password")
        u1.id = 11
        db.session.commit()
        
        u1 = User.query.get(u1.id)
        self.u1 = u1
   
        Recipes.query.delete()
        recipe1 = Recipes(user_id = self.u1.id, recipe_id= 12, title="fakeTitle")
        recipe1.id = 22
        db.session.add(recipe1)
        db.session.commit()
        
        recipe1 = Recipes.query.get(22)
        self.recipe1 = recipe1

       

    def tearDown(self):
        db.session.rollback()

    def test_recipe_model(self):

        recipe2 = Recipes(user_id = self.u1.id, recipe_id= 15, title="fakeTitle")
        recipe2.id = 33
        db.session.add(recipe2)
        db.session.commit()
        
        recipe2 = Recipes.query.get(33)
        
        self.assertEqual(recipe2.recipe_id,12)
        self.assertEqual(recipe2.user_id,11)
        self.assertEqual(len(self.u1.recipes), 2)