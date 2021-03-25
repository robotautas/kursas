import requests
import json

def create_user():
    name = input('Name: ')
    new_user = {'name': name}
    r = requests.post('http://127.0.0.1:5000/create_user', json=new_user)
    print(r.text)

def create_post():
    title = input('Title: ')
    user = input('User: ')
    new_post = {'title': title, 'user': user}
    r = requests.post('http://127.0.0.1:5000/create_post', json=new_post)
    print(r.text)

def update_user():
    _id = input('ID: ')
    name = input('Name: ')
    updated_user = {'name': name}
    r = requests.put(f'http://127.0.0.1:5000/update_user/{_id}', json=updated_user)
    print(r.text)

def update_post():
    _id = input('ID: ')
    title = input('Title: ')
    user = input('User: ')
    updated_post = {'title': title, 'user': user}
    r = requests.put(f'http://127.0.0.1:5000/update_post/{_id}', json=updated_post)
    print('\nUPDATED!\n')
    print(r.text)

def delete_user():
    _id = input('ID: ')
    r = requests.delete(f'http://127.0.0.1:5000/delete_user/{_id}')
    print(r.text)

def delete_post():
    _id = input("ID: ")
    r = requests.delete(f'http://127.0.0.1:5000/delete_post/{_id}')
    print(r.text)


while True:
    print(
        '''Functions available:
        create_user: cu | create_post: cp | update user: uu | update post: up | delete user: du | delete post: dp'''
        )
    choice = input('Choose function:')
    if choice=='cu': create_user()
    elif choice=='cp': create_post()
    elif choice=='uu': update_user()
    elif choice=='up': update_post()
    elif choice=='du': delete_user()
    elif choice=='dp': delete_post()
    elif choice=='q': break
    else: print('wrong choice')