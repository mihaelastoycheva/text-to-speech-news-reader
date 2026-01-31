import streamlit as st
import requests
import os
from dotenv import load_dotenv
from docx import Document
from elevenlabs.client import ElevenLabs
from bs4 import BeautifulSoup


# Load API key
load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Streamlit UI
st.title("Слушай сега любимите ти бизнес новини на български език 🇧🇬")

voice_id = st.text_input("Въведи ElevenLabs Voice ID:", "31jwlwrRwpOA5yGuVAby")


# Function: Extract article text from Lider.BG link
def extract_article(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")

    # Extract Title
    title_element = soup.find("h1", class_="entry-title")
    title = title_element.get_text().strip() if title_element else ""

    # Extract Article Content
    content = soup.find("div", class_="td-post-content tagdiv-type")
    paragraphs = []

    if content:
        for p in content.find_all("p"):
            text = p.get_text().strip()
            if text:
                paragraphs.append(text)

    article_text = "\n".join(paragraphs)

    return title, article_text


# TAB 1 — Paste text directly
st.header("✏️ Въведи статията като текст и го превърни в аудио")

user_text = st.text_area("Постави статията тук:", height=200)

if st.button("Генерирай аудио от текст"):
    if user_text.strip():
        with st.spinner("Генериране на аудио..."):
            audio = client.text_to_speech.convert(
                text=user_text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )

            output_path = "text_output.mp3"
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)

        st.success("Аудиото е генерирано успешно. Наслади се на новините!")
        st.audio(output_path)
    else:
        st.error("Моля, въведи текст.")


# TAB 2 — Read DOCX file
st.header("📄 Конвертирай статия от DOCX файл в аудио")

uploaded_file = st.file_uploader("Прикачи DOCX файл тук", type=["docx"])

if uploaded_file is not None:
    document = Document(uploaded_file)
    extracted_text = "\n".join([p.text for p in document.paragraphs])

    st.subheader("Текст:")
    st.text_area("", extracted_text, height=200)

    if st.button("Генерирай аудио"):
        if extracted_text.strip():
            with st.spinner("Генериране на аудио..."):
                audio = client.text_to_speech.convert(
                    text=extracted_text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )

                output_path = "docx_output.mp3"
                with open(output_path, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)

            st.success("Аудиото е генерирано успешно. Наслади се на новините!")
            st.audio(output_path)
        else:
            st.error("DOCX файлът не съдържа файл за изчитане")


# TAB 3 — Read Lider.BG Article URL
st.header("🌐 Конвертирай статия от Лидер.БГ в аудио")

url = st.text_input("Постави линк към статия от Лидер.БГ:")

if url:
    with st.spinner("Извличане на статията..."):
        title, article_text = extract_article(url)

    if not title and not article_text:
        st.error("Не може да бъде извлечена статия от посочения линк. Провери дали линкът е валиден и сочи към статия от медията Лидер.БГ.")
    else:
        st.success("Статията е извлечена успешно!")

        st.write("### 📰 Заглавие")
        st.write(title)

        st.write("### 📘 Съдържание на статията")
        st.write(article_text)

        full_text = f"{title}\n\n{article_text}"

        if st.button("Генерирай аудио"):
            with st.spinner("Генериране на аудио..."):
                audio = client.text_to_speech.convert(
                    text=full_text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )

                output_path = "article_output.mp3"
                with open(output_path, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)

            st.success("Аудиото е генерирано успешно. Наслади се на новините!")
            st.audio(output_path)
