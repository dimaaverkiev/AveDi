🎬 Movie Search "AveDi"

A simple command-line interface (CLI) project written in Python to search movies from a MySQL database by different criteria. The app allows users to browse movies, view descriptions, and keep track of popular search terms and history.


📁 Project Structure

final_project/
├── .env                 # Environment variables (not tracked)
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py        # Loads DB settings from .env
│   ├── database.py      # Database connection and insert logic
│   ├── search.py        # Logic for searching movies
│   ├── menus.py         # Menu interface and user input
├── main.py              # Program entry point
└── requirements.txt     # Python dependencies


⚙️ Features

* Search by:
        - Title
        - Year
        - Genre
        - Year + Genre
        - Popular searches
        
* View movie descriptions
* Pagination for results
* Records search history and counters in DB


🛠️ Requirements

* Python 3.8+
* MySQL server
* Python dependencies in requirements.txt:
        - mysql-connector-python==9.3.0
        - python-dotenv==1.0.0



🔧 Setup Instructions


1. Clone the repository

bash:
git clone git@github.com:dimaaverkiev/AveDi.git
cd AveDi


2. Create and configure .env file
Add your DB credentials in the .env file:

ini:

ICH_DB_HOST=localhost
ICH_DB_USER=your_user
ICH_DB_PASSWORD=your_password
ICH_DB_NAME=your_db_name

EDIT_DB_HOST=localhost
EDIT_DB_USER=your_user
EDIT_DB_PASSWORD=your_password
EDIT_DB_NAME=your_db_name


3. Install dependencies

bash:
pip install -r requirements.txt


4. Run the program

bash:
python main.py


📌 Notes

* All sensitive configuration (e.g., passwords) is loaded from .env.
* Uses two MySQL connections: one for reading (ich), another for writing (edit).
* Make sure the database contains film, search_counter, and search_history tables.


