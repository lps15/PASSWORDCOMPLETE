import random
import string
import csv
from cryptography.fernet import Fernet
UPPERCASE_LETTERS = string.ascii_uppercase
LOWERCASE_LETTERS = string.ascii_lowercase
DIGITS = string.digits
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}|;:,.<>?/`~"
CHARACTER_SET = UPPERCASE_LETTERS + LOWERCASE_LETTERS + DIGITS + SPECIAL_CHARACTERS
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

key = load_key()
cipher = Fernet(key)

def passwordGenerator():
    print("------PASSWORD GENERATOR-------")
    length = int(input("How many characters do you want your generated password to be: "))
    pas = "".join(random.choice(CHARACTER_SET) for i in range(length))
    print("Generated Password:", pas)
    return pas
def passwordsaver_add(username, password, website):
    data = f"{website},{username},{password}\n"
    encrypted_data = cipher.encrypt(data.encode())
    with open("secret.csv", mode="ab") as file:  # "ab" mode for binary write
        file.write(encrypted_data + b'\n')
    print("Password saved to encrypted file.")

def passwordsaver_view():
    print("------SAVED PASSWORDS------")
    saved = int(input("Do you want to view all passwords(1) or a specific password(2): "))
    
    if saved == 1:
        try:
            with open("secret.csv", mode="rb") as file:
                for line in file:
                    encrypted_data = line.strip()
                    decrypted_data = cipher.decrypt(encrypted_data).decode()
                    website, username, password = decrypted_data.split(',')
                    print(f"Website: {website}, User: {username}, Password: {password}")
        except FileNotFoundError:
            print("No saved passwords found.")
    elif saved == 2:
        website_search = input("Enter the website name to retrieve the password: ")
        try:
            with open("secret.csv", mode="rb") as file:  # Open file in binary mode for encrypted data
                for line in file:
                    encrypted_data = line.strip()
                    decrypted_data = cipher.decrypt(encrypted_data).decode()  # Decrypt each line
                    website, username, password = decrypted_data.split(',')
                    if website.lower() == website_search.lower():  # Compare case-insensitive
                        print(f"Website: {website}, User: {username}, Password: {password}")
                        found = True
                        break
                if not found:
                    print("No password found for that website.")
        except FileNotFoundError:
            print("No saved passwords found.")

def passwordsaver():
    print("-----PASSWORD SAVER-----")
    options = 0
    while options != 1 and options != 2:
        options = int(input("Would you like to view your passwords (1) or add a new password (2)?: "))
        if options != 1 and options != 2:
            print("Invalid option, please try again.")
    if options == 1:
        passwordsaver_view()
    elif options == 2:
        website = input("What is the name of the website?: ")
        username = input(f"What is the username for {website}?: ")
        password = input("What is the password?: ")
        passwordsaver_add(username, password, website)

print("Welcome to Password Complete")
movement = 0
while(movement != 3):
    movement = int(input("Would you like to go to Password Generator(1), Password Storage(2) or exit(3): "))
    if(movement ==1):
        passwordGenerator()
    elif(movement ==2):
        passwordsaver()


