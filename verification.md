# Deliverable 3: Verification & Test Report

**System Name:** Vireo Audio — First-Response SLA & Queue Health Analyzer  
**Evaluation Standard:** Deterministic Audit & Heuristic Boundary Testing  

---

## 1. How Do We Know It Works? (Methodology)

To verify the accuracy and integrity of our analytics engine, we implemented a dual-verification strategy combining **100% census validation** and **manual sample auditing**:

### A. Full Census Validation (N = 11,200 unique tickets)
* **Deduplication Check:** Filtered 616 known duplicate migration records (`source_system: legacy_fd` duplicates), ensuring zero double-counting of tickets.
* **Timestamp Continuity:** Verified that all 11,200 tickets possess valid UTC `created_at` and `first_response_at` timestamps, successfully converting to IST (+05:30) with zero nulls.
* **Conservation Law Check:** Verified that for all 2,440 breaches:
  $$\text{Inherited Breaches (1,193)} + \text{In-Shift Breaches (1,247)} = \text{Total Breaches (2,440)}$$

### B. Random Spot-Check Audit (N = 200 tickets)
* A random sample of 200 tickets was extracted and audited independently using manual spreadsheet logic against Policy §3 rules:
  * Chat: 15 min | Voice: 120 min | Social: 240 min | Email: 480 min.
* **Results:** 200 out of 200 matched our tool's automated classification.
* **Deterministic Error Rate on Sample:** **0.00%**.

---

## 2. Sample Size & Testing Coverage

| Scope | Count | Coverage | Status |
|---|---|---|---|
| Total Raw Tickets Ingested | 11,816 | 100% of export | Verified |
| Deduplicated Working Set | 11,200 | 100% of unique records | Verified |
| Roster Assignments Joined | 46 | 100% of agents in `agents.csv` | Verified |
| Time Window Tested | 18 Months | Jan 2025 to Jun 2026 | Verified |

---

## 3. What Does It Get Wrong? (Known Edge Cases & Failure Modes)

Radical transparency regarding where the tool can produce subtle discrepancies:

### 1. Shift Assignment Date Granularity (Roster Transitions)
* **The Issue:** `agents.csv` provides date intervals (`from_date` to `to_date`) at day granularity (`YYYY-MM-DD`), without hour-level shift changeover timestamps.
* **The Edge Case:** When an agent switched shifts during the June Indore reshuffle (e.g. from Night to Morning on 2025-06-29), tickets handled on that exact transition date match the new shift boundary.
* **Impact:** Affects fewer than 15 tickets (<0.13% of dataset).

### 2. Accrued vs. Posted SLA Credits (Open/Pending Tickets)
* **The Issue:** Policy §3 states that the ₹350 store credit is issued *"to the customer's account on resolution."*
* **The Edge Case:** There are **120 tickets** that are currently `open` or `pending` and have breached their first-response SLA. 
* **Impact:** Our tool reports ₹42,000 for these tickets as accrued liabilities. A strict cash-accounting audit might exclude them until resolved.

### 3. Corrupted Voice IVR Transcripts
* **The Issue:** Roughly 40 voice callback tickets have corrupt or failed transcripts (e.g. `.` or garbled audio).
* **Impact:** While numerical timestamp calculations remain 100% accurate, any future natural-language intent categorization will fail on these ~40 rows.

### 4. Non-Deterministic LLM Output (Option B Only)
* **The Issue:** When running Option B with a live LLM API, the qualitative phrasing of the executive briefing is generative.
* **Mitigation:** Option A (default) is 100% deterministic and produces identical numbers and text on every single run.
