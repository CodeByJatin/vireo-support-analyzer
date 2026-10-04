def compute_financials(metrics, weekly_volume=650):
    """
    Calculates SLA breach penalty liabilities, transfer costs,
    and financial savings from reducing breaches to 10.0%.
    """
    total_breaches = metrics['total_breaches']
    inherited_breaches = metrics['inherited_breaches']
    in_shift_breaches = metrics['in_shift_breaches']
    
    # 1. Total penalty across dataset
    penalty_per_breach = 350  # INR (Policy §3)
    total_penalty_inr = total_breaches * penalty_per_breach
    inherited_penalty_inr = inherited_breaches * penalty_per_breach
    in_shift_penalty_inr = in_shift_breaches * penalty_per_breach
    
    # 2. Internal Transfers (Policy §4: Rs 305 per transfer)
    df = metrics['processed_df']
    total_transfers = int(df['transfers'].sum()) if 'transfers' in df.columns else 0
    transfer_cost_inr = total_transfers * 305
    
    # 3. Weekly run-rate projections at standard Vireo volume
    breach_rate = metrics['overall_breach_rate'] / 100.0
    monthly_volume = (weekly_volume * 52) / 12
    quarterly_volume = weekly_volume * 13
    
    weekly_breaches = weekly_volume * breach_rate
    monthly_breaches = monthly_volume * breach_rate
    quarterly_breaches = quarterly_volume * breach_rate
    
    weekly_penalty_inr = weekly_breaches * penalty_per_breach
    monthly_penalty_inr = monthly_breaches * penalty_per_breach
    quarterly_penalty_inr = quarterly_breaches * penalty_per_breach
    annual_penalty_inr = quarterly_penalty_inr * 4
    
    # 4. Target Projections (10.0% breach rate)
    target_rate = 0.100
    target_monthly_breaches = monthly_volume * target_rate
    target_quarterly_breaches = quarterly_volume * target_rate
    
    avoided_monthly_breaches = monthly_breaches - target_monthly_breaches
    avoided_quarterly_breaches = quarterly_breaches - target_quarterly_breaches
    
    monthly_savings_inr = avoided_monthly_breaches * penalty_per_breach
    quarterly_savings_inr = avoided_quarterly_breaches * penalty_per_breach
    annual_savings_inr = quarterly_savings_inr * 4
    
    # 5. Tool Unit Economics
    # Local: Rs 0
    # AI (Gemini 1.5 Flash): ~4.5 paise/run, ~20 paise/month
    tool_cost_local_monthly = 0.0
    tool_cost_ai_monthly = 0.20  # INR
    
    financials = {
        'total_penalty_inr': total_penalty_inr,
        'inherited_penalty_inr': inherited_penalty_inr,
        'in_shift_penalty_inr': in_shift_penalty_inr,
        'total_transfers': total_transfers,
        'transfer_cost_inr': transfer_cost_inr,
        'current_weekly_penalty_inr': weekly_penalty_inr,
        'current_monthly_penalty_inr': monthly_penalty_inr,
        'current_quarterly_penalty_inr': quarterly_penalty_inr,
        'current_annual_penalty_inr': annual_penalty_inr,
        'monthly_savings_inr': monthly_savings_inr,
        'quarterly_savings_inr': quarterly_savings_inr,
        'annual_savings_inr': annual_savings_inr,
        'avoided_monthly_breaches': avoided_monthly_breaches,
        'avoided_quarterly_breaches': avoided_quarterly_breaches,
        'tool_cost_local_monthly': tool_cost_local_monthly,
        'tool_cost_ai_monthly': tool_cost_ai_monthly
    }
    
    return financials
