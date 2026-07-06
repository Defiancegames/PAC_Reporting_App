import pandas as pd
from datetime import datetime
import plotly.express as px
import os as os
import plotly.graph_objects as go
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

### consultation types ###
telephone_consultations = [
    "Telephone consultation",
    "Telephone call from a patient",
    "Telephone call to a patient",
    "Telephone encounter",
    "Telephone call to relative/carer",  # wasnt used in PAC Stats V1 - might not be needed, want to check
    "Telephone call from relative/carer"  # wasnt used in PAC Stats V1 - might not be needed, want to check

]
gp_surgery_consultations = [
    "GP Surgery"
]
home_visit_consultations = [
    "Home visit note"
]

primary_types = {'telephone_consultations':telephone_consultations, 'f2f_consultations':gp_surgery_consultations, 'home_visits':home_visit_consultations}

### Secondary care interactions ###
discharged_from_hospital = [
    "Discharged from hospital",
    "Discharge summary"
]
# do i need more codes here?!
seen_in_ae = [
    "Seen in accident and emergency department"
    ,"A&E report"
    ,"Admission to accident and emergency department"
    ,"Emergency hospital admission to accident and emergency service"
]
ambulance_attendance = [
    "Seen by ambulance crew"
]

secondary_types = {'hospital_discharges':discharged_from_hospital, 'seen_in_A&E':seen_in_ae, 'ambulance_attendances':ambulance_attendance}

ooh = [
    "Out of hour report"
    ,"NHS 111 Report"
    ,"NHS 111 service"
    ,"NHS 111 report received"
    ,"OOH report"
]

fall_incidents = [
    "Urgent care service accessed - falls incident"
    ,"Falls"
    ,"Fall from bed"
    ,"Fall from chair or bed"
    ,"Patient has had a fall"
    ,"Fall on same level due to nature of surface" # Excludes fall on travelling pavement and fall due to roller skates or skateboard
    ,"Fall on same level from slipping, tripping or stumbling"
    ,"[RFC] Reason for care : Elderly fall"
    ,"Geriatric fall"
    ,"Unexplained fall"
    ,"Fall-accidental" # Only includes: Fall in home, fall in nursing home, fall on ice, fall on or from stairs or steps, fall on same level, fell onto outstretched hand, simple fall
    ,"Recurrent falls"
]

other_comparators = {'ooh':ooh,'falls':fall_incidents}

###PACcodes

provision_of_pac = [
    'Provision of proactive care'
]

pac_declined = [
    'Proactive care needs assessment declined'
]

pac_ended = [
    'Proactive care ended'
]

#### Codes for system reporting #####
pcsp_agreed = [
    "Personalised Care and Support Plan agreed"
    ,"Care plan type (community care) : Personalised care and support plan"
]
pcsp_declined = [
    "Personalised Care and Support Planning declined"
]

cga_codes = [
    'assessment using comprehensive geriatric assessment toolkit'
    ,'holistic needs assessment'
    ,'Comprehensive proactive care needs assessment'
]

smr_codes = [
    'Structured medication review'
]

tep_codes = [
    'Treatment escalation plan'
]

adv_cp_dec_codes = [
    'Advance care planning declined'
]

frat_codes = [
    "FRAT - falls risk assessment tool"
    # "FRAT (falls risk assessment tool) score" # seen in code list but not included yet (need to speak to team)
    # "Assessment using FRAT (falls risk assessment tool)"
]

referral_for_mfra = [
    "Referral for falls risk assessment"
]

#### Codes for system reporting #####
brave_assessed = [
    'Targeted proactive care needs assessment'
]
referrals_assessed = [
    'Proactive care needs assessment'
]
provision_of_pac = [
    'Provision of proactive care'
]
not_appropriate = [
    'Proactive care needs assessment not appropriate'
]
pac_declined = [
    'Proactive care needs assessment declined'
]
pac_ended = [
    'Proactive care ended'
]

referral_cols = [
    "Referral to continence nurse",
    "Referral to mental health crisis team",
    "Referral to district nurse",
    "Referral to fire service",
    "Referral to health care assistant",
    "Referral to housing department",
    "Referral to dementia service",
    "Referral to learning disability team",
    "Referral to memory assessment service",
    "Referral to memory clinic",
    "Referral to community-based occupational therapist",
    "Referral to Parkinsons service",
    "Referral to police",
    "Referral to practice nurse",
    "Referral to social services",
    "Referral to community mental health team",
    "Referral to community rehabilitation",
    "Referral to social prescribing service",
    "Referral to advanced primary nurse",
    "Referred for health coaching",
    "Referral to mental health team",
    "Referral to older age community mental health team",
    "Referral to occupational therapist",
    "Referral to social prescribing service",
    "Referral to speech and language therapist",
    "Referral to substance abuse service",
    "Referral to independent living service",
    "Referral to Age UK",
    "Provision of telecare community alarm service",
    "Referral to domestic abuse agency"
]

ref_to_weekly_mdt = [
"Referral to community multidisciplinary care team"
]

mdt_cols = [
    # "Multidisciplinary team meeting with patient", # Used by MARMS not Community MDT
    # "Multidisciplinary team meeting without patient", # Used by MARMS not Community MDT
    "Multidisciplinary care conference"
]

ha_cols = [
    "frailty assessment",
    "Holistic needs assessment"
]

provision_of_equipment_cols = [
    "Provision of appliances",
    "Provision of equipment"
]

advance_care_cols = [
    "Advance care planning review offered",
    "Discussion about advance care planning",
    "Referred for advance care planning"
]

discharged_from_mdt = [
    'Discharge from community multidisciplinary care team'
]

falls_cols = [
    "Falls risk assessment complete",
    "Falls assessment"
    
]

frat_codes = [
    "FRAT - falls risk assessment tool"
    # "FRAT (falls risk assessment tool) score" # seen in code list but not included yet (need to speak to team)
    # "Assessment using FRAT (falls risk assessment tool)"
]

