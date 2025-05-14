import os
import openai
import streamlit as st

# Título y descripción
st.title("💬 Chatbot")
st.write("Hola! estos son tus resultados:")

# Obtener la API Key desde los secretos de Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Inicializar el historial de mensajes en la sesión si no existe
if "messages" not in st.session_state:
 st.session_state.messages = [
    {"role": "system", "content": (
        "Actúa como un psicólogo profesional con especialización en prevención y tratamiento del consumo de alcohol en adolescentes. "
        "Ofrece respuestas empáticas, basadas en evidencia, y orientadas a guiar tanto a jóvenes como a sus familias. "
        "Responde siempre desde este rol con lenguaje claro y profesional."
    )}
]

# Mostrar el historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de mensaje del usuario
if prompt := st.chat_input("¿Qué te gustaría preguntar?"):

    # Agregar el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar el mensaje del usuario en el chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Solicitar una respuesta al modelo de OpenAI
    try:
        stream = openai.chat.completions.create(
            model="gpt-4.1-nano",  # Usa un modelo válido y disponible en tu cuenta
            messages=st.session_state.messages,
            stream=True,
        )

        # Mostrar la respuesta del asistente y agregarla al historial
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"❌ Error al generar la respuesta: {e}")

