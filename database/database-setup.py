import sqlite3 as sql3


con = sql3.connect('becl-libros.db')

# Function to create a user table 
def create_user_table(con):
    cursorObj = con.cursor()
    # drop table if exists
    cursorObj.execute("DROP TABLE IF EXISTS usuario")
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS usuario ( \
            codigo text PRIMARY KEY, \
            nombre text, \
            correo text \
        )"
    )
    con.commit()

# Function to create a book table
def create_book_table(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS libro ( \
            id text PRIMARY KEY, \
            titulo text, \
            autor text, \
            anio integer, \
            editorial text, \
            link1 text, \
            link2 text, \
            link3 text, \
            categoria text \
            )"
    )
    con.commit()

# Function to create a rating table
def create_rating_table(con):
    cursorObj = con.cursor()
    
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS calificacion ( \
            codigo integer PRIMARY KEY AUTOINCREMENT,  \
            codigo_usuario text, \
            codigo_libro text, \
            calificacion integer,  \
            FOREIGN KEY(codigo_usuario) REFERENCES usuario(codigo), FOREIGN KEY(codigo_libro) REFERENCES libro(id) \
        )"
    )
    
    con.commit()

# execute functions to create tables
create_user_table(con)
create_book_table(con)
create_rating_table(con)
# ====================================================================================================


# function to get unique title values from a csv books file 

def insert_value(con, statement = '', values = []):
    cursor = con.cursor()
    for value in values:
        cursor.execute(statement, value)
    con.commit()




