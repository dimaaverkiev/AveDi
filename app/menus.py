from .database import Database

class Menus:
    @staticmethod
    def show_movie_page(movie_list, offset, cursor):

        """
        Registers a search query:
        - increases the counter or creates a new entry,
        - saves the query in history with the current date.
        """

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        while True:
            choice = input("\n----- MENU -----\n"
                           "1. View description\n"
                           "2. Next page\n"
                           "3. Previous page\n"
                           "4. Search again\n"
                           "5. Back to choose criteria\n"
                           "6. Close the program\n"
                           "Your choice: ")

            if choice == '1':
                movie_num = input("\n[?] Enter movie number to view description: ")
                if not movie_num.isdigit():
                    print("\nFalse value! Try again!")
                    continue

                movie_title = movie_list[int(movie_num) - offset - 1]
                cursor.execute('SELECT title, description FROM film WHERE title = %s', (movie_title,))
                result = cursor.fetchone()
                print(f"\n[✔] Description for your movie: {movie_title}")
                print(100 * "*")
                print(f"{result[0]} -> {result[1]}")
                print(100 * "*")

            elif choice == '2':
                return 'next'

            elif choice == '3':
                return 'prev'

            elif choice == '4':
                return 'restart'

            elif choice == '5':
                return 'back'

            elif choice == '6':
                print("\n[✔] The program is closed by you, good man, best wishes!")
                cursor_edit.close(), cursor_ich.close(), conn_edit.close(), conn_ich.close()
                exit()

            else:
                print("\n[✖] Please enter a valid number or value!")


    @staticmethod
    def choice_type():

        """
        Menu for selecting the search type.
        Allows you to select a criterion and calls the corresponding function.
        """

        from .search import Search

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        try:
            while True:
                type_search = input("\n[?] What criteria will we use to search?"
                                    "\n1. Title "
                                    "\n2. Year "
                                    "\n3. Genre "
                                    "\n4. Year and Genre "
                                    "\n5. Search by popularity "
                                    "\n6. Back "
                                    "\n7. Close the program "
                                    "\nYour choice: ")

                if type_search == '1' or type_search.lower() == "title":
                    Search.by_title()

                elif type_search == '2' or type_search.lower() == "year":
                    Search.by_year()

                elif type_search == '3' or type_search.lower() == "genre":
                    Search.by_genre()

                elif type_search == '4' or type_search.lower() == "year and genre":
                    Search.by_year_and_genre()

                elif type_search == '5' or type_search.lower() == "search by popularity":
                    Search.popular_searches()

                elif type_search == '6' or type_search.lower() == "back":
                    return

                elif type_search == '7' or type_search.lower() == "close the program":
                    print("\n[✔] The program is closed by you, good man, best wishes!")
                    cursor_edit.close(), cursor_ich.close(), conn_edit.close(), conn_ich.close()
                    exit()

                else:
                    print("\n[✖] Please enter a valid number or criteria!")

        except Exception as e:
            print(f"[✖] There was an error:", e)

        finally:
            cursor_edit.close()
            cursor_ich.close()
            conn_edit.close()
            conn_ich.close()