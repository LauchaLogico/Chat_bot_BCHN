import streamlit as st
import json
import re

# Datos de los cursos (Tambien se podrían cargar desde un JSON similar y vincularlo con funcion)
cursos_info = {
    "Virtual T": {
        "description": "100% práctico, diseñado para docentes, capacitadores y formadores que quieren actualizarse en nuevas metodologías sin complicarse la vida. Aprenderás a usar herramientas tecnológicas, aplicar metodologías ágiles, mantener la atención de tus estudiantes y convertir tus clases en experiencias memorables. Incluye módulos sobre emociones, atención, transformación digital educativa e inteligencia emocional educativa.",
        "keywords": ["metodologias", "tecnologia", "atencion", "memorables", "emociones", "transformacion digital", "inteligencia emocional"]
    },
    "Bara Games": {
        "description": "Descubrirás cómo el juego puede ser tu mejor aliado. Dirigido a docentes, formadores y conferencistas 100% online. Aprenderás a conocer comportamientos de estudiantes mediante el juego, utilizar el juego como herramienta pedagógica y aplicar actividades prácticas, sencillas y listas. Contenido sobre características de los juegos, jugadores, modelo MDA, beneficios de la gamificación y enseñar a pensar jugando.",
        "keywords": ["juego", "gamificacion", "pedagogica", "actividades", "comportamientos"]
    },
    "Fabrica de Creativos": {
        "description": "Aprenderás a identificar tu estilo creativo, desbloquear ideas, aplicar procesos creativos en clases, talleres o capacitaciones, diseñar actividades innovadoras y escribir con soltura y creatividad. Módulos sobre innovación, creatividad, storytelling, creatividad sensorial, escritura creativa y desarrollo de ideas.",
        "keywords": ["creatividad", "innovacion", "ideas", "storytelling", "escritura creativa"]
    },
    "Algo Líder": {
        "description": "Diseñado para docentes y facilitadores que quieren liderar con propósito, construir equipos colaborativos y generar cambios positivos desde el aula. Aprenderás a desarrollar un liderazgo empático y estratégico, gestionar dinámicas educativas, motivar a estudiantes y colegas, y ser un agente de cambio. Módulos sobre características de un líder, cómo motivar, cómo dirigir y manejo de emociones.",
        "keywords": ["liderazgo", "lider", "motivacion", "equipos", "cambio", "emociones"]
    },
    "Disrupted": {
        "description": "¿Sientes curiosidad por la inteligencia artificial? Este curso es tu punto de partida para revolucionar tu práctica educativa con IA y Web3, 100% desde cero. Aprenderás casos reales en educación, aplicaciones prácticas y seguras. Módulos sobre Chat GPT, modelos de IA, IA Generativa, Web3, Billeteras Digitales, Agentes de IA e Ingeniería de Prompt básica, e Insignias Digitales.",
        "keywords": ["inteligencia artificial", "IA", "chat gpt", "web3", "generativa", "prompt", "digitales"]
    },
    "D Mentes Verdes": {
        "description": "Un curso para docentes que quieren ir más allá del aula y dejar huella. Aprende a integrar la sostenibilidad en tu práctica educativa y forma generaciones conscientes, críticas y comprometidas con el planeta. Aprenderás el impacto de la sostenibilidad, a integrar la eco-conciencia, transformar tu escuela con hábitos sostenibles, diseñar proyectos reales y medir avances ambientales. Módulos sobre introducción a la sostenibilidad, sostenibilidad en el currículo, prácticas sostenibles, diseño de proyectos sostenibles y evaluación y seguimiento.",
        "keywords": ["sostenibilidad", "planeta", "eco-conciencia", "ambiental", "reciclaje", "recursos"]
    }
}

# Inicializar estado del chatbot
if "recommendation_stage" not in st.session_state:
    st.session_state.recommendation_stage = 0 # 0: inicio, 1-5: preguntas, 6: resultado
    st.session_state.scores = {curso: 0 for curso in cursos_info.keys()}
    st.session_state.chat_history = []
    st.session_state.last_displayed_question = -1 # Nueva variable para controlar la visualización de la pregunta