sg_colls = [
    "Adult safeguarding concern",
    "Referral to Safeguarding Adults Team",
    "Adult is subject to Section 42 enquiry",
    "Adult was not brought to appointment",
    "Referral to social services for care needs assessment"
]

capacity_decision_colls = [
    "Has the capacity to make this decision (Mental Capacity Act 2005)",
    "Lacks the capacity to make this decision (Mental Capacity Act 2005)",
    "Has appointed person with personal welfare lasting power of attorney (Mental capacity Act 2005)",
    "Best interest decision made on behalf of patient (Mental Capacity Act 2005)"
]

domestic_abuse_colls = [
    "Assessment using Domestic Abuse, Stalking and Harassment and Honour Based Violence (2009) Risk Identification and Assessment and Management Model Checklist (procedure)",
    "Referral to multi-agency risk assessment conference (procedure)",
    "Family Subject of multi-agency risk assessment conference (finding)",
    "History of Domestic Abuse",
    "Referral to Domestic Abuse agency",
    "Alleged Perpetrator of Domestic Abuse",
    "Victim of Domestic Abuse",
    "Police domestic incident report received"
]

def code_lists():
    print("to be implamented, will show codes being used")

def codes_used():
    print("to be implamented, will show codes being used")

def clean_and_combine_raw(reports):
    print("Cleaning data")
    #reports = [r[0] for r in reports]
    combined_raw = pd.DataFrame(columns=reports[0].columns)
    for raw_p in reports:
        combined_raw = pd.concat([combined_raw, raw_p])

    # Fills blank NHS numbers so i can break this into multiple tables with the NHS number as the Primary/Foregin Key
    #combined_raw = combined_raw[~combined_raw.isnull().all(axis=1)] # remove null rows caused by confidential hidden patients
    combined_raw['NHS Number'] = combined_raw['NHS Number'].ffill() 
    date_cols = ['Date of Birth','Date','Date.1', 'Date Status Added']
    combined_raw[date_cols] = combined_raw[date_cols].apply(pd.to_datetime, format="%d-%b-%Y", errors='coerce')
    combined_raw.rename(columns={'Usual GP\'s Full Name':'Usual GP',
                            'User Details\' Forenames':'User Forename',
                            'Episode (First, New...)':'Episode',
                            'User Details\' Surname':'User Surname',
                            'Date.1':'Consultation Date',
                            'Date':'Date Code Added',
                            'User Details\' User Type':'User Type'}, inplace=True)
    return combined_raw

