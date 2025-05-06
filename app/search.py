from .database import Database
from .menus import Menus
from .config import Config


class Search:
    @staticmethod
    def by_title(title_name=None):

        """
        Searches for movies by title.
        If no title is specified, prompts the user for one.
        """

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        try:
            if title_name is None:
                title_name = input("\n[?] Enter title to search your movie: ")

            Database.insert_search(title_name, "Keyword", conn_edit, cursor_edit)
            page = 0

            while True:
                offset = page * Config.PAGINATION_LIMIT
                cursor_ich.execute(
                    "SELECT title, release_year, length, cat.name FROM film "
                    "JOIN film_category AS f_a ON f_a.film_id = film.film_id "
                    "JOIN category AS cat ON cat.category_id = f_a.category_id "
                    f"WHERE title LIKE '%{title_name}%' OR description LIKE '%{title_name}%' "
                    f"LIMIT {Config.PAGINATION_LIMIT} OFFSET {offset}"
                )
                results = cursor_ich.fetchall()

                if not results:
                    if page == 0:
                        print("\n[✖] No movie found matching these criteria.")
                        return Search.by_title()
                    else:
                        print("\n[!] No more movies.")
                        page = 0
                        continue

                print(f"\n[✔] Found movies for '{title_name}' - Page: {page + 1}")
                print(50 * "*")
                for num, (title, year, length, genre) in enumerate(results, start=1 + offset):
                    print(num, title, year, length, genre)
                print(50 * "*")

                action = Menus.show_movie_page([item[0] for item in results], offset, cursor_ich)

                if action == 'next':
                    page += 1
                elif action == 'prev':
                    page = max(0, page - 1)
                elif action == 'restart':
                    return Search.by_title()
                elif action == 'back':
                    return

        finally:
            cursor_ich.close()
            cursor_edit.close()
            conn_ich.close()
            conn_edit.close()


    @staticmethod
    def by_year(year_num=None):

        """
        Searches for movies by year.
        If one number is entered, we search for that year,
        if 8 digits are entered, we consider this range of years.
        """

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        try:
            print("\n§ Search by year! §")
            if year_num is None:
                year_num = input(
                    "\n[?] Enter a year to search by year, or two years separated by a space to search in a range: ")

            page_year = 0

            while True:
                offset_year = page_year * Config.PAGINATION_LIMIT

                if year_num.replace(' ', '').isdigit() and len(list(year_num.replace(' ', ''))) == 4:

                    Database.insert_search(year_num.replace(" ", ""), "Year", conn_edit, cursor_edit)

                    cursor_ich.execute('select title, release_year, length, cat.name as category from film '
                                       'join film_category as f_a on f_a.film_id = film.film_id '
                                       'join category as cat on cat.category_id = f_a.category_id '
                                       f'where release_year = {year_num.replace(" ", "")} '
                                       f'Limit {Config.PAGINATION_LIMIT} offset {offset_year}')

                    result_year = cursor_ich.fetchall()

                    if not result_year:
                        if page_year == 0:
                            print("\n[✖] No movies found for this year.")
                        else:
                            print("\n[✖] No more movies.")
                            page_year = 0
                            continue


                    print(f"\n[✔] Found movies for year '{year_num}' - Page: {page_year + 1}")
                    print(50 * "*")
                    for num, vel in enumerate(result_year, start=1 + offset_year):
                        print(num, vel[0], vel[1], vel[2], vel[3])
                    print(50 * "*")

                    action_year = Menus.show_movie_page([item[0] for item in result_year], offset_year, cursor_ich)

                    if action_year == 'next':
                        page_year += 1

                    elif action_year == 'prev':
                        if page_year > 0:
                            page_year -= 1
                        else:
                            print("\n[!] You are already on the first page.")

                    elif action_year == 'restart':
                        return Search.by_year()

                    elif action_year == 'back':
                        return


                elif year_num.replace(' ', '').isdigit() and len(list(year_num.replace(' ', ''))) == 8:
                    year_num = f"{year_num[:4]} {year_num[4:]}"

                    Database.insert_search(f"{year_num.split()[0]} - {year_num.split()[-1]}", "Year", conn_edit, cursor_edit)

                    cursor_ich.execute('select title, release_year, length, cat.name as category from film '
                                       'join film_category as f_a on f_a.film_id = film.film_id '
                                       'join category as cat on cat.category_id = f_a.category_id '
                                       f'where release_year between {year_num.split()[0]} and {year_num.split()[-1]} '
                                       f'Limit {Config.PAGINATION_LIMIT} offset {offset_year}')

                    result_two_years = cursor_ich.fetchall()

                    if not result_two_years:
                        if page_year == 0:
                            print("\n[✖] No movies found for this year.")
                        else:
                            print("\n[!] No more movies.")
                            page_year = 0
                            continue


                    print(
                        f"\n[✔] Found movies for years '{year_num.split()[0]} - {year_num.split()[-1]}' - Page: {page_year + 1}")
                    print(50 * "*")
                    for num, vel in enumerate(result_two_years, start=1 + offset_year):
                        print(num, vel[0], vel[1], vel[2], vel[3])
                    print(50 * "*")

                    action_two_years = Menus.show_movie_page([item[0] for item in result_two_years], offset_year, cursor_ich)

                    if action_two_years == 'next':
                        page_year += 1

                    elif action_two_years == 'prev':
                        if page_year > 0:
                            page_year -= 1
                        else:
                            print("\n[!] You are already on the first page.")

                    elif action_two_years == 'restart':
                        return Search.by_year()

                    elif action_two_years == 'back':
                        return

                else:
                    print("\n[✖] False year number! Try again!")
                    return Search.by_year()

        except Exception as e:
            print(f"[✖] There was an error:", e)


    @staticmethod
    def by_genre(genre_name=None):

        """
        Searches for movies by genre.
        If the genre is not specified, the user selects it from the list of categories.
        """

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        try:
            print("\n§ Search by genre! §")

            page_genre = 0

            if genre_name is None:
                cursor_ich.execute('SELECT name FROM category')
                res_gen = cursor_ich.fetchall()
                list_genre = []

                print("\n[✔] Possible genres to search for:")
                print(50 * "*")
                for num, vel in enumerate(res_gen, start=1):
                    print(num, vel[0])
                    list_genre.append(vel[0])
                print(50 * "*")

                genre_name_num = input("\n[?] Enter genre number to search your movie: ")

                if not genre_name_num.isdigit() or genre_name_num == "0" or int(genre_name_num) > len(list_genre):
                    print("\n[✖] False genre number! Try again!")
                    return Search.by_genre()

                genre_name = list_genre[int(genre_name_num) - 1]

            Database.insert_search(genre_name, "Genre", conn_edit, cursor_edit)

            while True:
                offset_genre = page_genre * Config.PAGINATION_LIMIT

                cursor_ich.execute(
                    'SELECT title, release_year, length, cat.name FROM film '
                    'JOIN film_category AS f_a ON f_a.film_id = film.film_id '
                    'JOIN category AS cat ON cat.category_id = f_a.category_id '
                    'WHERE cat.name = %s '
                    f'limit {Config.PAGINATION_LIMIT} offset {offset_genre}', (genre_name,))

                result_genre = cursor_ich.fetchall()


                if not result_genre:
                    if page_genre == 0:
                        print("\n[✖] No movies found for this genre.")
                        break
                    else:
                        print("\n[!] No more movies.")
                        page_genre = 0
                        continue

                print(f"\n[✔] Found movies for '{genre_name}' - Page: {page_genre + 1}")
                print(50 * "*")
                for num, vel in enumerate(result_genre, start=1 + offset_genre):
                    print(num, vel[0], vel[1], vel[2], vel[3])
                print(50 * "*")

                action_genre = Menus.show_movie_page([item[0] for item in result_genre], offset_genre, cursor_ich)

                if action_genre == 'next':
                    page_genre += 1

                elif action_genre == 'prev':
                    if page_genre > 0:
                        page_genre -= 1
                    else:
                        print("\n[!] You are already on the first page.")

                elif action_genre == 'restart':
                    return Search.by_genre()

                elif action_genre == 'back':
                    return

        except Exception as e:
            print(f"[✖] There was an error:", e)

    @staticmethod
    def by_year_and_genre(year_input=None, genre_input_name=None):

        """
        Searches for movies by a combination of year (or range of years) and genre.
        If parameters are not specified, prompts the user for them.
        """

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        try:
            print("\n§ Search by year and genre! §")

            page_year_genre = 0

            cursor_ich.execute('select name from category')
            res_gen_gen = cursor_ich.fetchall()
            list_genre_gen = [g[0] for g in res_gen_gen]

            if genre_input_name is None and year_input is None:

                print("[✔] Possible genres to search for:")
                print(50 * "*")
                for num, vel in enumerate(res_gen_gen, start=1):
                    print(num, vel[0])
                print(50 * "*")

                genre_input = input("\n[?] Enter genre number to search your movie: ")
                year_input = input(
                    "\n[?] Enter a year to search by year, or two years separated by a space to search in a range: ")

                if not genre_input.isdigit() or not int(genre_input) <= len(list_genre_gen):
                    print("\n[✖] False value! Try again!")
                    return Search.by_year_and_genre()

                genre_input_name = list_genre_gen[int(genre_input) - 1]

            while True:
                offset_year_genre = page_year_genre * Config.PAGINATION_LIMIT

                if year_input.replace(' ', '').isdigit() and len(
                        list(year_input.replace(' ', ''))) == 4:

                    Database.insert_search(f"{year_input.replace(' ', '')} | {genre_input_name}", "Year and Genre", conn_edit, cursor_edit)

                    cursor_ich.execute('select title, release_year, length, cat.name as category from film '
                                       'join film_category as f_a on f_a.film_id = film.film_id '
                                       'join category as cat on cat.category_id = f_a.category_id '
                                       f'where release_year = {year_input.replace(' ', '')} and cat.name = "{genre_input_name}" '
                                       f'Limit {Config.PAGINATION_LIMIT} offset {offset_year_genre}')

                    res_year_gen = cursor_ich.fetchall()

                    if not res_year_gen:
                        if page_year_genre == 0:
                            print("\n[✖] No movies found for this criteria.")
                            return Search.by_year_and_genre()
                        else:
                            print("\n[!] No more movies.")
                            page_year_genre = 0
                            continue


                    print(
                        f"\n[✔] Found movies for by year -> '{year_input}' and genre -> '{genre_input_name}' - Page: {page_year_genre + 1}")
                    print(50 * "*")
                    for num, vel in enumerate(res_year_gen, start=1 + offset_year_genre):
                        print(num, vel[0], vel[1], vel[2], vel[3])
                    print(50 * "*")

                    action_year_genre = Menus.show_movie_page([item[0] for item in res_year_gen], offset_year_genre, cursor_ich)

                    if action_year_genre == 'next':
                        page_year_genre += 1

                    elif action_year_genre == 'prev':
                        if page_year_genre > 0:
                            page_year_genre -= 1
                        else:
                            print("\n[!] You are already on the first page.")

                    elif action_year_genre == 'restart':
                        return Search.by_year_and_genre()

                    elif action_year_genre == 'back':
                        return


                elif year_input.replace(' ', '').isdigit() and len(
                        list(year_input.replace(' ', ''))) == 8:

                    year_input = f"{year_input[:4]} {year_input[4:]}"

                    Database.insert_search(f"'{year_input.split()[0]} - {year_input.split()[-1]}' | {genre_input_name}",
                                  "Year and Genre", conn_edit, cursor_edit)

                    cursor_ich.execute('select title, release_year, length, cat.name as category from film '
                                       'join film_category as f_a on f_a.film_id = film.film_id '
                                       'join category as cat on cat.category_id = f_a.category_id '
                                       f'where release_year between {year_input.split()[0]} and {year_input.split()[-1]} and cat.name = "{genre_input_name}" '
                                       f'Limit {Config.PAGINATION_LIMIT} offset {offset_year_genre}')

                    result_two_years_gen = cursor_ich.fetchall()

                    if not result_two_years_gen:
                        if page_year_genre == 0:
                            print("\n[✖] No movies found for this criteria.")
                        else:
                            print("\n[!] No more movies.")
                            page_year_genre = 0
                            continue


                    print(
                        f"\n[✔] Found movies by years -> '{year_input.split()[0]} - {year_input.split()[-1]}' and genre -> '{genre_input_name}' - Page: {page_year_genre + 1}")
                    print(50 * "*")
                    for num, vel in enumerate(result_two_years_gen, start=1 + offset_year_genre):
                        print(num, vel[0], vel[1], vel[2], vel[3])
                    print(50 * "*")

                    action_two_years_genre = Menus.show_movie_page([item[0] for item in result_two_years_gen], offset_year_genre, cursor_ich)

                    if action_two_years_genre == 'next':
                        page_year_genre += 1

                    elif action_two_years_genre == 'prev':
                        if page_year_genre > 0:
                            page_year_genre -= 1
                        else:
                            print("\n[!] You are already on the first page.")

                    elif action_two_years_genre == 'restart':
                        return Search.by_year_and_genre()

                    elif action_two_years_genre == 'back':
                        return


                else:
                    print("\n[✖] False year number! Try again!")
                    return Search.by_year_and_genre()

        except Exception as e:
            print(f"[✖] There was an error:", e)


    @staticmethod
    def popular_searches():

        """
        Displays popular search queries by various criteria
        and allows the user to select one.
        """

        conn_ich = Database.get_connection('ich')
        conn_edit = Database.get_connection('edit')
        cursor_ich = conn_ich.cursor()
        cursor_edit = conn_edit.cursor()

        try:
            print("\n§ Search by popularity! §")

            # Popular by Title
            cursor_edit.execute('SELECT filter_text, filter_counter '
                                'FROM search_counter '
                                'WHERE filter_type = "Keyword" and '
                                'filter_counter = (SELECT MAX(filter_counter) FROM search_counter WHERE filter_type = "Keyword")')
            pop_title = cursor_edit.fetchall()

            # Popular by Year
            cursor_edit.execute('SELECT filter_text, filter_counter '
                                'FROM search_counter '
                                'WHERE filter_type = "Year" and '
                                'filter_counter = (SELECT MAX(filter_counter) FROM search_counter WHERE filter_type = "Year")')
            pop_year = cursor_edit.fetchall()

            # Popular by Genre
            cursor_edit.execute('SELECT filter_text, filter_counter '
                                'FROM search_counter '
                                'WHERE filter_type = "Genre" and '
                                'filter_counter = (SELECT MAX(filter_counter) FROM search_counter WHERE filter_type = "Genre")')
            pop_genre = cursor_edit.fetchall()

            # Popular by Year and Genre
            cursor_edit.execute('SELECT filter_text, filter_counter '
                                'FROM search_counter '
                                'WHERE filter_type = "Year and Genre" and '
                                'filter_counter = (SELECT MAX(filter_counter) FROM search_counter WHERE filter_type = "Year and Genre")')
            pop_year_genre = cursor_edit.fetchall()

            print(75 * "*")
            print("1. Popular searches by Title:")
            for title, count in pop_title:
                print(f"Title: {title}, COUNT: {count}")

            print("\n2. Popular searches by Year:")
            for year, count in pop_year:
                print(f"Year: {year}, COUNT: {count}")

            print("\n3. Popular searches by Genre:")
            for genre, count in pop_genre:
                print(f"Genre: {genre}, COUNT: {count}")

            print("\n4. Popular searches by Year and Genre:")
            for year_gen, count in pop_year_genre:
                print(f"Year and Genre: {year_gen}, COUNT: {count}")
            print(75 * "*")

            search_choice = input("\n[?] Do you want to search by one of the popular searches?"
                                  "\n1. Yes"
                                  "\n2. No"
                                  "\nYour choice: ")

            if search_choice == '1' or search_choice.lower() == 'yes':
                pop_choice = input("\n[?] Search by:"
                                   "\n1. Popular Title"
                                   "\n2. Popular Year"
                                   "\n3. Popular Genre"
                                   "\n4. Popular Year and Genre"
                                   "\nYour choice: ")

                if pop_choice == '1' or pop_choice.lower() == 'popular title':
                    return Search.by_title(pop_title[0][0])

                elif pop_choice == '2' or pop_choice.lower() == 'popular year':
                    if sum(1 for char in str(pop_year[0]) if char.isdigit()) == 8:
                        return Search.by_year(
                            f"{str(pop_year[0][0]).replace("'", "").split()[0]} {str(pop_year[0][0]).replace("'", "").split()[1]}")
                    else:
                        return Search.by_year(pop_year[0][0].replace("-", ""))

                elif pop_choice == '3' or pop_choice.lower() == 'popular genre':
                    return Search.by_genre(pop_genre[0][0])

                elif pop_choice == '4' or pop_choice.lower() == 'popular year and genre':
                    text, count = pop_year_genre[0]
                    year_part, genre_part = [x.strip() for x in text.replace("'", "").split("|")]

                    if "-" in year_part:
                        year_input = year_part.replace("-", "")
                    else:
                        year_input = year_part

                    return Search.by_year_and_genre(year_input, genre_part)

                else:
                    print("\n[✖] Invalid choice. Try again.")
                    return Search.popular_searches()

            elif search_choice == '2' or search_choice.lower() == 'no':
                print("\n[!] Back to choose criteria")
                return

            else:
                print("\n[✖] Invalid choice. Try again.")
                return Search.popular_searches()

        except Exception as e:
            print(f"[✖] There was an error:", e)