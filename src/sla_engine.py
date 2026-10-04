import pandas as pd
import numpy as np

SLA_TARGETS_MINUTES = {
    'chat': 15.0,
    'voice': 120.0,
    'social': 240.0,
    'email': 480.0
}

def analyze_slas(df):
    """
    Computes SLA performance, channel compliance, and separates
    Inherited Overnight Breaches from True In-Shift Breaches.
    """
    tickets = df.copy()
    
    # 1. First Response Time in Minutes
    tickets['response_time_min'] = (
        (tickets['first_response_at_utc'] - tickets['created_at_utc']).dt.total_seconds() / 60.0
    )
    
    # 2. SLA Target & Breach Flag
    tickets['sla_target_min'] = tickets['channel'].map(SLA_TARGETS_MINUTES).fillna(15.0)
    tickets['is_breach'] = tickets['response_time_min'] > tickets['sla_target_min']
    
    # 3. Detect Inherited Breaches
    # Tickets created overnight (Night shift: 22:00 to 06:00) that were already
    # breached before the Morning shift started at 06:00 IST.
    def check_inherited(row):
        if not row['is_breach']:
            return False
        if row['created_shift_ist'] != 'Night':
            return False
            
        created_time = row['created_at_ist']
        # Find next 06:00 AM
        if created_time.hour >= 22:
            morning_start = created_time.normalize() + pd.Timedelta(days=1, hours=6)
        else:
            morning_start = created_time.normalize() + pd.Timedelta(hours=6)
            
        wait_until_morning_min = (morning_start - created_time).total_seconds() / 60.0
        # If the queue wait until 6 AM alone exceeded the SLA target, it was already breached upon morning clock-in
        return wait_until_morning_min >= row['sla_target_min']

    tickets['is_inherited_breach'] = tickets.apply(check_inherited, axis=1)
    
    # 4. In-Shift Breach (Agent genuinely missed it during staffed shift)
    tickets['is_in_shift_breach'] = tickets['is_breach'] & (~tickets['is_inherited_breach'])
    
    # Aggregations
    total_tickets = len(tickets)
    total_breaches = int(tickets['is_breach'].sum())
    overall_breach_rate = (total_breaches / total_tickets) * 100 if total_tickets > 0 else 0
    inherited_count = int(tickets['is_inherited_breach'].sum())
    in_shift_count = int(tickets['is_in_shift_breach'].sum())
    
    # Channel summary
    channel_summary = tickets.groupby('channel').agg(
        total=('ticket_id', 'count'),
        breaches=('is_breach', 'sum'),
        breach_rate=('is_breach', lambda x: (x.sum() / len(x)) * 100)
    ).reset_index()
    
    # Creation Shift summary
    creation_shift_summary = tickets.groupby('created_shift_ist').agg(
        total=('ticket_id', 'count'),
        breaches=('is_breach', 'sum'),
        breach_rate=('is_breach', lambda x: (x.sum() / len(x)) * 100),
        inherited_breaches=('is_inherited_breach', 'sum')
    ).reset_index()
    
    # Resolving Shift summary (Roster Shift)
    resolving_shift_col = 'agent_shift_roster' if 'agent_shift_roster' in tickets.columns else None
    if resolving_shift_col:
        resolving_summary = tickets.groupby(resolving_shift_col).agg(
            total_resolved=('ticket_id', 'count'),
            breaches_assigned=('is_breach', 'sum'),
            breach_rate=('is_breach', lambda x: (x.sum() / len(x)) * 100),
            inherited_breaches=('is_inherited_breach', 'sum'),
            active_breaches=('is_in_shift_breach', 'sum')
        ).reset_index()
    else:
        resolving_summary = pd.DataFrame()
        
    metrics = {
        'total_tickets': total_tickets,
        'total_breaches': total_breaches,
        'overall_breach_rate': overall_breach_rate,
        'inherited_breaches': inherited_count,
        'in_shift_breaches': in_shift_count,
        'channel_summary': channel_summary,
        'creation_shift_summary': creation_shift_summary,
        'resolving_summary': resolving_summary,
        'processed_df': tickets
    }
    
    return metrics
