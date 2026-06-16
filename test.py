from auth.security import hash_password, verify_password

hashed = hash_password("mysecret123")
print(hashed)
print(verify_password("mysecret123", hashed))   # should print True
print(verify_password("wrongpassword", hashed))  # should print False