import utils as ut

Username = input().strip()
profile = ut.load_user_profile(Username)
print(profile)
for k , v in profile.items():
    print(k, v)