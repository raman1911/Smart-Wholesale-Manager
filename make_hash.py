import bcrypt

password = "noor123"

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())