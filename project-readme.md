# Working Days Calculator
A simple tool to calculate working days between dates, considering Indian holidays. In dev speak, you might know this as a "Bizdays Calculator" 🗓️

## Features
- Upload Excel with dates, get working days calculated
- Handles weekends, public holidays, and festival days
- Preview results before downloading
- Simple Excel input/output

## Quick Start
```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
streamlit run app.py
```

### What your Excel file should look like

Keep it simple - just two columns:
- `Start_Date`: When your period starts
- `End_Date`: When it ends

| Start_Date | End_Date   |
|------------|------------|
| 2024-01-01 | 2024-01-31 |

If the dates look weird:
- Make sure they're actual Excel dates
- Avoid dates written as plain text

## Requirements
- Python 3.8+
- streamlit==1.29.0
- pandas==2.1.4
- openpyxl==3.1.2

## Try It Live
https://bankworkingday-gdqhmyaqkpnmzfa7mut3ef.streamlit.app/

## Coming Soon
- Config file for custom holidays
- Second/Fourth Saturday rules
- State-specific holidays
- Bulk processing
- API access

## Known Limitations
- Currently hardcoded holidays
- Fixed weekend rules (all Saturdays/Sundays)
- Single region (India) support

## Want to Help?
Got ideas or found bugs? Feel free to:
- Raise an issue
- Submit a PR
- Fork the project

## Questions?
Drop me a line at snehapainen@gmail.com

Made with ☕ and Python, Streamlit and of course AI 😍
