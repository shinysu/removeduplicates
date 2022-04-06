import os
import pandas as pd

def write_to_excel(downloads_path, result, duplicates):
    with pd.ExcelWriter(downloads_path) as writer:
        result.to_excel(writer, sheet_name='unique_records', index=False)
        duplicates.to_excel(writer, sheet_name='duplicates', index=False)
    return None

def remove_duplicates(path, filename, outputfile):
    downloads_path = os.path.join(path, outputfile)
    df = pd.DataFrame(pd.read_excel(filename))
    thismonth = df[['Article', 'Page count']]
    previous_article = df[['Article IDs from already invoiced']]
    unique_data = thismonth.drop_duplicates()
    duplicates = unique_data.loc[unique_data['Article'].isin(previous_article['Article IDs from already invoiced'])]
    result = unique_data.loc[~unique_data['Article'].isin(previous_article['Article IDs from already invoiced'])]
    write_to_excel(downloads_path, result, duplicates)
    

if __name__ == "__main__":
    remove_duplicates('/home/shiny/PythonProjects/removeduplicates/')
    print("Main Program is here.")