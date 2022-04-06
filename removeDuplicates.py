import os
import pandas as pd

def write_to_excel(downloads_path, result, duplicates):
    with pd.ExcelWriter(downloads_path) as writer:
        result.to_excel(writer, sheet_name='unique_records', index=False)
        duplicates.to_excel(writer, sheet_name='duplicates', index=False)
    return None

def remove_duplicates(path, file, outputfile):
    downloads_path = os.path.join(path, outputfile)
    df = pd.DataFrame(pd.read_excel(file))
    print(df.shape[0])
    thismonth = df[['Article', 'Page count']]
    previous_article = df[['Article IDs from already invoiced']]
    unique_data = thismonth.drop_duplicates()
    duplicates = unique_data[unique_data.set_index('Article').index.isin(previous_article.set_index('Article IDs from already invoiced').index)]
    print(duplicates)
    #duplicates = unique_data.loc[unique_data['Article'].isin(previous_article['Article IDs from already invoiced'])]
    print(duplicates.shape[0])
    result = unique_data[~unique_data.set_index('Article').index.isin(previous_article.set_index('Article IDs from already invoiced').index)]
    print(result.shape[0])
    write_to_excel(downloads_path, result, duplicates)
    

if __name__ == "__main__":
    remove_duplicates('/home/shiny/Downloads/Feb 2022 Breakup Workout Excel.xlsx')
    print("Main Program is here.")