def create_data_tables(combined_raw, pac_staff):
    print("creating dataframes")
    patients_df = combined_raw[["NHS Number", "Full Name", "Date of Birth", "Usual GP", "Registration Status", "Date Status Added", "Practice"]]
    patients_df = patients_df[~patients_df['Full Name'].isnull()]
    # drop duplicates where patient has moved within the PCN
    patients_df = patients_df.sort_values('Date Status Added', ascending=True)
    patients_df = patients_df.drop_duplicates(subset='NHS Number', keep='last')

    code_entries = combined_raw[["NHS Number", "Date Code Added", "Code Term", "Episode", "User Forename", "User Surname"]]
    code_entries = code_entries[~code_entries['Code Term'].isnull()]
    code_entries['User Forename'] = code_entries['User Forename'].str.lower().str.strip()
    code_entries['User Surname'] = code_entries['User Surname'].str.lower().str.strip()

    if len(combined_raw) > 1:
        print("accounting for patients that have move between reporting practices")
        # drop duplicates where patient has moved within the PCN
        code_entries = code_entries.merge(patients_df[['NHS Number', 'Practice']], on='NHS Number', how='left')
        code_entries = code_entries.sort_values(by=['NHS Number', 'Date Code Added'], ascending=True)
        print(f"{len(code_entries)} code entries before finding movers")
        code_entries = code_entries.drop_duplicates(keep='last')
        print(f"{len(code_entries)} code entries after")
        code_entries.drop(columns='Practice', inplace=True)

    # Consultations
    consultations = combined_raw[["NHS Number", "Consultation Date", "Type of Consultation", "User Details' Forenames.1", "User Details' Surname.1", "User Type"]]
    consultations.rename(columns={'User Details\' Forenames.1':'User Forename',
                                'User Details\' Surname.1': 'User Surname'}, inplace=True)
    consultations = consultations[~consultations['Consultation Date'].isnull()]
    consultations['User Forename'] = consultations['User Forename'].str.lower().str.strip()
    consultations['User Surname'] = consultations['User Surname'].str.lower().str.strip()

    if len(combined_raw) > 1:
        # drop duplicates where patient has moved within the PCN
        consultations = consultations.merge(patients_df[['NHS Number', 'Practice']], on='NHS Number', how='left')
        consultations = consultations.sort_values(by=['NHS Number', 'Consultation Date'], ascending=True)
        print(f"{len(consultations)} consultation berfore finding movers")
        consultations = consultations.drop_duplicates(keep='last')
        print(f"{len(consultations)} consultations after")
        consultations.drop(columns='Practice', inplace=True)

    pac_staff = pd.DataFrame(
        pac_staff,
        columns=["Forename", "Surname"]
    )

    pac_staff['Forename'] = pac_staff['Forename'].str.lower().str.strip()
    pac_staff['Surname'] = pac_staff['Surname'].str.lower().str.strip()

    # Convert to list of tuples for fast iteration
    pac_list = list(zip(
        pac_staff['Forename'],
        pac_staff['Surname']
    ))

    def is_pac(row):
        uf = str(row['User Forename'])
        us = str(row['User Surname'])

        return any(
            (pf in uf) and (ps in us)
            for pf, ps in pac_list
        )
    code_entries['Added by PAC'] = code_entries.apply(is_pac, axis=1)
    consultations['Added by PAC'] = consultations.apply(is_pac, axis=1)

    pac_code_entries = code_entries[code_entries['Added by PAC']==True].copy()

    print("identifying proactive care cases")
    casebase = pac_code_entries[(pac_code_entries['Code Term']=='Provision of proactive care') | (
        pac_code_entries['Code Term']=='Proactive care ended')].copy()
    df = casebase[casebase['Added by PAC']].copy()

    # Sort properly (so that code terms can be collapsed)
    df = df.sort_values(by=['NHS Number', 'Date Code Added', 'Code Term'], ascending=[True, True, False])

    # create event flags
    df['event'] = df['Code Term'].map({
        'Provision of proactive care': 'start',
        'Proactive care ended': 'end'
    })

    # collapse duplicate starts
    df['prev_event'] = df.groupby('NHS Number')['event'].shift()

    df_clean = df[
        (df['event'] == 'end') |
        ((df['event'] == 'start') & (df['prev_event'] != 'start'))
    ].copy()

    def build_cases(group):
        starts = group[group['event'] == 'start']
        ends = group[group['event'] == 'end']

        starts = starts.reset_index(drop=True)
        ends = ends.reset_index(drop=True)

        cases = []
        end_idx = 0

        for i, start_row in starts.iterrows():
            start_date = start_row['Date Code Added']

            # find next end AFTER this start
            while end_idx < len(ends) and ends.loc[end_idx, 'Date Code Added'] < start_date:
                end_idx += 1

            if end_idx < len(ends):
                end_date = ends.loc[end_idx, 'Date Code Added']
                end_idx += 1
            else:
                end_date = pd.NaT

            cases.append({
                'NHS Number': group.name,
                'start_date': start_date,
                'end_date': end_date
            })

        return pd.DataFrame(cases)

    case_summary = (
        df_clean.groupby('NHS Number', group_keys=False)
        .apply(build_cases)
        .reset_index(drop=True)
    )

    case_summary['duration_days'] = (
        case_summary['end_date'] - case_summary['start_date']
    ).dt.days

    most_recent_report_end = code_entries['Date Code Added'].max()
    case_summary['reporting_end'] = case_summary['end_date'].fillna(most_recent_report_end) #line might be superfluous

    last_pac_interaction = pac_code_entries.sort_values(by='Date Code Added', ascending=True).drop_duplicates(subset='NHS Number', keep='last')[['NHS Number','User Forename','User Surname']]

    last_pac_interaction['last_pac_interaction_by'] = (
        last_pac_interaction['User Forename'] + ' ' +
        last_pac_interaction['User Surname']
    )

    last_pac_interaction = last_pac_interaction.drop(columns=['User Forename', 'User Surname'])

    case_summary = case_summary.merge(last_pac_interaction, on='NHS Number', how='left')

    case_summary = case_summary.merge(patients_df[['NHS Number','Registration Status','Date Status Added','Practice']], on='NHS Number', how='left')
    case_summary['is_active'] = case_summary['end_date'].isna()

    left_open_mask = ((case_summary['is_active']==True) & (case_summary['Registration Status']=='Left'))
    case_summary.loc[left_open_mask, 'end_date'] = case_summary.loc[left_open_mask, 'Date Status Added']
    case_summary.loc[left_open_mask, 'is_active'] = False

    declines = code_entries[
            ((code_entries['Code Term']=='Proactive care needs assessment declined') | (
                code_entries['Code Term']=='Targeted proactive care needs assessment declined'
            ) & (code_entries['Added by PAC']==True))
        ][['NHS Number','Date Code Added']]

    merged = case_summary.merge(
        declines,
        on = 'NHS Number',
        how= 'left',
        suffixes= ('', '_dec')
    )

    mask = (
        ((merged['Date Code Added'] >= merged['start_date']) &
        (merged['Date Code Added'] <= merged['end_date'])) |
        ((merged['Date Code Added'] >= merged['start_date']) &
        (merged['end_date'].isna()))
    )

    decs_in_cases = merged[mask].copy()

    decs_in_cases['drop_me'] = True

    case_summary = case_summary.merge(
        decs_in_cases[['NHS Number', 'start_date', 'drop_me']],
        on=['NHS Number', 'start_date'],
        how='left'
    )

    case_summary = case_summary[case_summary['drop_me'] != True]
    case_summary = case_summary.drop(columns='drop_me')

    long_duration = case_summary[(~case_summary['duration_days'].isna()) & (case_summary['duration_days'] > 3)]['duration_days'].quantile(0.85)
    long_duration

    today = pd.Timestamp.today().normalize()

    case_summary['open_duration_days'] = (
        today - case_summary['start_date']
    ).dt.days


    case_summary['long_active_flag'] = (
        case_summary['is_active'] &
        (case_summary['open_duration_days'] > long_duration)
    )

    case_summary.drop(columns='open_duration_days', inplace=True)

    case_summary['minor_intervention'] = (~case_summary['duration_days'].isna()) & (case_summary['duration_days'] < 4)
    print("creating reporting periods")
    case_summary['window_start_12m'] = case_summary['start_date'] - pd.DateOffset(months=12)
    case_summary['lagged_start_12m'] = case_summary['start_date'] + pd.DateOffset(months=2)
    case_summary['window_start_6m'] = case_summary['start_date'] - pd.DateOffset(months=6)
    case_summary['window_start_3m'] = case_summary['start_date'] - pd.DateOffset(months=3)
    case_summary['lagged_end_12m'] = case_summary['lagged_start_12m'] + pd.DateOffset(months=12)
    case_summary['window_end_6m'] = case_summary['end_date'] + pd.DateOffset(months=6)
    case_summary['window_end_3m'] = case_summary['end_date'] + pd.DateOffset(months=3)

    case_summary['3m_reportable'] = (
        case_summary['window_end_3m'] < most_recent_report_end) & ((                        # Ensures reporting window is before search was last run
            (case_summary['Registration Status'] != 'Left') & (                             # Ensures patient hasnt left the practice
                case_summary['Date Status Added'] < case_summary['window_end_3m'])) | ((    # Ensures the registration status of the patient is before the with end
                    case_summary['Registration Status'] == 'Left') & (                      # Checks to make sure if they have left that the status is after reporting window
                        case_summary['Date Status Added'] > case_summary['window_end_3m'])
                )
        )
    case_summary['6m_reportable'] = (
        case_summary['window_end_6m'] < most_recent_report_end) & ((
            (case_summary['Registration Status'] != 'Left') & (
                case_summary['Date Status Added'] < case_summary['window_end_6m'])) | ((
                    case_summary['Registration Status'] == 'Left') & (
                        case_summary['Date Status Added'] > case_summary['window_end_6m'])
                )
        )

    case_summary['12m_reportable'] = (
        case_summary['lagged_end_12m'] < most_recent_report_end) & ((
            (case_summary['Registration Status'] != 'Left') & (
                case_summary['Date Status Added'] < case_summary['lagged_end_12m'])) | ((
                    case_summary['Registration Status'] == 'Left') & (
                        case_summary['Date Status Added'] > case_summary['lagged_end_12m'])
                )
        )

    for period in ['3m', '6m', '12m']:
        match period:
            case '3m':
                window_start = 'window_start_3m'
                post_start =  'end_date'
                window_end = 'window_end_3m'
            case '6m':
                window_start = 'window_start_6m'
                post_start =  'end_date'
                window_end = 'window_end_6m'
            case '12m':
                window_start = 'window_start_12m'
                post_start =  'lagged_start_12m'
                window_end = 'lagged_end_12m'

        for type_of_con, code_list in primary_types.items():
            code_list = [x.lower() for x in code_list]
            con_df = consultations[
                consultations['Type of Consultation'].str.lower().isin(code_list)
            ]

            merged = case_summary.merge(
                con_df,
                on = 'NHS Number',
                how= 'left',
                suffixes= ('', '_con')
            )

            prior_mask = (
                (merged['Consultation Date'] >= merged[window_start]) &
                (merged['Consultation Date'] <= merged['start_date'])
            )

            prior_merged = merged[prior_mask].copy()

            post_mask = (
                (merged['Consultation Date'] >= merged[post_start]) &
                (merged['Consultation Date'] <= merged[window_end])
            )

            post_merged = merged[post_mask].copy()

            for mdfn, mdf in {'prior':prior_merged, 'post':post_merged}.items():
                count_of_con = (
                    mdf.groupby(['NHS Number', 'start_date'])
                    .size()
                    .rename(f'{type_of_con}_{mdfn}_{period}')
                    .reset_index()
                )

                case_summary = case_summary.merge(
                    count_of_con,
                    on=['NHS Number', 'start_date'],
                    how='left'
                )

                case_summary[f'{type_of_con}_{mdfn}_{period}'] = case_summary[f'{type_of_con}_{mdfn}_{period}'].fillna(0).astype(int)
            case_summary[f'{type_of_con}_diff_{period}'] = case_summary[f'{type_of_con}_post_{period}'] - case_summary[f'{type_of_con}_prior_{period}']

    for period in ['3m', '6m', '12m']:
        match period:
            case '3m':
                window_start = 'window_start_3m'
                post_start =  'end_date'
                window_end = 'window_end_3m'
            case '6m':
                window_start = 'window_start_6m'
                post_start =  'end_date'
                window_end = 'window_end_6m'
            case '12m':
                window_start = 'window_start_12m'
                post_start =  'lagged_start_12m'
                window_end = 'lagged_end_12m'

        for type_of_code, code_list in secondary_types.items():
            code_list = [x.lower() for x in code_list]
            code_df = code_entries[
                code_entries['Code Term'].str.lower().isin(code_list)
            ]
            merged = case_summary.merge(
                code_df,
                on='NHS Number',
                how='left',
                suffixes=('', '_discharge')
            )

            prior_mask = (
                (merged['Date Code Added'] >= merged[window_start]) &
                (merged['Date Code Added'] <= merged['start_date'])
            )

            prior_merged = merged[prior_mask].copy()

            post_mask = (
                (merged['Date Code Added'] >= merged[post_start]) &
                (merged['Date Code Added'] <= merged[window_end])
            )

            post_merged = merged[post_mask].copy()

            for mdfn, mdf in {'prior':prior_merged, 'post':post_merged}.items():
                count_of_code = (
                    mdf.groupby(['NHS Number', 'start_date'])
                    .size()
                    .rename(f'{type_of_code}_{mdfn}_{period}')
                    .reset_index()
                )

                case_summary = case_summary.merge(
                    count_of_code,
                    on=['NHS Number', 'start_date'],
                    how='left'
                )

                case_summary[f'{type_of_code}_{mdfn}_{period}'] = case_summary[f'{type_of_code}_{mdfn}_{period}'].fillna(0).astype(int)
            case_summary[f'{type_of_code}_diff_{period}'] = case_summary[f'{type_of_code}_post_{period}'] - case_summary[f'{type_of_code}_prior_{period}']   
            
    for period in ['3m', '6m', '12m']:
        match period:
            case '3m':
                window_start = 'window_start_3m'
                post_start =  'end_date'
                window_end = 'window_end_3m'
            case '6m':
                window_start = 'window_start_6m'
                post_start =  'end_date'
                window_end = 'window_end_6m'
            case '12m':
                window_start = 'window_start_12m'
                post_start =  'lagged_start_12m'
                window_end = 'lagged_end_12m'

        for type_of_code, code_list in other_comparators.items():
            code_list = [x.lower() for x in code_list]
            code_df = code_entries[
                code_entries['Code Term'].str.lower().isin(code_list)
            ]
            merged = case_summary.merge(
                code_df,
                on='NHS Number',
                how='left',
                suffixes=('', '_discharge')
            )

            prior_mask = (
                (merged['Date Code Added'] >= merged[window_start]) &
                (merged['Date Code Added'] <= merged['start_date'])
            )

            prior_merged = merged[prior_mask].copy()

            post_mask = (
                (merged['Date Code Added'] >= merged[post_start]) &
                (merged['Date Code Added'] <= merged[window_end])
            )

            post_merged = merged[post_mask].copy()

            for mdfn, mdf in {'prior':prior_merged, 'post':post_merged}.items():
                count_of_code = (
                    mdf.groupby(['NHS Number', 'start_date'])
                    .size()
                    .rename(f'{type_of_code}_{mdfn}_{period}')
                    .reset_index()
                )

                case_summary = case_summary.merge(
                    count_of_code,
                    on=['NHS Number', 'start_date'],
                    how='left'
                )

                case_summary[f'{type_of_code}_{mdfn}_{period}'] = case_summary[f'{type_of_code}_{mdfn}_{period}'].fillna(0).astype(int)
            case_summary[f'{type_of_code}_diff_{period}'] = case_summary[f'{type_of_code}_post_{period}'] - case_summary[f'{type_of_code}_prior_{period}'] 
    for period in ['3m', '6m', '12m']:
        primary_diff = 0
        for type_of_con, code_list in primary_types.items():
            primary_diff += case_summary[f'{type_of_con}_diff_{period}']
        case_summary[f'primary_diff_{period}'] = primary_diff

    for period in ['3m', '6m', '12m']:
        secondary_diff = 0
        for type_of_con, code_list in secondary_types.items():
            secondary_diff += case_summary[f'{type_of_con}_diff_{period}']
        case_summary[f'secondary_diff_{period}'] = secondary_diff 
    dataframes = {'patients':patients_df,
                  'code_entries':code_entries,
                  'pac_code_entries': pac_code_entries,
                  'consultations':consultations,
                  'case_summary':case_summary}
    return dataframes

