import streamlit as st
from difflib import SequenceMatcher

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="English Master", layout="centered")

# CSS para melhorar a interface mobile e botões
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 18px !important;
        border-radius: 10px;
    }
    .main {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTEÚDO DAS LIÇÕES ---
LESSONS_DATA = {
    "Iniciante": [
        {"question": "Como se diz 'Oi' em inglês?", "answer": "Hello", "hint": "Começa com 'H'", "explanation": "'Hello' é a forma padrão mais comum."},
        {"question": "Traduza: 'Eu sou um estudante'", "answer": "I am a student", "hint": "Use o verbo 'To Be'", "explanation": "Estrutura: Sujeito + Verb to be + Substantivo."}
    ],
    "Intermediário": [
        {"question": "Qual o passado de 'Go'?", "answer": "Went", "hint": "É um verbo irregular", "explanation": "Irregulares não terminam em 'ed'. Go vira Went."},
        {"question": "Traduza: 'Eu tenho trabalhado'", "answer": "I have been working", "hint": "Present Perfect Continuous", "explanation": "Ações que continuam: Have been + verb-ing."}
    ],
    "Avançado": [
        {"question": "Traduza: 'Se eu soubesse, teria ido'", "answer": "If I had known, I would have gone", "hint": "Third Conditional", "explanation": "Expressa um arrependimento no passado."}
    ]
}

# --- FUNÇÕES DE LÓGICA ---
def check_similarity(a, b):
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

# --- INICIALIZAÇÃO DO ESTADO ---
if 'step' not in st.session_state:
    st.session_state.step = 'diagnostic'
    st.session_state.level = None
    st.session_state.current_idx = 0
    st.session_state.attempts = 0
    st.session_state.mistakes = []

# --- FLUXO DO APLICATIVO ---
if st.session_state.step == 'diagnostic':
    st.title("🎯 Diagnóstico Inicial")
    diag_q = "Responda: 'She ___ (like) pizza'."
    answer = st.text_input(diag_q).strip().lower()
    if st.button("Avaliar Nível"):
        st.session_state.level = "Intermediário" if "likes" in answer else "Iniciante"
        st.session_state.step = 'lesson'
        st.rerun()

elif st.session_state.step == 'lesson':
    lessons = LESSONS_DATA[st.session_state.level]
    if st.session_state.current_idx < len(lessons):
        lesson = lessons[st.session_state.current_idx]
        st.title(f"📖 Nível {st.session_state.level}")
        st.write(f"Pergunta: {lesson['question']}")
        
        user_ans = st.text_input("Sua resposta:", key=f"q_{st.session_state.current_idx}")
        
        if st.button("Verificar"):
            sim = check_similarity(user_ans, lesson['answer'])
            if sim >= 0.9:
                st.success("Correto!")
                st.session_state.current_idx += 1
                st.session_state.attempts = 0
                st.rerun()
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts == 1: st.error("Tente de novo!")
                elif st.session_state.attempts == 2: st.info(f"Dica: {lesson['hint']}")
                else:
                    st.session_state.mistakes.append(lesson)
                    st.error(f"Resposta: {lesson['answer']}")
                    st.write(lesson['explanation'])
                    if st.button("Próxima"):
                        st.session_state.current_idx += 1
                        st.session_state.attempts = 0
                        st.rerun()
    else:
        st.session_state.step = 'review'
        st.rerun()

elif st.session_state.step == 'review':
    st.title("🏁 Fim da Aula!")
    if st.session_state.mistakes:
        for m in st.session_state.mistakes:
            with st.expander(f"Revisar: {m['question']}"):
                st.write(f"Resposta: {m['answer']}")
                st.write(m['explanation'])
    if st.button("Reiniciar"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
