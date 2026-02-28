#!/usr/bin/env python3
"""
Mutual Fund FAQ Assistant - Web Application
Flask backend with modern minimalist UI
"""

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/faqs')
def get_all_faqs():
    return jsonify([{
        "id": faq["id"],
        "question": faq["question"]
    } for faq in FAQ_DATABASE])


@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower().strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    best_match = None
    best_score = 0
    
    for faq in FAQ_DATABASE:
        score = 0
        for keyword in faq["keywords"]:
            if keyword in query:
                score += len(keyword)
        
        if score > best_score:
            best_score = score
            best_match = faq
    
    if best_match:
        return jsonify({
            "found": True,
            "question": best_match["question"],
            "answer": best_match["answer"],
            "source": best_match["source"],
            "source_name": best_match["source_name"]
        })
    
    return jsonify({"found": False})


@app.route('/api/faq/<int:faq_id>')
def get_faq(faq_id):
    for faq in FAQ_DATABASE:
        if faq["id"] == faq_id:
            return jsonify({
                "found": True,
                "question": faq["question"],
                "answer": faq["answer"],
                "source": faq["source"],
                "source_name": faq["source_name"]
            })
    return jsonify({"found": False}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
