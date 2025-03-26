def calIntake (weight: float, target: float, time: float, height: float, age: float, gender: str, actLvl: int):
    if actLvl not in range(1, 6):
            raise ValueError("Activity level must be between 1 and 5.")
    
    if gender.lower() == "male":
        s = 5.00
    elif gender.lower() == "female":
        s = -161.00
    else:
        raise ValueError("Invalid gender. Please specify 'male' or 'female'")
    
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

    calDef = round((target * 7700) / time, 2)
    calInt = round(USER_TDEE - calDef, 2)
    return calInt

