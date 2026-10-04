# Vireo Audio — Support Ticket SLA Analyzer

A simple, lightweight Python tool to analyze Vireo Audio's support tickets, fix timezone issues, and find the real cause of first-response SLA breaches.

---

## Quickstart

Requires Python 3.9+ and `pandas`.

```bash
# 1. Install pandas
pip install -r requirements.txt

# 2. Run the tool (Offline, ₹0 cost)
python app.py
```

That's it. It prints the analysis to the terminal and saves a report in `reports/weekly_sla_report.md`.

---

## Optional: Run with AI Mode

```bash
python app.py --ai
```
* If you have a Google Gemini API key (using Gemini Flash-Lite), enter it when prompted to generate an AI summary.
* If you don't have a key, just type `no` when asked. The tool will run offline for free without crashing.

---

## What the Data Actually Shows

The support manager (Neha) wanted to scold morning shift agents for late replies. Here is what the numbers actually show:

1. **Timezone issue:** Helpdesk timestamps are in UTC, while Vireo shifts are in Indian Standard Time (IST). Converting to IST is necessary to see which shift tickets belong to.
2. **Duplicate tickets:** 616 duplicate tickets from the old Freshdesk migration were removed, leaving **11,200 unique tickets**.
3. **The real problem:**
   * In standard reports, morning agents resolved **2,018 breached tickets** (32.2% breach rate).
   * But looking at when customers actually messaged, **65.6% of all breaches happened overnight (10 PM to 6 AM)** when live chat was unstaffed.
   * Morning staff clocked in at 6 AM to tickets that had already been late for hours.

---

## Business Impact & Cost Numbers

* **Current loss:** Vireo pays a ₹350 store credit for every breach (Policy §3). At 650 tickets/week and a ~25% breach rate, this costs **~₹7.45 Lakhs every quarter**.
* **Target:** Drop the breach rate from 25.2% to 10.0%.
* **Savings:** Saves ~428 breached tickets a month = **₹4,49,540 saved per quarter** (~₹18 Lakhs a year).
* **Zero hiring needed:** Reassign 2 agents from quiet afternoon hours to cover 8 PM to midnight, and update the night chatbot to tell customers human support opens at 6 AM.
* **Running cost:**
  * Local mode: **₹0.00**
  * AI mode (Gemini Flash-Lite): **~4.5 paise per run** (~20 paise per month).

---

## Files in This Repository

* `app.py`: Main script to run the analysis.
* `memo.md`: 1-page non-technical note to Neha explaining the findings.
* `verification.md`: How we tested the calculations (0.00% error rate on 200 random samples).
* `submission-form.md`: Answers to all required submission questions.
* `src/`: Cleaner, SLA engine, financial math, and AI helper scripts.
* `reports/`: Generated markdown reports.