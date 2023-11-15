import pandas as pd
import sqlite3 as sql3
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
from collections import defaultdict

# Conexión a la base de datos SQLite
con = sql3.connect('becl-libros.db')

# Función para obtener las mejores predicciones para cada usuario
def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[f'{uid}'].append((iid, est))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n


# Función para obtener recomendaciones colaborativas
def recocolaborativa(usuario, top_n):
    recoco = []
    for pelicula, calificacion in top_n[usuario]:
        recoco.append([pelicula, calificacion])
    return recoco


# Función que realiza el filtrado colaborativo para recomendar libros a un usuario específico
def rec_col(con, usuario, n=3):
    df1 = pd.read_sql_query('SELECT c.codigo_usuario, b.titulo, c.calificacion FROM calificacion c join libro b on (c.codigo_libro = b.id)', con)
    # Lee el archivo CSV recién creado y configura el objeto Dataset para Surprise
    # df2 = pd.read_csv('cal-2.csv')
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df1, reader)

    # Configura la cuadrícula de parámetros para la búsqueda de hiperparámetros
    param_grid = { 'n_factors': [50,100,150], "n_epochs": [20, 30, 40, 50, 90], "lr_all": [0.002, 0.005, 0.01, 0.02, 0.04], "reg_all": [0.02, 0.005, 0.1] }

    # Realiza la búsqueda de hiperparámetros utilizando validación cruzada

    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)
    gs.fit(data)

    # Obtiene los mejores parámetros encontrados durante la búsqueda
    params = gs.best_params['rmse']

    # Entrena un modelo SVD con los mejores parámetros en el conjunto de entrenamiento completo
    trainset = data.build_full_trainset()
    svdtuned = SVD(**params)
    svdtuned.fit(trainset)

    # Predice las calificaciones para todas las combinaciones (usuario, ítem) que NO están en el conjunto de entrenamiento
    testset = trainset.build_anti_testset()
    predictions = svdtuned.test(testset)

    # Obtiene las mejores predicciones para cada usuario (top 3)
    top_n = get_top_n(predictions, n)

    # Retorna la lista de recomendaciones colaborativas para el usuario dado
    return recocolaborativa(usuario, top_n)




# Ejemplo de uso
usuario = input('Ingrese el usuario: ')
n = int(input('Ingrese el número de recomendaciones: '))
recomendaciones_colaborativas = rec_col(con, usuario, n)
print(recomendaciones_colaborativas)