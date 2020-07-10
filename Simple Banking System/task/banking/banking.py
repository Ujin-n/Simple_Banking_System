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
        cur.execute(f"SELECT id, number, pin, balance FROM card WHERE number = '{input_card}';")
        card_info = cur.fetchone()

        if card_info and card_info[2] == input_pin:

            # Unpack sqlite tuple
            db_id = card_info[0]
            db_number = card_info[1]
            db_pin = card_info[2]
            db_balance = int(card_info[3])

            # Welcome message
            print("\nYou have successfully logged in!")
            print()

            # Cycle inside account
            while True:
                # Main menu inside account
                logged_option = input("1. Balance\n"
                                      "2. Add income\n"
                                      "3. Do transfer\n"
                                      "4. Close account\n"
                                      "5. Log out\n"
                                      "0. Exit\n> ")

                # Balance
                if logged_option == '1':
                    cur.execute(f"SELECT balance FROM card WHERE id = {db_id};")
                    db_balance = cur.fetchone()[0]
                    print(f"\nBalance: {db_balance}\n")
                    continue

                # Add income
                elif logged_option == '2':
                    print("\nEnter income:")
                    input_income = int(input('> '))

                    # Update balance in DB
                    cur.execute(f'UPDATE card SET balance = balance + {input_income} WHERE id = {db_id};')
                    conn.commit()
                    print('Income was added!\n')

                    continue

                # Do transfer
                elif logged_option == '3':
                    print("\nTransfer")
                    print("Enter card number:")

                    # target card number
                    in_card_tr = input('> ')

                    # check if the same card number has been entered
                    if in_card_tr == db_number:
                        print("You can't transfer money to the same account!")
                        continue

                    # apply Luhn algorithm
                    in_card_tr_list = [int(i) for i in in_card_tr[:-1]]

                    luhn_sum = 0
                    for i in range(len(in_card_tr_list)):
                        if (i + 1) % 2 != 0:
                            in_card_tr_list[i] *= 2

                        if in_card_tr_list[i] > 9:
                            in_card_tr_list[i] -= 9

                        luhn_sum += in_card_tr_list[i]

                    if (luhn_sum + int(in_card_tr[-1])) % 10 != 0:
                        print("Probably you made mistake in the card number. Please try again!\n")
                        continue

                    # Search target card in DB
                    cur.execute(f"SELECT id, number, pin, balance FROM card WHERE number = '{in_card_tr}';")
                    target_card_info = cur.fetchone()

                    if not target_card_info:
                        print("Such a card does not exist.\n")
                        continue

                    # Unpack target card info
                    db_id_trg = target_card_info[0]
                    db_number_trg = target_card_info[1]
                    db_pin_trg = target_card_info[2]
                    db_balance_trg = target_card_info[3]

                    # Ask for amount of money to transfer
                    print("Enter how much money you want to transfer:")
                    transfer_amount = int(input('> '))

                    if transfer_amount > db_balance:
                        print("Not enough money!\n")
                        continue

                    # Transfer money
                    cur.execute(f"UPDATE card SET balance = {db_balance_trg + transfer_amount} WHERE id = {db_id_trg};")
                    cur.execute(f"UPDATE card SET balance = {db_balance - transfer_amount} WHERE id = {db_id};")
                    conn.commit()

                    print("Success!\n")

                # Close account
                elif logged_option == '4':
                    cur.execute(f"DELETE FROM card WHERE id = {db_id};")
                    conn.commit()
                    break

                elif logged_option == '5':
                    break

                elif logged_option == '0':
                    print('Bye!')
                    exit()

        else:
            print("\nWrong card number or PIN!\n")
            continue
