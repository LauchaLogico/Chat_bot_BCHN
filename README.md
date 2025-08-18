# Chat Bot recomendacion de Cursos

## Introducción
Una de las tareas asignadas en mi pasantía en Bara Creativa era crear un chatbot que recomiende un curso a una persona de acuerdo a las respuestas a ciertas preguntas. Es por esto que teniendo la caracteristicas de los cursos, a continuacion un resumen de estas caracteristicas: \
### Perfiles de Curso:
### Virtual T: 
Metodologías ágiles, herramientas tecnológicas, mantener la atención, clases memorables, transformación digital educativa, inteligencia emocional. 
### Bara Games: 
Uso del juego como herramienta pedagógica, gamificación, conocer comportamientos de estudiantes mediante el juego, actividades prácticas. 
### Fabrica de Creativos: 
Identificar estilo creativo, desbloquear ideas, procesos creativos, actividades innovadoras, escritura creativa. 
### Algo Líder:
Liderazgo con propósito, equipos colaborativos, cambios positivos, liderazgo empático y estratégico, gestionar dinámicas, motivar, agente de cambio. 
### Disrupted: 
Inteligencia artificial (IA), Web3, Chat GPT, IA Generativa, Agentes de IA, Ingeniería de Prompt. 
### D Mentes Verdes:
Sostenibilidad en educación, eco-conciencia, hábitos sostenibles (gestión de recursos, energía, residuos), proyectos sostenibles, impacto ambiental.
Lo primero que hice fue como, segun las respuestas de cinco preguntas puedo decidir que curso recomendar. El numero de preguntas fue arbitrario. 
La idea, entonces, fue la siguiente. Segun la respues de cada pregunta se va asignando un puntaje a cada curso, cuando se responden las 5 pregustas se suman los puntos obtenidos por cada uno y el que más puntos tiene es el curso recomendado. 

## Link a la aplicación

Les dejo el link a la aplicacion en Streamlit.\
[Aplicacion recomendacion de cursos ](https://tucursoidealbc.streamlit.app/) \
Todo comentario y sugerencia será bienvenido, muchas gracias

## Contenido

$recomendar_cursos.py$ Programa principal  \
$requirements.txt:$ requerimientos para que todo funcione correctamente \

## Tecnología

El programa se generó uyilizando lenguaje Python. Las librerias necesarias para que todo funcione correctamente son las siguientes: \
streamlit (importada como st) - Es un framework para crear aplicaciones web interactivas en Python, ideal para dashboards y visualizaciones de datos. \
json - Es un módulo estándar de Python para trabajar con datos en formato JSON (JavaScript Object Notation). \
re - Es el módulo de expresiones regulares (regex) de Python, usado para búsqueda y manipulación de patrones en cadenas de texto. \

Para la visualización de la aplicacion se utilizó la página de [Streamlit](https://streamlit.io/)
