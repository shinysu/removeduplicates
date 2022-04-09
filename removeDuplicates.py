import os
import pandas as pd

def write_to_excel(downloads_path, result, duplicates):
    with pd.ExcelWriter(downloads_path) as writer:
        result.to_excel(writer, sheet_name='unique_records', index=False)
        duplicates.to_excel(writer, sheet_name='duplicates', index=False)
    return None

def remove_duplicates(path, file, outputfile):
    downloads_path = os.path.join(path, outputfile)
    master_file = os.path.join(path, "invoiced_files.csv")
    df1 = pd.DataFrame(pd.read_excel(file, sheet_name='Published kriyadocs articles'))
    df2 = pd.DataFrame(pd.read_excel(file, sheet_name='Banked kriyadocs articles'))
    df = pd.concat([df1, df2])
    previous_article = pd.DataFrame(pd.read_csv(master_file))
    unique_data = df.drop_duplicates()
    duplicates = previous_article[previous_article.set_index('Article IDs from already invoiced').index.isin(unique_data.set_index('Article ID').index)]
    result = unique_data[~unique_data.set_index('Article ID').index.isin(previous_article.set_index('Article IDs from already invoiced').index)]
    write_to_excel(downloads_path, result, duplicates)
    return result
    

def update_master_csv(path, unique, month):
    date = convert_month(month)
    master_file = os.path.join(path, "invoiced_files.csv")
    previous_article = pd.DataFrame(pd.read_csv(master_file))
    to_append = unique[['Article ID']]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    to_append['Invoiced month'] = date
    to_append = to_append.rename(columns={"Article ID":"Article IDs from already invoiced"})
    final_data = pd.concat([previous_article, to_append])
    print(final_data.tail(10))
    final_data.to_csv("removeduplicates/invoiced_files.csv", index=False)
    
def convert_month(month):
    year, month = month.split('-')
    return month +'/' + year

if __name__ == "__main__":
    remove_duplicates('/home/shiny/Downloads/Invoice_March 2022_Artwork_and_K2.xlsx')
    print("Main Program is here.")