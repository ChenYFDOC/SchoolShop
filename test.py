import jwt
token=jwt.encode({1:1},'asd')
print(jwt.decode(token, 'asd'),algorithms=[''])
