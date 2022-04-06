import os
import pandas as pd

def write_to_excel(downloads_path, result):
    with pd.ExcelWriter(downloads_path) as writer:
        result.to_excel(writer, sheet_name='unique', index=False)
    return None

def remove_duplicates(path):
    print(path)
    downloads_path = os.path.join(path, 'unique_records.xlsx')
    duplicates_path = os.path.join(path, 'duplicates.xlsx')
    #df = pd.DataFrame(pd.read_excel(downloads_path))
    df = pd.DataFrame(pd.read_excel('/home/shiny/PythonProjects/removeduplicates/test.xlsx'))
    thismonth = df[['Article', 'Page count']]
    previous_article = df[['Article IDs from already invoiced']]
    previous_article_s = previous_article['Article IDs from already invoiced']
    unique_data = thismonth.drop_duplicates()
    articles = unique_data['Article']
    #final_articles = previous_article_s.append(articles)
    duplicates = unique_data.loc[unique_data['Article'].isin(previous_article['Article IDs from already invoiced'])]
    '''final_articles_df = final_articles.to_frame(name='Article IDs from already invoiced')
    final_articles_df = final_articles_df.reset_index(drop=True)
    df['Article IDs from already invoiced'] = final_articles_df['Article IDs from already invoiced']'''
    result = unique_data.loc[~unique_data['Article'].isin(previous_article['Article IDs from already invoiced'])]
    write_to_excel(downloads_path, result)
    write_to_excel(duplicates_path, duplicates)
    
    #df['Article IDs from already invoiced'] = final_articles
  #  print(df[df.index.duplicated()])
    #previous_article.append(unique_data - duplicates)
    #print(previous_article_s)

if __name__ == "__main__":
    remove_duplicates('/home/shiny/PythonProjects/removeduplicates/')
    print("Main Program is here.")