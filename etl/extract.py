import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def extract():
    path = os.getenv("RAW_DATA_PATH")
    df = pd.read_excel(path)
    print("Extracted:", df.shape)
    return df
