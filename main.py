import utils as ut
import os

if not os.path.exists(".env"):
    raise FileNotFoundError("❌ Missing .env file. Please create one with APP_ID and API_KEY.")

def main():
    print("=" * 50)
    print("          Welcome to the Calorie Tracker")
    print("=" * 50)

    print("\n1.Create a new user\n2.Log in exisiting user")
    print("-" * 50)
    new_Choice = int(input("Enter your choice: "))
    userName = input("\nEnter your username: ").strip()

    if new_Choice == 1:
        if ut.load_user_profile(userName):
            confirm = input("⚠️ A profile with this username already exists. Overwrite? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❌ Profile creation canceled.")
            return
        calories = ut.get_info(userName)
        print(f"\n✨Your daily calorie intake should be: {calories} calories\n")
    elif new_Choice == 2:
        profile = ut.load_user_profile(userName)
        if profile:
            calories = profile['calIn']
            print(f"\n✨Welcome back, {userName}! Your daily calorie intake is: {calories} calories\n")
        else:
            print("❌ No profile found for this username. Please create a new user.")
            return

    while True:
        print("\nMain Menu")
        print("-" * 50)
        print("1. Log Food\n2. View Log\n3. Exit")
        print("-" * 50)
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            while True:
                print("\nLog Food Menu")
                print("-" * 50)
                print("1. Breakfast\n2. Lunch\n3. Snacks\n4. Dinner\n5. Back to Main Menu")
                print("-" * 50)
                meal_choice = input("Enter meal type: ").strip()
                meal_map = {"1": "Breakfast", "2": "Lunch", "3": "Snacks", "4": "Dinner"}

                if meal_choice in meal_map:
                    meal_type = meal_map[meal_choice]
                    food = input("Enter food name: ").strip()
                    portion = input("Enter portion size (e.g., 100g, 1 unit): ").strip()
                    query = f"{portion} of {food}"
                    data = ut.get_nutrition(query)
                    if data and "foods" in data:
                        item = data["foods"][0]
                        ut.log_food(userName, meal_type, item['food_name'], portion, item['nf_calories'])
                        print(f"✅ Logged: {item['food_name']} ({portion}) - {item['nf_calories']} cal")
                    else:
                        print("⚠️ Error: Unable to fetch nutrition data.")
                elif meal_choice == "5":
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
        elif choice == "2":
            print("\n📜 Viewing Food Log...")
            ut.view_logs(userName)
            print(f"🔥 Your target Calories :{calories} cal")
        elif choice == "3":
            print("\nThank you for using the Calorie Tracker. Goodbye!")
            print("=" * 50)
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()