from app.menus import Menus


def start_program():

    """
    Displays a welcome message.
    Start menu.
    Asks the user if they are ready to start searching.
    """

    print("\n-------------------------------------")
    print('| Greetings to you, good man!       |\n| Welcome to "AveDi - MovieSearch"! |')
    print("-------------------------------------")

    while True:
        choice = input("\n[?] Ready to search for movies? "
                       "\n1. Yes "
                       "\n2. No "
                       "\nYour choice: ")

        if choice == '1':
            Menus.choice_type()

        elif choice == '2':
            print("\n[✔] Goodbye!")
            break

        else:
            print("\n[✖] Invalid choice!")


if __name__ == "__main__":
    start_program()