# Preguntas y lógica de puntuación
questions = [
    {
        "text": "¿Cuál es tu objetivo principal al tomar un curso de formación?",
        "options": {
            "A) Quiero actualizar mis metodologías de enseñanza y usar más tecnología.": {"Virtual T": 3, "Disrupted": 1},
            "B) Me interesa incorporar el juego y la diversión en mis clases para mejorar el aprendizaje.": {"Bara Games": 3, "Fabrica de Creativos": 1},
            "C) Busco potenciar mi creatividad e innovar en el diseño de actividades y contenidos.": {"Fabrica de Creativos": 3, "Virtual T": 1},
            "D) Deseo desarrollar mis habilidades de liderazgo y motivar a mis estudiantes y equipo.": {"Algo Líder": 3},
            "E) Tengo curiosidad por la Inteligencia Artificial y cómo aplicarla en el ámbito educativo.": {"Disrupted": 3},
            "F) Quiero enseñar sobre sostenibilidad y cómo cuidar el planeta en mi institución.": {"D Mentes Verdes": 3}
        },
        "type": "single"
    },
    {
        "text": "¿Qué tipo de herramientas o conceptos te gustaría explorar más a fondo?",
        "options": {
            "A) Herramientas tecnológicas para dinamizar clases.": {"Virtual T": 2},
            "B) Estrategias de gamificación y diseño de juegos.": {"Bara Games": 2},
            "C) Técnicas para generar ideas y escribir de forma más fluida.": {"Fabrica de Creativos": 2},
            "D) Habilidades para dirigir equipos y gestionar emociones.": {"Algo Líder": 2},
            "E) Chat GPT, IA generativa y Web3.": {"Disrupted": 2},
            "F) Conceptos de eco-conciencia y prácticas sostenibles.": {"D Mentes Verdes": 2}
        },
        "type": "multi" # Permite seleccionar varias opciones
    },
    {
        "text": "¿Cuál de estos desafíos te resuena más en tu práctica actual?",
        "options": {
            "A) Mantener el interés y la atención de mis estudiantes.": {"Virtual T": 2, "Bara Games": 1},
            "B) Lograr que mis estudiantes participen activamente y se diviertan aprendiendo.": {"Bara Games": 2},
            "C) Romper con la rutina y crear experiencias de aprendizaje únicas.": {"Fabrica de Creativos": 2},
            "D) Inspirar a otros y guiar un cambio positivo en mi entorno educativo.": {"Algo Líder": 2},
            "E) Integrar nuevas tecnologías disruptivas de manera efectiva y segura.": {"Disrupted": 2},
            "F) Fomentar valores de responsabilidad ambiental en el aula.": {"D Mentes Verdes": 2}
        },
        "type": "single"
    },
    {
        "text": "¿Qué tan cómodo/a te sientes con la tecnología actualmente?",
        "options": {
            "A) Básico/a (Necesito aprender desde cero).": {"Virtual T": 1, "Disrupted": 2},
            "B) Intermedio/a (Conozco algunas herramientas y quiero profundizar).": {"Virtual T": 2, "Bara Games": 1, "Fabrica de Creativos": 1, "Algo Líder": 1, "Disrupted": 1, "D Mentes Verdes": 1},
            "C) Avanzado/a (Busco las últimas tendencias y aplicaciones innovadoras).": {"Disrupted": 3}
        },
        "type": "single"
    },
    {
        "text": "¿Te interesa que el curso tenga un enfoque en...?",
        "options": {
            "A) La transformación del aula y la pedagogía.": {"Virtual T": 2, "Bara Games": 2},
            "B) El desarrollo personal y profesional como líder.": {"Algo Líder": 2},
            "C) La aplicación de nuevas tendencias tecnológicas (como la IA).": {"Disrupted": 2},
            "D) La responsabilidad social y ambiental.": {"D Mentes Verdes": 2}
        },
        "type": "multi"
    }
]

