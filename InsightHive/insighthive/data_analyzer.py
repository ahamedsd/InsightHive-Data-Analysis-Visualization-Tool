import pandas as pd

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_summary(self):
        return self.df.describe()
