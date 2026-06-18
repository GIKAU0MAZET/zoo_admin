import bcrypt

password = "cassa"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

print(hashed.decode())