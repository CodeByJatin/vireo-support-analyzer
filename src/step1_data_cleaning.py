import pandas as pd
import numpy as np

def run_step1():
    print("=== STEP 1: DATA INGESTION & CLEANING ===")
    
    # 1. Load tickets
    raw_tickets = pd.read_csv('tickets.csv')
    initial_rows = len(raw_tickets)
    print(f"1. Ingested tickets.csv: {initial_rows} rows")
    
    # 2. Deduplicate tickets
    # Sameer noted: 'Some tickets appear twice from the migration re-import'
    # Keep the last record or helpdesk record if duplicate
    # Let's sort so 'helpdesk' source_system is preferred over 'legacy_fd'
    raw_tickets = raw_tickets.sort_values(by=['ticket_id', 'source_system'], ascending=[True, False])
    tickets = raw_tickets.drop_duplicates(subset=['ticket_id'], keep='first').copy()
    duplicates_removed = initial_rows - len(tickets)
    print(f"2. Deduplication: Removed {duplicates_removed} duplicate rows. Remaining unique tickets: {len(tickets)}")
    
    # 3. Timezone conversion: UTC to IST (+5 hours 30 minutes)
    for col in ['created_at', 'first_response_at', 'resolved_at']:
        tickets[f'{col}_utc'] = pd.to_datetime(tickets[col], errors='coerce')
        tickets[f'{col}_ist'] = tickets[f'{col}_utc'] + pd.Timedelta(hours=5, minutes=30)
    
    print("3. Timezone conversion: Converted created_at, first_response_at, resolved_at from UTC to IST (+05:30).")
    
    # 4. Assign Creation Shift (IST)
    # Morning: 06:00 to 14:00 IST
    # Day: 14:00 to 22:00 IST
    # Night: 22:00 to 06:00 IST
    created_hour = tickets['created_at_ist'].dt.hour
    
    def get_shift(hour):
        if pd.isna(hour):
            return 'Unknown'
        if 6 <= hour < 14:
            return 'Morning'
        elif 14 <= hour < 22:
            return 'Day'
        else:
            return 'Night'
            
    tickets['created_shift_ist'] = created_hour.apply(get_shift)
    
    # 5. Calculate First Response Time (in minutes)
    tickets['response_time_minutes'] = (
        (tickets['first_response_at_utc'] - tickets['created_at_utc']).dt.total_seconds() / 60.0
    )
    
    # 6. Apply SLA Targets by Channel (support-policy.pdf §3)
    # Chat: 15 min, Voice: 120 min (2h), Social: 240 min (4h), Email: 480 min (8h)
    sla_map = {
        'chat': 15.0,
        'voice': 120.0,
        'social': 240.0,
        'email': 480.0
    }
    tickets['sla_target_minutes'] = tickets['channel'].map(sla_map)
    tickets['is_breach'] = tickets['response_time_minutes'] > tickets['sla_target_minutes']
    
    # 7. Merge Agent Roster by Date (agents.csv)
    # The roster has from_date and to_date because agents moved in June
    agents = pd.read_csv('agents.csv')
    agents['from_date'] = pd.to_datetime(agents['from_date'])
    agents['to_date'] = pd.to_datetime(agents['to_date']).fillna(pd.to_datetime('2099-12-31'))
    
    # Extract ticket creation date for matching
    tickets['ticket_date'] = tickets['created_at_ist'].dt.normalize()
    
    # Merge agents with date interval check
    merged_tickets = tickets.merge(agents, on='agent_id', how='left')
    valid_assignment = (
        (merged_tickets['ticket_date'] >= merged_tickets['from_date']) &
        (merged_tickets['ticket_date'] <= merged_tickets['to_date'])
    )
    # Filter to only the valid roster assignment matching the date
    resolved_roster = merged_tickets[valid_assignment].copy()
    
    # In case any ticket didn't match an interval (or agent_id is blank), preserve it
    missing_ids = set(tickets['ticket_id']) - set(resolved_roster['ticket_id'])
    if missing_ids:
        unmatched = tickets[tickets['ticket_id'].isin(missing_ids)].copy()
        final_df = pd.concat([resolved_roster, unmatched], ignore_index=True)
    else:
        final_df = resolved_roster
        
    print(f"4. Roster joined by effective dates: {len(final_df)} tickets matched with agent shift/tier/site.")
    
    # 8. Clean CSAT score:
    # Legacy system used 0 for no response; new system leaves blank.
    # Exclude 0 and NaN from valid CSAT calculations as per §8.
    final_df['csat_valid'] = final_df['csat_score'].replace(0, np.nan)
    
    # 9. Save cleaned dataset
    final_df.to_csv('cleaned_tickets.csv', index=False)
    print("5. Successfully saved cleaned data to cleaned_tickets.csv\n")
    
    # Summary Metrics
    print("--- KEY STATS SUMMARY ---")
    print(f"Total Unique Tickets: {len(final_df)}")
    print(f"Total Breaches: {final_df['is_breach'].sum()} ({final_df['is_breach'].mean()*100:.2f}%)")
    print("\nBreaches by Channel:")
    print(final_df.groupby('channel')['is_breach'].agg(Total='count', Breaches='sum', BreachRate=lambda x: f"{x.mean()*100:.1f}%"))
    
    print("\nBreaches by CREATION Shift (IST):")
    print(final_df.groupby('created_shift_ist')['is_breach'].agg(Total='count', Breaches='sum', BreachRate=lambda x: f"{x.mean()*100:.1f}%"))
    
    if 'shift' in final_df.columns:
        print("\nBreaches by RESOLVING AGENT Shift (on roster):")
        print(final_df.groupby('shift')['is_breach'].agg(Total='count', Breaches='sum', BreachRate=lambda x: f"{x.mean()*100:.1f}%"))

if __name__ == '__main__':
    run_step1()