def _flag_against_coded_history(dataframes, codes:list, metric:str, date_range=0, mode='from_end'):
    print(f"flagging {metric} events")
    codes = [txt.lower() for txt in codes]
    # check for codes
    code_entries = dataframes['code_entries']
    case_summary = dataframes['case_summary']
    df_coded_history = code_entries[
        code_entries['Code Term'].str.lower().isin(codes)
    ][['NHS Number', 'Date Code Added']].copy()

    merged = case_summary.merge(
        df_coded_history,
        on='NHS Number',
        how='left',
        suffixes=('', f'_{metric}')
    )
    # will look for codes added before the start date (PAC intervention),
    # if a range is passed it will look between the start date and the date range before (in months)
    if mode == 'from_start':
        if date_range == 0:
            merged[f'{metric}_valid'] = (
                merged['Date Code Added'] <= merged['start_date']
            )
        else:
            merged['range_start']= merged['start_date'] - pd.offsets.MonthBegin(date_range)
            merged[f'{metric}_valid'] = (
                (merged['Date Code Added'] <= merged['start_date']) &
                (merged['Date Code Added'] >= merged['range_start'])
            )
    # if the mode is from_end then it will look for the codes added before the reporting end date (or latest date if still active)
    # if a range is passed then it will look for codes between the reporting end date and x amount of months before that.
    elif mode == 'from_end':
        if date_range == 0:
            merged[f'{metric}_valid'] = (
                merged['Date Code Added'] <= merged['reporting_end']
            )
        else:
            merged['range_start']= merged['reporting_end'] - pd.offsets.MonthBegin(date_range)
            merged[f'{metric}_valid'] = (
                (merged['Date Code Added'] <= merged['reporting_end']) &
                (merged['Date Code Added'] >= merged['range_start'])
            )
    # if the mode is during it will look for codes between start and end dates of cases (includes active cases)
    # if a range is passed it will shift the start date back by that many months
    elif mode == 'during':
        if date_range == 0:
            merged[f'{metric}_valid'] = (
                (merged['Date Code Added'] <= merged['reporting_end']) &
                (merged['Date Code Added'] >= merged['start_date'])
            )
        else:
            merged['range_start']= merged['start_date'] - pd.offsets.MonthBegin(date_range)
            merged[f'{metric}_valid'] = (
                (merged['Date Code Added'] <= merged['reporting_end']) &
                (merged['Date Code Added'] >= merged['range_start'])
            )
    else:
        os.error('mode not recognised use from_start, from_end or during')

    flag = (
        merged.groupby(['NHS Number', 'start_date'])
        .agg(in_place=(f'{metric}_valid', 'max'))
        .reset_index()
    )

    # Merge back in
    case_summary = case_summary.merge(
        flag,
        on=['NHS Number', 'start_date'],
        how='left'
    )

    case_summary['in_place'] = case_summary['in_place'].fillna(False)
    case_summary.rename(columns={'in_place':f'{metric}_in_place'}, inplace=True)
    dataframes['case_summary'] = case_summary
    return dataframes

