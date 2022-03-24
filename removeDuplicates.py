import pandas as pd
from os.path import expanduser
import os

def remove_duplicates(file):
    df = pd.DataFrame(pd.read_excel(file))
    thismonth = df[['Article', 'Page count']]
    unique_data = thismonth.drop_duplicates()
    home = expanduser("~")
    downloads_path = home + os.sep + 'Unique_records.xlsx'
    with pd.ExcelWriter(downloads_path) as writer: 
        unique_data.to_excel(writer, sheet_name='unique',index=False)
    return downloads_path

if __name__ == "__main__":
    file = "test.xlsx"
    remove_duplicates(file)
