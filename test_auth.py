from auth import get_credentials

creds = get_credentials()

print("Authentication Successful!")

print(creds.valid)