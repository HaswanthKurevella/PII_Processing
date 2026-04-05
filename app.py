import streamlit as st
from nlp_processor import NLPProcessor
from PII_analyzer import PIIanalyzer
from PII_anonymizer import PIIanonymizer

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PII Anonymizer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global font & background ── */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Sora:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }

    /* ── Hero header ── */
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f4c81 100%);
        border-radius: 16px;
        padding: 2.5rem 2.5rem 2rem;
        margin-bottom: 1.8rem;
        border: 1px solid #1e40af33;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: "🔐";
        position: absolute;
        right: 2rem; top: 50%;
        transform: translateY(-50%);
        font-size: 6rem;
        opacity: 0.07;
    }
    .hero h1 {
        color: #f8fafc;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.4rem;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0;
    }
    .hero .badge {
        display: inline-block;
        background: #1d4ed8;
        color: #bfdbfe;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 99px;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* ── Step cards ── */
    .step-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.6rem;
    }
    .step-num {
        background: #1d4ed8;
        color: white;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        width: 28px; height: 28px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .step-title {
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    /* ── Result box ── */
    .result-box {
        background: #0f172a;
        border: 1px solid #1e40af55;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #e2e8f0;
        line-height: 1.7;
        word-break: break-word;
    }
    .result-box .redacted {
        background: #dc2626;
        color: white;
        border-radius: 4px;
        padding: 1px 6px;
        font-weight: 600;
        font-size: 0.82rem;
    }

    /* ── PII type pill colors ── */
    .pii-pill {
        display: inline-block;
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 0.78rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        margin: 2px;
    }
    .pill-PERSON      { background:#1e3a5f; color:#93c5fd; border:1px solid #1d4ed8; }
    .pill-ORG         { background:#1a3a2a; color:#86efac; border:1px solid #16a34a; }
    .pill-PHONE_NUMBER{ background:#3b1f5e; color:#d8b4fe; border:1px solid #7c3aed; }
    .pill-EMAIL       { background:#1e3a5f; color:#93c5fd; border:1px solid #2563eb; }
    .pill-DATE_TIME   { background:#3b2a0e; color:#fcd34d; border:1px solid #d97706; }
    .pill-NRP         { background:#3b1a1a; color:#fca5a5; border:1px solid #dc2626; }
    .pill-DEFAULT     { background:#1e293b; color:#94a3b8; border:1px solid #334155; }

    /* ── Score bar ── */
    .score-bar-bg {
        background: #1e293b;
        border-radius: 99px;
        height: 6px;
        width: 100%;
        margin-top: 4px;
    }
    .score-bar-fill {
        height: 6px;
        border-radius: 99px;
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
    }

    /* ── Divider ── */
    .section-divider {
        border: none;
        border-top: 1px solid #1e293b;
        margin: 1.4rem 0;
    }

    /* ── Summary metrics ── */
    .metric-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-card .metric-label {
        font-size: 0.78rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }

    /* hide streamlit branding */
    /*#MainMenu, footer { visibility: hidden; }*/
    footer { visibility: hidden; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">NLP · Privacy · Security</div>
    <h1>PII Anonymizer</h1>
    <p>Detects and redacts Personally Identifiable Information using tokenization,
    POS tagging, named-entity recognition, and pattern-based analysis.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT SECTION
# ─────────────────────────────────────────────
col_input, col_gap = st.columns([3, 1])
with col_input:
    text = st.text_area(
        "✍️ Paste or type your text below",
        height=120,
        placeholder="e.g. My name is John Doe and my phone number is 9876543210...",
    )

col_btn, col_clear, _ = st.columns([1, 1, 5])
with col_btn:
    analyze = st.button("Analyze", type="primary", use_container_width=True)
with col_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()

# ─────────────────────────────────────────────
#  HELPER: pill HTML
# ─────────────────────────────────────────────
def pill(label: str) -> str:
    known = {"PERSON", "ORG", "PHONE_NUMBER", "EMAIL", "DATE_TIME", "NRP"}
    css = f"pill-{label}" if label in known else "pill-DEFAULT"
    return f'<span class="pii-pill {css}">{label}</span>'

# ─────────────────────────────────────────────
#  ANALYSIS
# ─────────────────────────────────────────────
if analyze:
    if not text.strip():
        st.warning("⚠️ Please enter some text before analyzing.")
    else:
        with st.spinner("Running NLP pipeline…"):
            processor   = NLPProcessor()
            pii_analyzer = PIIanalyzer()
            anonymizer  = PIIanonymizer()

            doc        = processor.processText(text)
            tokens     = processor.getTokens(doc)
            pos_tags   = processor.getPosTags(doc)
            entities   = processor.getEntities(doc)
            pii_results = pii_analyzer.detectPII(text)
            anonymized  = anonymizer.anonymizePII(text, pii_results)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── SUMMARY METRICS ────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{len(tokens)}</div>
                <div class="metric-label">Tokens</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{len(entities)}</div>
                <div class="metric-label">Entities</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{len(pii_results)}</div>
                <div class="metric-label">PII Hits</div></div>""", unsafe_allow_html=True)
        with m4:
            high_conf = sum(1 for r in pii_results if getattr(r, "score", 0) >= 0.75)
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{high_conf}</div>
                <div class="metric-label">High-Confidence</div></div>""", unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── PIPELINE STEPS ─────────────────────────
        left, right = st.columns(2, gap="large")

        # STEP 1 – Tokenization
        with left:
            st.markdown("""
            <div class="step-header">
                <div class="step-num">1</div>
                <div class="step-title">Tokenization</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("View tokens", expanded=False):
                token_html = " ".join(
                    f'<code style="background:#1e293b;color:#7dd3fc;border-radius:4px;'
                    f'padding:2px 7px;margin:2px;display:inline-block;font-family:JetBrains Mono,monospace;'
                    f'font-size:0.82rem;">{t}</code>'
                    for t in tokens
                )
                st.markdown(token_html, unsafe_allow_html=True)

        # STEP 2 – POS Tagging
        with right:
            st.markdown("""
            <div class="step-header">
                <div class="step-num">2</div>
                <div class="step-title">POS Tagging</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("View POS tags", expanded=False):
                pos_colors = {
                    "NOUN": "#86efac", "PROPN": "#38bdf8", "VERB": "#fbbf24",
                    "PRON": "#d8b4fe", "AUX": "#f9a8d4", "NUM": "#fb923c",
                    "ADP": "#94a3b8", "CCONJ": "#94a3b8", "ADJ": "#6ee7b7",
                }
                rows = "".join(
                    f'<tr style="border-bottom:1px solid #1e293b">'
                    f'<td style="padding:4px 10px;color:#e2e8f0;font-family:JetBrains Mono,monospace;font-size:0.82rem;">{tag[0]}</td>'
                    f'<td style="padding:4px 10px;"><span style="color:{pos_colors.get(tag[1],"#94a3b8")};font-size:0.78rem;font-weight:600;">{tag[1]}</span></td>'
                    f'</tr>'
                    for tag in pos_tags if tag[0].strip()
                )
                st.markdown(
                    f'<table style="width:100%;border-collapse:collapse;">{rows}</table>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        left2, right2 = st.columns(2, gap="large")

        # STEP 3 – NER
        with left2:
            st.markdown("""
            <div class="step-header">
                <div class="step-num">3</div>
                <div class="step-title">Named Entity Recognition</div>
            </div>""", unsafe_allow_html=True)
            if entities:
                for ent in entities:
                    text_val, label = ent[0], ent[1]
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:0.6rem;'
                        f'padding:6px 10px;background:#0f172a;border-radius:8px;margin-bottom:6px;">'
                        f'<span style="color:#e2e8f0;font-family:JetBrains Mono,monospace;font-size:0.85rem;">{text_val}</span>'
                        f'<span style="margin-left:auto">{pill(label)}</span></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No named entities found.")

        # STEP 4 – PII Detection
        with right2:
            st.markdown("""
            <div class="step-header">
                <div class="step-num">4</div>
                <div class="step-title">PII Detection</div>
            </div>""", unsafe_allow_html=True)
            if pii_results:
                for item in pii_results:
                    # Support both string representations and object attributes
                    if hasattr(item, "entity_type"):
                        etype  = item.entity_type
                        score  = item.score
                        start  = item.start
                        end    = item.end
                    else:
                        parts  = str(item).split(",")
                        etype  = parts[0].split(":")[-1].strip() if parts else "UNKNOWN"
                        score  = float(parts[-1].split(":")[-1].strip()) if len(parts) > 3 else 0.0
                        start  = int(parts[1].split(":")[-1].strip()) if len(parts) > 1 else 0
                        end    = int(parts[2].split(":")[-1].strip()) if len(parts) > 2 else 0

                    pct = int(score * 100)
                    bar_color = "#22c55e" if pct >= 75 else "#f59e0b" if pct >= 40 else "#ef4444"
                    snippet   = text[start:end] if start < len(text) and end <= len(text) else ""

                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;
                                padding:10px 14px;margin-bottom:8px;">
                        <div style="display:flex;align-items:center;justify-content:space-between;">
                            {pill(etype)}
                            <span style="font-family:JetBrains Mono,monospace;font-size:0.8rem;
                                         color:{bar_color};font-weight:600;">{pct}%</span>
                        </div>
                        <div style="font-family:JetBrains Mono,monospace;font-size:0.78rem;
                                    color:#64748b;margin-top:6px;">
                            pos {start}–{end}
                            {"· <em>" + snippet + "</em>" if snippet else ""}
                        </div>
                        <div class="score-bar-bg">
                            <div class="score-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{bar_color},{bar_color}99);"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("✅ No PII detected.")

        # ── STEP 5 – Anonymized Output ─────────────────
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="step-header">
            <div class="step-num">5</div>
            <div class="step-title">Anonymized Output</div>
        </div>""", unsafe_allow_html=True)

        # Highlight redacted tokens visually
        import re
        highlighted = re.sub(
            r"<([^>]+)>",
            lambda m: f'<span class="redacted">&lt;{m.group(1)}&gt;</span>',
            str(anonymized),
        )
        st.markdown(
            f'<div class="result-box">{highlighted}</div>',
            unsafe_allow_html=True,
        )

        col_dl, _ = st.columns([1, 4])
        with col_dl:
            st.download_button(
                "⬇️ Download anonymized text",
                data=str(anonymized),
                file_name="anonymized_output.txt",
                mime="text/plain",
                use_container_width=True,
            )