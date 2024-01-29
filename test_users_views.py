from unittest import TestCase
from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lets_eat_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config["WTF_CSRF_ENABLED"]=False
app.config['TESTING'] = True
db.drop_all()
db.create_all()


class UsersTest(TestCase):

    def setUp(self):
        
        User.query.delete()
        u1 = User.register("tester1", "email1@test.com","testman", "password")
        u1.id = 1111
        db.session.commit()

        u1 = User.query.get(u1.id)
        self.u1 = u1

    def tearDown(self):
        db.session.rollback()

    
    def test_handle_registration(self):
        with app.test_client() as client:
            d = {"name":"tester2", "email":"email2@test.com", "username":"testwoman", "password":"password"}
            resp = client.post("/users/register", data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<span>No fuss</span>",html)
            
            
    def test_handle_login(self):
        with app.test_client() as client:
            
            data={"username":"testman", "password": "password"}
            resp = client.post("/users/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<span>No fuss</span>",html)

    def test_show_user_profile(self):
        with app.test_client() as client:
            resp = client.get("users/profile/1111")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn(f"<h2>Welcome {self.u1.username}</h2>", html)

    def test_show_favorite_recipes(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["user_id"] = self.u1.id
            resp = client.get("/users/profile/favorites")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Saved recipes</h1>",html)

    def test_handle_logout(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["user_id"] = self.u1.id
            resp = client.get("/users/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Login</h1>",html)

