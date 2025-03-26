import utils as ut

def main():
    print("=" * 50)
    print("          Welcome to the Calorie Tracker")
    print("=" * 50)
    print(f"\n✨Your daily calorie intake should be: {ut.get_info()} calories\n")

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
                        ut.log_food(meal_type, item['food_name'], portion, item['nf_calories'])
                        print(f"✅ Logged: {item['food_name']} ({portion}) - {item['nf_calories']} kcal")
                    else:
                        print("⚠️ Error: Unable to fetch nutrition data.")
                elif meal_choice == "5":
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
        elif choice == "2":
            print("\n📜 Viewing Food Log...")
            ut.view_logs()
        elif choice == "3":
            print("\nThank you for using the Calorie Tracker. Goodbye!")
            print("=" * 50)
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()