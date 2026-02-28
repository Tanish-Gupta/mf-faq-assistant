#!/usr/bin/env python3
"""
Mutual Fund FAQ Assistant
Answers factual questions about mutual fund schemes using official public sources.
No investment advice provided.
"""

import re
from typing import Optional

FAQ_DATABASE = [
    {
        "keywords": ["expense ratio", "expense", "ter", "total expense ratio"],
        "question": "What is expense ratio in mutual funds?",
        "answer": """Expense Ratio (Total Expense Ratio - TER) is the annual fee charged by mutual funds to manage your investments. It includes fund management fees, administrative costs, and distribution expenses. SEBI has capped the maximum TER based on AUM:
- Equity schemes: 2.25% for first ₹500 crore, reducing progressively
- Debt schemes: 2.00% for first ₹500 crore, reducing progressively
- Index funds/ETFs: Maximum 1.00%

The expense ratio is deducted daily from the fund's NAV.""",
        "source": "https://www.sebi.gov.in/legal/circulars/sep-2018/circular-on-total-expense-ratio-ter-and-performance-disclosure-for-mutual-funds_40456.html"
    },
    {
        "keywords": ["exit load", "exit", "redemption charge", "withdrawal charge"],
        "question": "What is exit load in mutual funds?",
        "answer": """Exit load is a fee charged when you redeem (sell) mutual fund units before a specified period. Common exit load structures:
- Equity funds: Typically 1% if redeemed within 1 year
- Liquid funds: Usually nil or graded (up to 7 days)
- ELSS funds: No exit load (but 3-year lock-in applies)
- Overnight funds: Nil

Exit load is deducted from the redemption NAV. Always check the Scheme Information Document (SID) for exact exit load details.""",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/exit-load.html"
    },
    {
        "keywords": ["minimum sip", "sip amount", "sip minimum", "systematic investment"],
        "question": "What is the minimum SIP amount?",
        "answer": """Minimum SIP (Systematic Investment Plan) amounts vary by fund house and scheme:
- Most funds: ₹500 per month minimum
- Some funds: ₹100 per month (micro-SIP)
- Premium/specialized funds: ₹1,000 - ₹5,000

SIP frequency options include monthly, weekly, daily, or quarterly. Check the specific scheme's SID or the AMC website for exact minimum amounts.""",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/sip.html"
    },
    {
        "keywords": ["lock-in", "lockin", "elss", "tax saving", "80c"],
        "question": "What is the lock-in period for ELSS funds?",
        "answer": """ELSS (Equity Linked Savings Scheme) has a mandatory lock-in period of 3 years from the date of each investment. Key points:
- Lock-in: 3 years (shortest among Section 80C instruments)
- Tax benefit: Up to ₹1.5 lakh deduction under Section 80C
- Each SIP installment has its own 3-year lock-in
- No premature withdrawal allowed during lock-in
- After lock-in, units can be redeemed freely (no exit load)

LTCG tax applies: 12.5% on gains exceeding ₹1.25 lakh per year.""",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/tax-planning-through-elss.html"
    },
    {
        "keywords": ["riskometer", "risk", "risk level", "risk category"],
        "question": "What is a riskometer in mutual funds?",
        "answer": """Riskometer is a visual risk indicator mandated by SEBI that shows a mutual fund's risk level. It has 6 categories:

1. Low - Principal at low risk (liquid, overnight funds)
2. Low to Moderate - Principal at low to moderate risk
3. Moderate - Principal at moderate risk
4. Moderately High - Principal at moderately high risk
5. High - Principal at high risk (equity funds)
6. Very High - Principal at very high risk (sectoral, thematic funds)

The riskometer must be displayed in all scheme documents and advertisements. It is reviewed monthly.""",
        "source": "https://www.sebi.gov.in/legal/circulars/oct-2020/circular-on-product-labeling-in-mutual-funds-riskometer_47796.html"
    },
    {
        "keywords": ["benchmark", "index", "comparison", "nifty", "sensex"],
        "question": "What is a benchmark in mutual funds?",
        "answer": """A benchmark is a standard index against which a mutual fund's performance is measured. Common benchmarks:

- Large cap funds: Nifty 50, BSE Sensex
- Mid cap funds: Nifty Midcap 150
- Small cap funds: Nifty Smallcap 250
- Flexi cap funds: Nifty 500
- Debt funds: CRISIL indices, Nifty bond indices

SEBI mandates funds to declare a Tier 1 benchmark (broad market index) and optionally a Tier 2 benchmark. Performance comparison with benchmark must be shown in factsheets.""",
        "source": "https://www.sebi.gov.in/legal/circulars/jan-2022/circular-on-benchmarking-of-scheme-s-performance-to-total-return-index_55270.html"
    },
    {
        "keywords": ["statement", "download", "cas", "account statement", "portfolio"],
        "question": "How do I download my mutual fund statement?",
        "answer": """You can download your Consolidated Account Statement (CAS) through these official methods:

1. **CAMS/KFintech** - Visit the registrar's website
2. **MF Central** (AMFI portal) - Single source for all funds
3. **Individual AMC websites** - Login to your folio
4. **Email request** - Send email to cams@camsonline.com or mfs@kfintech.com with PAN

MF Central is recommended as it provides a single consolidated view of all your mutual fund holdings across all AMCs.""",
        "source": "https://www.mfcentral.com/"
    },
    {
        "keywords": ["nav", "net asset value", "price", "unit price"],
        "question": "What is NAV in mutual funds?",
        "answer": """NAV (Net Asset Value) is the per-unit market value of a mutual fund scheme. It is calculated as:

NAV = (Total Assets - Total Liabilities) / Number of Units Outstanding

Key points:
- NAV is declared daily (except holidays)
- Cut-off time: 3 PM for equity funds, 1:30 PM for liquid funds
- NAV is published on AMFI website by 11 PM daily
- Purchase/redemption happens at applicable NAV based on cut-off time""",
        "source": "https://www.amfiindia.com/nav-history-download"
    },
    {
        "keywords": ["kyc", "know your customer", "verification", "pan"],
        "question": "What is KYC for mutual funds?",
        "answer": """KYC (Know Your Customer) is a one-time verification mandatory for mutual fund investments. Requirements:
- PAN card (mandatory)
- Address proof (Aadhaar, passport, etc.)
- Photograph
- In-Person Verification (IPV)

You can complete KYC through:
1. KRA agencies (CAMS KRA, KFintech, CVL)
2. Online eKYC using Aadhaar
3. Through AMC or distributor

Once KYC is done with one KRA, it's valid across all mutual funds.""",
        "source": "https://www.camskra.com/"
    },
    {
        "keywords": ["aum", "assets under management", "fund size"],
        "question": "What is AUM in mutual funds?",
        "answer": """AUM (Assets Under Management) is the total market value of all investments managed by a mutual fund scheme. Key points:

- Higher AUM generally indicates investor confidence
- Very large AUM in small/mid cap funds may impact performance
- AUM affects expense ratio (larger funds have lower TER)
- Industry AUM data is published monthly by AMFI

Check the monthly AMFI data for scheme-wise and AMC-wise AUM figures.""",
        "source": "https://www.amfiindia.com/research-information/aum-data"
    }
]


