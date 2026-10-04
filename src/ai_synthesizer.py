import os
import json
import urllib.request
import urllib.error

# API Key variable in code file (can be populated directly or from environment)
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def generate_local_digest(metrics, financials):
    """
    Intelligent local heuristic synthesizer (Zero API cost / Offline).
    Dynamically generates the 3-paragraph executive briefing from live computed metrics.
    """
    total = metrics['total_tickets']
    breaches = metrics['total_breaches']
    rate = metrics['overall_breach_rate']
    inherited = metrics['inherited_breaches']
    in_shift = metrics['in_shift_breaches']
    
    inherited_pct = (inherited / breaches * 100) if breaches > 0 else 0
    quarterly_penalty = financials['current_quarterly_penalty_inr']
    quarterly_savings = financials['quarterly_savings_inr']
    
    top_channel_row = metrics['channel_summary'].sort_values(by='breach_rate', ascending=False).iloc[0]
    top_channel = top_channel_row['channel'].title()
    top_channel_rate = top_channel_row['breach_rate']
    
    digest = f"""### Executive Briefing (Operations Digest)

**1. Queue Health & Shift Distortion:**
During this reporting period, Vireo recorded {total:,} tickets with an overall first-response SLA breach rate of {rate:.1f}% ({breaches:,} total breaches). However, analyzing ticket creation timestamps proves that **{inherited:,} of these breaches ({inherited_pct:.1f}%) were inherited from overnight queues**. In standard reports, morning agents are unfairly penalized for clearing chat tickets that had already exceeded their 15-minute SLA hours before morning clock-in (06:00 IST). In reality, in-shift daytime execution remains strong, with {top_channel} driving the bulk of delays ({top_channel_rate:.1f}% channel breach rate).

**2. Financial Impact & Liability:**
At Vireo's current standard run-rate, SLA penalty credits (Policy §3: Rs 350 per breach) represent a quarterly liability of **Rs {int(quarterly_penalty):,}** (~Rs {int(quarterly_penalty/3):,} per month). Additionally, internal team handoffs have generated {financials['total_transfers']:,} transfers, incurring Rs {int(financials['transfer_cost_inr']):,} in re-handling overhead.

**3. Actionable Recommendation (Zero Headcount Cost):**
To comply with the Q4 hiring freeze while stopping credit leakage:
* **Reallocate Staffing:** Reassign 2 agents from low-volume afternoon hours to a late evening overlap shift (20:00 to 00:00 IST) to clear chat queues before midnight.
* **Intake Bot Guardrails:** Update the website chat widget between 00:00 and 06:00 IST to set realistic morning callback expectations rather than promising a 15-minute response.
* **Expected Outcome:** These zero-cost measures will reduce the breach rate to **10.0%**, saving **Rs {int(quarterly_savings):,} per quarter** in customer credits."""
    return digest


def call_gemini_api(api_key, prompt):
    """
    Calls Google Gemini REST API using standard urllib (zero external pip dependencies).
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1000
        }
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15) as response:
            resp_data = json.loads(response.read().decode('utf-8'))
            text = resp_data['candidates'][0]['content']['parts'][0]['text']
            return True, text
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8', errors='ignore')
        return False, f"HTTP Error {e.code}: {error_msg}"
    except Exception as e:
        return False, str(e)


def run_synthesizer(metrics, financials, force_ai=False):
    """
    Runs executive digest synthesis.
    Checks API key, prompts user if empty or failing, and falls back to local synthesizer if needed.
    """
    prompt = f"""
You are an expert customer support operations consultant advising Vireo Audio's leadership (Neha Kulkarni, Support Ops Manager, and Arjun Mehta, Finance Controller).
Write a 3-paragraph executive memo based on these live data metrics:
- Total tickets analyzed: {metrics['total_tickets']}
- Total first-response SLA breaches: {metrics['total_breaches']} ({metrics['overall_breach_rate']:.1f}% breach rate)
- Inherited overnight breaches (created at night, breached before morning): {metrics['inherited_breaches']}
- In-shift active breaches: {metrics['in_shift_breaches']}
- Top channel by breach rate: {metrics['channel_summary'].to_dict(orient='records')}
- Current quarterly SLA credit penalty: Rs {int(financials['current_quarterly_penalty_inr']):,}
- Projected quarterly savings if breach rate cut to 10%: Rs {int(financials['quarterly_savings_inr']):,}
- Internal transfers: {financials['total_transfers']} costing Rs {int(financials['transfer_cost_inr']):,}

Paragraph 1: Uncover the morning shift queue distortion vs overnight reality.
Paragraph 2: State the financial liability and quarterly cost numbers.
Paragraph 3: Give zero-cost operational solutions (scheduling overlap, bot intake tweak) to cut breach rate to 10% without hiring.
Keep it crisp, objective, and executive-ready.
"""

    if not force_ai:
        # Default mode (Option A): Local synthesizer, zero API cost
        return generate_local_digest(metrics, financials)

    # If Option B (--ai) is requested:
    api_key = DEFAULT_API_KEY.strip()
    
    # 1. If an API key is already present in code or env, try it
    if api_key:
        print("[INFO] Attempting AI synthesis with configured API key...")
        success, result = call_gemini_api(api_key, prompt)
        if success:
            return result
        print(f"[WARNING] Configured API key failed: {result}")

    # 2. Prompt user interactively if empty or failed
    print("\n[AI Synthesis Mode]")
    while True:
        try:
            choice = input("Do you have an API key? (yes/no): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Non-interactive environment detected. Falling back to local synthesizer.")
            return generate_local_digest(metrics, financials)

        if choice in ['no', 'n']:
            print("[INFO] Running built-in intelligent local synthesizer (Zero API cost)...")
            return generate_local_digest(metrics, financials)
        elif choice in ['yes', 'y']:
            try:
                entered_key = input("Enter API key: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[INFO] Falling back to local synthesizer.")
                return generate_local_digest(metrics, financials)

            if not entered_key:
                print("[ERROR] API key cannot be blank. Please try again.")
                continue

            print("[INFO] Testing API key with model...")
            success, result = call_gemini_api(entered_key, prompt)
            if success:
                print("[SUCCESS] AI executive briefing successfully generated!\n")
                return result
            else:
                print(f"[ERROR] API call failed: {result}\nPlease try again or type 'no'.\n")
        else:
            print("Please type 'yes' or 'no'.")
