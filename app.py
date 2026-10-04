import os
import argparse
import pandas as pd
from datetime import datetime

from src.cleaner import clean_and_merge_data
from src.sla_engine import analyze_slas
from src.financial_model import compute_financials
from src.ai_synthesizer import run_synthesizer

def df_to_md(df):
    if df.empty:
        return ""
    headers = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        formatted_row = []
        for val in row:
            if isinstance(val, float):
                formatted_row.append(f"{val:.2f}")
            else:
                formatted_row.append(str(val))
        lines.append("| " + " | ".join(formatted_row) + " |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Vireo Audio — First-Response SLA & Queue Health Analyzer"
    )
    parser.add_argument("--tickets", default="tickets.csv", help="Path to tickets.csv (default: tickets.csv)")
    parser.add_argument("--agents", default="agents.csv", help="Path to agents.csv (default: agents.csv)")
    parser.add_argument("--start-date", default=None, help="Start date filter (YYYY-MM-DD)")
    parser.add_argument("--end-date", default=None, help="End date filter (YYYY-MM-DD)")
    parser.add_argument("--ai", action="store_true", help="Enable AI executive briefing mode (Option B)")
    parser.add_argument("--output", default=None, help="Output report markdown path (default: updates reports/weekly_sla_report.md and saves timestamped copy)")
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("   VIREO AUDIO — FIRST-RESPONSE SLA & QUEUE HEALTH ANALYZER")
    print("="*70 + "\n")
    
    # 1. Clean and merge
    print(f"[*] Ingesting and cleaning data from '{args.tickets}' and '{args.agents}'...")
    df = clean_and_merge_data(
        tickets_path=args.tickets,
        agents_path=args.agents,
        start_date=args.start_date,
        end_date=args.end_date
    )
    print(f"[+] Loaded and verified {len(df):,} unique tickets.")
    
    # 2. SLA calculations
    print("[*] Running SLA compliance and inherited breach detection...")
    metrics = analyze_slas(df)
    
    # 3. Financial calculations
    print("[*] Computing financial liability and quarterly savings projections...")
    financials = compute_financials(metrics)
    
    # 4. AI / Heuristic synthesis
    print(f"[*] Generating executive briefing (Mode: {'AI-Assisted' if args.ai else 'Local Analytics Engine'})...")
    executive_digest = run_synthesizer(metrics, financials, force_ai=args.ai)
    
    # 5. Display terminal dashboard
    print("\n" + "-"*70)
    print("                     OPERATIONAL METRICS DASHBOARD")
    print("-"*70)
    print(f"Total Tickets Analyzed:        {metrics['total_tickets']:,}")
    print(f"Total SLA Breaches:            {metrics['total_breaches']:,} ({metrics['overall_breach_rate']:.1f}%)")
    print(f"Inherited Overnight Breaches:  {metrics['inherited_breaches']:,} ({(metrics['inherited_breaches']/max(metrics['total_breaches'], 1))*100:.1f}% of all breaches)")
    print(f"Active In-Shift Breaches:      {metrics['in_shift_breaches']:,}")
    print(f"Total SLA Penalty Incurred:    Rs {financials['total_penalty_inr']:,}")
    print(f"Internal Transfer Costs:       Rs {financials['transfer_cost_inr']:,} ({financials['total_transfers']:,} transfers)")
    
    print("\n[A] BREACHES BY CHANNEL")
    print(metrics['channel_summary'].to_string(index=False))
    
    print("\n[B] TRUE ROOT CAUSE: BREACHES BY CREATION SHIFT (IST)")
    print(metrics['creation_shift_summary'].to_string(index=False))
    
    print("\n[C] NEHA'S DISTORTED VIEW: BREACHES PINNED ON RESOLVING AGENTS")
    if not metrics['resolving_summary'].empty:
        print(metrics['resolving_summary'].to_string(index=False))
    
    print("\n" + "-"*70)
    print("                     FINANCIAL OUTCOME SUMMARY")
    print("-"*70)
    print(f"Current Quarterly SLA Liability:   Rs {int(financials['current_quarterly_penalty_inr']):,}")
    print(f"Target Quarterly Liability (10%):  Rs {int(financials['current_quarterly_penalty_inr'] - financials['quarterly_savings_inr']):,}")
    print(f"Quarterly Savings Achievable:      Rs {int(financials['quarterly_savings_inr']):,} (Rs {int(financials['annual_savings_inr']):,} / year)")
    print(f"Tool Monthly Run Cost:             {'Rs 0.00' if not args.ai else 'Rs 0.20 (20 paise)'}")
    
    print("\n" + "="*70)
    print(executive_digest)
    print("="*70 + "\n")

    # 6. Export report
    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_content = f"""# Vireo Audio — Support SLA & Queue Health Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Data Source:** `{args.tickets}` | **Scope:** {metrics['total_tickets']:,} tickets

---

## 1. Executive Summary

{executive_digest}

---

## 2. Core Operational Metrics

| Metric | Value |
|---|---|
| Total Tickets Analyzed | **{metrics['total_tickets']:,}** |
| Total First-Response Breaches | **{metrics['total_breaches']:,}** ({metrics['overall_breach_rate']:.1f}%) |
| Inherited Overnight Breaches | **{metrics['inherited_breaches']:,}** ({(metrics['inherited_breaches']/max(metrics['total_breaches'], 1))*100:.1f}%) |
| Active In-Shift Breaches | **{metrics['in_shift_breaches']:,}** |
| Total SLA Penalty Accrued | **Rs {financials['total_penalty_inr']:,}** |
| Internal Team Transfers | **{financials['total_transfers']:,}** (Rs {financials['transfer_cost_inr']:,}) |

### Channel Performance

{df_to_md(metrics['channel_summary'])}

### Creation Shift Breakdown (IST)

{df_to_md(metrics['creation_shift_summary'])}

### Resolving Agent Shift Breakdown

{df_to_md(metrics['resolving_summary']) if not metrics['resolving_summary'].empty else ''}

---

## 3. Financial Projections & Business Goal

> **Official Business Target:** Cut first-response breach rate from 25.2% to 10.0%, eliminating ~428 breached tickets per month and saving **Rs {int(financials['quarterly_savings_inr']):,} per quarter (Rs {int(financials['annual_savings_inr']):,} annually)** at zero headcount cost.

* **Current Quarterly Penalty:** Rs {int(financials['current_quarterly_penalty_inr']):,}
* **Projected Quarterly Savings:** Rs {int(financials['quarterly_savings_inr']):,}
* **Tool Operating Cost:** {'Rs 0.00 / month' if not args.ai else 'Rs 0.20 / month (20 paise)'}
"""

    os.makedirs("reports", exist_ok=True)
    
    # Save the latest report
    latest_file = args.output if args.output else "reports/weekly_sla_report.md"
    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[+] Latest report updated at: {latest_file}")
    
    # Also save a timestamped historical copy if default
    if not args.output:
        history_file = f"reports/sla_report_{timestamp_str}.md"
        with open(history_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"[+] Historical timestamped copy saved at: {history_file}\n")

if __name__ == "__main__":
    main()
