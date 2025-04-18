import os
import json
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style

load_dotenv()

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
USER_PROFILE_FILE = "userProfile/user_profiles.json"

init(autoreset=True)

def save_user_profile(userName, profile_data):
    try:
        with open(USER_PROFILE_FILE, "r") as file:
            profiles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}

    profiles[userName] = profile_data

    with open(USER_PROFILE_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

def load_user_profile(userName):
    try:
        with open(USER_PROFILE_FILE, "r") as file:
            profiles = json.load(file)
        return profiles.get(userName)
    except(FileNotFoundError, json.JSONDecodeError):
        return None

def get_user_log_file(userName):
    os.makedirs("dietLogs", exist_ok=True)
    return f"dietLogs/{userName}_diet_log.json"

def get_info(userName):
    existing_profile = load_user_profile(userName)
    if existing_profile:
        print("\n✅ Found existing profile. Using saved data")
        return existing_profile['calIn']
    
    while True:
        try:
            age = float(input("\nEnter your age (in years): "))
            if age <= 0:
                raise ValueError("Age can not be a negative number")
            gender = input("Enter your gender (male/female): ").strip().lower()
            if gender == "male":
                s = 5.00
            elif gender == "female":
                s = -161.00
            else:
                raise ValueError("Invalid gender. Please specify 'male' or 'female'.")
            height = float(input("Enter your height (in cm): "))
            weight = float(input("Enter your weight (in kg): "))
            target = float(input("Enter how much weight you want to lose (in kg): "))
            time = float(input("Enter the time to achieve your target (in days): "))
            print("Enter your activity level (1-5):")
            print("1. Sedentary (little to no exercise)")
            print("2. Lightly active (1-3 days/week)")
            print("3. Moderately active (3-5 days/week)")
            print("4. Very active (6-7 days/week)")
            print("5. Super active (athlete, intense training)")
            actLvl = int(input("Your choice: "))
            if actLvl not in range(1, 6):
                raise ValueError("Activity level must be between 1 and 5.")

            
            # Mifflin-St Jeor Equation to calculate Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE)
            USER_BMR = (10.00 * weight) + (6.25 * height) - (5.00 * age) + s

            activity_multipliers = {
                1: 1.20,
                2: 1.37,
                3: 1.55,
                4: 1.72,
                5: 1.90
            }
            multiplier = activity_multipliers.get(int(actLvl))
            USER_TDEE = round(USER_BMR * multiplier, 2)

            calDef = round((target * 7700) / time, 2)

            if calDef >= USER_TDEE:
                print("\n⚠️ Warning: Your target weight loss is too aggressive.")
                print("Please adjust your target weight loss or time frame.")
                continue

            calIn = round(USER_TDEE - calDef, 2)

            profile_data = {
                "weight": weight,
                "target": target,
                "time": time,
                "height": height,
                "age": age,
                "gender": gender,
                "actLvl": actLvl,
                "calIn": calIn
            }
            save_user_profile(userName, profile_data)

            return calIn

        except ValueError as e:
            print(f"❌ Error: {e}. Please Re-enter your inputs.")

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

def view_logs(userName):
    log_file = get_user_log_file(userName)
    try:
        with open(log_file, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
    
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Food Log:")

    total_calories_per_meal = {"Breakfast": 0, "Lunch": 0, "Snacks": 0, "Dinner": 0}
    grand_total_calories = 0
    
    for meal, items in logs.items():
        print(f"\n{Fore.CYAN}{meal}:")
        if items:
            for entry in items:
                print(f"{Fore.WHITE}  - {entry['food']} ({entry['portion']}) - {Fore.YELLOW}{entry['calories']} cal")
                total_calories_per_meal[meal] += entry['calories']
        else:
            print(f"{Fore.YELLOW}No entries.")

    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}--- Total Calories per Meal ---")
    for meal, total in total_calories_per_meal.items():
        print(f"{Fore.CYAN}{meal}: {Fore.YELLOW}{total} cal")
        grand_total_calories += total 
    
    print(f"\n{Fore.CYAN}Grand Total Calories for the Day: {Fore.WHITE}{Style.BRIGHT}{grand_total_calories} cal")
    
def log_food(userName, meal_type, food_name, portion, calories):
    log_file = get_user_log_file(userName)
    try:
        with open(log_file, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
    
    default_logs = {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
    logs = {**default_logs, **logs}

    logs[meal_type].append({"food": food_name, "portion": portion, "calories": calories})

    with open(log_file, "w") as file:
        json.dump(logs, file, indent=4)

    print(f"Logged: {food_name} ({portion}) - {calories} kcal for {meal_type}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')