def get_recommendation():
    max_score = -1
    recommended_course = None
    tied_courses = []

    for course, score in st.session_state.scores.items():
        if score > max_score:
            max_score = score
            recommended_course = course
            tied_courses = [course]
        elif score == max_score and score > 0: # Handle ties, only if score > 0
            tied_courses.append(course)

    if not recommended_course or max_score <= 0:
        return "No pude encontrar una recomendación clara basada en tus respuestas. Te invitamos a explorar todos nuestros cursos o contactarnos para una asesoría personalizada.", []

    if len(tied_courses) > 1:
        return f"Basado en tus respuestas, los cursos que mejor se adaptan a tus necesidades son: **{', '.join(tied_courses)}**.", tied_courses
    else:
        return f"Basado en tus respuestas, el curso más apropiado para ti es: **{recommended_course}**.", [recommended_course]

def display_course_details(course_name):
    if course_name in cursos_info:
        st.markdown(f"### Detalles de {course_name}:")
        st.markdown(cursos_info[course_name]["description"])
    else:
        st.markdown(f"No se encontraron detalles para el curso {course_name}.")

# Interfaz de Streamlit
st.title("Asistente de Recomendación de Cursos de Bara Creativa HN 🎓")
st.write("¡Hola! Te haré 5 preguntas para recomendarte el curso más adecuado para ti.")

# Mostrar historial de chat
for chat_entry in st.session_state.chat_history:
    with st.chat_message(chat_entry["role"]):
        st.markdown(chat_entry["content"])

# Lógica de las preguntas
if st.session_state.recommendation_stage < len(questions):
    current_question_data = questions[st.session_state.recommendation_stage]

    # Solo agrega la pregunta al historial si es una nueva pregunta o si no se ha mostrado 
    if st.session_state.recommendation_stage != st.session_state.last_displayed_question:
        with st.chat_message("assistant"):
            st.markdown(f"**Pregunta {st.session_state.recommendation_stage + 1}:** {current_question_data['text']}")
        st.session_state.chat_history.append({"role": "assistant", "content": f"**Pregunta {st.session_state.recommendation_stage + 1}:** {current_question_data['text']}"})
        st.session_state.last_displayed_question = st.session_state.recommendation_stage # Actualiza la última pregunta mostrada

    # Mostrar opciones para la pregunta actual
    if current_question_data["type"] == "single":
        selected_option = st.radio("Selecciona una opción:", list(current_question_data["options"].keys()), key=f"q_{st.session_state.recommendation_stage}")
        if st.button("Siguiente Pregunta", key=f"btn_q_{st.session_state.recommendation_stage}"):
            for course, points in current_question_data["options"][selected_option].items():
                st.session_state.scores[course] += points
            st.session_state.chat_history.append({"role": "user", "content": selected_option})
            st.session_state.recommendation_stage += 1
            st.rerun() # Rerun to update the display
    elif current_question_data["type"] == "multi":
        selected_options = []
        for i, option_text in enumerate(current_question_data["options"].keys()):
            if st.checkbox(option_text, key=f"multi_q_{st.session_state.recommendation_stage}_{i}"):
                selected_options.append(option_text)
        
        if st.button("Siguiente Pregunta", key=f"btn_q_{st.session_state.recommendation_stage}"):
            if not selected_options:
                st.warning("Por favor, selecciona al menos una opción.")
            else:
                user_choices_text = ""
                for option_text in selected_options:
                    user_choices_text += f"- {option_text}\n"
                    for course, points in current_question_data["options"][option_text].items():
                        st.session_state.scores[course] += points
                st.session_state.chat_history.append({"role": "user", "content": f"Mis selecciones:\n{user_choices_text}"})
                st.session_state.recommendation_stage += 1
                st.rerun() # Rerun to update the display

else:
    # Muestra la recomendación final
    recommendation_text, recommended_courses_list = get_recommendation()
    # Solo añade la recomendación al historial si no es la última entrada
    if not st.session_state.chat_history or st.session_state.chat_history[-1]["content"] != recommendation_text:
        st.chat_message("assistant").markdown(recommendation_text)
        st.session_state.chat_history.append({"role": "assistant", "content": recommendation_text})

    if recommended_courses_list:
        for course_name in recommended_courses_list:
            display_course_details(course_name)
    
    if st.button("Reiniciar Recomendador", key="reset_button"):
        st.session_state.recommendation_stage = 0
        st.session_state.scores = {curso: 0 for curso in cursos_info.keys()}
        st.session_state.chat_history = []
        st.session_state.last_displayed_question = -1 # Reiniciar también esta variable
        st.rerun()
