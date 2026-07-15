**Installation**

Go to releases https://github.com/Defiancegames/PAC_Reporting_App/releases
Download PAC.Metrics.zip from the latest release (shown at the bottom of the release notes)
Extract the PAC Metrics folder

You will have to right click "PAC Metrics.exe" and go to properties. in there the will be a checkbox that blocks the application, uncheck this and click okay.

Then open the application.

In the app there is a button to download the emis report template which will need importing to your practies systems and running.

When you export them select the following options
- Export Format: HTML
- Exclude report headers
- Override hidden patients where possible

Those exported results can then be added as practices in the app.

You will also want to add a list of staff so the app can identify proactive care activity.
in that list you also need to include any services accounts like Black Pear (SIDeR) that may also write to the patient records off the back of proactive care staff activity.

Once both the practice reports and staff are added you can generate the reports and graphs.

**Features:**
- ICB compliant report
- Check coding for:
   - Missing PAC Ended report
   - Missing PCSP report
- runs locally with your selected data
- EMIS Template included (open the app and download the template)
- Graphs showing you the distributions of cases across practices and your teams impact

Below is the list of codes being looked for.
The ones in italics are considered to be the codes we are meant to be using.
 
**General:**
- Triage of brave patient
   - _“Targeted Proactive care needs assessment”_
- Triage of referred patient (via GP or other org)
   - _“Proactive care needs assessment”_
- Proactive care not appropriate
   - _'Proactive care needs assessment not appropriate'_
- Patient accepted PAC intervention
   - _“Provision of Proactive Care”_
- Patient declined PAC intervention
   - _“Proactive care needs assessment declined”_
- PAC intervention ended
   - _“Proactive care ended”_

 
**Unit of measure:**
Caseload overview stats = number of patients
Impact: coverage across caseload (this is looking codes added by anyone not just the pac teams)
- % of pts on pac caseload with PCSP in place = cases closed or were open/active during month with the one of the following codes in their history
   - _"Personalised Care and Support Plan agreed"_
   - "Care plan type (community care) : Personalised care and support plan"
- % of pts with CGA covering key domains = cases closed or were open/active that month with the one of the following codes in the 18 months before the closed date (or latest month in open cases)
   - 'Assessment using Comprehensive Geriatric Assessment toolkit' (used by ardens)
   - 'holistic needs assessment'
   - _'Comprehensive proactive care needs assessment'_ (used by eCAF)
- % of pts with a SMR = cases closed or were open that month with the one of the following codes in the 12 months before the closed date (or latest month in open cases)
   - _'Structured medication review'_
- % of pts with a FRAT score recorded = cases closed or were open that month with the one of the following codes in their history
   - _"FRAT - falls risk assessment tool"_
- % of pts with a MFRAs = cases closed or were open that month with the one of the following codes in their history
   - _"Falls risk assessment complete",_
   - "Falls assessment"
- % of pts with MFRA referrals = cases closed or were open that month that have had a referral for risk assessment
   - _"Referral for falls risk assessment"_
- % of pts with TEPs = cases closed or were open that month with the one of the following codes in their history
   - _'Treatment escalation plan'_

Impact: Completion of care
- % of closed cases with PCSP in place = Cases closed with a PCSP in place using one of the follow codes
   - _"Personalised Care and Support Plan agreed"_
   - "Care plan type (community care) : Personalised care and support plan"
- % of closed cases with CGA in place = Cases closed with a CGA in place using one of the follow codes
   - _'Assessment using Comprehensive Geriatric Assessment toolkit'_
   - 'holistic needs assessment'
   - 'Comprehensive proactive care needs assessment'

 
All of the following measure change shown in total over 12months before Provision vs total over 12 months after 2 months after Provision of PAC (so if Provision was in June 2025 it would measure June 2024-June 2025 for before and August 2025 – August 2026 for after).

Also they are totals counted per patient then totalled as a month, which does make this data fairly susceptible to outliers.
Change in GP demand: based on Type of consultations, counted per consultation, it includes the following types:
- telephone_consultations
   - "Telephone consultation",
   - "Telephone call from a patient",
   - "Telephone call to a patient",
   - "Telephone encounter",
   - "Telephone call to relative/carer",
   - "Telephone call from relative/carer"
- gp_surgery_consultations
   - "GP Surgery"
- home_visit_consultations
   - "Home visit note"

Change in Secondary: based on coded entries, includes the following codes:
- discharged_from_hospital
   - "Discharged from hospital"
   - "Discharge summary"
- seen_in_ae
   - "Seen in accident and emergency department"
   - "A&E report"
   - "Admission to accident and emergency department"
   - "Emergency hospital admission to accident and emergency service"
- ambulance_attendance
   - "Seen by ambulance crew"
Change in OOH: based on coded entries, includes the following codes:
- ooh
   - “Out of hour report"
   - "NHS 111 Report"
   - "NHS 111 service"
   - “NHS 111 report received"
   - "OOH report"
Change in Falls: based on coded entries, includes the following codes:
- fall_incidents
   - "Urgent care service accessed - falls incident"
   - "Falls"
   - "Fall from bed"
   - "Fall from chair or bed"
   - "Patient has had a fall"
   - "Fall on same level due to nature of surface" # Excludes fall on travelling pavement and fall due to roller skates or skateboard
   - "Fall on same level from slipping, tripping or stumbling"
   - "[RFC] Reason for care : Elderly fall"
   - "Geriatric fall"
   - "Unexplained fall"
   - "Fall-accidental" # Only includes: Fall in home, fall in nursing home, fall on ice, fall on or from stairs or steps, fall on same level, fell onto outstretched hand, simple fall
   - "Recurrent falls"
