from json import JSONDecodeError

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import json
import os
import re
import datetime as dt
from groq import Groq
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Bizrise",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* =========================
GLOBAL STYLING
========================= */

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #020617 100%);
    color: white !important;
}

.stApp {
    background: radial-gradient(circle at top left, rgba(0,255,255,0.08), transparent 30%),
                radial-gradient(circle at bottom right, rgba(255,0,255,0.08), transparent 30%),
                linear-gradient(135deg, #0f172a 0%, #111827 50%, #020617 100%);
    color: rgba(255,255,255,0.6) !important;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* =========================
ANIMATIONS
========================= */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

@keyframes glow {
    0% {
        box-shadow: 0 0 10px rgba(0,255,255,0.2);
    }
    50% {
        box-shadow: 0 0 30px rgba(0,255,255,0.4);
    }
    100% {
        box-shadow: 0 0 10px rgba(0,255,255,0.2);
    }
}

@keyframes pulse {
    0% {transform: scale(1);}
    50% {transform: scale(1.02);}
    100% {transform: scale(1);}
}

/* =========================
HEADINGS
========================= */

.hero-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 800;
    color: white;
    margin-top: 30px;
    animation: fadeIn 1s ease-in-out;
    background: linear-gradient(90deg, #00f5ff, #9f7aea, #00f5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    text-align: center;
    font-size: 1.5rem;
    font-style: italic;
    color: #cbd5e1;
    margin-bottom: 20px;
    animation: fadeIn 1.5s ease-in-out;
}

.hero-description {
    text-align: center;
    color: #d1d5db;
    max-width: 900px;
    margin: auto;
    font-size: 1.1rem;
    line-height: 1.8;
    animation: fadeIn 2s ease-in-out;
}

/* =========================
GLASS CARDS
========================= */

.glass-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 24px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.4s ease;
    animation: fadeIn 1s ease-in-out;
}

.glass-card:hover {
    transform: translateY(-8px);
    border: 1px solid rgba(0,255,255,0.4);
    animation: glow 2s infinite;
}

/* =========================
BUTTONS
========================= */

.stButton > button {
    width: 100%;
    border-radius: 16px;
    border: none;
    padding: 0.8rem 1rem;
    background: linear-gradient(90deg, #06b6d4, #8b5cf6);
    color: white;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(0,255,255,0.4);
}

/* =========================
TEXT AREA
========================= */

textarea {
    border-radius: 20px !important;
    background: rgba(255,255,255,0.06) !important;
    color: #31333F !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    padding: 15px !important;   
}


/* =========================
DETAIL CARDS
========================= */

.detail-card {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
    border-left: 4px solid #00f5ff;
    transition: 0.3s ease;
}

.detail-card:hover {
    transform: translateX(5px);
    background: rgba(255,255,255,0.08);
}

/* =========================
SECTION TITLES
========================= */

.section-title {
    font-size: 2rem;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 20px;
    color: white;
}

/* =========================
DIVIDERS
========================= */

.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #00f5ff, transparent);
    margin: 30px 0;
}

/* =========================
SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.9);
    border-right: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.6) !important;
}

.sidebar-title {
    font-size: 2rem;
    font-weight: 800;
    color: #00f5ff;
    text-align: center;
    margin-bottom: 20px;
}

/* =========================
RESULT CONTAINER
========================= */

.result-box {
    background: rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-top: 20px;
    animation: fadeIn 1s ease;
}

/* =========================
SPINNER
========================= */

.loading-container {
    text-align: center;
    padding: 40px;
    animation: pulse 1.5s infinite;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "order_extracted" not in st.session_state:
    st.session_state.order_extracted = False
if "order_details" not in st.session_state:
    st.session_state.order_details = False

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🚀 Bizrise</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Intelligent SME Automation

    Empowering businesses with:
    - 📦 Smart Order Structuring
    - 🛡️ Fraud Detection
    - ⚡ Workflow Efficiency
    """)

    st.markdown("---")

    if st.button("🏠 Home"):
        st.session_state.page = "home"

# =========================================================
# SAMPLE PLACEHOLDER DATA
# =========================================================

sample_order_result = {
    "customer_name": "John Doe",
    "items": [
        {"item": "Rice", "quantity": 2},
        {"item": "Beans", "quantity": 5}
    ],
    "details_left": {
        "Phone": "+234-800-123-4567",
        "Location": "Lagos",
        "Delivery": "Express",
        "Payment": "Paid"
    },
    "details_right": {
        "Order ID": "BR-2026-101",
        "Priority": "High",
        "Status": "Processing",
        "Agent": "Sarah"
    }
}

sample_fraud_result = {
    "risk_level": "High",
    "scam_type": "Phishing",
    "red_flags": [
        "Urgent payment request",
        "Suspicious link",
        "Grammar inconsistencies"
    ],
    "explanation": "This message contains several indicators commonly associated with phishing scams.",
    "recommended_action": "Do not click links or send money.",
    "confidence_score": 87
}

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def back_button():
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

def send_email(email):
    if st.button("Send Email"):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email) is not None:
            st.error(f'Error: Invalid email.', icon="🚨")
            st.stop()
        data = st.session_state.order_details

        mail_sender = "ebifredrick07@gmail.com"
        PASSWORD = os.getenv("PWORD")
        msg_subject = "New Customer Order for Processing – Structured Details Attached"
        order_items = data["order_items"]
        # msg_body = msg[1]

        with open("email.txt", mode="r") as email_file:
            email_content = email_file.read()
        date = dt.datetime.now()
        f_date = date.strftime("%H:%M | %b %d, %Y.")
        email_content = email_content.replace("{{Date}}", f_date)
        email_content = email_content.replace("{{customer_name}}", str(data["customer_name"]))
        for i in range(len(order_items)):
            the_new = f"{order_items[i]['item']} — Quantity: {order_items[i]['quantity']}"
            if i != len(order_items)-1:
                the_new += "\n{{#each order_items}}"
            email_content = email_content.replace(
                "{{#each order_items}}",
                the_new
            )
        details_left = data["details_left"]
        email_content = email_content.replace("{{delivery_date}}", str(details_left["delivery_date"]))
        email_content = email_content.replace("{{payment_status}}", str(details_left["payment_status"]))
        email_content = email_content.replace("{{priority_level}}", str(details_left["priority_level"]))
        details_right = data["details_right"]
        email_content = email_content.replace("{{customer_phone}}", str(details_right["customer_phone"]))
        email_content = email_content.replace("{{delivery_location}}", str(details_right["delivery_location"]))
        email_content = email_content.replace("{{special_instructions}}", str(details_right["special_instructions"]))

        # 4. Send the letter generated in step 3 to that person's email address.
        message = EmailMessage()
        message["From"] = f"BizRise <{mail_sender}>"
        message["To"] = email
        message["Subject"] = msg_subject
        message.add_alternative(email_content, subtype='html')
        message.add_header("Reply-to", "ebifredrick07@gmail.com")

        context = ssl.create_default_context()
        # breaks = 0
        while True:
            try:
                with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as mail:
                    mail.login(user=mail_sender, password=PASSWORD)
                    mail.sendmail(from_addr=mail_sender, to_addrs=email, msg=message.as_string())
            except smtplib.SMTPConnectError as f:
                print("error as", f)
            except smtplib.SMTPException as e:
                print("Encountered smtp error :", e)
                break
            # except socket.gaierror as e:
            #     print("there is an error:", e)
            #     breaks += 1
            #     time.sleep(3)
            #     if breaks > 4:
            #         # error404()
            #         break
            else:
                break
        st.rerun()

def render_divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def render_loading(text):
    st.markdown(f"""
    <div class="loading-container">
        <h3>{text}</h3>
    </div>
    """, unsafe_allow_html=True)

def render_confidence_gauge(score, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#10b981'},
                {'range': [40, 70], 'color': '#facc15'},
                {'range': [70, 100], 'color': '#ef4444'}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# LANDING PAGE
# =========================================================

def analyze(form: str, message: str):
    filenames = {"product1": "prompt.txt", "product2": "prompt2.txt"}
    form = form.lower()
    if form != "product1" and form != "product2":
        return False

    with open(filenames[form], mode="r") as f:
        prompt = f.read()
    prompt = prompt.replace("{conversation_text}", message)
    # print(prompt)
    client = Groq()
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
        stop=None,
    )
    response = ""
    for i, chunk in enumerate(completion):
        response += chunk.choices[0].delta.content or ""
    response = None if response == "" else response
    try:
        return json.loads(response)
    except JSONDecodeError:
        print("DecodeError", response)
        return [{"failed": response}]

def landing_page():

    st.markdown("""
    <div class="hero-title">
        Welcome to Bizrise!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-subtitle">
        Your ultimate SME solution
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-description">
        Bizrise helps businesses scale using intelligent automation and modern digital tools.
        Streamline operations, improve efficiency, and make smarter decisions with AI-powered systems built for modern SMEs.
        <br><br>
        🚀 Convert chaotic WhatsApp customer chats into structured order data automatically.<br>
        🛡️ Detect suspicious messages and estimate scam likelihood with advanced fraud intelligence.
    </div>
    """, unsafe_allow_html=True)

    render_divider()

    col1, col2 = st.columns(2)

    # =========================
    # CARD 1
    # =========================
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h2>📦 Smart Order Extractor</h2>
            <p>
                Transform messy WhatsApp conversations into organized, actionable business orders instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Launch Tool"):
            st.session_state.page = "order"

    # =========================
    # CARD 2
    # =========================
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h2>🛡️ Scam Detection System</h2>
            <p>
                Detect suspicious messages, phishing attempts, and scam patterns before they become costly.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Analyze Messages"):
            st.session_state.page = "fraud"

# =========================================================
# ORDER EXTRACTION PAGE
# =========================================================

def order_extraction_page():

    st.markdown("""
    <div class="section-title">
        📦 WhatsApp Order Extraction Tool
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        Paste WhatsApp customer conversations below to simulate intelligent order extraction.
    </div>
    """, unsafe_allow_html=True)

    render_divider()

    whatsapp_input = st.text_area(
        "Paste WhatsApp Messages",
        height=250,
        placeholder="""
Customer: Hi, I need 2 bags of rice and 5 packs of beans.
Customer: Please deliver tomorrow morning.
Customer: My address is Lekki Phase 1...
        """
    )

    # Placeholder for future AI logic
    # =====================================================
    # REAL AI EXTRACTION LOGIC WILL BE INSERTED HERE LATER
    # =====================================================

    if st.button("Extract Order"):

        render_loading("🔄 Extracting structured order data...")
        time.sleep(2)

        render_divider()
        if not whatsapp_input:
            st.rerun()
        order_result = analyze("product1", whatsapp_input)
        order_result = order_result[0]
        if order_result.get("failed"):
            st.error(f'Error: {order_result.get("failed")}', icon="🚨")
            st.stop()
        st.session_state.order_details = order_result

        print("hello there:", order_result, ":end")
        st.markdown(f"""
        <h2 style='text-decoration: underline;'>
            {order_result['customer_name']}'s Order Details
        </h2>
        """, unsafe_allow_html=True)

        # TABLE
        df = pd.DataFrame(order_result["order_items"])
        df.columns = ["Item", "Quantity"]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        render_divider()

        left_col, right_col = st.columns(2)

        # LEFT DETAILS
        with left_col:
            for key, value in order_result["details_left"].items():
                st.markdown(f"""
                <div class="detail-card">
                    <strong>{key}</strong><br>
                    {value}
                </div>
                """, unsafe_allow_html=True)

        # RIGHT DETAILS
        with right_col:
            for key, value in order_result["details_right"].items():
                st.markdown(f"""
                <div class="detail-card">
                    <strong>{key}</strong><br>
                    {value}
                </div>
                """, unsafe_allow_html=True)
        st.session_state.order_extracted = True

    render_divider()
    st.markdown(f"""
            <h4 style='text-decoration: underline;'>
                Send order details to order processing team.
            </h4>
            """, unsafe_allow_html=True)
    title = st.text_input(label="",
                          placeholder="Put in your Order team email...",
                          value="",
                          disabled=not st.session_state.order_extracted)
    send_email(title)
    render_divider()
    back_button()

# =========================================================
# FRAUD DETECTION PAGE
# =========================================================

def fraud_detection_page():

    st.markdown("""
    <div class="section-title">
        🛡️ Scam Detection System
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        Analyze suspicious-looking messages and estimate scam likelihood with futuristic fraud intelligence.
    </div>
    """, unsafe_allow_html=True)

    render_divider()

    fraud_input = st.text_area(
        "Paste Suspicious Message",
        height=250,
        placeholder="""
URGENT: Your bank account has been compromised.
Click this link immediately to verify your identity and avoid suspension...
        """
    )

    # Placeholder for future AI fraud analysis
    # =====================================================
    # REAL FRAUD DETECTION AI LOGIC WILL BE INSERTED HERE
    # =====================================================

    if st.button("Analyze Risk"):

        render_loading("🧠 Running fraud intelligence analysis...")
        time.sleep(4)

        render_divider()

        if not fraud_input:
            st.rerun()
        fraud_result = analyze("product2", fraud_input)
        # fraud_result = fraud_result[0]
        if fraud_result.get("failed"):
            st.error(f'Error: {fraud_result.get("failed")}', icon="🚨")
            st.stop()

        submitted_preview = fraud_input[:100] if fraud_input else "No message provided."

        st.markdown("""
        <div class="result-box">
            <h4>Submitted Message Preview</h4>
        </div>
        """, unsafe_allow_html=True)

        st.code(submitted_preview, language="text")

        risk_level = fraud_result["risk_level"]

        if risk_level == "Safe":
            risk_color = "#10b981"
        elif risk_level == "Suspicious":
            risk_color = "#facc15"
        elif risk_level == "High Risk":
            risk_color = "#EC6D0C"
        else:
            risk_color = "#B71C1C" #"#ef4444"

        # RESULT DETAILS
        st.markdown(f"""
        <div class="glass-card">
            <h2 style="color:{risk_color};">
                ⚠ Risk Level: {fraud_result['risk_level']}
            </h2>

        <div>
            <strong>Scam Type:</strong>
            {fraud_result['scam_type']}
        </div>
    
        <br>
    
        <div>
            <strong>Explanation:</strong><br>
            {fraud_result['explanation']}
        </div>
    
        <br>
    
        <div>
            <strong>Recommended Action:</strong><br>
            {fraud_result['recommended_action']}
        </div>
        </div>
        """, unsafe_allow_html=True)

        render_divider()

        st.markdown("### 🚨 Red Flags")

        for flag in fraud_result["red_flags"]:
            st.markdown(f"""
            <div class="detail-card">
                ❌ {flag}
            </div>
            """, unsafe_allow_html=True)

        render_divider()

        st.markdown("### 📊 Confidence Score")

        render_confidence_gauge(
            fraud_result["confidence_score"],
            risk_color
        )

    render_divider()
    back_button()

# =========================================================
# ROUTER
# =========================================================

if st.session_state.page == "home":
    landing_page()

elif st.session_state.page == "order":
    order_extraction_page()

elif st.session_state.page == "fraud":
    fraud_detection_page()