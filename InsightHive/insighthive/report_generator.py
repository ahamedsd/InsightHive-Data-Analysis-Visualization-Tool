import pandas as pd
import io

class ReportGenerator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate_report(self):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            self.df.to_excel(writer, index=False, sheet_name='Report')
        output.seek(0)
        return output
