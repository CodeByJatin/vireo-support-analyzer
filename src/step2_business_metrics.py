import pandas as pd
import numpy as np

def run_step2():
    print("=== STEP 2: BUSINESS GOAL & FINANCIAL CALCULATIONS ===\n")
    
    df = pd.read_csv('cleaned_tickets.csv')
    df['created_at_ist'] = pd.to_datetime(df['created_at_ist'])
    
    # 1. Historical Metrics (Last 6 Months: Jan 2026 to Jun 2026)
    recent_df = df[df['created_at_ist'] >= '2026-01-01'].copy()
    recent_total = len(recent_df)
    recent_breaches = recent_df['is_breach'].sum()
    recent_breach_rate = (recent_breaches / recent_total) * 100
    
    print(f"--- 1. Recent Baseline (Jan-Jun 2026) ---")
    print(f"Total Tickets in 6 months: {recent_total}")
    print(f"Total Breaches in 6 months: {recent_breaches}")
    print(f"Baseline Breach Rate: {recent_breach_rate:.2f}%")
    print(f"Total SLA Credits Paid (6 mo): Rs {recent_breaches * 350:,}")
    print(f"Average Monthly SLA Credits: Rs {(recent_breaches * 350) / 6:,.2f}\n")
    
    # 2. Transfer Analysis (Policy §4: Rs 305 per transfer)
    total_transfers = df['transfers'].sum()
    transfer_cost = total_transfers * 305
    print(f"--- 2. Internal Transfer Cost Analysis ---")
    print(f"Total Transfers across dataset: {int(total_transfers):,}")
    print(f"Cost of internal transfers (@ Rs 305/transfer): Rs {int(transfer_cost):,}\n")
    
    # 3. Current Run-Rate at Vireo's Volume (650 tickets/week)
    weekly_volume = 650
    monthly_volume = (weekly_volume * 52) / 12  # 2,816.67 tickets/month
    quarterly_volume = weekly_volume * 13       # 8,450 tickets/quarter
    
    # At baseline breach rate (25.2%)
    baseline_rate = 0.252
    current_weekly_breaches = weekly_volume * baseline_rate
    current_monthly_breaches = monthly_volume * baseline_rate
    current_quarterly_breaches = quarterly_volume * baseline_rate
    
    current_weekly_credits = current_weekly_breaches * 350
    current_monthly_credits = current_monthly_breaches * 350
    current_quarterly_credits = current_quarterly_breaches * 350
    current_annual_credits = current_quarterly_credits * 4
    
    print(f"--- 3. Current Volume Run-Rate (650 tickets/week) ---")
    print(f"Weekly Breaches: {current_weekly_breaches:.1f} tickets/week")
    print(f"Monthly Breaches: {current_monthly_breaches:.1f} tickets/month")
    print(f"Quarterly Breaches: {current_quarterly_breaches:.1f} tickets/quarter")
    print(f"Current Monthly SLA Penalty: Rs {current_monthly_credits:,.2f}")
    print(f"Current Quarterly SLA Penalty: Rs {current_quarterly_credits:,.2f}")
    print(f"Current Annualized SLA Penalty: Rs {current_annual_credits:,.2f}\n")
    
    # 4. Target Outcome (Drop from 25.2% to 10.0%)
    target_rate = 0.100
    target_weekly_breaches = weekly_volume * target_rate
    target_monthly_breaches = monthly_volume * target_rate
    target_quarterly_breaches = quarterly_volume * target_rate
    
    target_quarterly_credits = target_quarterly_breaches * 350
    
    # 5. Financial Savings
    saved_monthly_breaches = current_monthly_breaches - target_monthly_breaches
    saved_quarterly_breaches = current_quarterly_breaches - target_quarterly_breaches
    
    saved_monthly_inr = saved_monthly_breaches * 350
    saved_quarterly_inr = saved_quarterly_breaches * 350
    saved_annual_inr = saved_quarterly_inr * 4
    
    print(f"--- 4. Target Outcome (Breach Rate: 10.0%) ---")
    print(f"Avoided Breaches per Month: {saved_monthly_breaches:.1f} tickets")
    print(f"Avoided Breaches per Quarter: {saved_quarterly_breaches:.1f} tickets")
    print(f"Monthly Cost Savings: Rs {saved_monthly_inr:,.2f}")
    print(f"Quarterly Cost Savings: Rs {saved_quarterly_inr:,.2f}")
    print(f"Annual Cost Savings: Rs {saved_annual_inr:,.2f}\n")
    
    # 6. Deliverable 2 Official Statement
    print("--- 5. Deliverable 2 Business Goal Statement ---")
    goal_statement = (
        f"Cut Vireo's first-response breach rate from 25.2% to 10.0%, "
        f"eliminating ~428 breached tickets per month and saving "
        f"Rs {int(saved_quarterly_inr):,} per quarter (Rs {int(saved_annual_inr):,} annually) "
        f"in automatic Rs 350 SLA customer credits, at zero headcount cost."
    )
    print(f'"{goal_statement}"\n')
    
    # 7. Tool Run Cost Arithmetic (650 tickets/week)
    print("--- 6. Tool Run Cost Arithmetic ---")
    # Scenario A: Local deterministic computation (Python/Pandas)
    print("Scenario A: Local Execution (Rules & Analytics Engine):")
    print("  Cost per run: Rs 0.00 ($0.00)")
    print("  Cost per month: Rs 0.00 ($0.00) (No paid API calls required)")
    
    # Scenario B: AI Executive Summary via LLM (e.g., Gemini 1.5 Flash / GPT-4o-mini)
    # 1 run per week summarizing weekly aggregated metrics + top breach drivers
    input_tokens_per_run = 4000
    output_tokens_per_run = 800
    # Gemini 1.5 Flash pricing: $0.075 / 1M input, $0.30 / 1M output
    cost_input = (input_tokens_per_run / 1_000_000) * 0.075
    cost_output = (output_tokens_per_run / 1_000_000) * 0.30
    usd_to_inr = 84.0
    cost_per_run_usd = cost_input + cost_output
    cost_per_run_inr = cost_per_run_usd * usd_to_inr
    
    monthly_runs = 52 / 12  # 4.33 runs
    monthly_cost_inr = cost_per_run_inr * monthly_runs
    
    print("\nScenario B: LLM-Assisted Weekly Executive Digest (Gemini 1.5 Flash):")
    print(f"  Input tokens per weekly run: ~{input_tokens_per_run:,} tokens ($0.075/1M)")
    print(f"  Output tokens per weekly run: ~{output_tokens_per_run:,} tokens ($0.30/1M)")
    print(f"  Cost per run: ${cost_per_run_usd:.6f} (~Rs {cost_per_run_inr:.3f} or ~4 paise)")
    print(f"  Cost per month (4.33 runs): ${cost_per_run_usd * monthly_runs:.5f} (~Rs {monthly_cost_inr:.2f} or ~18 paise)")
    print(f"  ROI: Over {(saved_monthly_inr / max(monthly_cost_inr, 0.01)) * 100:,.0f}%")

if __name__ == '__main__':
    run_step2()
