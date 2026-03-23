import gspread
import pandas as pd
import re
from google.oauth2.service_account import Credentials


class StockDataExtractor:

    def __init__(self, creds_file, sheet_id):

        self.creds_file = creds_file
        self.sheet_id = sheet_id
        self.df = None


    # -----------------------------
    # Load Google Sheet Data
    # -----------------------------
    def load_data(self):

        scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

        creds = Credentials.from_service_account_file(
            self.creds_file,
            scopes=scope
        )

        client = gspread.authorize(creds)

        sheet = client.open_by_key(self.sheet_id).sheet1

        rows = sheet.get_all_records()

        self.df = pd.DataFrame(rows)

        # remove extra spaces in column names
        self.df.columns = self.df.columns.str.strip()

        print("Google sheet loaded successfully")


    # -----------------------------
    # Normalize company names
    # -----------------------------
    def normalize(self, name):

        if name is None:
            return ""

        name = str(name).lower()

        # convert Limited → Ltd
        name = name.replace("limited", "ltd")

        # remove dots
        name = name.replace(".", "")

        # remove extra spaces
        name = " ".join(name.split())

        return name


    # -----------------------------
    # Extract company name from notification
    # -----------------------------
    def extract_company_name(self, text):

        pattern = r"([A-Za-z\s]+?(?:Ltd\.?|Limited))"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

        return None


    # -----------------------------
    # Get company data from sheet
    # -----------------------------
    def get_company_history(self, notification):

        company = self.extract_company_name(notification)

        if company is None:
            print("Company not detected in notification")
            return ""

        print("Extracted company:", company)

        company_norm = self.normalize(company)

        # match company after normalization
        company_rows = self.df[
            self.df["Company Name"].apply(
                lambda x: company_norm in self.normalize(x)
            )
        ]

        if company_rows.empty:
            print("Company not found in sheet")
            return ""

        history_text = ""

        for _, row in company_rows.iterrows():

            history_text += f"""
Exchange Time: {row.get("exchange_received_time")}
Market Cap: {row.get("Market_cap_value")}
Stock PE: {row.get("Stock_pe_value")}
Industry PE: {row.get("Industry_pe_value")}
Current Price: {row.get("Current_price_value")}
Week Volume Avg: {row.get("Week Volume Avg")}
Month Volume Avg: {row.get("Month Volume Avg")}
Revenue (Qtr|Last Year): {row.get("Revenue (Qtr|Last Year")}
"""

        return history_text