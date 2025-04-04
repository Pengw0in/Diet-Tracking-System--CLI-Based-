import utils as ut
import os

if not os.path.exists(".env"):
    raise FileNotFoundError("❌ Missing .env file. Please create one with APP_ID and API_KEY.")

def main():
    while True:
        ut.clear_screen()
        print("=" * 50)
        print("          Welcome to the Calorie Tracker")
        print("=" * 50)

        print("\n1.Create a new user\n2.Log in exisiting user")
        print("-" * 50)
        while True:
            try:
                new_Choice = int(input("Enter your choice: "))
                if new_Choice not in [1, 2]:
                    raise ValueError("Invalid choice. Please enter 1 or 2.")
                break
            except ValueError as e:
                print(f"❌ Error: {e}")
        userName = input("\nEnter your username: ").strip()

        if new_Choice == 1:
            ut.clear_screen()
            if ut.load_user_profile(userName):
                confirm = input("⚠️ A profile with this username already exists. Overwrite? (yes/no): ").strip().lower()
                if confirm != "yes":
                    print("❌ Profile creation canceled.")
                continue
            calories = ut.get_info(userName)
            print(f"\n✨Your daily calorie intake should be: {calories} calories\n")
            input("\nPress Enter to return to the main menu...")
        elif new_Choice == 2:
            ut.clear_screen()
            profile = ut.load_user_profile(userName)
            if profile:
                calories = profile['calIn']
                print(f"\n✨Welcome back, {userName}! Hope your are doing well!\n"
                      f"As per your Previous data, your daily calorie intake should be {calories} calories")
                input("\nPress Enter to move to the main menu...")
            else:
                print("❌ No profile found for this username. Please create a new user.")
                input("\nPress Enter to return to the Login menu...")
                continue

        while True:
            ut.clear_screen()
            print("\nMain Menu")
            print("-" * 50)
            print("1. View Food Nutrition\n2. Log Food\n3. View Log\n4. Exit")
            print("-" * 50)
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                ut.clear_screen()
                food = input("\nEnter food name: ").strip()
                portion = input("Enter portion size (e.g., 100g, 1 unit): ").strip()
                query = f"{portion} of {food}"
                data = ut.get_nutrition(query)

                if not data or "foods" not in data:
                    print("\n⚠️ Error: Unable to fetch nutrition data for the entered food.")
                    print("Please check the food name and try again.")
                    input("\nPress Enter to return to the main menu...")
                    

                if data and "foods" in data:
                    item = data["foods"][0]
                    print(
                        f"\n🍽️ Nutrition Values of {item['food_name'].upper()} as per inputted portion of {portion.upper()}:\n"
                        f" - Calories: {item['nf_calories']} calories\n"
                        f" - Carbs   : {item['nf_total_carbohydrate']} grams\n"
                        f" - Proteins: {item['nf_protein']} grams\n"
                        f" - Fibers  : {item['nf_dietary_fiber']} grams\n"
                        f" - Fats    : {item['nf_total_fat']} grams"
                    )
                    input("\nPress Enter to return to the main menu...")
        
            elif choice == 2:
                ut.clear_screen()
                while True:
                    print("\nLog Food Menu")
                    print("-" * 50)
                    print("1. Breakfast\n2. Lunch\n3. Snacks\n4. Dinner\n5. Back to Main Menu")
                    print("-" * 50)
                    meal_choice = int(input("\nEnter meal type: "))
                    meal_map = {1: "Breakfast", 2: "Lunch", 3: "Snacks", 4: "Dinner"}
                    if meal_choice not in meal_map and meal_choice != 5:
                        print("❌ Invalid choice. Please try again.")
                        input("\nPress Enter to return to the log food menu...")
                        continue

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
                            input("\nPress Enter to return to the main menu...")
                    elif meal_choice == 5:
                        break
            elif choice == 3:
                ut.clear_screen()
                print("\n📜 Viewing Food Log...")
                ut.view_logs(userName)
                print(f"🔥 Your target Calories : {calories} cal")
                input("\nPress Enter to return to the main menu...")
            elif choice == 4:
                ut.clear_screen()
                print("\nThank you for using the Calorie Tracker. Goodbye!")
                print("=" * 50)
                exit()
            else:
                print("❌ Invalid choice. Please try again.")
                input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()