def find_answer(query: str) -> Optional[dict]:
    """Find the best matching FAQ for the given query."""
    query_lower = query.lower()
    
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


def format_response(faq: dict) -> str:
    """Format the FAQ response with source link."""
    return f"""
{'='*60}
📌 {faq['question']}
{'='*60}

{faq['answer']}

📎 Source: {faq['source']}
{'='*60}
"""


def show_help():
    """Display available topics."""
    print("""
╔══════════════════════════════════════════════════════════╗
║          MUTUAL FUND FAQ ASSISTANT                       ║
║          Factual information only • No advice            ║
╠══════════════════════════════════════════════════════════╣
║  Available topics:                                       ║
║  • expense ratio    • exit load      • minimum sip       ║
║  • lock-in/ELSS     • riskometer     • benchmark         ║
║  • download statement • NAV          • KYC               ║
║  • AUM                                                   ║
╠══════════════════════════════════════════════════════════╣
║  Commands: 'help', 'list', 'quit'                        ║
╚══════════════════════════════════════════════════════════╝
""")


def list_all_faqs():
    """List all available questions."""
    print("\n📋 All Available Questions:\n")
    for i, faq in enumerate(FAQ_DATABASE, 1):
        print(f"  {i}. {faq['question']}")
    print()


def main():
    """Main function to run the FAQ assistant."""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          🏦 MUTUAL FUND FAQ ASSISTANT 🏦                 ║
║                                                          ║
║     Factual information from official sources only       ║
║     ⚠️  This is NOT investment advice                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    show_help()
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using MF FAQ Assistant. Goodbye!\n")
                break
            
            if query.lower() in ['help', 'h', '?']:
                show_help()
                continue
            
            if query.lower() in ['list', 'all', 'topics']:
                list_all_faqs()
                continue
            
            result = find_answer(query)
            
            if result:
                print(format_response(result))
            else:
                print("""
❌ Sorry, I couldn't find information on that topic.

Type 'help' to see available topics or 'list' to see all questions.
""")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except EOFError:
            print("\n\n👋 Goodbye!\n")
            break


if __name__ == "__main__":
    main()
