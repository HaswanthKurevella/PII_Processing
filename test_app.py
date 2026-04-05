import streamlit as st
from nlp_processor import NLPProcessor
from PII_analyzer import PIIanalyzer
from PII_anonymizer import PIIanonymizer

# ------------------ PAGE CONFIG ------------------ 
st.set_page_config( page_title="PII Analyzer", page_icon="🔐", layout="wide" )
# ------------------ PAGE TITILE ------------------
st.title("PII :blue[Anonymizer] :sunglasses:")
st.caption("This application detects and anonymizes Personally Identifiable Information (PII) in the input text. Enter your text below to see the results.")


# ------------------ INPUT ------------------
text = st.text_area("✍️ Enter your text here:", height=150)

# ------------------ ANALYZE BUTTON ------------------
if st.button("🔍 Analyze") :
    if text.strip() =="":
        st.warning("Please enter some text to analyze.")
    else:
         # Initialize objects
        processor = NLPProcessor()
        pii_analyzer = PIIanalyzer()
        anonymizer = PIIanonymizer()

        # NLP processing
        doc=processor.processText(text)
        tokens=processor.getTokens(doc)
        pos_tags = processor.getPosTags(doc)
        entities = processor.getEntities(doc)

        # PII detection
        pii_results = pii_analyzer.detectPII(text)
        
        # PII anonymization
        anonymized_text = anonymizer.anonymizePII(text, pii_results)
        # Display results
        st.text("step 1:Tokenization    ")
        st.write(tokens)
        st.text("step 2:POS Tagging    ")
        st.write(pos_tags)
        st.text("step 3:Named Entity Recognition    ")
        st.write(entities)
        st.text("step 4:PII Detection    ")
        st.write(pii_results)
        st.text("step 5:PII Anonymization    ")
        st.write(anonymized_text)
        
    