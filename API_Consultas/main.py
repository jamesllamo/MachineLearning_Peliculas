#Instalamos las Librerías de arranque
import pandas as pd
import numpy as np
from fastapi import FastAPI

#Importamos los datos a utilizar
movies= pd.read_csv('movies_API.csv')

#Configuro el FastApi
app = FastAPI(title='App',
            description='API Recomendaciones de Películas Multiplataforma',
            version='1.0.1')
@app.get('/') #Designamos la Ruta 1
def get_bienvenida():
    return 'Saludos, esta aplicacion muestra datos sobre películas'

#------------------------------------------------------------------------------------- Primera
#Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
#(la función debe llamarse get_max_duration(year, platform, duration_type))
@app.get('/duracion/{year}/{platform}/{duration_type}')
def get_max_duration(year, platform, duration_type):
    df=movies

    # apply the filters
    if platform != 'all':
        df =movies[movies['id'].str.contains(platform[0],case=False)]
    if year != 'all':
        df = df[df['release_year'] == int(year)]
    if duration_type != 'all':
        if duration_type == 'minutos':
            df = df[df['duration_type'] == 'minutos']
        elif duration_type == 'season':
            df = df[df['duration_type'] == 'season']

    # sort by duration
    df = df.sort_values('duration_int', ascending=False)
    pelicula_max_duration= df.iloc[0]

    # display the results
    return{pelicula_max_duration[['title', 'duration', 'release_year', 'id']}

#------------------------------------------------------------------------------------- Segunda
#Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (the function must be called get_score_count(platform, scored, year))
@app.get('/score/{platform}/{scored}/{year}')
def get_score_count(platform,scored,year:int):
    df=movies
    # apply the filters
    if platform != 'all':
        df =movies[movies['id'].str.contains(platform[0],case=False)]
    if scored != 'all':
        if scored == '0.5':
            df = df[df['score'] >= '0.5']
        if scored == '1':
            df = df[df['score'] >= '1']
        if scored == '1.5':
            df = df[df['score'] >= '1.5']
        elif scored == '2':
            df = df[df['score'] >= '2']
        if scored == '2.5':
            df = df[df['score'] >= '2.5']
        elif scored == '3':
            df = df[df['score'] >= '3']
        if scored == '3.5':
            df = df[df['score'] >= '3.5']
        elif scored == '4':
            df = df[df['score'] >= '4']
    if year != 'all':
        df = df[df['release_year'] == int(year)]

    # We measure the number of rows
    cantidad_peliculas_filtradas= len(df)

    # Display the results
    return{cantidad_peliculas_filtradas}

#------------------------------------------------------------------------------------- Tercera
#Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
@app.get('/plataforma/{platform}')
def get_count_platform(platform):
    df=movies

    # apply the filters
    if platform != 'all':
        df =df[df['id'].str.contains(platform[0],case=False)]

    # sort by duration
    cantidad_peliculas_plataforma= len(df)

    # display the results
    return{cantidad_peliculas_plataforma}

#------------------------------------------------------------------------------------- Cuarta
#Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
@app.get('/actor/{platform}/{year}')
def get_actor(platform, year):

    df=movies

    # apply the filters
    if platform != 'all':
        df =df[df['id'].str.contains(platform[0],case=False)]
    if year != 'all':
        df = df[df['release_year'] == int(year)]

    # Contamos las veces que aparece cada actor
    Actor_cuenta=df['cast'].value_counts()
    #Buscamos al que más se repite
    Actor_mas_frecuente=Actor_cuenta.idxmax()

    # display the results
    return{Actor_mas_frecuente}