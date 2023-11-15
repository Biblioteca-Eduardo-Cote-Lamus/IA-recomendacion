import pandas as pd 
import sqlite3 as sql3
from random import randint

# excute this only if don't have the database

def read_books():
    books = pd.read_csv('csv/libros.csv', sep=';')
    books.to_sql('libro', sql3.connect('becl-libros.db'), if_exists='replace', index=False)

def insert_value(con, statement = '', values = []):
    cursor = con.cursor()
    for value in values:
        cursor.execute(statement, value)
    con.commit()


users = [
    ('1152069', 'Angel Garcia', 'angelgabrielgara@ufps.edu.co'),
    ('1151874', 'Joel Lizarazo', 'joellizarazo@ufps.edu.co'),
    ('1152073', 'Ana', 'ana@ufps.edu.co'),
]

def create_rating(users, books):

    def get_random_book_code():
        return books[randint(0, len(books) - 1)][0]
    
    def mapped_to_sql(rating):
        return [(user_code, book_code, rating) for user_code, books in rating for book_code, rating in books]

    ratings = []

    for user in users:
        user_code = user[0]
        set_books = set()
        books_to_rate = 0

        while books_to_rate < 10:
            book_code = get_random_book_code()
            rating = randint(1, 5)
            if book_code not in set_books:
                set_books.add((book_code, rating))
                books_to_rate += 1
            
            if books_to_rate == 10:
                break
        
        ratings.append( (user_code, set_books) )

    return mapped_to_sql(ratings)

# insert_value(sql3.connect('becl-libros.db'), 'INSERT INTO usuario VALUES(?, ?, ?)', users)

# con = sql3.connect('becl-libros.db')
# books = con.execute('SELECT * FROM libro').fetchall()
# users = con.execute('SELECT * FROM usuario').fetchall()

# rating = create_rating(users, books)

# insert_value(con, 'INSERT INTO calificacion(codigo_usuario, codigo_libro, calificacion) VALUES(?, ?, ?)', rating)


# print(books)