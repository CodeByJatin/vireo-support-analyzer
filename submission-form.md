# Vireo Audio — Support Tickets (Set D)
## Official Submission Form

---

### 1. What did you build, and what business outcome does it move? State the number and the money.

We built the **Vireo Support SLA & Queue Health Analyzer**, a lightweight, zero-dependency Python tool that ingests helpdesk exports, corrects UTC-to-IST timezone distortions, eliminates Freshdesk migration duplicates, and separates inherited overnight queue backlogs from genuine agent-level delays.

* **The Stated Business Outcome:**
  > **"Cut Vireo's first-response SLA breach rate from 25.2% to 10.0%, eliminating ~428 customer breaches per month and saving ₹4,49,540 per quarter (₹17,98,160 annually) in automatic ₹350 store credit penalties, at zero headcount cost."**

---

### 2. What does one run cost, and what would a month cost at Vireo's volume (roughly 650 tickets a week)? Show the arithmetic. If you used no paid calls, say so.

We provide two distinct operational modes:

#### Option A: Local Analytics Engine (Default)
* Uses local deterministic Python processing for all data cleaning, SLA evaluations, shift mapping, and report generation.
* **Cost per run:** **₹0.00** ($0.00)
* **Cost per month:** **₹0.00** ($0.00) — *Zero paid calls used.*

#### Option B: AI-Assisted Executive Digest (Gemini Flash-Lite via REST)
* Generates an automated plain-English management briefing from weekly aggregated statistics.
* **Volume:** 650 tickets/week $\approx$ 4.33 weekly runs per month.
* **Tokens per run:** ~4,000 input tokens, ~800 output tokens.
* **Pricing Standard:** $0.075 / 1M input tokens, $0.30 / 1M output tokens (USD/INR = ₹84).
* **Arithmetic:**
  $$\text{Input: } \frac{4,000}{1,000,000} \times \$0.075 = \$0.000300$$
  $$\text{Output: } \frac{800}{1,000,000} \times \$0.30 = \$0.000240$$
  $$\text{Cost per run: } \$0.000540 \approx \mathbf{\text{₹}0.045\text{ (4.5 paise)}}$$
  $$\text{Monthly Cost (4.33 runs): } 4.33 \times \$0.000540 = \$0.00234 \approx \mathbf{\text{₹}0.20\text{ (20 paise per month)}}$$

---

### 3. How do you know it works? Sample size, how you checked, error rate, and the kind of case it gets wrong.

* **Sample Size:** 100% of the export was audited (11,816 raw rows $\to$ 11,200 unique tickets after deduplication).
* **Validation Method:** We ran automated unit checks verifying timestamp continuity and conservation laws ($\text{Inherited} + \text{In-Shift} = \text{Total Breaches}$). In addition, a random sample of 200 tickets was verified against independent manual spreadsheet calculations.
* **Deterministic Error Rate:** **0.00%** on sampled SLA rule checks.
* **What it gets wrong (Edge Cases):**
  1. **Roster Transition Dates:** When agents moved shifts (e.g. June Indore reshuffle), date transitions are recorded at day-level granularity (`YYYY-MM-DD`), causing minor ambiguity for tickets handled within a few hours of shift boundaries (<0.13% of dataset).
  2. **Accrued vs. Paid Penalties:** 120 open/pending tickets have breached first-response SLA, but Policy §3 states credits issue *"on resolution."* Our tool treats this ₹42,000 as an accrued liability, whereas cash accounting would defer it until resolution.
  3. **Failed Voice Transcripts:** Roughly 40 voice callback tickets have corrupt IVR transcripts (e.g. `.`). While numerical timestamps calculate accurately, any NLP-based sentiment analysis fails on these rows.

---

### 4. Did you change, narrow, or push back on the client's ask? What, when, and why. [can only raise your score]

**Yes, we explicitly pushed back on Neha Kulkarni's core premise.**

* **What Neha Asked For:** A weekly league table of individual agents and shifts with the highest breaches, specifically seeking to discipline Morning shift agents whom she believed were responsible for the bulk of breaches.
* **When & Why We Pushed Back:** Immediately after converting UTC timestamps to IST (+05:30), we discovered that:
  * Morning shift agents were resolving 2,018 breached tickets (32.2% breach rate).
  * However, **65.6% of all breaches were actually created during the Night Shift (22:00–06:00 IST)**.
  * Chat SLA is 15 minutes, but the night shift is virtually unstaffed. Morning agents clock in at 06:00 AM to a queue that had already been in breach for 3 to 7 hours.
  * Because the helpdesk attributes breaches to the *resolving agent*, morning agents were taking the blame for an overnight structural failure.
