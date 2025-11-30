import pandas as pd
import io

class DataLoader:
    def __init__(self, file):
        self.file = file

    def load_data(self):
        if self.file.name.endswith('.csv'):
            return pd.read_csv(self.file)
        elif self.file.name.endswith('.xlsx'):
            return pd.read_excel(self.file)
        else:
            raise ValueError("Unsupported file type")
