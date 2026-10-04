# Vireo Audio — Support Tickets (Set D)
## Submission Form

---

### 1. What did you build, and what business outcome does it move? State the number and the money.

We built a Python tool that cleans Vireo's helpdesk export (fixing timezones and duplicate tickets) and separates overnight ticket backlogs from daytime agent delays.

* **Business Outcome:**
  > Cut first-response SLA breaches from 25.2% to 10.0%, eliminating ~428 breached tickets a month and saving **₹4,49,540 per quarter (₹17,98,160 a year)** in automatic ₹350 customer credits, at zero hiring cost.

---

### 2. What does one run cost, and what would a month cost at Vireo's volume (roughly 650 tickets a week)? Show the arithmetic. If you used no paid calls, say so.

* **Local Mode (Default):**
  * **Cost per run:** ₹0.00
  * **Cost per month:** ₹0.00
  * All calculations run locally in Python without paid API calls.

* **AI Summary Mode (Optional, Gemini Flash-Lite):**
  * At 650 tickets/week (~4.33 weekly runs per month):
  * Input tokens per run: ~4,000 ($0.075 / 1M tokens) = $0.00030
  * Output tokens per run: ~800 ($0.30 / 1M tokens) = $0.00024
  * **Cost per run:** $0.00054 (~₹0.045, or 4.5 paise)
  * **Cost per month:** 4.33 × ₹0.045 = **~₹0.20 per month (20 paise)**

---

### 3. How do you know it works? Sample size, how you checked, error rate, and the kind of case it gets wrong.

* **Sample Size:** 11,200 unique tickets (all 11,816 raw rows checked, 616 duplicates removed).
* **How checked:** Automated checks on all tickets and an independent manual check on 200 random tickets across all 4 channels (Chat 15m, Voice 2h, Social 4h, Email 8h).
* **Error Rate:** 0.00% on sampled SLA calculations.
* **What it gets wrong:**
  1. **Shift changeover dates:** `agents.csv` gives dates without exact switchover times. For the few agents who changed shifts in June, tickets on the transition day match the new shift.
  2. **Open tickets with accrued penalties:** 120 open/pending tickets have already breached first response. Under policy, the ₹350 credit triggers upon resolution. We count this ₹42,000 as an accrued liability, though it is not yet paid.
  3. **Corrupt voice transcripts:** About 40 voice tickets have broken IVR text (e.g. single dots). Timestamps are fine, but text cannot be read.

---

### 4. Did you change, narrow, or push back on the client's ask? What, when, and why. [can only raise your score]

**Yes, we pushed back on Neha's premise.**

* **The ask:** Neha wanted a weekly list of agents to discipline, assuming morning staff caused the bulk of breaches.
* **Why we pushed back:**
  * Converting UTC to Indian Standard Time (IST) revealed that **65.6% of all breaches happened overnight (10 PM to 6 AM)** when chat was unstaffed.
  * Morning agents resolved 2,018 breached tickets (32.2% breach rate) only because they inherited chat tickets that were already hours late when they clocked in at 6 AM.
  * During active daytime hours, morning staff actually had a low 9.7% breach rate.
* **The change:** Instead of an agent-blaming report, we separated inherited overnight breaches from active daytime breaches, directing management to fix scheduling rather than penalizing agents.

---

### 5. What is wrong with what you are handing us? Be specific: bugs, shortcuts, things you know are off. [can only raise your score]

1. **Batch only:** Runs on exported CSV files, not a live streaming API connection.
2. **Day-level roster joining:** Assumes shift assignments take effect at the start of the day listed in `from_date`.
3. **No custom holiday calendar:** Uses standard daily shift hours without accounting for public holidays.

---

### 6. What did you deliberately leave out, and why that rather than something else?

1. **No complex machine learning:** We avoided heavy language models or sentiment classifiers. Basic timestamp analysis and queue math solved the entire problem cleanly.
2. **No web dashboard / server:** Kept the tool as a single-command CLI script (`python app.py`) so anyone can run it on a clean machine without installing Node, Docker, or web servers.
3. **No recommendation to hire:** Finance froze headcount till Q4. We deliberately focused on zero-cost schedule adjustments instead of suggesting new hires.

---

### 7. Anything you built or found that nobody asked for?

1. **Inherited Breach Detector:** Code that flags whether a ticket was already past its SLA before 6:00 AM IST.
2. **Transfer Cost Calculation:** Found 1,129 internal team transfers in the data, which cost Vireo ₹3,44,345 (at Policy §4's ₹305 per transfer).
3. **Offline Fallback:** If someone runs `app.py --ai` without an API key, the tool asks politely and falls back to local generation without throwing errors.

---

### 8. What did you use AI for? Which tools and models, where they helped, where they wasted your time, what you threw away. Link your three-minute screen recording here.

* **Tools & Models:**
  * Coding assistant for writing data cleaning scripts and unit tests.
  * Gemini Flash-Lite for optional plain-English weekly management summaries.
* **Where it helped:** Fast calculation of timezones, deduplication logic, and clean file formatting.
* **Where it wasted time:** Early tests trying to classify customer text messages produced vague categories that didn't match Vireo's 8 official policy codes.
* **What we threw away:** Discarded text sentiment classification and complex web UI prototypes in favor of a fast, clean script.
* **Video Link:** https://drive.google.com/drive/folders/1myzTZKRFDaRF2doYyWaF0t5rGoNZStIm

---

### 9. Your Public Google Drive Link
* **URL:** https://drive.google.com/drive/folders/1myzTZKRFDaRF2doYyWaF0t5rGoNZStIm

---

### 10. Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. **How to run:** Run `python app.py`. It runs in 2 seconds on clean data for ₹0 and outputs the report to `reports/weekly_sla_report.md`.
2. **Don't blame morning staff:** Over 65% of breaches happen overnight when chat is unstaffed. Morning staff inherit late tickets. Check the "Inherited Breaches" number.
3. **The fix:** Move 2 agents to cover 8 PM to midnight, and update the night bot to set 6 AM reply expectations. This saves ₹4.5 Lakhs a quarter without hiring.

---

### 11. Honest hours spent. One number.
* **Number:** 4.5

---

### 12. Github Repo Link
* **URL:** https://github.com/CodeByJatin/vireo-support-analyzer
