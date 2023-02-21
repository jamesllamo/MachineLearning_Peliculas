import pandas as pd                                             # Se importa Pandas
from fastapi import FastAPI                                     # Se importa FastAPI
from sklearn.neighbors import NearestNeighbors                  # Se importa NearestNeighbors de sklearn
from sklearn.preprocessing import MinMaxScaler                  # Se importa MinMaxScaler de sklearn
import numpy as np                                              # Se importa numpy
from sklearn.metrics import mean_squared_error                  # Se importa mean_squared_error de sklearn
from sklearn.model_selection import train_test_split            # Se importa train_test_split de sklearn

# Cargamos el modelo entrenado
model = load('movies_modelo_entrenado.joblib')

# Cargamos la data
df = pd.read_csv('movies_api_recomendaciones.csv')                        # Cargamos la información dentro del dataframe data
data=df                                                                   #Creamos una copia

# Eliminamos duplicados
df_aux = df.drop_duplicates()                                   # Eliminar filas duplicadas
df=df_aux                                                       # Actualizamos el dataframe df

# Escalamos la data
scaler = MinMaxScaler()                                         # Utilizamos MinMaxScaler() para convertir la data entre 0 y 1
df['score'] = scaler.fit_transform(df[['score']])               # El escalamiento lo realizamos sobre la columna 'score'

# Transformamos la data en una matriz
user_movie_matrix = df.pivot_table(index='userId', columns='id', values='score')    # Creamos una matriz en la que cada fila represente un usuario y cada columna represente una película
user_movie_matrix = user_movie_matrix.fillna(0)                                     # Rellenamos los valores que faltan con ceros

# Volvemos a correr el modelo KNN
k = 5                                                                           # Number of neighbors to consider
model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=k)     # Asignamos las variables al modelo
model.fit(user_movie_matrix)                                                    # Entrenamos al modelo


#Configuro el FastApi
app = FastAPI(title='App',
            description='API Recomendaciones de Películas Multiplataforma',
            version='1.0.1')
@app.get('/') #Designamos la Ruta 1
def get_bienvenida():
    return 'Saludos, por favor ingresa el user_id a consultar (ejemplo: 1) y el movie_id como cadena de texto (ejemplo: ''as8979'')'

#------------------------------------------------------------------------------------- Primera
#Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
#(la función debe llamarse get_max_duration(year, platform, duration_type))
@app.get('/usuario_movieId/{user_id}/{movie_id}')
def get_usuario_movieId(user_id, movie_id):
    # Hacer una recomendación para un usuario y una película

    user_index = user_movie_matrix.index.get_loc(user_id)                                                               # Esta línea obtiene el índice de user_id en user_movie_matrix
    movie_index = user_movie_matrix.columns.get_loc(movie_id)                                                           # Esta línea obtiene el índice de movie_id en user_movie_matrix
    distances, indices = model.kneighbors(user_movie_matrix.iloc[user_index, :].values.reshape(1, -1), n_neighbors=k+1) # Clcular las distancias y los índices de los k+1 vecinos más cercanos a las calificaciones de películas del usuario.
    recommended_movies = []                                                                                             # Esta línea inicializa una lista vacía que almacenará las películas recomendadas

    # Este ciclo itera a través de los índices de los vecinos más cercanos y agrega las películas correspondientes a la lista de películas recomendadas.
    for i in range(1, len(distances.flatten())):
        movie_index = user_movie_matrix.index[indices.flatten()[i]]
        recommended_movies.append(movie_index)

    # Si el movie_id de entrada está en la lista de películas recomendadas, se recomienda al usuario
    if movie_index in recommended_movies:
        s1 = user_movie_matrix.iloc[recommended_movies[0]].idxmax()                 # Recuperamos el id del primer vecino
        sp1 = data.loc[data['id'] == s1, 'title'].values[0]                         # Recuperamos el id y el título de la primera película 
        s2 = user_movie_matrix.iloc[recommended_movies[1]].idxmax()                 # Recuperamos el id del segundo vecino
        sp2 = data.loc[data['id'] == s2, 'title'].values[0]                         # Recuperamos el id y el título de la segunda película
        return(f'La pelicula {movie_id} es recomendada para el usuario {user_id}. También podrías ver: ','s1'," - ",sp1,". ",s2," - ",sp2,". ")

    # Si el movie_id de entrada no está en la lista de películas recomendadas, entonces no se recomienda al usuario.
    else:
        s1 = user_movie_matrix.iloc[recommended_movies[0]].idxmax()                 # Recuperamos el id del primer vecino
        sp1 = data.loc[data['id'] == s1, 'title'].values[0]                         # Recuperamos el id y el título de la primera película 
        s2 = user_movie_matrix.iloc[recommended_movies[1]].idxmax()                 # Recuperamos el id del segundo vecino
        sp2 = data.loc[data['id'] == s2, 'title'].values[0]                         # Recuperamos el id y el título de la segunda película 
        return(f'{movie_id} no es recomendada para el usuario {user_id}. Te recomendamos las siguientes películas: ',s1," - ",sp1,". ",s2," - ",sp2,". ")  




    

 