def flag_history(dataframes):
    _flag_against_coded_history(dataframes, codes=pcsp_agreed, mode='during', metric='pcsp', date_range=3)
    _flag_against_coded_history(dataframes, codes=pcsp_declined, metric='pcsp_declined', mode='during', date_range=3)
    _flag_against_coded_history(dataframes, codes=cga_codes, metric='cga', date_range=18) 
    _flag_against_coded_history(dataframes, codes=smr_codes, metric='smr', date_range=12)
    _flag_against_coded_history(dataframes, codes=frat_codes, metric='frat')
    _flag_against_coded_history(dataframes, codes=falls_cols, metric='mfra')
    _flag_against_coded_history(dataframes, codes=referral_for_mfra, metric='mfra_referral', mode='during', date_range=2)
    _flag_against_coded_history(dataframes, codes=tep_codes, metric='tep')
    _flag_against_coded_history(dataframes, codes=adv_cp_dec_codes, metric='tep_declined', mode='during', date_range=6)
    _flag_against_coded_history(dataframes, codes=advance_care_cols, metric='tep_discussed', mode='during')
    _flag_against_coded_history(dataframes, codes=brave_assessed, metric='brave_pt', date_range=3, mode='from_start')
    _flag_against_coded_history(dataframes, codes=referrals_assessed, metric='referred_pt', date_range=2, mode='from_start')

