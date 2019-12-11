def returns_string(some_string):
    return some_string


def returns_reversed_string(string):
    return string[::-1]


def returns_upper_string(text, func):
    some_text = func(text)
    if type(some_text) != str:
        return 'input must be a type of string'
    return some_text.upper()


print(returns_upper_string('higher order functions!', returns_string))
print(returns_upper_string('higher order functions!', returns_reversed_string))


def upper_decorator(func):
    def wrapper(our_text):
        some_text = func(our_text)
        if type(some_text) != str:
            return 'input must be a type of string'
        return some_text.upper()
    return wrapper


# result = upper_decorator('decorator!', returns_string)
# tluser = upper_decorator('decorator!', returns_reversed_string)
# print(result, tluser)


@upper_decorator
def returns_string(some_string):
    return some_string


@upper_decorator
def returns_reversed_string(string):
    return string[::-1]


print(returns_string('Decorator!'))
print(returns_reversed_string('Decorator!'))


