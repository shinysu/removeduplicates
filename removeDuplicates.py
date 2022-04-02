import os
import pandas as pd


def remove_duplicates(path, filename):

    downloads_path = os.path.join(path, filename)
    df = pd.DataFrame(pd.read_excel(downloads_path))
    thismonth = df[['Article', 'Page count']]
    unique_data = thismonth.drop_duplicates()
    with pd.ExcelWriter(downloads_path) as writer:
        unique_data.to_excel(writer, sheet_name='unique', index=False)
    return None

if __name__ == "__main__":
    print("Main Program is here.")