def create_icb_report(dataframes, exclude_minor_intervention=False, brave_monthly=None):
    print("creating metrics data")
    case_summary = dataframes['case_summary']
    pac_code_entries = dataframes['pac_code_entries']
    row_list = ['Active caseload'
                ,'Cases Closed'] 

    # date range from April 2026 to current month ---
    start_date = '2025-04-01'
    end_date = datetime.today().replace(day=1)  # start of current month

    # Generate monthly dates
    columns = pd.date_range(start=start_date, end=end_date, freq='MS')
    columns = columns.strftime('%Y-%m')

    # --- create dataframe ---
    icb_report = pd.DataFrame(index=row_list, columns=columns)


    date_range = pd.date_range(
        case_summary['start_date'].min(),
        case_summary['reporting_end'].max(),
        freq='MS'   # Month start
    )

    months = pd.DataFrame({'month_start': date_range})
    months['month_end'] = months['month_start'] + pd.offsets.MonthEnd(0)

    # create a key to cross join every case to every month
    case_summary['_key'] = 1
    months['_key'] = 1

    expanded = case_summary.merge(months, on='_key').drop('_key', axis=1)

    # Work out if case is active in that month
    active_mask = (
        (expanded['start_date'] <= expanded['month_end']) &
        (expanded['reporting_end'] >= expanded['month_start'])
    )

    # Filter and count
    expanded['active_in_month'] = active_mask
    active_cases = expanded[expanded['active_in_month']].copy()

    monthly_active = (
        active_cases 
        .groupby('month_start')
        .size()
        .rename('active_cases')
        #.reset_index()
    )
    monthly_active.index = monthly_active.index.to_period('M')
    # Convert index to match your dataframe column format (YYYY-MM)
    monthly_active.index = monthly_active.index.astype(str)

    # Align with your dataframe columns
    monthly_active = monthly_active.reindex(icb_report.columns, fill_value=0)

    # Assign to Caseload row
    icb_report.loc['Active caseload'] = monthly_active

    active_percent_stats = {'PCSP Coverage %':'pcsp_in_place'
                 ,'PCSP Declined Coverage %':'pcsp_declined_in_place'
                 ,'CGA Coverage %':'cga_in_place'
                 ,'SMR Coverage %':'smr_in_place'
                 ,'FRAT scored Coverage %':'frat_in_place'
                 ,'MFRA Coverage %':'mfra_in_place'
                 ,'MFRA referral Coverage %':'mfra_referral_in_place'
                 ,'TEP Coverage %':'tep_in_place'
                 ,'TEPs Declined Coverage %':'tep_declined_in_place'}
    
    for stat, flag in active_percent_stats.items():
        # Aggregate totals 
        monthly_pcsp = active_cases.groupby('month_start').agg(
            total_cases=('NHS Number', 'count'),
            flagged_cases=(flag, 'sum')  # True = 1 for the purposes of the sum
        )

        # Calculate %
        monthly_pcsp[stat] = ((
            monthly_pcsp['flagged_cases'] /
            monthly_pcsp['total_cases']
        )*100).round(1)

        # Merge into icb report
        monthly_pcsp.index = monthly_pcsp.index.to_period('M').astype(str)
        monthly_pcsp = monthly_pcsp.reindex(icb_report.columns, fill_value=0)
        icb_report.loc[stat] = monthly_pcsp[stat]
    
    closed_percent_stats = {'PCSP % Complete of Closed':'pcsp_in_place' ,'CGA % Complete of Closed':'cga_in_place'}

    for stat, flag in closed_percent_stats.items():
        closed_cases = case_summary[case_summary['end_date'].notna()].copy()   
        closed_cases['month'] = closed_cases['end_date'].dt.to_period('M')

        # Aggregate totals 
        monthly_pcsp = closed_cases.groupby('month').agg(
            total_cases=('NHS Number', 'count'),
            flagged_cases=(flag, 'sum')
        )

        # Calculate %
        monthly_pcsp[stat] = (
            (monthly_pcsp['flagged_cases'] / monthly_pcsp['total_cases']) * 100
        ).round(1)

        # Merge into icb report
        monthly_pcsp.index = monthly_pcsp.index.astype(str)
        monthly_pcsp = monthly_pcsp.reindex(icb_report.columns, fill_value=0)
        icb_report.loc[stat] = monthly_pcsp[stat]

    counted_stats = {'PCSPs By Month':'pcsp_in_place'
                    ,'CGAs By Month':'cga_in_place'
                    ,'SMRs By Month':'smr_in_place'
                    ,'FRAT Scored By Month':'frat_in_place'
                    ,'MFRAs By Month':'mfra_in_place'
                    ,'MFRA Referrals By Month':'mfra_referral_in_place'
                    ,'TEPs By Month':'tep_in_place'
                    ,'TEP Discussions By Month':'tep_discussed_in_place'
                    ,'TEPs Declined By Month':'tep_declined_in_place'}
    
    for stat, flag in counted_stats.items():
            
        s = case_summary[case_summary[flag]==True]['end_date'].copy() # this will pick up on pts that have died

        # 1. Count by year-month
        monthly_counts = (
            s.dropna()
            .dt.to_period('M')       # convert to Year-Month
            .value_counts()
            .sort_index()
        )

        # 2. Convert index to match your dataframe column format (YYYY-MM)
        monthly_counts.index = monthly_counts.index.astype(str)

        # 3. Align with your dataframe columns
        monthly_counts = monthly_counts.reindex(icb_report.columns, fill_value=0)

        # 4. Assign to relevent row
        icb_report.loc[stat] = monthly_counts

    for rn, cnl in {
        'Brave assessed':brave_assessed
        ,'Referrals assessed':referrals_assessed
        ,'Provision of proactive care': provision_of_pac
        ,'PAC not appropriate': not_appropriate
        ,'Proactive care needs assessment delcined': pac_declined
        ,'PAC Ended codes added': pac_ended
        ,'Referrals onwards': referral_cols
        ,'Referral to weekly MDT': ref_to_weekly_mdt
        ,'Discharged from MDT': discharged_from_mdt
        ,'Discussions about Adv care planning' : advance_care_cols
        ,'Safeguarding adults': sg_colls
    }.items():
        cnl = [x.lower() for x in cnl]
        df_tmp = pac_code_entries[
            pac_code_entries['Code Term'].str.lower().isin(cnl)
        ].copy()
        df_tmp['month'] = df_tmp['Date Code Added'].dt.to_period('M')
        df_tmp_monthly = df_tmp.groupby('month')['NHS Number'].nunique()
        df_tmp_monthly.index = df_tmp_monthly.index.astype(str)
        df_tmp_monthly = df_tmp_monthly.reindex(
            icb_report.columns,
            fill_value=0
        )
        icb_report.loc[rn] = df_tmp_monthly

    if brave_monthly is not None:
        brave_monthly.index = brave_monthly.index.astype(str)
        brave_monthly = brave_monthly.reindex(icb_report.columns, fill_value=0)
        icb_report.loc['Brave Identified'] = brave_monthly['Identified']

    cases_closed = case_summary[['NHS Number']].groupby(case_summary.end_date.dt.to_period('M')).count()
    cases_closed.index = cases_closed.index.astype(str)
    cases_closed = cases_closed.reindex(icb_report.columns, fill_value=0)
    icb_report.loc['Cases Closed'] = cases_closed['NHS Number']

    pcsp_declined_monthly = case_summary[(case_summary['pcsp_declined_in_place']==True) & (case_summary['pcsp_in_place']==False)]['NHS Number'].groupby(case_summary.end_date.dt.to_period('M')).count()
    pcsp_declined_monthly.index = pcsp_declined_monthly.index.astype(str)
    pcsp_declined_monthly = pcsp_declined_monthly.reindex(icb_report.columns, fill_value=0)
    icb_report.loc['PCSPs Declined'] = pcsp_declined_monthly

    for cn, c in {
        'Change in falls':'falls_diff_12m',
        'Change in OOH':'ooh_diff_12m',
        'Change in GP demand':'primary_diff_12m',
        'Change in Secondary':'secondary_diff_12m'}.items():
        if exclude_minor_intervention:
            comparrison = case_summary[(case_summary['12m_reportable']==True) & (case_summary['minor_intervention']==False)][c].groupby(
                case_summary.lagged_end_12m.dt.to_period('M')
            ).sum()
        else:
            comparrison = case_summary[(case_summary['12m_reportable']==True)][c].groupby(
                case_summary.lagged_end_12m.dt.to_period('M')
            ).sum()

        comparrison.index = comparrison.index.astype(str)
        comparrison = comparrison.reindex(icb_report.columns, fill_value=0)
        icb_report.loc[cn] = comparrison

    extended_report_export = icb_report.loc[['Brave assessed'
                                        ,'Referrals assessed'
                                        ,'PAC not appropriate'
                                        ,'Provision of proactive care'
                                        ,'Proactive care needs assessment delcined'
                                        ,'PAC Ended codes added'
                                        ,'Active caseload'
                                        ,'Cases Closed'
                                        ,'PCSP Coverage %'
                                        ,'PCSPs Declined'
                                        ,'CGA Coverage %'
                                        ,'SMR Coverage %'
                                        ,'FRAT scored Coverage %'
                                        ,'MFRA Coverage %'
                                        ,'MFRA referral Coverage %'
                                        ,'TEP Coverage %'
                                        ,'TEPs Declined Coverage %'
                                        ,'Discussions about Adv care planning'
                                        ,'PCSP % Complete of Closed'
                                        ,'CGA % Complete of Closed'
                                        ,'Change in GP demand'
                                        ,'Change in Secondary'
                                        ,'Change in OOH'
                                        ,'Change in falls'
                                        ,'Referrals onwards'
                                        ,'Referral to weekly MDT'
                                        ,'Discharged from MDT'
                                        ,'Safeguarding adults']]
    if brave_monthly is not None:
        brave_row = icb_report.loc[['Brave Identified']]
        extended_report_export = pd.concat([brave_row, extended_report_export])

    icb_report_export = icb_report.loc[['Referrals assessed'
                                        ,'Provision of proactive care'
                                        ,'Active caseload'
                                        ,'Cases Closed'
                                        ,'PCSP Coverage %'
                                        ,'PCSP Declined Coverage %'
                                        ,'CGA Coverage %'
                                        ,'SMR Coverage %'
                                        ,'FRAT scored Coverage %'
                                        ,'MFRA Coverage %'
                                        ,'MFRA referral Coverage %'
                                        ,'TEP Coverage %'
                                        ,'PCSP % Complete of Closed'
                                        ,'CGA % Complete of Closed'
                                        ,'Change in GP demand'
                                        ,'Change in Secondary'
                                        ,'Change in OOH'
                                        ,'Change in falls']]
    if brave_monthly is not None:
        brave_row = icb_report.loc[['Brave Identified']]
        icb_report_export = pd.concat([brave_row, icb_report_export])
    return icb_report_export.drop(columns=end_date.strftime('%Y-%m')), extended_report_export.drop(columns=end_date.strftime('%Y-%m'))

