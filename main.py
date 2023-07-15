import requests
import string
import random
from colorama import Fore, Style, init
from time import sleep
import os

init(autoreset=True)

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()

ascii_art = """
888888b.   d8b          
888  "88b  Y8P          
888  .88P               
8888888K.  888  .d88b.  
888  "Y88b 888 d88P"88b 
888    888 888 888  888 
888   d88P 888 Y88b 888 
8888888P"  888  "Y88888 
                    888 
               Y8b d88P 
                "Y88P"
"""

print(Fore.LIGHTRED_EX + ascii_art)


def generate_username(length, use_numbers, use_underscore):
  if use_numbers and use_underscore:
    pool = string.ascii_lowercase + string.digits + '_'
  elif use_numbers:
    pool = string.ascii_lowercase + string.digits
  elif use_underscore:
    pool = string.ascii_lowercase + '_'
  else:
    pool = string.ascii_lowercase

  username = ''.join(random.choice(pool) for _ in range(length))
  while username.count('_') > 1:
    username = ''.join(random.choice(pool) for _ in range(length))
  return username.capitalize()


def generate_custom_username(base_word, length, use_numbers, use_underscore):
  if use_numbers and use_underscore:
    pool = string.ascii_lowercase + string.digits + '_'
  elif use_numbers:
    pool = string.ascii_lowercase + string.digits
  elif use_underscore:
    pool = string.ascii_lowercase + '_'
  else:
    pool = string.ascii_lowercase

  partial_len = length - len(base_word)
  if partial_len < 0:
    partial_len = 0

  split_index = random.randint(0, partial_len)

  start = ''.join(random.choice(pool) for _ in range(split_index))
  end = ''.join(random.choice(pool) for _ in range(partial_len - split_index))

  username = start + base_word + end
  while username.count('_') > 1:
    start = ''.join(random.choice(pool) for _ in range(split_index))
    end = ''.join(
      random.choice(pool) for _ in range(partial_len - split_index))
    username = start + base_word + end

  return username.capitalize()


while True:
  username_length = input(Fore.WHITE + "\nEnter the username length: " +
                          Fore.LIGHTRED_EX)
  if username_length.isdigit() and 3 <= int(username_length) <= 20:
    break
  else:
    print(Fore.LIGHTRED_EX + "Invalid length")

use_numbers = input(Fore.WHITE + "\nInclude numbers? Enter 'yes' or 'no': " +
                    Fore.LIGHTRED_EX) == 'yes'
use_underscore = input(Fore.WHITE +
                       "\nInclude underscores? Enter 'yes' or 'no': " +
                       Fore.LIGHTRED_EX) == 'yes'

gen_type = input(
  Fore.WHITE +
  "\nDo you prefer random/custom gen? Enter 'random' or 'custom': " +
  Fore.LIGHTRED_EX)

if gen_type.lower() == 'custom':
  base_words = input(Fore.WHITE + "\nEnter one word to take as example: " +
                     Fore.LIGHTRED_EX)
  print(Fore.LIGHTRED_EX + "\n\nStatus: " + Fore.WHITE +
        "Generating custom usernames...")
  while True: 
    username = generate_custom_username(base_words, int(username_length),
                                        use_numbers, use_underscore)
    response = requests.get(
      f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2005-12-10"
    )
    data = response.json()
    if 'code' in data and data['code'] in [0, 5]:
      print(Fore.WHITE + username)
    sleep(0.5)  
else:
  print(Fore.LIGHTRED_EX + "\n\nStatus: " + Fore.WHITE +
        "Generating random usernames...")
  while True:  # Infinite loop
    username = generate_username(int(username_length), use_numbers,
                                 use_underscore)
    response = requests.get(
      f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2005-12-10"
    )
    data = response.json()
    if 'code' in data and data['code'] in [0, 5]:
      print(Fore.WHITE + username)
    sleep(0.5) 
