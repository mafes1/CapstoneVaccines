# CapstoneVaccines

Este proyecto es un análisis de sentimientos de las vacunas del Coronavirus en Twitter en los últimos meses. Este proyecto se ha desarrollado en cuatro fases secuenciales, cada una de las cuales tiene una carpeta en este repositorio:

1. Scraping y obtención de los datos.
2. Preprocesado y limpieza de los datos.
3. Análisis exploratorio.
4. Visualización de los datos y polaridad.
5. Extracción de muestras y creación de un clasificador.

La mayoría del código se ha migrado a notebooks para poder visualizar en línea los aspectos más importantes del proyecto, sin tener que ejecutar el código.

## 1. Scraping

Para la recuperación de los datos se ha hecho uso de la biblioteca _snscrape_. La dificultad en este apartado radica en la dificultad para encontrar la herramienta adecuada.

La intención del proyecto es el análisis de sentimientos en Twitter en los últimos meses entorno a la vacunación contra el coronavirus. Por lo tanto, la herramienta utilizada para extraer los datos tiene que permitir esta opción. Para superar esta dificultad, se ha trabajado con las siguentes bibliotecas, las dos primeras sin éxito:
- Tweepy: usa la API de Twitter, y no deja ir más allá de unas semanas atrás en el tiempo.
- [GetOldTweets3](https://github.com/Mottl/GetOldTweets3): no ha funcionado para este proyecto.
- [SNScrape](https://github.com/JustAnotherArchivist/snscrape): ha funcionado, pero con dificultades y matices.

La biblioteca para la extracción de tweets ha sido la _snscrape_. El script [scrap.py](scrap.py) hace uso de esta biblioteca para extraer los datos empleados en este proyecto.

En un principio, se intentaron extraer todos los tweets que contenieran la palabra _vacuna_ entre el 1 de agosto de 2020 y el 1 de mayo de 2021. Sin embargo, el script se volvía muy inestable y devolvía respuestas sin sentido (un número de tweets muy pequeño). Buscando tweets por menos días y varias veces, el problema parecía solucionarse, pero el número de tweets era demasiado grande como para poder iterar por períodos de tiempo de manera eficiente y después trabajar con ellos. Para solventar este problema, se hicieron pruebas manualmente con el buscador de Twitter avanzado desde el navegador, se identifico un parámetro que no estaba en la documentación de la biblioteca pero sí funcionó. De esta manera, como está en el script, se filtraron los tweets por número de _retweets_. Limitando el estudio, por una parte, a los tweets que circularon mínimamente y tuvieron un impacto relativo, pudiendo trabajar con un dataset no muy grande pero con un gran abanico de fechas.

Se hicieron pruebas extrayendo datos filtrando por lengua (catalán y castellano). Al extraer los datos en castellano se obtuvo una ingente cantidad de _tweets_ correspondientes a apenas unos días antes. Se descartó este criterio porque no permitía obtener una distribución equilibrada, ni siquiera combinándolo con filtros por fechas. Sin embargo, al extraer datos en catalán se obtuvo una cantidad mucho más manejable por mes que, remontándonos hasta agosto de 2020, llegó a alcanzar los 100000 _tweets_. El dataset original se redujo utlizando el script [reduce_translate.py].

Finalmente, se optó por trabajar con el dataset de los 100 _retweets_, que es el que se ha utilizado para la extracción de las muestras.


## 2. Preprocesado y limpieza de los datos

Esta sección se ha dividido en dos tareas. Por una parte, la traducción de los tweets del castellano al inglés, para poder usar clasificadores preentrenados en inglés, y la limpieza de los tweets en tokens para poder estudiar su contenido.

### 2.1. Traducción

Como el volumen de tweets seguía siendo considerable, se ha empleado una herramienta que permitiera traducir los tweets de manera automatizada. Para ello, se contempló el uso de *google_trans*, pero este no funcionó adecuadamente y se tuvo que usar la herramienta *google_trans_new*. La dificultad en este apartado radicó en la lentitud del proceso, pues cualquier intento para acelerarlo provocó que la API de Google devolviera los tweets sin traducir. Hubo que buscar un compromiso entre esperar unos segundos entre petición y petición para evitar cualquier limitación de la API pero sin demorar mucho la traducción. La traducción se encuentra en el script [reduce_translate.py](preprocessing/translate.py).

### 2.2. Limpieza

#### 2.2.1. En inglés

La limpieza de los datos traducidos al inglés se encuentra en el script [clean_english.ipynb](preprocessing/clean_english.ipynb). Este script se basa en el script [preprocessing_es_cat](preprocessing/preprocessing_es_cat.py), con la particularidad de que en este caso se ha optado por usar la librería SpaCy para lematizar el texto en inglés.

Los datos traducidos al inglés se han usado para crear el clasificador, del que se habla en la última sección de este documento.

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
- Se ha pasado un Stemmer en castellano. Se ha desestimado el uso de un lemmatizer, pese haber contemplado usar _spacy_, por ser demasiado lento. Además, se ha dejado comentada la opción de usar un Stemmer en catalán, que ha tenido que ser instalado por una biblioteca tercera.

## 3. Análisis exploratorio

El análisis exploratorio se divide en dos archivos:

### 3.1.1 Características básicas

En este notebook se analizan las características del dataset recuperado por scraping.

### 3.1.2. Nubes de palabras y aprendizaje no supervisado

En el notebook [words_unsupervised.ipynb](exploratory/words_unsupervised.ipynb) se han estudiado las palabras y bigramas más frecuentes de los tweets preprocesados. Se han obtenido los gráficos de la frecuencia de cada término.

Para intentar una primera clasificación, se han intentado encontrar los tópicos de los tweets mediante LDA con la biblioteca gensim y más tarde en TruncatedSVD. Como este no era el objetivo del proyecto y exigía demasiado trabajo, en el notebook se plantea un código donde más adelante se podría trabajar más a fondo.

### 3.2 Similaridad

En el notebook [explore_similarities.ipynb](exploratory/explore_similarities.ipynb) se ha usado el package Word2Vec de la librería Gensim para explorar las relaciones semánticas entre las palabras. El archivo utlizado para entrenar el modelo es el dataset de los 100 _retweets_ traducido y limpio (vacunes_100rt_en_clean.csv). EL objetivo es observar asociaciones que se han aprendido a partir de los datos. Podemos encontrar:
- Cuáles son las palabras más similares a una palabra concreta.
- El grado de similaridad entre dos palabras.
- Qué palabras sobran de entre un grupo de palabras.
- A qué analogías dan lugar las asociaciones entre palabras.

Se han usado visualizaciones basadas en el algoritmo t-SNE para comparar grupos de palabras similares y disimilares entre sí.

## 4. Visualización de los datos y polaridad

En este apartado se han estudiado la distribución de tweets por día. Se han cuantificado a modo de producción de tweets diaria, y después se les ha pasado un clasificador precompilado para intentar predecir su polaridad. Se han usado clasificadores precompilados, que se han aplicado sobre la muestra traducida al inglés. Los clasificadores empleados son los que han dado mejor resultado según la última sección de este proyecto, y que se suelen usar para análisis de redes sociales:
- TextBlob
- Vader

### 4.1. Producción de tweets diaria

En el script [visualizacion_textblob.ipynb](visualization/visualizacion_textblob.ipynb) se muestra la distribución de la producción de tweets diaria, que se ha obtenido sumando los tweets de cada día. A partir de diciembre de 2020 se puede observar, sin ayuda de herramientas externas, como esta producción aumenta en gran medida.

### 4.2. Producción de tweets según su polaridad diaria

Para decidir si un tweet es negativo, neutral o positivo se atiende solamente a la polaridad que devuelve TextBlob, o a la polaridad (_compound_) que devuelve VADER. De esta forma, se decide que:
- Si esta polaridad está entre -1 y -0.05 el tweet es negativo.
- Si está entre -0.05 y 0.05 es neutral.
- Si está entre 0.01 y 1 es positivo.

Esta regla se ha extraído de la documentación de VADER y se ha aplicado para ambos clasificadores.

#### 4.2.1. Según TextBlob

En el notebook [visualizacion_textblob.ipynb](visualization/visualizacion_textblob.ipynb) está el estudio de la polaridad de los tweets temporal según TextBlob.

Mirando en números absolutos la cantidad de tweets negativos, positivos y neutrales en un gráfico de barras apliadas según polaridad no se puede sacar ninguna conclusión a priori, pues es casi incomprensible.

Sin embargo, si se miran el porcentaje de tweets de cada polaridad en relación a la producción total de tweets, es complicado distinguir cualquier características. Sin embargo, aplicando un algoritmo de Estadística Bayesiana se puede identificar como a partir de mediados de septiembre la media esperada de la proporción de tweets negativos aumenta en un 5%.

Aplicando el mismo algoritmo a los tweets positivos y neutrales, en el primer caso aparece una ligera disminución sobre la misma fecha pero es prácticamente imperceptible y carente de significado; mientras que en el segundo hay una variación un poco más percepetible pero no tan clara.

#### 4.2.2. Según VADER

El notebook [visualizacion_vader.ipynb](visualization/visualizacion_vader.ipynb) se ha seguido el mismo procedimiento pero empleando en éste el clasificador de VADER. Respecto el algoritmo de Estadística Bayesiana, se ha observado un aumento sobre la misma fecha (en este caso una semana antes) de un 10% de la proporción de tweets negativos. A este aumento de la media esperada de tweets negativos le va seguido, en la misma fecha, una caída de algo más del 5% de tweets positivos, y otro descenso del 5% de tweets neutrales.

## 5. Extracción de las muestras y creación de un clasificador

### 5.1. Extracción de las muestras

El objetivo de este proyecto es realizar un análisis de sentimientos entorno a la vacuna. Sin embargo, este se quería enmarcar a la idea de un rechazo a la vacuna por miedo a efectos adversos o similar. Por esta razón, se han extraído dos muestras de mil tweets cada una en el script [generate_sample.py](data/samples/generate_sample.py) y se han etiquetado manualmente en cuatro categorías:

- Positivo: si había, implícitamente o explícitamente, un apoyo o admiración a la vacuna a pesar que el tweet mostrara enfado hacia una tercer actor.
- Negativo: si había, implícitamente o explícitamente, un rechazo o una muestra de miedo hacia la vacuna a pesar de que el tweet mostrara cierta simpatía.
- Neutral: cuando la vacuna cobraba importancia en el tweet pero no se podía dilucidar si era positivo o negativo.
- Irrelevante: cuando la vacuna dejaba de tener importancia en el tweet o no tenía nada que ver con el tema propuesto.

Debido a la complejidad de distinguir entre neutral e irrelevante, a la práctica se han incluido los irrelevantes dentro de los neutrales.

### 5.2. Comparación con los clasificadores preentrenados

Se han comparado las etiquetas elaboradas manualmente con las devueltas por diferentes clasificadores en el script [comparing_textblob.ipynb](classifier/comparing_textblob.ipynb) y se ha elaborado para cada uno una matriz de confusión. Los clasificadores contemplados son:
- TextBlob
- Vader
- Sentiment Analysis Spanish

El tercero ha arrojado unos datos realmente malos y desbalanceados, por lo que se ha obviado en el resto de secciones. Los otros dos son bastante competitivos entre ellos. La manera de comprarlos ha sido mediante matrices de confusión normalizadas en el eje horizontal. De esta manera, se mira el porcentaje de tweets de cada polaridad reales que se aciertan. Mirar solamente la _accuracy_ en este caso sería insuficiente, pues, en las muestras, la mayoría de los tweets son neutrales y un fallo en los neutrales representaría una caída de la _accuracy_ considerable.

#### 5.2.1. Discusión

En el script [comparing_textblob.ipynb](classifier/comparing_textblob.ipynb) se puede ver como TextBlob es mejor detectando tweets positivos (que tienen la etiqueta 2), y bastante malo detectando tweets negativos (que tienen la etiqueta 1). Así, solo fue capaz de identificar como negativos un 17% de los tweets negativos, pero un 50% de los tweets positivos fueron etiquetados correctamente. Es importante notar que tiene poca pretensión a categorizar cualquier tweet como negativo cuando se equivoca. Los suele categorizar como positivo o neutral. Según estos resultados, se puede ver como polariza los resultados hacia etiquetas positivas (sobretodo) y neutrales.

Por otra parte, en el mismo script, se puede ver que con VADER el clasificador funciona mejor en términos relativos. Es un poco más equilibrado pese a tener una menor accuracy (a causa de que predice peor los neutrales). En este caso, sigue predeciendo igual de bien los positivos pero cuando se equivoca lo hace de forma más equilibrada. Si que es cierto que le cuesta más decir que un tweet es neutral, pero no es tan grave que con el caso de TextBlob. Para nuestro caso, se considera este clasificador más fiable por resultar más equilibrado, aunque sí que es cierto que sigue polarizando parcialmente la muestra hacia los dos extremos.

Finalmente, se ha hecho la media aritmética de los dos clasificadores. El resultado no ha sido mejor que los anteriores, por lo que se desestima en esta discusión.

Una vez estudiados los dos clasificadores, se ha llegado a las siguientes conclusiones:
- Para este proyecto, se considera VADER como el mejor clasificador precompilado.
- Viendo las carencias de cada clasificador, se entiende por qué TextBlob detectaba pocas fluctuaciones en los tweets positivos (en mayor medida) y los neutrales y una subida menos perceptible que en el caso de VADER. En el caso de VADER, es entiende lo contrario: se predicen mejor los negativos aunque aún mejor los positivos. Sin embargo, tendirá a polarizar las muestras en positivos y negativos pues detecta bastante mal los neutrales.
- Siguiendo a lo anterior, aunque VADER tiende a polarizar las muestras, parece que las polarizará más sobre lo positivo que lo negativo. Esto quiere decir que, según Vader, igual que con TextBlob, hay una tendencia a inflar más los tweets positivos, y, por lo tanto, este aumento del 10% se puede tener en cuenta como real.
- El hecho que el clasificador de Textblob, que subestimaba los tweets negativos, haya detectado una subida de los tweets negativos aunque sea ligera, significa que esta percepción puede ser considerada como real.
- Esta gran divergencia entre lo esperado según la clasificación manual y automática con los clasificadores precompilados se asume a que muchos tweets que tenían connotaciones negativas y que albergaban una crítica fuerte eran categorizados como positivos o neutrales cuando no mostraban o admiraban la vacuna.

Finalmente, se propone ampliar el espectro de VADER para decidir que un tweet es neutral, pues la cantidad de tweets neutrales es muy grande. Esto se ha inentado abordar construyendo un clasificador que decidiera, según la polaridad de TextBlob y Vader, la polaridad del tweet, y se explica en la siguiente sección.

### 5.3. Construcción de clasificadores

Una vez visto las carencias de cada clasificador, se propone cerar un clasificador acorde con las necesidades de este proyecto. Se intentan abordar desde diferentes perspectivas.

#### 5.3.1. A partir de la salida de los clasificadores anteriores

Se ha creado un clasificador a partir de la salida de los tres clasificadores estudiados. Esto se ha realizado en el notebook [textblob_classifier.ipynb](classifier/textblob_classifier.ipynb). Se ha creado mediante una SVM pues, igual que en los demás clasificadores, era el que arrojaba mejores resultados y que permitía controlar más fácilmente el problema de desbalanceo, presente en los demás clasificadores. Los campos usados son:
- La subjetividad que proporciona TextBlob entre 0 y 1.
- La polaridad que proporciona Textblob entre -1 y 1.
- La polaridad del atributo _compound_ que proporciona VADER entre -1 y 1.
- La polaridad que devuelve _Sentiment Analysis Spanish_ entre 0 y 1.

Se ha usado el objeto MinMaxScaler para elaborar este clasificador, pero no ha sido mejor que VADER solo.


#### 5.3.2. A partir del texto traducido en inglés

Se ha creado un clasificador estudiando la frecuencia de las palabras con la base de datos traducida al inglés. Este acercamiento se puede ver en el notebook [english_classifier.ipynb](classifier/english_classifier.ipynb)

#### 5.3.3. A partir del texto original en español

Este clasificador ha sido una SVM por las mismas razones que el clasificador de la salida de los clasificadores preentrenados. Se ha intentado realizar de dos maneras, ambas en el script [spanish_classifier.ipynb](classifier/spanish_classifier.ipynb).

##### 5.3.3.1. Tres categorías
Primero se ha intentado realizar un clasificador con las tres categorías. Se ha relizado una Cross Validation y se han buscado los mejores parámetros. Cuando se ha aplicado el clasificador entrenado con los datos _training_ a _test_, se ha visto que no se cumplía lo observado en _Validation_ y resultaba completamente desbalanceado.

#### 5.3.3.2. Dos clasificadores de dos categorías

La manera de abordarlo fue creando un clasificador que fuera capaz de discernir entre neutrales (la clase mayoritaria) y positivos y negativos. Después, elaborar un clasificador solo para positivos y negativos que discerniera entre estos dos. El problema de este acercamiento ha sido el desbalanceo. Debido al gran volumen de tweets neutrales, una proporción relativamente pequeña de los tweets neutrales que se identifiquen erróneamente como con polaridad, se pasarían al segundo clasificador. Además, la precisión del clasificador no fue lo suficientemente satisfactoria.