def full_process(reports, pac_staff, exclude_minor_intervention = False, brave_monthly=None, graph=False):
    loaded_reports = []
    for report in reports:
        df = pd.read_html(report["path"])[0]
        df = df[~df.isnull().all(axis=1)]
        df["Practice"] = report["practice"]
        loaded_reports.append(df)
    combined_raw = clean_and_combine_raw(loaded_reports)
    dfs = create_data_tables(combined_raw, pac_staff)
    flag_history(dfs)
    icb_report_export, extended_report_export = create_icb_report(dfs, exclude_minor_intervention, brave_monthly)
    missing_pac_ended, missing_pcsp = assess_coding(dfs)
    # write_report_to_path(icb_report_export, extended_report_export, missing_pac_ended, missing_pcsp, export_path)
    dfs["missing_pac_ended"] = missing_pac_ended
    dfs["missing_pcsp"] = missing_pcsp
    if graph:
        boxgraph(dfs)
        practice_distribution(dfs)
    return_dfs = {
        "missing_pac_ended" : missing_pac_ended,
        "missing_pcsp" : missing_pcsp,
        "icb_report_export" : icb_report_export,
        "extended_report_export" : extended_report_export,
        "cases" : dfs['case_summary'][dfs['case_summary']["start_date"] > datetime.today().replace(day=1) - pd.DateOffset(months=12)]
    }
    print("complete!")
    return return_dfs

