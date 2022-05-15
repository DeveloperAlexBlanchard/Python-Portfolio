rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇
import random

player_input = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors. "))

if player_input == 0:
    print(rock)
elif player_input == 1:
    print(paper)
elif player_input == 2:
    print(scissors)

com_input = (random.randint(0, 2))

if com_input == 0:
    print(rock)
elif com_input == 1:
    print(paper)
elif com_input == 2:
    print(scissors)

if player_input == 0:
    if com_input == 0:
        print("Tie.")
    elif com_input == 1:
        print("You Lose.")
    elif com_input == 2:
        print("You Win.")
elif player_input == 1:
    if com_input == 0:
        print("You Win.")
    elif com_input == 1:
        print("Tie.")
    elif com_input == 2:
        print("You Lose.")
elif player_input == 2:
    if com_input == 0:
        print("You Lose.")
    elif com_input == 1:
        print("You Win.")
    elif com_input == 2:
        print("Tie.")