import utils as ut
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

if not os.path.exists(".env"):
    raise FileNotFoundError(f"{Fore.RED}Missing .env file. Please create one with APP_ID and API_KEY.")

def main():
    while True:
        ut.clear_screen()
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + Style.BRIGHT + "          Welcome to the Calorie Tracker")
        print(Fore.CYAN + "=" * 50)

        print(f"\n{Fore.YELLOW}1.Create a new user\n{Fore.YELLOW}2.Log in existing user")
        print(Fore.CYAN + "-" * 50)
        while True:
            try:
                new_Choice = int(input(f"{Fore.GREEN}Enter your choice: "))
                if new_Choice not in [1, 2]:
                    raise ValueError("Invalid choice. Please enter 1 or 2.")
                break
            except ValueError as e:
                print(f"{Fore.RED}Error: {e}")
        userName = input(f"\n{Fore.GREEN}Enter your username: ").strip()

        if new_Choice == 1:
            ut.clear_screen()
            if ut.load_user_profile(userName):
                confirm = input(f"{Fore.YELLOW}A profile with this username already exists. Load the data? (yes/no): ").strip().lower()
                if confirm != "yes":
                    print(f"{Fore.GREEN}Using existing profile.")
                    profile = ut.load_user_profile(userName)
                    calories = profile['calIn']
                    print(f"\n{Fore.CYAN}Your daily calorie intake should be: {Fore.WHITE}{Style.BRIGHT}{calories} calories\n")
                    input(f"\n{Fore.GREEN}Press Enter to continue...")
                    continue
            calories = ut.get_info(userName)
            print(f"\n{Fore.CYAN}Your daily calorie intake should be: {Fore.WHITE}{Style.BRIGHT}{calories} calories\n")
            input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")
        elif new_Choice == 2:
            ut.clear_screen()
            profile = ut.load_user_profile(userName)
            if profile:
                calories = profile['calIn']
                print(f"\n{Fore.CYAN}Welcome back, {userName}! Hope you are doing well!\n"
                      f"{Fore.CYAN}As per your Previous data, your daily calorie intake should be {Fore.WHITE}{Style.BRIGHT}{calories} calories")
                input(f"\n{Fore.GREEN}Press Enter to move to the main menu...")
            else:
                print(f"{Fore.RED}No profile found for this username. Please create a new user.")
                input(f"\n{Fore.GREEN}Press Enter to return to the Login menu...")
                continue

        while True:
            ut.clear_screen()
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Main Menu")
            print(Fore.CYAN + "-" * 50)
            print(f"{Fore.YELLOW}1. View Food Nutrition\n{Fore.YELLOW}2. Log Food\n{Fore.YELLOW}3. View Log\n{Fore.YELLOW}4. Exit")
            print(Fore.CYAN + "-" * 50)
            try:
                choice = int(input(f"{Fore.GREEN}Enter your choice: "))
                
                if choice == 1:
                    ut.clear_screen()
                    food = input(f"\n{Fore.GREEN}Enter food name: ").strip()
                    portion = input(f"{Fore.GREEN}Enter portion size (e.g., 100g, 1 unit): ").strip()
                    query = f"{portion} of {food}"
                    data = ut.get_nutrition(query)

                    if not data or "foods" not in data:
                        print(f"\n{Fore.RED}Error: Unable to fetch nutrition data for the entered food.")
                        print(f"{Fore.YELLOW}Please check the food name and try again.")
                        input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")
                        continue

                    if data and "foods" in data:
                        item = data["foods"][0]
                        print(
                            f"\n{Fore.CYAN}Nutrition Values of {Fore.WHITE}{Style.BRIGHT}{item['food_name'].upper()} {Fore.CYAN}as per inputted portion of {Fore.WHITE}{Style.BRIGHT}{portion.upper()}:\n"
                            f"{Fore.WHITE} - Calories: {Fore.YELLOW}{item['nf_calories']} calories\n"
                            f"{Fore.WHITE} - Carbs   : {Fore.YELLOW}{item['nf_total_carbohydrate']} grams\n"
                            f"{Fore.WHITE} - Proteins: {Fore.YELLOW}{item['nf_protein']} grams\n"
                            f"{Fore.WHITE} - Fibers  : {Fore.YELLOW}{item['nf_dietary_fiber']} grams\n"
                            f"{Fore.WHITE} - Fats    : {Fore.YELLOW}{item['nf_total_fat']} grams"
                        )
                        input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")
            
                elif choice == 2:
                    ut.clear_screen()
                    while True:
                        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Log Food Menu")
                        print(Fore.CYAN + "-" * 50)
                        print(f"{Fore.YELLOW}1. Breakfast\n{Fore.YELLOW}2. Lunch\n{Fore.YELLOW}3. Snacks\n{Fore.YELLOW}4. Dinner\n{Fore.YELLOW}5. Back to Main Menu")
                        print(Fore.CYAN + "-" * 50)
                        try:
                            meal_choice = int(input(f"\n{Fore.GREEN}Enter meal type: "))
                            meal_map = {1: "Breakfast", 2: "Lunch", 3: "Snacks", 4: "Dinner"}
                            if meal_choice not in meal_map and meal_choice != 5:
                                print(f"{Fore.RED}Invalid choice. Please try again.")
                                input(f"\n{Fore.GREEN}Press Enter to return to the log food menu...")
                                continue

                            if meal_choice in meal_map:
                                meal_type = meal_map[meal_choice]
                                food = input(f"{Fore.GREEN}Enter food name: ").strip()
                                portion = input(f"{Fore.GREEN}Enter portion size (e.g., 100g, 1 unit): ").strip()
                                query = f"{portion} of {food}"
                                data = ut.get_nutrition(query)
                                if data and "foods" in data:
                                    item = data["foods"][0]
                                    ut.log_food(userName, meal_type, item['food_name'], portion, item['nf_calories'])
                                    print(f"{Fore.GREEN}Logged: {Fore.WHITE}{Style.BRIGHT}{item['food_name']} ({portion}) - {item['nf_calories']} cal")
                                    input(f"\n{Fore.GREEN}Press Enter to continue...")
                                else:
                                    print(f"{Fore.RED}Error: Unable to fetch nutrition data.")
                                    input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")
                            elif meal_choice == 5:
                                break
                        except ValueError:
                            print(f"{Fore.RED}Invalid input. Please enter a number.")
                            input(f"\n{Fore.GREEN}Press Enter to try again...")
                            
                elif choice == 3:
                    ut.clear_screen()
                    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Viewing Food Log...")
                    ut.view_logs(userName)
                    print(f"{Fore.CYAN}Your target Calories : {Fore.WHITE}{Style.BRIGHT}{calories} cal")
                    input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")
                    
                elif choice == 4:
                    ut.clear_screen()
                    print(f"\n{Fore.CYAN}Thank you for using the Calorie Tracker. Goodbye!")
                    print(Fore.CYAN + "=" * 50)
                    exit()
                    
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.")
                    input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.")
                input(f"\n{Fore.GREEN}Press Enter to try again...")

if __name__ == "__main__":
    main()