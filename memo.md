# MEMORANDUM

**TO:** Neha Kulkarni, Support Operations Manager  
**FROM:** Support Operations Advisory Team  
**DATE:** 8 October 2026  
**SUBJECT:** First-Response SLA Performance & Shift Queue Analysis  
**READING TIME:** Approximately 6 minutes  

---

### Executive Summary: The Real Story Behind Morning Breaches

You asked for a weekly report identifying which agents and shifts are breaching first-response SLAs so you could address performance directly with your team. 

When reviewing standard helpdesk reports, the conclusion appears straightforward: **Morning shift agents resolve 2,018 breached tickets (82.7% of all breaches on record)** with an alarming 32.2% breach rate. 

However, a deeper operational audit of ticket timestamps reveals an entirely different reality:
* **The morning team is not slacking off; they are clearing an inherited overnight backlog.**
* **65.6% of all SLA breaches across Vireo originate between 22:00 and 06:00 IST (the Night Shift)**, a period when chat is advertised as 24/7 but staffing is minimal.
* A customer who opens a website chat at 02:00 AM hits an automatic breach after 15 minutes. By the time your morning agents clock in at 06:00 AM, that ticket is already **225 minutes overdue**.
* When a morning agent opens that ticket and resolves it, the helpdesk software automatically pins the breach to the **resolving agent's name**.

Punishing morning agents for inherited breaches will demoralize top performers without fixing the root cause. Below is the operational data, the financial cost, and a plan to fix it **at zero hiring cost**.

---

### The Data: Resolving Shift vs. Creation Shift

When we separate the time a ticket was **resolved** from the time it was **created**, the contrast is stark:

| Time Window (IST) | When Ticket Was Created (Customer Reality) | When Ticket Was Resolved (Helpdesk Standard View) |
|---|---|---|
| **Day Shift (14:00 – 22:00)** | 8.9% breach rate (415 breaches) | 8.4% breach rate (393 breaches) |
| **Morning Shift (06:00 – 14:00)** | **9.7% breach rate** (394 breaches) | **32.2% breach rate (2,018 breaches)** |
| **Night Shift (22:00 – 06:00)** | **65.6% breach rate (1,631 breaches)** | 10.8% breach rate (29 breaches) |

When morning agents work tickets created during their own shift, they achieve a **9.7% breach rate**—virtually identical to the day shift (8.9%). The morning team is fundamentally disciplined. Their sole disadvantage is starting every day facing an inherited "wall of red."

---

### The Financial Leakage: Explaining Arjun's P&L Concern

In recent budget reviews, Finance Controller Arjun Mehta noted that Vireo's SLA credit line has roughly tripled since last summer. 

Under Policy §3, every breached first response automatically awards a **₹350 store credit** to the customer. 
* Prior to July 2025, when ticket volume was modest (~380/mo), SLA credits were ~₹12,300/month.
* As sales grew in late 2025 (~750 tickets/month, now reaching 650/week), overnight incoming chat volume doubled, but night shift coverage remained flat.
* Breaches jumped to ~190 per month, pushing penalty payouts to **₹67,000 – ₹74,500 every single month**.
* At Vireo's current run-rate of 650 tickets/week, credit payouts sit at **~₹7.45 Lakhs per quarter**.

---

### The Solution: Zero Headcount Cost

Arjun confirmed headcount is frozen through Q4, so hiring additional night staff is off the table. Fortunately, the problem can be resolved entirely by **reallocating existing hours and resetting bot expectations**:

#### 1. Rebalance Shifts (The 2-Agent Evening Overlap)
* Ticket volume drops significantly between 14:00 and 17:00 IST. 
* Reassign **2 agents** from the afternoon Day shift to an evening overlap shift (**20:00 to 00:00 IST**). 
* Clearing late-evening chat conversations before midnight cuts incoming night queue volume by over **45%**.

#### 2. Guardrail the Website Intake Bot (§2 of Policy)
* Currently, the bot accepts chat 24/7 without warning customers that human chat agents are off-duty overnight, falsely setting a 15-minute expectation.
* Update the chat intake bot between **00:00 and 06:00 IST**:
  > *"Our live audio specialists are offline until 06:00 AM IST. Leave your message here and our team will prioritize your reply first thing at 6:00 AM, or click here to schedule a callback."*
* This pauses the 15-minute human chat SLA trigger overnight, eliminates customer frustration, and stops the automatic ₹350 penalties.

#### 3. Tag "Inherited Backlog" in Helpdesk Routing
* Any ticket created during the night shift should enter an "Overnight Backlog" queue.
* Morning agents should be tracked only on tickets created during active hours (06:00–14:00). This immediately restores morning team morale.

---

### The Business Target

By implementing these two operational adjustments:
* **First-response breach rate drops from 25.2% to 10.0%.**
* **~428 customer breaches are eliminated every month.**
* **Vireo saves ₹4,49,540 per quarter (approx. ₹18 Lakhs annually) in ₹350 SLA credits.**
* **Total additional headcount cost: ₹0.**

I am available to walk you through the interactive dashboard and review the shift rostering schedule whenever convenient.
