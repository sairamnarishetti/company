import bcrypt

# p = 'password@123'
# encoded = p.encode('utf-8')

# salt = bcrypt.gensalt(rounds=12)

# hashed_pass = bcrypt.hashpw(encoded,salt).decode('utf-8')
# print(hashed_pass)

reg_pass = 'password@123'
encoded = reg_pass.encode('utf-8')
salt = bcrypt.gensalt(rounds=12)
hashed_pass = bcrypt.hashpw(encoded,salt).decode('utf-8')

login_pass = 'password@123'
encoded1 = login_pass.encode('utf-8')
if bcrypt.checkpw(encoded1,hashed_pass.encode('utf-8')):
    print("login succesfull")
else:
    print("login fail")
