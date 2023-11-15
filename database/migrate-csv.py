import sqlite3 as sql3
import pandas as pd

con = sql3.connect('becl-libros.db')

def migrate_to_csv(con):

    books = pd.read_sql_query('SELECT * FROM libro', con)
    users = pd.read_sql_query('SELECT * FROM usuario', con)
    ratings = pd.read_sql_query('SELECT * FROM calificacion', con)

    # migrate to csv from dataframe

    books.to_csv('csv/libros.csv', sep=';', index=False)
    users.to_csv('csv/usuarios.csv', sep=';', index=False)
    ratings.to_csv('csv/calificaciones.csv', sep=';', index=False)

def migrate_to_database_from_csv():
    books = pd.read_csv('csv/libros.csv', sep=';')
    users = pd.read_csv('csv/usuarios.csv', sep=';')
    ratings = pd.read_csv('csv/calificaciones.csv', sep=';')

    books.to_sql('libro', con, if_exists='replace', index=False)
    users.to_sql('usuario', con, if_exists='replace', index=False)
    ratings.to_sql('calificacion', con, if_exists='replace', index=False)
