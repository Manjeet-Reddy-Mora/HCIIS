import streamlit as st

from nlp_utils import preprocess_text
from cognitive_load import cognitive_load
from manipulation_analysis import manipulation_score
from emotion_analysis import emotion_analysis
from decision_risk import decision_risk
from info_quality import information_quality
from pdf_report import generate_pdf_report

# ---------------- Page Setup ----------------
st.set_page_config(
    page_title="Human-Centered Information Intelligence System",
    layout="wide"
)

st.title("🧠 Human-Centered Information Intelligence System (HCIIS)")
st.caption(
    "A Multi-Dimensional NLP Framework for Cognitive Load, Manipulation, "
    "Emotion, Decision Risk, and Information Quality Analysis"
)

# ---------------- Input ----------------
text_input = st.text_area(
    "Paste text for analysis",
    height=280,
    placeholder="Paste any article, policy, review, news, or document text here..."
)

if not text_input.strip():
    st.info("Please enter text to begin analysis.")
    st.stop()

clean_text = preprocess_text(text_input)

# ---------------- Analysis ----------------
cog = cognitive_load(clean_text)
manip = manipulation_score(clean_text)
emo = emotion_analysis(clean_text)
dec = decision_risk(clean_text)
qual = information_quality(clean_text)

# ---------------- Tabs ----------------
tabs = st.tabs([
    "🧠 Cognitive Load",
    "🎯 Manipulation",
    "😊 Emotion",
    "⚖️ Decision Risk",
    "📊 Information Quality",
    "📄 Download Report"
])

with tabs[0]:
    st.subheader("Cognitive Load & Attention Risk")
    st.metric("Cognitive Load Score", cog["load"])
    st.metric("Attention Drop Risk", cog["attention_drop"])
    st.write(cog["explanation"])

    with st.expander("ℹ️ What is Cognitive Load & How It Is Calculated"):
        st.write("""
        **Cognitive Load** represents the mental effort required to process text.
        This score is calculated using:
        - **Average sentence length** (long sentences increase working memory demand)
        - **Sentence length variance** (irregular structure increases effort)
        - **Lexical density** (high concentration of content words increases complexity)
        Higher scores indicate greater attention fatigue and higher risk of reader disengagement.
        """)

with tabs[1]:
    st.subheader("Manipulation & Persuasion")
    st.metric("Manipulation Score", manip["score"])
    st.write(manip["details"])
    st.json(manip["breakdown"])

    with st.expander("ℹ️ What is Manipulation & Persuasion Analysis"):
        st.write("""
        This module detects **linguistic persuasion techniques** that influence reader judgment.

        It analyzes:
        - **Fear framing** (threats, urgency, loss)
        - **Authority masking** (claims without evidence)
        - **Certainty inflation** (absolute, unquestionable language)
        - **Emotional pressure** (loaded adjectives)

        Scores are normalized by text length to avoid overestimation in short content.
        """)

with tabs[2]:
    st.subheader("Emotion & Tone Analysis")
    st.metric("Dominant Emotion", emo["dominant"])
    st.metric("Emotional Volatility", emo["volatility"])
    st.write(emo["summary"])
    st.json(emo["counts"])

    with st.expander("ℹ️ What is Emotion & Tone Analysis"):
        st.write("""
        This module identifies the **emotional character** of the text.

        It calculates:
        - **Dominant emotion** based on affective lexical cues
        - **Emotional volatility**, measuring emotional shifts across sentences
        - **Suppressed emotion**, where neutral language masks emotional content

        This provides insight into emotional stability and hidden affect.
        """)

with tabs[3]:
    st.subheader("Decision Risk & Ambiguity")
    st.metric("Decision Density", dec["density"])
    st.metric("Ambiguity Score", dec["ambiguity"])
    st.write(dec["notes"])
    st.json(dec["details"])

    with st.expander("ℹ️ What is Decision Risk & Ambiguity"):
        st.write("""
        Decision Risk measures how clearly a text presents choices and consequences.

        It evaluates:
        - **Decision density** (how often decisions are required)
        - **Ambiguity markers** (vague terms like 'may', 'as applicable')
        - **Risk visibility** (whether consequences are explicitly stated)

        High ambiguity scores indicate unclear commitments and potential decision traps.
        """)

with tabs[4]:
    st.subheader("Information Quality Index")
    st.metric("Quality Score", qual["quality"])
    st.write(qual["analysis"])
    st.json(qual["details"])

    with st.expander("ℹ️ What is the Information Quality Index"):
        st.write("""
        The Information Quality Index evaluates **how meaningful and reliable** the text is.

        It combines:
        - **Evidence density** (presence of data, studies, results)
        - **Rhetorical intensity** (emphasis without substance)
        - **Redundancy** (repetition and filler)
        - **Structural variance** (informational richness)

        Higher scores indicate high signal-to-noise ratio and substantive content.
        """)

with tabs[5]:
    st.subheader("Generate Academic PDF Report")

    if st.button("Generate PDF"):
        pdf_file = generate_pdf_report(
            text_input, cog, manip, emo, dec, qual
        )

        with open(pdf_file, "rb") as f:
            st.download_button(
                "⬇ Download PDF Report",
                f,
                file_name="HCIIS_Report.pdf",
                mime="application/pdf"
            )
