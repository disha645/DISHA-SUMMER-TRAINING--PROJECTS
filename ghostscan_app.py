import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageChops, ImageEnhance
import io

# ---------------------------------------------------------
# Page Configuration & Forensic Dark Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="GhostScan | Border Forensics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    .status-badge {
        padding: 14px;
        border-radius: 8px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 12px;
    }
    .status-danger {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid #ef4444;
    }
    .status-success {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Forensic Inspection Functions
# ---------------------------------------------------------
def generate_synthetic_passport(name, doc_no, dob_text, tamper_mode=None):
    """Draws a synthetic identity document canvas."""
    img = np.ones((340, 520, 3), dtype=np.uint8) * 32

    # Outer border & header
    cv2.rectangle(img, (10, 10), (510, 330), (70, 80, 95), 2)
    cv2.putText(img, "REPUBLIC OF KALDORIA - TRAVEL DOCUMENT", (25, 38), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 175, 200), 1)
    cv2.line(img, (15, 50), (505, 50), (60, 70, 85), 1)

    # ID Photo box
    cv2.rectangle(img, (30, 70), (160, 230), (55, 65, 80), -1)
    cv2.putText(img, "ID PHOTO", (60, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (130, 140, 160), 1)

    # Visual OCR Fields
    cv2.putText(img, "SURNAME / GIVEN", (180, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (120, 130, 150), 1)
    cv2.putText(img, name, (180, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (235, 240, 250), 1)

    cv2.putText(img, "DOCUMENT NO.", (180, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (120, 130, 150), 1)
    cv2.putText(img, doc_no, (180, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 215, 255), 1)

    cv2.putText(img, "DATE OF BIRTH", (180, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (120, 130, 150), 1)
    cv2.putText(img, dob_text, (180, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (235, 240, 250), 1)

    # Machine Readable Zone (MRZ)
    cv2.rectangle(img, (20, 250), (500, 315), (15, 20, 28), -1)
    cv2.rectangle(img, (20, 250), (500, 315), (45, 55, 70), 1)
    mrz_line1 = f"P<UTOPETROV<<{name.replace(' ', '<')}<<<<<<<<<<<<<<<<<<<<"[:44]
    mrz_line2 = f"{doc_no}<8UTO9403125M2911190<<<<<<<<<<<<<<<<<0"[:44]
    cv2.putText(img, mrz_line1, (30, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (120, 210, 170), 1)
    cv2.putText(img, mrz_line2, (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (120, 210, 170), 1)

    # Tamper simulation artifacts
    if tamper_mode == "dob":
        noise = np.random.randint(40, 230, (30, 120, 3), dtype=np.uint8)
        img[185:215, 180:300] = noise
    elif tamper_mode == "photo":
        noise = np.random.randint(60, 210, (150, 120, 3), dtype=np.uint8)
        img[75:225, 35:155] = noise

    return Image.fromarray(img)

def run_ela(image: Image.Image, quality=90, scale_factor=20):
    """Computes Error Level Analysis (ELA) to highlight digital alterations."""
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, "JPEG", quality=quality)
    buffer.seek(0)
    resaved = Image.open(buffer)

    diff = ImageChops.difference(image.convert("RGB"), resaved)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1
    multiplier = (255.0 / max_diff) * (scale_factor / 15.0)
    return ImageEnhance.Brightness(diff).enhance(multiplier)

# ---------------------------------------------------------
# Sidebar Scenario Controls
# ---------------------------------------------------------
with st.sidebar:
    st.title("🛡️ GhostScan AI")
    st.caption("Automated Identity Screening | Terminal 3")

    preset = st.selectbox(
        "Active Inspection Scenario",
        [
            "Scenario A: Altered DOB (Forgery)",
            "Scenario B: Clear Passport (Authentic)",
            "Scenario C: Replaced Photo (Identity Swap)"
        ]
    )

    uploaded_doc = st.file_uploader("Or Upload Real Document", type=["jpg", "png", "jpeg"])
    ela_res = st.slider("ELA Filter Sensitivity", 5, 40, 20)

    st.divider()
    st.markdown("**Officer:** J. Miller (ID: 8841)")
    st.markdown("**Lane:** Automated E-Gate #04")

# Load scenario dataset
if "Scenario A" in preset:
    doc_name = "ALEXEI V. PETROV"
    doc_no = "P89210488"
    ocr_dob = "12 MAR 1982"
    mrz_dob = "12 MAR 1994"
    tamper_mode = "dob"
    face_score = 96.2
    interpol_hit = False
elif "Scenario B" in preset:
    doc_name = "SARAH CHEN"
    doc_no = "D44901923"
    ocr_dob = "04 AUG 1991"
    mrz_dob = "04 AUG 1991"
    tamper_mode = None
    face_score = 98.9
    interpol_hit = False
else:
    doc_name = "MARCUS D. VANCE"
    doc_no = "V00293112"
    ocr_dob = "29 JUN 1978"
    mrz_dob = "29 JUN 1978"
    tamper_mode = "photo"
    face_score = 41.2
    interpol_hit = True

# Composite Risk Score calculation
risk_score = 5
if ocr_dob != mrz_dob: risk_score += 40
if tamper_mode is not None: risk_score += 35
if face_score < 75.0: risk_score += 45
if interpol_hit: risk_score += 50
risk_score = min(risk_score, 99)

# ---------------------------------------------------------
# Dashboard Grid Layout
# ---------------------------------------------------------
col_view, col_extract, col_decision = st.columns([5, 4, 3])

# --- Column 1: Document Viewport & Forensics ---
with col_view:
    st.subheader("1. Forensic Image Viewer")
    view_tab = st.radio("Active Inspection Layer", ["Standard White Light", "ELA Heatmap Overlay"], horizontal=True)

    base_img = Image.open(uploaded_doc) if uploaded_doc else generate_synthetic_passport(doc_name, doc_no, ocr_dob, tamper_mode)

    if view_tab == "Standard White Light":
        st.image(base_img, use_container_width=True, caption="Visible Light Spectrum")
    else:
        ela_img = run_ela(base_img, scale_factor=ela_res)
        st.image(ela_img, use_container_width=True, caption="Error Level Analysis (Tamper Signal)")

    if tamper_mode == "dob":
        st.error("⚠️ Forensic Flag: Localized compression discontinuity detected in Date of Birth field.")
    elif tamper_mode == "photo":
        st.error("⚠️ Forensic Flag: Substrate seam anomaly detected on primary photo substrate.")
    else:
        st.success("✓ Forensic Check: Uniform compression across entire document boundary.")

# --- Column 2: Data Integrity & Biometrics ---
with col_extract:
    st.subheader("2. Field Verification")

    st.markdown("**OCR vs. MRZ Cross-Check**")
    st.table({
        "Field": ["Holder", "Document No.", "DOB (Visual OCR)", "DOB (MRZ)"],
        "Extracted": [doc_name, doc_no, ocr_dob, mrz_dob],
        "Status": ["VALID", "VALID", "MISMATCH" if ocr_dob != mrz_dob else "VALID", "VALID"]
    })

    st.markdown("**Security Database Verification**")
    m1, m2 = st.columns(2)
    with m1:
        st.metric("ICAO Checksum", "FAIL" if ocr_dob != mrz_dob else "PASS")
    with m2:
        st.metric("Interpol SLTD", "FLAGGED" if interpol_hit else "CLEAR")

    st.markdown("**Biometric Face Verification**")
    st.progress(face_score / 100.0, text=f"Biometric Match Confidence: {face_score}%")

# --- Column 3: Decision Engine & Actions ---
with col_decision:
    st.subheader("3. Triage Verdict")

    if risk_score > 60:
        st.markdown(f"""
        <div class="status-badge status-danger">
            <h1 style="margin:0; font-size:42px;">{risk_score}%</h1>
            <h3 style="margin:4px 0;">CRITICAL THREAT</h3>
            <span style="font-size:12px;">SUSPECTED FORGERY / IMPERSONATION</span>
        </div>
        """, unsafe_allow_html=True)
        st.warning("Action Required: Divert passenger immediately to Secondary Search Booth.")
        if st.button("Divert to Secondary [F2]", type="primary", use_container_width=True):
            st.toast("Alert dispatched to Secondary Screening unit.")
    else:
        st.markdown(f"""
        <div class="status-badge status-success">
            <h1 style="margin:0; font-size:42px;">{risk_score}%</h1>
            <h3 style="margin:4px 0;">CLEARED</h3>
            <span style="font-size:12px;">ALL INTEGRITY CHECKS PASSED</span>
        </div>
        """, unsafe_allow_html=True)
        st.success("Action Required: Permit automated entry gate passage.")
        if st.button("Clear & Open Gate [F1]", type="secondary", use_container_width=True):
            st.toast("Passage cleared. Audit record committed.")
