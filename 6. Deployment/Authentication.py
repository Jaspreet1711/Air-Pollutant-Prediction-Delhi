import pyrebase as pb

config = {
    "apiKey": "AIzaSyCJj5yJgV2QdpkBxZN8QNvaZQiWh-TjntA",
    "authDomain": "aqi-prediction-338709.firebaseapp.com",
    "databaseURL": "https://aqi-prediction-338709-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "aqi-prediction-338709",
    "storageBucket": "aqi-prediction-338709.appspot.com",
    "messagingSenderId": "1068395558929",
    "appId": "1:1068395558929:web:089594c34c4f8f523119b0",
    "measurementId": "G-B1PN8WHJMG"
}

firebase = pb.initialize_app(config)
auth = firebase.auth()

# Creating User
email = "test@gmail.com"
password = "123456"
#auth.create_user_with_email_and_password(email, password)

# sign in
user = auth.sign_in_with_email_and_password(email, password)
#print(user)
print(user['idToken'])

# Getting Account Info
info = auth.get_account_info(user['idToken'])
#print(info)

# Before 1 hour Expiry
user = auth.refresh(user['refreshToken'])
print(user['idToken'])

# Verifying Email
#auth.send_email_verification(user['idToken'])

# Deleting Account
#auth.delete_user_account(user['idToken'])