# CapstoneVaccines

Este proyecto es un análisis de sentimientos de las vacunas del Coronavirus en Twitter en los últimos meses. Este proyecto se ha desarrollado en cuatro fases secuenciales, cada una de las cuales tiene una carpeta en este repositorio:

1. Scraping y obtención de los datos.
2. Preprocesado y limpieza de los datos.
3. Análisis exploratorio.
4. Visualización de los datos.
5. Comparación y creación de un clasificador.

La mayoría del codigo se ha migrado a notebooks para poder visualizar en línea los aspectos más importantes del proyecto, sin tener que ejecutar el código.

## 1. Scraping

Para la recuperación de los datos se ha hecho uso de la biblioteca _snscrape_. La dificultad en este apartado radica en la dificultad para encontrar la herramienta adecuada.

La intención del proyecto es el análisis de sentimientos en Twitter en los últimos meses entorno a la vacunación contra el coronavirus. Por lo tanto, la herramienta utilizada para extraer los datos tiene que permitir esta opción. Para superar esta dificultad, se ha trabajado con las siguentes bibliotecas, las dos primeras sin éxito:
- Tweepy: usa la API de Twitter, y no deja ir más allá de unas semanas atrás en el tiempo.
- [GetOldTweets3](https://github.com/Mottl/GetOldTweets3): no ha funcionado para este proyecto.
- [SNScrape](https://github.com/JustAnotherArchivist/snscrape): ha funcionado, pero con dificultades y matices.

La biblioteca para la extracción de tweets ha sido la _snscrape_. El script [scrap.py](scrap.py) hace uso de esta biblioteca para extraer los datos empleados en este proyecto.

En un principio, se intentaron extraer todos los tweets que contenieran la palabra _vacuna_ entre el 1 de agosto de 2020 y el 1 de mayo de 2021. Sin embargo, el script se volvía muy inestable y devolvía respuestas sin sentido (un número de tweets muy pequeño). Buscando tweets por menos días y varias veces, el problema parecía solucionarse, pero el número de tweets era demasiado grande como para poder iterar por períodos de tiempo de manera eficiente y después trabajar con ellos. Para solventar este problema, se hicieron pruebas manualmente con el buscador de Twitter avanzado desde el navegador, se identifico un parámetro que no estaba en la documentación de la biblioteca pero sí funcionó. De esta manera, como está en el script, se filtraron los tweets por número de _retweets_. Limitando el estudio, por una parte, a los tweets que circularon mínimamente y tuvieron un impacto relativo, pudiendo trabajar con un dataset no muy grande pero con un gran abanico de fechas.

Se hicieron pruebas extrayendo datos en catalán, etc.

## 2. Preprocesado y limpieza de los datos

Esta sección se ha dividido en dos tareas. Por una parte, la traducción de los tweets del castellano al inglés, para poder usar clasificadores preentrenados en inglés, y la limpieza de los tweets en tokens para poder estudiar su contenido.

### 2.1. Traducción

Como el volumen de tweets seguía siendo considerable, se ha empleado una herramienta que permitiera traducir los tweets de manera automatizada. Para ello, se contempló el uso de *google_trans*, pero este no funcionó adecuadamente y se tuvo que usar la herramienta *google_trans_new*. La dificultad en este apartado radicó en la lentitud del proceso, pues cualquier intento para acelerarlo provocó que la API de Google devolvería los tweets sin traducir. Hubo que buscar un compromiso entre esperar unos segundos entre petición y petición para evitar cualquier limitación de la API pero sin demorar mucho la traducción. La traducción se encuentra en el script [translate.py](preprocessing/translate.py).

### 2.2. Limpieza

#### 2.2.1. En inglés

La limpieza de los datos traducidos al inglés se encuentran en el script [clean_english.ipynb](preprocessing/clean_english.ipynb). En este caso, se han usado para crear el clasificador, del que se habla en la última sección de este documento.

#### 2.2.2. En castellano y catalán

La limpieza de los datos sin traducir se encuentra en el script [preprocessing_es_cat](preprocessing/preprocessing_es_cat.py).

Los puntos que se han seguido para la limpieza son los siguientes:
- Para tratar los emoticonos se han seguido tres pasos:
  1. Extraer los emoticonos más frecuentes de los tweets filtrando por carácteres a un archivo _csv_.
  2. Rellenar dicho archivo _csv_ con una hoja de cálculo con palabras equivalentes para los emoticonos, añadiendo una columna.
  3. Leer este archivo otra vez e intercambiar los emoticonos por palabras.
- Se ha intentado sustuir las expresiones informales de más de un carácter (como ":)") pasando un diccionario con dichas expresiones y su palabra equivalente. Sin embargo, las ocurrencias en este caso fueron mínimas.
- Se han separado los hashtags por palabras cuando estas no estaban separadas pero tenían mayúsuclas. De esta manera, "#YoMeVacuno" pasa a ser "Yo Me Vacuno".
- Se han pasado todos los carácteres a minúsculas
- Se han eliminado enlaces y vínculos.
- Los interrogantes y exclamaciones se han sustituido por "pregunta" y "exclamacion", respectivamente, mientras que los demás puntos de puntuación se han eliminado.
- Se han sustituido todos los espacios y saltos de línea y tabulaciones por un espacio simple.

## 3. Análisis exploratorio

El análisis exploratorio se divide en dos archivos:

### 3.1.

### 3.1.2. Nubes de palabras y aprendizaje no supervisado

En el notebook [words_unsupervised.ipynb](exploratory/words_unsupervised.ipynb) se han estudiado las palabras y bigramas más frecuentes de los tweets preprocesados. Se han obtenido los gráficos de la frecuencia de cada término.

Para intentar una primera clasificación, se han intentado encontrar los tópicos de los tweets mediante LDA con la biblioteca gensim y más tarde en TruncatedSVD. Como este no era el objetivo del proyecto y exigía demasiado trabajo, en el notebook se plantea un código donde más adelante se podría trabajar más a fondo.


