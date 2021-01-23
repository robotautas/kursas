import sqlite3
from random import randint

conn = sqlite3.connect('quotes.db')
c = conn.cursor()

while True:
    i = randint(1,100)
    with conn:
        random_row = randint(1,100)
        c.execute('SELECT * FROM quotes WHERE rowid=?', (random_row,))
        row = c.fetchone()
    
    quote = row[0]
    author = row[1]
    hint1 = row[2]
    hint2 = row[3]

    print(quote)
    answer1 = input('Your answer: ')
    if answer1 != author:
        print(hint1)
        answer2 = input('Your answer: ')
        if answer2 != author:
            print(hint2)
            answer3 = input('Your answer: ')
            if answer3 != author:
                if_continue = input(f'Correct answer is {author}. Continue? y/n: ')
                if if_continue == 'y':
                    continue
                else:
                    break
