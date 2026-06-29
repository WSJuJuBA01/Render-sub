import random

number = random.randint(1, 10)
guess = 0

while guess != number:
    guess = int(input("Угадай число от 1 до 10: "))
    if guess < number:
        print("Больше!")
    elif guess > number:
        print("Меньше!")

print("🎉 Угадал! Молодец!")
