#!/usr/bin/env python3
"""
Mutual Fund FAQ Assistant - Streamlit App
Modern, minimalist UI for mutual fund FAQs
"""

import streamlit as st

st.set_page_config(
    page_title="MF FAQ Assistant",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern minimalist design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #fafafa;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    
    .logo {
        font-size: 14px;
        font-weight: 500;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .title {
        font-size: 32px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 15px;
    }
    
    .disclaimer {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        font-size: 12px;
        font-weight: 500;
        padding: 6px 12px;
        border-radius: 20px;
        margin-top: 12px;
    }
    
    .answer-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .answer-question {
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 16px;
    }
    
    .answer-content {
        color: #4b5563;
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-line;
    }
    
    .source-section {
        margin-top: 20px;
        padding-top: 16px;
        border-top: 1px solid #e5e7eb;
    }
    
    .source-label {
        font-size: 12px;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 400;
        color: #1a1a1a;
        transition: all 0.15s ease;
    }
    
    .stButton > button:hover {
        border-color: #2563eb;
        background: #eff6ff;
        color: #2563eb;
    }
    
    div[data-testid="stTextInput"] > div > div > input {
        font-size: 16px;
        padding: 16px 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: white;
    }
    
    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px #eff6ff;
    }
    
    .footer {
        text-align: center;
        margin-top: 60px;
        padding-top: 24px;
        border-top: 1px solid #e5e7eb;
        color: #6b7280;
        font-size: 13px;
    }
    
    .footer a {
        color: #2563eb;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

FAQ_DATABASE = [
    {
        "id": 1,
        "keywords": ["expense ratio", "expense", "ter", "total expense ratio", "fees", "charges"],
        "question": "What is expense ratio in mutual funds?",
        "answer": """Expense Ratio (Total Expense Ratio - TER) is the annual fee charged by mutual funds to manage your investments. It includes fund management fees, administrative costs, and distribution expenses. SEBI has capped the maximum TER based on AUM:

• Equity schemes: 2.25% for first ₹500 crore, reducing progressively
• Debt schemes: 2.00% for first ₹500 crore, reducing progressively
• Index funds/ETFs: Maximum 1.00%

The expense ratio is deducted daily from the fund's NAV.""",
        "source": "https://www.sebi.gov.in/legal/circulars/sep-2018/circular-on-total-expense-ratio-ter-and-performance-disclosure-for-mutual-funds_40456.html",
        "source_name": "SEBI Circular"
    },
    {
        "id": 2,
        "keywords": ["exit load", "exit", "redemption charge", "withdrawal charge", "sell"],
        "question": "What is exit load in mutual funds?",
        "answer": """Exit load is a fee charged when you redeem (sell) mutual fund units before a specified period. Common exit load structures:

• Equity funds: Typically 1% if redeemed within 1 year
• Liquid funds: Usually nil or graded (up to 7 days)
• ELSS funds: No exit load (but 3-year lock-in applies)
• Overnight funds: Nil

Exit load is deducted from the redemption NAV. Always check the Scheme Information Document (SID) for exact exit load details.""",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/exit-load.html",
        "source_name": "AMFI India"
    },
    {
        "id": 3,
        "keywords": ["minimum sip", "sip amount", "sip minimum", "systematic investment", "monthly investment"],
        "question": "What is the minimum SIP amount?",
        "answer": """Minimum SIP (Systematic Investment Plan) amounts vary by fund house and scheme:

• Most funds: ₹500 per month minimum
• Some funds: ₹100 per month (micro-SIP)
• Premium/specialized funds: ₹1,000 - ₹5,000

SIP frequency options include monthly, weekly, daily, or quarterly. Check the specific scheme's SID or the AMC website for exact minimum amounts.""",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/sip.html",
        "source_name": "AMFI India"
    },
    {
        "id": 4,
        "keywords": ["lock-in", "lockin", "elss", "tax saving", "80c", "tax benefit"],
        "question": "What is the lock-in period for ELSS funds?",
        "answer": """ELSS (Equity Linked Savings Scheme) has a mandatory lock-in period of 3 years from the date of each investment. Key points:

• Lock-in: 3 years (shortest among Section 80C instruments)
• Tax benefit: Up to ₹1.5 lakh deduction under Section 80C
• Each SIP installment has its own 3-year lock-in
• No premature withdrawal allowed during lock-in
• After lock-in, units can be redeemed freely (no exit load)

LTCG tax applies: 12.5% on gains exceeding ₹1.25 lakh per year.""",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/tax-planning-through-elss.html",
        "source_name": "AMFI India"
    },
    {
        "id": 5,
        "keywords": ["riskometer", "risk", "risk level", "risk category", "risk meter"],
        "question": "What is a riskometer in mutual funds?",
        "answer": """Riskometer is a visual risk indicator mandated by SEBI that shows a mutual fund's risk level. It has 6 categories:

1. Low - Principal at low risk (liquid, overnight funds)
2. Low to Moderate - Principal at low to moderate risk
3. Moderate - Principal at moderate risk
4. Moderately High - Principal at moderately high risk
5. High - Principal at high risk (equity funds)
6. Very High - Principal at very high risk (sectoral, thematic funds)

The riskometer must be displayed in all scheme documents and advertisements. It is reviewed monthly.""",
        "source": "https://www.sebi.gov.in/legal/circulars/oct-2020/circular-on-product-labeling-in-mutual-funds-riskometer_47796.html",
        "source_name": "SEBI Circular"
    },
    {
        "id": 6,
        "keywords": ["benchmark", "index", "comparison", "nifty", "sensex", "performance"],
        "question": "What is a benchmark in mutual funds?",
        "answer": """A benchmark is a standard index against which a mutual fund's performance is measured. Common benchmarks:

• Large cap funds: Nifty 50, BSE Sensex
• Mid cap funds: Nifty Midcap 150
• Small cap funds: Nifty Smallcap 250
• Flexi cap funds: Nifty 500
• Debt funds: CRISIL indices, Nifty bond indices

SEBI mandates funds to declare a Tier 1 benchmark (broad market index) and optionally a Tier 2 benchmark. Performance comparison with benchmark must be shown in factsheets.""",
        "source": "https://www.sebi.gov.in/legal/circulars/jan-2022/circular-on-benchmarking-of-scheme-s-performance-to-total-return-index_55270.html",
        "source_name": "SEBI Circular"
    },
    {
        "id": 7,
        "keywords": ["statement", "download", "cas", "account statement", "portfolio", "holdings"],
        "question": "How do I download my mutual fund statement?",
        "answer": """You can download your Consolidated Account Statement (CAS) through these official methods:

1. CAMS/KFintech - Visit the registrar's website
2. MF Central (AMFI portal) - Single source for all funds
3. Individual AMC websites - Login to your folio
4. Email request - Send email to cams@camsonline.com or mfs@kfintech.com with PAN

MF Central is recommended as it provides a single consolidated view of all your mutual fund holdings across all AMCs.""",
        "source": "https://www.mfcentral.com/",
        "source_name": "MF Central"
    },
    {
        "id": 8,
        "keywords": ["nav", "net asset value", "price", "unit price", "value"],
        "question": "What is NAV in mutual funds?",
        "answer": """NAV (Net Asset Value) is the per-unit market value of a mutual fund scheme. It is calculated as:

NAV = (Total Assets - Total Liabilities) / Number of Units Outstanding

Key points:
• NAV is declared daily (except holidays)
• Cut-off time: 3 PM for equity funds, 1:30 PM for liquid funds
• NAV is published on AMFI website by 11 PM daily
• Purchase/redemption happens at applicable NAV based on cut-off time""",
        "source": "https://www.amfiindia.com/nav-history-download",
        "source_name": "AMFI India"
    },
    {
        "id": 9,
        "keywords": ["kyc", "know your customer", "verification", "pan", "documents"],
        "question": "What is KYC for mutual funds?",
        "answer": """KYC (Know Your Customer) is a one-time verification mandatory for mutual fund investments. Requirements:

• PAN card (mandatory)
• Address proof (Aadhaar, passport, etc.)
• Photograph
• In-Person Verification (IPV)

You can complete KYC through:
1. KRA agencies (CAMS KRA, KFintech, CVL)
2. Online eKYC using Aadhaar
3. Through AMC or distributor

Once KYC is done with one KRA, it's valid across all mutual funds.""",
        "source": "https://www.camskra.com/",
        "source_name": "CAMS KRA"
    },
    {
        "id": 10,
        "keywords": ["aum", "assets under management", "fund size", "corpus"],
        "question": "What is AUM in mutual funds?",
        "answer": """AUM (Assets Under Management) is the total market value of all investments managed by a mutual fund scheme. Key points:

• Higher AUM generally indicates investor confidence
• Very large AUM in small/mid cap funds may impact performance
• AUM affects expense ratio (larger funds have lower TER)
• Industry AUM data is published monthly by AMFI

Check the monthly AMFI data for scheme-wise and AMC-wise AUM figures.""",
        "source": "https://www.amfiindia.com/research-information/aum-data",
        "source_name": "AMFI India"
    }
]


def find_answer(query: str):
    """Find the best matching FAQ for the given query."""
    query_lower = query.lower().strip()
    
    if not query_lower:
        return None
    
    best_match = None
    best_score = 0
    
    for faq in FAQ_DATABASE:
        score = 0
        for keyword in faq["keywords"]:
            if keyword in query_lower:
                score += len(keyword)
        
        if score > best_score:
            best_score = score
            best_match = faq
    
    return best_match if best_score > 0 else None


# Header
st.markdown("""
<div class="main-header">
    <div class="logo">MF FAQ</div>
    <div class="title">Mutual Fund FAQ Assistant</div>
    <div class="subtitle">Factual information from official sources</div>
    <div class="disclaimer">⚠️ Not investment advice</div>
</div>
""", unsafe_allow_html=True)

# Search input
query = st.text_input(
    "Search",
    placeholder="Ask about expense ratio, exit load, SIP, ELSS...",
    label_visibility="collapsed"
)

# Topic chips
st.markdown("#### Popular Topics")
topics = [
    ("Expense Ratio", "expense ratio"),
    ("Exit Load", "exit load"),
    ("Minimum SIP", "minimum sip"),
    ("ELSS Lock-in", "elss lock-in"),
    ("Riskometer", "riskometer"),
    ("Benchmark", "benchmark"),
    ("Download Statement", "download statement"),
    ("NAV", "nav"),
    ("KYC", "kyc"),
    ("AUM", "aum")
]

cols = st.columns(5)
selected_topic = None

for idx, (label, search_query) in enumerate(topics):
    with cols[idx % 5]:
        if st.button(label, key=f"topic_{idx}", use_container_width=True):
            selected_topic = search_query

# Use selected topic or typed query
search_term = selected_topic if selected_topic else query

# Display answer
if search_term:
    result = find_answer(search_term)
    
    if result:
        st.markdown(f"""
        <div class="answer-card">
            <div class="answer-question">{result['question']}</div>
            <div class="answer-content">{result['answer']}</div>
            <div class="source-section">
                <span class="source-label">Source: </span>
                <a href="{result['source']}" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: 500;">
                    {result['source_name']} ↗
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif query:
        st.warning("🔍 No matching FAQ found. Try a different search term.")

# Footer
st.markdown("""
<div class="footer">
    <p>Sources: 
        <a href="https://www.sebi.gov.in" target="_blank">SEBI</a> · 
        <a href="https://www.amfiindia.com" target="_blank">AMFI</a> · 
        <a href="https://www.mfcentral.com" target="_blank">MF Central</a>
    </p>
</div>
""", unsafe_allow_html=True)
