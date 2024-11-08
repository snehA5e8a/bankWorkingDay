import streamlit as st
import pandas as pd
from datetime import datetime, timedelta 
from io import BytesIO
import base64
from typing import List, Union

class IndianWorkingDayCalculator:
    # ... (previous class code remains the same) ...
    def __init__(self):
        self.fixed_holidays = [
            (1, 1),   # New Year's Day
            (1, 26),  # Republic Day
            (8, 15),  # Independence Day
            (10, 2),  # Gandhi Jayanti
            (12, 25)  # Christmas
        ]
        self.weekend_days = [5, 6]  # Saturday and Sunday
    
    def is_weekend(self, date: datetime) -> bool:
        return date.weekday() in self.weekend_days
    
    def is_fixed_holiday(self, date: datetime) -> bool:
        return (date.month, date.day) in self.fixed_holidays
    
    def add_custom_holidays(self, custom_holidays: List[datetime]) -> None:
        if not hasattr(self, 'custom_holidays'):
            self.custom_holidays = []
        self.custom_holidays.extend(custom_holidays)
    
    def is_working_day(self, date: datetime) -> bool:
        if self.is_weekend(date):
            return False
        if self.is_fixed_holiday(date):
            return False
        if hasattr(self, 'custom_holidays'):
            if any(date.date() == holiday.date() for holiday in self.custom_holidays):
                return False
        return True
    
    def calculate_working_days(self, start_date: Union[str, datetime],
                             end_date: Union[str, datetime],
                             date_format: str = "%Y-%m-%d") -> int:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, date_format)
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, date_format)
            
        if start_date > end_date:
            start_date, end_date = end_date, start_date
            
        working_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if self.is_working_day(current_date):
                working_days += 1
            current_date += timedelta(days=1)
            
        return working_days

def process_file(uploaded_file):
    """Process the uploaded Excel file and return results"""
    try:
        df = pd.read_excel(uploaded_file)
        
        # Verify required columns
        required_columns = ['Start_Date', 'End_Date']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return None, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Convert dates if they're not already datetime
        for col in ['Start_Date', 'End_Date']:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col])
        
        # Create calculator instance
        calculator = IndianWorkingDayCalculator()
        
        # Add custom holidays
        custom_holidays = [
            datetime(2024, 3, 25),  # Holi
            datetime(2024, 10, 31), # Diwali
            datetime(2024, 8, 19),  # Janmashtami
        ]
        calculator.add_custom_holidays(custom_holidays)
        
        # Calculate working days
        df['Working_Days'] = df.apply(
            lambda row: calculator.calculate_working_days(
                row['Start_Date'],
                row['End_Date']
            ),
            axis=1
        )
        
        return df, None
        
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

def get_downloadable_excel(df):
    """Convert DataFrame to downloadable Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_data = output.getvalue()
    return excel_data

def main():
    st.set_page_config(page_title="Working Days Calculator", page_icon="📅")
    
    st.title("📅 Working Days Calculator")
    st.write("""
    Calculate working days between dates considering Indian holidays and weekends.
    
    1. Upload your Excel file with 'Start_Date' and 'End_Date' columns
    2. Get results with working days calculated
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file:
        # Show file details
        st.write(f"File: {uploaded_file.name}")
        
        # Add a process button
        if st.button("Process File"):
            with st.spinner("Processing..."):
                # Process the file
                df, error = process_file(uploaded_file)
                
                if error:
                    st.error(error)
                else:
                    # Show preview of results
                    st.write("### Preview of Results")
                    st.dataframe(df.head())
                    
                    # Create download button
                    excel_data = get_downloadable_excel(df)
                    st.download_button(
                        label="📥 Download Results",
                        data=excel_data,
                        file_name="working_days_results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    # Show summary statistics
                    st.write("### Summary")
                    st.write(f"Total rows processed: {len(df)}")
                    st.write(f"Average working days: {df['Working_Days'].mean():.1f}")
    
    # Add sample file download
    st.sidebar.markdown("### Sample File")
    if st.sidebar.button("Download Sample File"):
        # Create sample DataFrame
        sample_data = {
            'Start_Date': ['2024-01-01', '2024-02-01', '2024-03-01'],
            'End_Date': ['2024-01-31', '2024-02-28', '2024-03-31']
        }
        sample_df = pd.DataFrame(sample_data)
        sample_df['Start_Date'] = pd.to_datetime(sample_df['Start_Date'])
        sample_df['End_Date'] = pd.to_datetime(sample_df['End_Date'])
        
        # Convert to downloadable Excel
        sample_excel = get_downloadable_excel(sample_df)
        st.sidebar.download_button(
            label="📥 Download Sample",
            data=sample_excel,
            file_name="sample_dates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Add information about holidays
    st.sidebar.markdown("### Holidays Considered")
    st.sidebar.markdown("""
    - All Saturdays and Sundays
    - Fixed Holidays:
        - New Year's Day (Jan 1)
        - Republic Day (Jan 26)
        - Independence Day (Aug 15)
        - Gandhi Jayanti (Oct 2)
        - Christmas (Dec 25)
    - Festival Holidays 2024:
        - Holi (Mar 25)
        - Janmashtami (Aug 19)
        - Diwali (Oct 31)
    """)

if __name__ == "__main__":
    main()