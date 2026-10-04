import pandas as pd
import numpy as np

def clean_and_merge_data(tickets_path='tickets.csv', agents_path='agents.csv', start_date=None, end_date=None):
    """
    Ingests and cleans tickets and roster data:
    1. Deduplicates tickets from migration re-import.
    2. Converts UTC timestamps to IST (+05:30).
    3. Merges agent roster dynamically using date intervals (from_date to to_date).
    4. Cleans legacy CSAT scores (0 -> NaN).
    5. Optionally filters by date range.
    """
    # Ingest tickets
    raw_tickets = pd.read_csv(tickets_path)
    
    # Sort to prioritize helpdesk system over legacy_fd on duplicate tickets
    if 'source_system' in raw_tickets.columns:
        raw_tickets = raw_tickets.sort_values(by=['ticket_id', 'source_system'], ascending=[True, False])
    tickets = raw_tickets.drop_duplicates(subset=['ticket_id'], keep='first').copy()
    
    # Convert UTC timestamps to IST (+05:30)
    for col in ['created_at', 'first_response_at', 'resolved_at']:
        if col in tickets.columns:
            tickets[f'{col}_utc'] = pd.to_datetime(tickets[col], errors='coerce')
            tickets[f'{col}_ist'] = tickets[f'{col}_utc'] + pd.Timedelta(hours=5, minutes=30)
            
    # Assign Creation Shift (IST)
    # Morning: 06:00-14:00, Day: 14:00-22:00, Night: 22:00-06:00
    created_hour = tickets['created_at_ist'].dt.hour
    
    def assign_shift(h):
        if pd.isna(h):
            return 'Unknown'
        if 6 <= h < 14:
            return 'Morning'
        elif 14 <= h < 22:
            return 'Day'
        else:
            return 'Night'
            
    tickets['created_shift_ist'] = created_hour.apply(assign_shift)
    
    # Clean CSAT: §8 of policy specifies blank means no response, legacy used 0
    if 'csat_score' in tickets.columns:
        tickets['csat_valid'] = tickets['csat_score'].replace(0, np.nan)
        
    # Ingest and join Agent Roster (agents.csv)
    agents = pd.read_csv(agents_path)
    agents['from_date'] = pd.to_datetime(agents['from_date'])
    agents['to_date'] = pd.to_datetime(agents['to_date']).fillna(pd.to_datetime('2099-12-31'))
    
    tickets['ticket_date'] = tickets['created_at_ist'].dt.normalize()
    
    merged = tickets.merge(agents, on='agent_id', how='left')
    valid_mask = (
        (merged['ticket_date'] >= merged['from_date']) &
        (merged['ticket_date'] <= merged['to_date'])
    )
    roster_assigned = merged[valid_mask].copy()
    
    # Preserve any unassigned/unmatched tickets
    missing_ids = set(tickets['ticket_id']) - set(roster_assigned['ticket_id'])
    if missing_ids:
        unmatched = tickets[tickets['ticket_id'].isin(missing_ids)].copy()
        final_df = pd.concat([roster_assigned, unmatched], ignore_index=True)
    else:
        final_df = roster_assigned
        
    # Rename 'shift' from roster for clarity
    if 'shift' in final_df.columns:
        final_df.rename(columns={'shift': 'agent_shift_roster'}, inplace=True)
        
    # Optional date filtering
    if start_date:
        final_df = final_df[final_df['created_at_ist'] >= pd.to_datetime(start_date)]
    if end_date:
        final_df = final_df[final_df['created_at_ist'] <= pd.to_datetime(end_date)]
        
    return final_df
