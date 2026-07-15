import streamlit as st
import os
import time

from speech_to_text import transcribe_audio
from semantic_eval import calculate_similarity
from scoring_engine import calculate_score
from report_generator import generate_pdf
from audio_utils import extract_features
from waveform import save_waveform
st.set_page_config(
    page_title="Voice-Based Communication Understanding Analyzer",
    page_icon="🎤",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.main{
    padding-top:1rem;
}

.score{
    font-size:55px;
    font-weight:bold;
    color:#00ff99;
}

.result-box{
    padding:15px;
    border-radius:10px;
    background:#262730;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------

st.title("🎤 Voice-Based Communication Understanding Analyzer")
st.caption("Automated evaluation of spoken conceptual explanations using AI.")

st.divider()

# ---------------- Input ----------------

left,right = st.columns([2,1])

with left:

    uploaded_file = st.file_uploader(
        "Upload Student Audio (WAV/MP3)",
        type=["wav","mp3"]
    )

with right:

    reference_text = st.text_area(
        "Concept Reference",
        height=180
    )

# ---------------- Analysis ----------------

if uploaded_file is not None and reference_text != "":

    audio_path = "sample.wav"

    with open(audio_path,"wb") as f:
        f.write(uploaded_file.read())

    st.audio(audio_path)
    waveform_path = save_waveform(audio_path)
    st.session_state.waveform_path = waveform_path
    st.subheader("📈 Audio Waveform")

    st.image(waveform_path, use_container_width=True)
    st.divider()

    if st.button("🚀 Analyze Concept Understanding"):

        with st.spinner("Processing Audio..."):

            transcription = transcribe_audio(audio_path)

            similarity = calculate_similarity(reference_text, transcription)

            score, grade = calculate_score(similarity)

            audio_features = extract_features(audio_path)

            waveform_path = save_waveform(audio_path)

            # SAVE STATE (IMPORTANT FIX)
            st.session_state.done = True
            st.session_state.transcription = transcription
            st.session_state.reference_text = reference_text 
            st.session_state.similarity = similarity
            st.session_state.score = score
            st.session_state.grade = grade
            st.session_state.audio_features = audio_features
            st.session_state.waveform_path = waveform_path
        # ---------------- Results ----------------

        col1,col2 = st.columns([2,1])

        with col1:

            st.subheader("📝 Transcribed Explanation")

            st.write(transcription)

        with col2:

            st.subheader("🏆 Final Result")

            st.markdown(
                f"<div class='score'>{score}/100</div>",
                unsafe_allow_html=True
            )

            if similarity >= 0.80:
                st.success("Excellent Understanding")

            elif similarity >= 0.60:
                st.warning("Moderate Understanding")

            else:
                st.error("Poor Understanding")

            st.write(f"**Grade :** {grade}")

        st.divider()

        # ---------------- Metrics ----------------

        m1,m2,m3 = st.columns(3)

        with m1:

            st.metric(
                "Semantic Similarity",
                f"{similarity:.2f}"
            )

        with m2:

            st.metric(
                "Duration (sec)",
                f"{audio_features['Duration']:.2f}"
            )

        with m3:

            st.metric(
                "RMS Energy",
                f"{audio_features['RMS Energy']:.4f}"
            )

        st.divider()

        # ---------------- Waveform ----------------

        st.subheader("📈 Audio Waveform")

        st.image(waveform_path, use_container_width=True)

        st.divider()
        

        # ---------------- Audio Features ----------------

        st.subheader("🎵 Audio Features")

        st.json(audio_features)

        st.divider()

        # ---------------- PDF ----------------

if st.session_state.get("done", False):
    transcription = st.session_state.transcription
    similarity = st.session_state.similarity
    score = st.session_state.score
    grade = st.session_state.grade
    if st.button("📄 Generate PDF Report"):

        pdf_path = generate_pdf(
            st.session_state.reference_text,
            st.session_state.transcription,
            st.session_state.similarity,
            st.session_state.score,
            st.session_state.grade,
            st.session_state.audio_features,
            st.session_state.waveform_path
        )
        st.success(f"Saved to: {pdf_path}")
        import os

        st.write("PDF Path:", pdf_path)
        st.write("File Exists:", os.path.exists(pdf_path))
        with open(pdf_path, "rb") as pdf:

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf,
                file_name="Communication_Report.pdf",
                mime="application/pdf"
            )
