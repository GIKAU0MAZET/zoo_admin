import bcrypt

password = "watcher"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

print(hashed.decode())