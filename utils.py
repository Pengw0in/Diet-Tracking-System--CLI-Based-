import os
import json
from dotenv import load_dotenv
import requests


load_dotenv()

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
LOG_FILE = "diet_log.json"

def get_info():
    weight = float(input("Enter your weight (in kg): "))
    target = float(input("Enter your target weight (in kg): "))
    time = float(input("Enter the time to achieve your target (in days): "))
    height = float(input("Enter your height (in cm): "))
    age = float(input("Enter your age (in years): "))
    gender = input("Enter your gender (male/female): ").strip().lower()
    if gender.lower() == "male":
        s = 5.00
    elif gender.lower() == "female":
        s = -161.00
    else:
        raise ValueError("Invalid gender. Please specify 'male' or 'female'")
    actLvl = int(input("Enter your activity level (1-5): "))
    if actLvl not in range(1, 6):
            raise ValueError("Activity level must be between 1 and 5.")

    USER_BMR = (10.00 * weight) + (6.25 * height) - (5.00 * age) - s

    activity_multipliers = {
        1: 1.20,
        2: 1.37,
        3: 1.55,
        4: 1.72,
        5: 1.90
    }
    multiplier = activity_multipliers.get(actLvl)
    USER_TDEE = round(USER_BMR * multiplier, 2)

    calDef = round(((weight - target) * 7700) / time, 2)
    calInt = round(USER_TDEE - calDef, 2)

    return calInt

def get_nutrition(food_item):
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"query": food_item}
    response = requests.post(BASE_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.text)
        return None


def view_logs():
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
    
    print("\nFood Log:")

    total_calories_per_meal = {"Breakfast": 0, "Lunch": 0, "Snacks": 0, "Dinner": 0}
    grand_total_calories = 0
    
    for meal, items in logs.items():
        print(f"\n{meal}:")
        if items:
            for entry in items:
                print(f"  - {entry['food']} ({entry['portion']}) - {entry['calories']} kcal")
                total_calories_per_meal[meal] += entry['calories']
        else:
            print("No entries.")

    print("\n--- Total Calories per Meal ---")
    for meal, total in total_calories_per_meal.items():
        print(f"{meal}: {total} kcal")
        grand_total_calories += total 
    

    print("\nGrand Total Calories for the Day:", grand_total_calories, "kcal") 
    print("Your target Calories :" , get_info()) 
      
    
    
def log_food(meal_type, food_name, portion, calories):
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
    
    default_logs = {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
    logs = {**default_logs, **logs}

    logs[meal_type].append({"food": food_name, "portion": portion, "calories": calories})

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

    print(f"Logged: {food_name} ({portion}) - {calories} kcal for {meal_type}")