def practice_distribution(dfs):
    case_history = dfs['case_summary']
    case_history_last_12m = case_history[case_history["start_date"] > datetime.today().replace(day=1) - pd.DateOffset(months=12)]
    practice_dist = (
        case_history_last_12m
        .groupby(
            [
                case_history_last_12m["start_date"].dt.to_period('M'),
                "Practice",
                "brave_pt_in_place"
            ]
        )["NHS Number"]
        .count()
        .unstack(fill_value=0)
        .rename(
            columns={
                False: "Practice_Referred",
                True: "Brave_Patient"
            }
        )
        .reset_index()
    )
    plot_df = practice_dist.melt(
        id_vars=['start_date', 'Practice'],
        value_vars=['Practice_Referred', 'Brave_Patient'],
        var_name='Source',
        value_name='Count'
    )

    plot_df['start_date'] = plot_df['start_date'].astype(str)

    fig = go.Figure()

    practices = plot_df['Practice'].unique()

    palette = px.colors.qualitative.D3

    practice_colours = {
        practice: palette[i % len(palette)]
        for i, practice in enumerate(sorted(practices))
    }

    for practice in practices:

        for source in ['Practice_Referred', 'Brave_Patient']:

            tmp = plot_df[
                (plot_df['Practice'] == practice) &
                (plot_df['Source'] == source)
            ]

            fig.add_bar(
                x=[
                    tmp['start_date'],
                    tmp['Source']
                ],
                y=tmp['Count'],
                name=practice,
                legendgroup=practice,
                showlegend=(source == 'Practice_Referred'),
                marker_color=practice_colours[practice],
                offsetgroup=source,
            )

    fig.update_layout(
        barmode='stack',
        title='PAC Starts by Source and Practice',
        xaxis_title='Month',
        yaxis_title='Patients',
        legend_title='Practice',
        height=700
    )

    fig.show()


def write_report_to_path(icb,extended,pac_ended,pcsp,path):
    
    if os.path.exists(path):
        with pd.ExcelWriter(path,
                            mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            icb.to_excel(writer, sheet_name="ICB")
            extended.to_excel(writer, sheet_name="Expanded")
            pac_ended.to_excel(writer, sheet_name="Missing PAC Ended")
            pcsp.to_excel(writer, sheet_name="Missing PCSP")

        print(f"Updated file located {path}")
    else:
        with pd.ExcelWriter(path,
                            mode="w", engine="openpyxl") as writer:
            icb.to_excel(writer, sheet_name="ICB")
            extended.to_excel(writer, sheet_name="Expanded")
            pac_ended.to_excel(writer, sheet_name="Missing PAC Ended")
            pcsp.to_excel(writer, sheet_name="Missing PCSP")
        print(f"Report file written to {path}")

def assess_coding(dfs):
    #possibly missing PAC end coding
    case_summary = dfs['case_summary']
    missing_provision = case_summary[case_summary['long_active_flag']==True][['Practice', 'NHS Number', 'start_date', 'last_pac_interaction_by']].sort_values(by=['last_pac_interaction_by','Practice', 'start_date'])
    missing_pcsp = case_summary[
        (case_summary['end_date'] > (datetime.today().replace(day=1) - pd.DateOffset(months=12))) &
        (~case_summary['is_active']) &
        (~case_summary['pcsp_in_place']) &
        (~case_summary['pcsp_declined_in_place']) &
        (~case_summary['duration_days'].isna())
        ].sort_values(by='reporting_end', ascending=False)[[
            'Practice',
            'NHS Number',
            'start_date',
            'last_pac_interaction_by',
            'Registration Status',
            'Date Status Added',
            'minor_intervention',
            'pcsp_in_place',
            'pcsp_declined_in_place',
            'tep_in_place',
            'tep_declined_in_place'
        ]].head(30)
    return missing_provision, missing_pcsp

def boxgraph(dfs):

    df_plot = dfs['case_summary'].copy()
    df_plot = df_plot[df_plot['12m_reportable']==True][['falls_diff_12m', 'ooh_diff_12m', 'primary_diff_12m', 'secondary_diff_12m', 'pcsp_in_place']]

    df_plot.rename(columns={'falls_diff_12m':'Change in falls',
                            'ooh_diff_12m':'Change in OOH',
                            'primary_diff_12m':'Change in GP demand',
                            'secondary_diff_12m':'Change in Secondary'})

    df_long = df_plot.melt(
        id_vars='pcsp_in_place',
        var_name='Metric',
        value_name='Value'
    )
    
    df_long['PCSP'] = df_long['pcsp_in_place'].map({
        True: 'PCSP in place',
        False: 'No PCSP'
    })

    fig = px.box(
        df_long,
        x='Metric',
        y='Value',
        color='PCSP',
        points='all' 
    )

    fig.update_xaxes(categoryorder='array', categoryarray=['Change in GP demand', 'Change in Secondary', 'Change in OOH', 'Change in falls'])
    fig.show()


def run_report():

    icb = pd.DataFrame({
        "2026-04":[100],
        "2026-05":[110]
    }, index=["Active Caseload"])

    missing_pac = pd.DataFrame({
        "Practice":["TVHC"],
        "NHS Number":["1234567890"]
    })

    missing_pcsp = pd.DataFrame({
        "Practice":["CMC"],
        "NHS Number":["9999999999"]
    })

    return (
        icb,
        missing_pac,
        missing_pcsp
    )

__all__ = [
    "full_process",
    "clean_and_combine_raw",
    "create_data_tables",
    "flag_history",
    "create_icb_report"
    "practice_distribution"
]
