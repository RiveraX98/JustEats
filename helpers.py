
import requests

BASE_URL ="https://api.spoonacular.com" 
API_KEY = "dc64625ccebe48d488c12a9b0796ac22"
API_KEY2="21b179b10a784b999875a187ad110186"
API_KEY3="13bfd76760c74610a427af43557ad4b4"



class Spoonacular_api:

    def get_random():
        res = requests.get(f"{BASE_URL}/recipes/random?number=10&apiKey={API_KEY3}")
        recipes = res.json()
        return recipes["recipes"]
    
    def get_by_type(type):
        res = requests.get(f"{BASE_URL}/recipes/complexSearch?query={type}&number=8&apiKey={API_KEY3}")
        recipes = res.json()
        print(recipes)
        return recipes["results"]
    
    def get_by_ingredient(ingredient):
        res = requests.get(f"{BASE_URL}/recipes/findByIngredients?ingredients={ingredient}&number=20&apiKey={API_KEY3}")
        recipes = res.json()
        return recipes
    
    def get_recipe(id):
        res = requests.get(f"{BASE_URL}/recipes/{id}/information?apiKey={API_KEY3}")
        recipes = res.json()
        return recipes
    
    def search(filter_by, item):
        res = requests.get(f"{BASE_URL}/recipes/complexSearch?{filter_by}={item}&number=24&apiKey={API_KEY3}")
        recipes = res.json()
        return recipes["results"]
    
    def filter(filter_by, filter):
        res = requests.get(f"{BASE_URL}/recipes/complexSearch?{filter_by}={filter}&number=8&apiKey={API_KEY3}")
        recipes = res.json()
        return recipes["results"]