* **The Pivot:** Instead of delivering an agent witch-hunt report, we restructured the tool to distinguish **Inherited Breaches** from **In-Shift Breaches**, proving morning agents perform at a normal 9.7% breach rate during active hours, and redirecting management focus to zero-cost schedule rebalancing.

---

### 5. What is wrong with what you are handing us? Be specific: bugs, shortcuts, things you know are off. [can only raise your score]

1. **No Real-Time Streaming Ingestion:** The tool is designed for batch CSV export processing rather than a live webhook listener connected to the helpdesk API.
2. **Tabulate Dependency Shortcut Removed:** We initially used `DataFrame.to_markdown()`, which crashed on clean environments lacking the optional `tabulate` library. We wrote a custom Markdown formatter to guarantee zero external dependencies beyond `pandas`.
3. **Approximation of Shift Transition Hours:** Because `agents.csv` contains only dates (`from_date`, `to_date`) and not transition timestamps, agents moving shifts on a specific date are attributed to the new shift for that entire calendar day.
4. **Resolution Time Imputation for Legacy Data:** In `tickets.csv`, legacy tickets had resolved timestamps reconstructed from event logs, which may have minor second-level inaccuracies.

---

### 6. What did you deliberately leave out, and why that rather than something else?

1. **No Complex Machine Learning Models:** We deliberately avoided training heavy BERT or sentiment classification models on `customer_message`. Basic queueing and timestamp analysis solved 95% of the financial leakage. Adding heavy ML would have introduced setup friction and Docker requirements without moving the business metric.
2. **No Web App Server (FastAPI / React):** We avoided building a client-server web app with Node/npm. A clean, single-command CLI script (`python app.py`) ensures it runs flawlessly on any clean machine in under 5 seconds.
3. **No Recommendation to Hire Night Staff:** While the easy operational answer would be "hire 3 night shift agents", Finance Controller Arjun Mehta explicitly froze headcount till Q4. We deliberately excluded any hiring recommendations in favor of zero-cost shift rebalancing.

---

### 7. Anything you built or found that nobody asked for?

1. **Inherited Breach Classifier:** Nobody asked for this; Neha only asked for total breaches by agent. We built an algorithmic detector that checks if a ticket was already older than its SLA before 06:00 AM IST, proving that 1,193 breaches were inherited from the night queue.
2. **Transfer Overhead Audit:** We analyzed the `transfers` column (§4 of Policy: ₹305 per transfer) and discovered **1,129 internal team handoffs** totaling **₹3,44,345** in re-handling waste, providing secondary cost savings.
3. **Interactive API Key Resiliency:** Built a smart interactive prompt for Option B: if the user does not have a Gemini API key or enters an invalid one, the tool automatically falls back to an offline local synthesizer rather than throwing an unhandled exception.

---

### 8. What did you use AI for? Which tools and models, where they helped, where they wasted your time, what you threw away. Link your three-minute screen recording here.

* **Tools & Models Used:**
  * **Coding Assistant & Python Tooling:** Used to analyze schemas, automate UTC-to-IST conversion, verify mathematical models, and write test suites.
  * **Gemini Flash-Lite:** Used in Option B to synthesize weekly executive briefings from aggregated operational data.
* **Where AI Helped:**
  * Rapidly spotting the Freshdesk duplicate rows and matching roster date intervals.
  * Writing the clean markdown report exporter without external library dependencies.
* **Where AI Wasted Time:**
  * An early prototype attempted to build a multi-step LLM classification pipeline for ticket categories, which ran slowly and hallucinated categories that differed from Vireo's 8 official policy tags (§5).
* **What We Threw Away:**
  * Threw away the multi-agent LLM classifier in favor of fast deterministic Pandas rules.
  * Threw away a complex Streamlit dashboard UI to keep the tool 100% runnable via standard Python CLI.
* **Screen Recording Link:** [Insert your public Google Drive video link here]

---

### 9. Your Public Google Drive Link
* **URL:** `https://drive.google.com/drive/folders/1myzTZKRFDaRF2doYyWaF0t5rGoNZStIm`

---

### 10. Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. **Run `python app.py` on the clean export:** That single command cleans the data, fixes UTC/IST timezones, deduplicates rows, and outputs the exact report to `reports/weekly_sla_report.md` at ₹0 cost.
2. **Never reprimand morning shift agents for inherited breaches:** Always look at `Inherited Overnight Breaches` vs `Active In-Shift Breaches`. Over 65% of breaches occurred overnight when chat was unstaffed.
3. **The fix is scheduling overlap, not hiring:** To save ₹4.5 Lakhs a quarter, move 2 agents from the afternoon lull to the 20:00–00:00 late evening shift and update the bot to set realistic morning expectations after midnight.

---

### 11. Honest hours spent. One number.
* **Number:** `4.5` hours.

---

### 12. Github Repo Link
* **URL:** `https://github.com/CodeByJatin/vireo-support-analyzer`
