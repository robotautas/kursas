from scaffold import stages
from words import words
from random import choice

word = choice(words)
covered_word = len(word) * '_'
errors = 0

while errors < len(stages) - 1:
    print(stages[errors])
    print(covered_word)
    if covered_word == word:
        print('You win!')
        break

    guess_letter = input('Guess a letter: ')
    
    if guess_letter in word:
        index = 0
        for char in word:
            if char == guess_letter:
                covered_letters_list = [char for char in covered_word]
                covered_letters_list[index] = guess_letter
                covered_word = ''.join(covered_letters_list)
            index += 1
    else:
        errors += 1
else:
    print(stages[-1])
    print('You lose!')
        
