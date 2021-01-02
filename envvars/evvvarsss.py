from os import environ, getenv

pswd = environ.get('SECRET')
print(pswd)