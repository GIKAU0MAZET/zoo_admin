import bcrypt

password = "dir"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

print(hashed.decode())