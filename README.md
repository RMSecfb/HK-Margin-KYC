# Hong Kong RPQ Prototype v1

## Files
- `app.py` — Streamlit main app
- `rpq_preview.html` — standalone HTML preview
- `requirements.txt` — Python dependency

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud
Set the main file path to:

`app.py`

## v1 business rules
- 15 RPQ questions; A/B/C/D/E = 1/2/3/4/5 points
- G1: 15–30
- G2: 31–45
- G3: 46–60
- G4: 61–75
- Age >= 65: internal-rule reminder for independent third-party witness
- Joint account: internal rule uses the higher RPQ risk grade when the other holder's grade is available
- Consistency checks are warnings; they do not change RPQ score
- Margin/Credit information is disclosed separately and does not affect RPQ score or grade

## Prototype note
This repository is a prototype only. Do not commit real client data. Production use should be approved against the firm's latest Hong Kong Compliance, Credit and Securities Margin Financing policies.
