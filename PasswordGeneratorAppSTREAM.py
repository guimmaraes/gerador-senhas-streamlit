import streamlit as st
import random
import string
from zxcvbn import zxcvbn

def gerar_alfabeto(use_num, use_upper, use_lower, use_symbols):
    chars = ""
    if use_num:     chars += string.digits
    if use_upper:   chars += string.ascii_uppercase
    if use_lower:   chars += string.ascii_lowercase
    if use_symbols: chars += string.punctuation
    return chars

def gerar_senha(length, alphabet, allow_repeat):
    if not allow_repeat and length > len(alphabet):
        return "Erro: tamanho maior que alfabeto disponível."
    if allow_repeat:
        return "".join(random.choice(alphabet) for _ in range(length))
    else:
        return "".join(random.sample(alphabet, length))

def força_senha(pwd):
    score = zxcvbn(pwd)["score"]
    cores = ['#FF4C4C','#FF7F50','#FFD700','#9ACD32','#4CAF50']
    return score, cores[score]

st.set_page_config(page_title="Gerador de Senhas Seguras", page_icon="🔐")

st.title("🔐 Gerador de Senhas Seguras")
nome = st.text_input("Nome da senha", "")
tamanho = st.slider("Tamanho da senha", 4, 20, 12)
quantidade = st.slider("Quantas senhas gerar", 1, 10, 1)

col1, col2 = st.columns(2)
with col1:
    use_num = st.checkbox("Incluir números", True)
    use_upper = st.checkbox("Incluir maiúsculas", True)
    use_lower = st.checkbox("Incluir minúsculas", True)
with col2:
    use_symbols = st.checkbox("Incluir símbolos", True)
    allow_repeat = st.checkbox("Permitir repetição de caracteres", True)

if st.button("🎲 Gerar Senhas"):
    alfabeto = gerar_alfabeto(use_num, use_upper, use_lower, use_symbols)
    if not alfabeto:
        st.error("Selecione ao menos um tipo de caractere.")
    else:
        senhas = [gerar_senha(tamanho, alfabeto, allow_repeat) for _ in range(quantidade)]
        st.subheader("🔑 Senhas Geradas")
        for s in senhas:
            st.code(s)

        if len(senhas) == 1 and "Erro" not in senhas[0]:
            score, cor = força_senha(senhas[0])
            st.write("💪 Força da senha:", score, "/ 4")
            st.progress(score / 4)
            st.markdown(f"<div style='width:100%;height:20px;background-color:{cor};'></div>", unsafe_allow_html=True)