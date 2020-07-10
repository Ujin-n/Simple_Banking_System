import random
import sqlite3
 
# Database holds information about client cards
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'number TEXT, '
            'pin TEXT, '
            'balance INTEGER DEFAULT 0);')
 
# Main cycle
while True:
    # Main menu
    option = input("1. Create an account\n2. Log into account\n0. Exit\n> ")
 
    # Exit option
    if option == '0':
        exit()
 
    # Create account option
    elif option == '1':
        # Generating 15 digits of credit card number (without the last checksum digit)
        card_number = '400000'
        for _ in range(9):
            card_number += str(random.randint(0, 9))
 
        # Multiply odd digits by 2
        luhn_number = [int(card_number[i]) if ((i + 1) % 2 == 0) else int(card_number[i]) * 2 for i in range(len(card_number))]
 
        # Subtract 9 to number over 9
        for i in range(len(luhn_number)):
            if luhn_number[i] > 9:
                luhn_number[i] -= 9
 
        # Sum number
        luhn_sum = sum(luhn_number)
        if luhn_sum % 10 == 0:
            check_sum = 0
        else:
            check_sum = (luhn_sum - luhn_sum % 10 + 10) - luhn_sum
 
        # Add checksum to card number
        card_number += str(check_sum)
 
        # Generating PIN
        pin = ''
        for _ in range(4):
            pin += str(random.randint(0, 9))
 
        # Save card+pin to dictionary
        # card_pin[card_number] = pin
 
        # Save card + pin to database
        cur.execute(f'INSERT INTO card (number, pin, balance) VALUES ({card_number}, {pin}, 0)')
        conn.commit()
 
        # Output information about created credit card
        print()
        print('Your card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{pin}\n')
 
    # Login option
    elif option == '2':
        input_card = input("Enter your card number:\n> ")
        input_pin = input("Enter your pin:\n> ")
 
        # Search input card number and pin in DB
        cur.execute(f"SELECT number, pin, balance FROM card WHERE number = '{input_card}';")
        card_info = cur.fetchone()
 
        if card_info and card_info[1] == input_pin:
            print("\nYou have successfully logged in!")
            print()
 
            while True:
                logged_option = input("1. Balance\n2. Log out\n0. Exit\n> ")
 
                if logged_option == '1':
                    print("\nBalance: 0\n")
                    continue
                elif logged_option == '2':
                    print("\nYou have successfully logged out!\n")
                    break
                elif logged_option == '0':
                    exit()
        else:
            print("\nWrong card number or PIN!\n")
            continue
