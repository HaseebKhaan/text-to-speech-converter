
import streamlit as st
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="Voxify | Text to Speech",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10172a, #172554);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    text-align: center;
    padding: 24px 10px;
}
.hero h1 {
    font-size: 44px;
    margin-bottom: 5px;
}
.hero p {
    color: #cbd5e1 !important;
    font-size: 17px;
}
.stTextArea textarea {
    background: #f8fafc;
    color: #111827;
    border-radius: 12px;
}
.stButton button {
    background: #14b8a6;
    color: #071b2b;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    min-height: 45px;
    width: 100%;
}
.stDownloadButton button {
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎙️ Voxify</h1>
    <p>Transform your text into speech in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### ✍️ Enter Your Text")

text = st.text_area(
    "Text to convert",
    placeholder="Type or paste your text here...",
    height=180,
    max_chars=5000,
    label_visibility="collapsed"
)

st.caption(f"Characters: {len(text)} / 5000")

language = st.selectbox(
    "🌐 Select language",
    options=["English", "Hindi", "Urdu", "Arabic", "French", "Spanish"],
    index=0
)

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es"
}

if st.button("🔊 Generate Speech"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Generating your audio..."):
                audio_buffer = BytesIO()
                speech = gTTS(
                    text=text.strip(),
                    lang=language_codes[language]
                )
                speech.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.session_state["audio"] = audio_buffer.getvalue()
                st.session_state["filename"] = "voxify_speech.mp3"

            st.success("Your speech is ready!")
        except Exception as e:
            st.error(
                "Speech generation failed. Check your internet "
                "connection and try again."
            )
            st.caption(f"Technical details: {e}")

if "audio" in st.session_state:
    st.markdown("### 🎧 Your Audio")
    st.audio(st.session_state["audio"], format="audio/mp3")
    st.download_button(
        label="⬇️ Download MP3",
        data=st.session_state["audio"],
        file_name=st.session_state["filename"],
        mime="audio/mpeg",
        use_container_width=True
    )

st.divider()
st.markdown(
    "<center>Made with Python, Streamlit & gTTS | PIMV CSD421</center>",
    unsafe_allow_html=True
)
