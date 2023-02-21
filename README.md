# <h1 align=center> **DATA SCIENCE** </h1>

# <h2 align=center> **ETL, EDA, Machine Learning y creación de API sobre Películas** </h2>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<hr>  

¡A continuación se describirá los procesos de Extract, transform and load - ETL, Exploratory Data Analysis - EDA y Machine Learning llevados a cabo en el presente proyecto de ***Data Science***.  

<hr>  

## Objetivos

+ Extraer, transformar y cargar la data para ser analizada en un área de Analítica. 

+ Analizar los datos para encontrar relaciones, valores nulos, duplicados y otros

+ Realizar un modelo de Machine Learning que permita recomendar películas a los usuarios en base su historial

<hr>  

# **I. ETL**

## 1. Extracción

Las `librerías` usadas son las siguientes: `pandas` para manejo de Dataframes y `datetime` para manejo de formatos fecha.

    import pandas as pd
    import datetime

+ Los archivos fueron cargados en las siguientes dataframes:

+ amazon_prime_titles.csv en `amazon`

+ disney_plus_titles.csv en `disney`

+ hulu_titles.csv en `hulu`

+ netflix_titles.csv en `netflix`

<br/>

## 2. Transformación

Se realizó las siguientes transformaciones en los **`datos de películas`**:

+ Generamos el campo **`id`**: Cada id se compone de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Los valores nulos del campo rating fueron reemplazados por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ Las fecha están en formato **`AAAA-mm-dd`**

+ Los campos de texto están en **minúsculas**, sin excepciones

+ El campo ***duration*** se ha dividido en dos campos: **`duration_int`** y **`duration_type`**. El primero es un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

Se realizó las siguientes transformaciones en los **`Ratings de los usuarios`**:

+ Las fecha están en formato **`AAAA-mm-dd`**

+ `Renombramos` columnas: renombramos la columna 'rating' a 'score' y la columna 'movieId' a 'id'

<br/>

## Carga

Para mejorar el manejo de los datos se ha construido un único dataframe de nombre `movies` mediante la columna `id`.

Posteriormente, se ha exportado la data en un formato csv en un archivo llamado `movies_ETL`. Este archivo se usará para el posterior procesamiento EDA.

    movies.to_csv('movies_ETL.csv')

Por otro lado, se ha exportado una data más pequeña en csv `movies_API` que contiene la información de las películas y un promedio de ratings por cada película. Este proceso se realizó con el fin de reducir el peso del archivo a cargar a Deta.

    
    movies_API.to_csv('movies_API.csv')

<br/>

# **II. API CONSULTAS**

## Desarrollo de la API

La API se ha **`desarrollado`** usando el framework ***FastAPI***. Las consultas desarrolladas son las siguientes:

+ Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))

+ Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))

+ Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))

+ Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))

<br/>

## Deployment

El Deployment fue realizado en [Deta](https://www.deta.sh/?ref=fastapi) debido a su versatilidad. Para lograrlo se cargaron a deta los siguientes archivos:

`main.py` contiene las funciones y el código para la comunicación de data entre la API y Deta.

`movies_API.csv` contiene la información sobre las películas y los rstings.

`requirements.txt` Contiene las librerías que se utilizarán dentro del archivo main.py.

`Spacefile` Contiene las instrucciones para la carga de arhivos y para la correcta instalación de la API.

`icon.jpg`  Es un icon declarado en Spacefile.

`.gitignore` Se crea por defecto durante la instalación

Carpeta `.space` Se crea por defecto durante la instalación


<br/>

# **III. EDA**

Realizamos el **`Análisis exploratorio de los datos`** como parte del proceso de entender la información con la que se trabajará. Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior.

A cotinuación presentamos el índice de los temas abordados:

    1. IMPORTACIÓN DE LIBRERÍAS
    2. CARGAMOS LA DATA
    3. VISUALIZAMOS LA DATA
    4. LIMPIEZA DE DATOS
        4.1. Gestión de Nulos
        4.2. Gestión de Duplicados
        4.3. Gestión de Valores inconsistentes
        4.4. Gestión de Outliers
    5. ANÁLISIS EXPLORATORIO
        Histograms
        Scatter plots
        Bar plots
        Correlation
    6. ANÁLISIS PROFUNDO
        Distribución
        Pivot Tables
        Cross-Tabulation

    7. EXPORTAR DATA PARA MACHINE LEARNING

<br/>

# **IV. SISTEMA DE RECOMENDACIÓN (Machine Learning)**

## Entrenamiento del modelo

Una vez que toda la data es consumible por la API ya lista para consumir para los departamentos de Analytics y de Machine Learning es hora de **`entrenar nuestro modelo de machine learning`** para armar un sistema de recomendación de películas para usuarios, donde dado un id de usuario y una película, nos diga si la recomienda o no para dicho usuario.

Para procesar correctamente la información se usaron las siguientes librerías:

    import pandas as pd
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import MinMaxScaler
    import numpy as np
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split

<br/>

Se importó el archivo `movies_etl_eda.csv` creado en los pasos anteriores para generar este modelo. Debido a que entrenamos al modelo unicamente con 100 mil datos obtuvimos un RMSE de 0.7330.

Posteriormente exportamos el modelo ya entrenado con el fin de deployarlo. Para eso usamos la `libería joblib.`

    from joblib import dump
    dump(model, 'movies_modelo_entrenado.joblib')

## Deployado

El deployado se realizará en la plataforma de deta.

Debido al uso de sklearn en machine learning y es muy pesado para ser cargado a deta.space. El código está creado.

<br/>
