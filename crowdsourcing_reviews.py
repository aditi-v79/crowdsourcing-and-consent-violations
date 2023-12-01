'''The approach adopted is to combine all the files irrespectively. Store 'title' and 'review' as a separte DF
    Then drop all the columns with names 'title' and 'review' and now combine the all the violations with the dataframe consisting only of 'title' and 'review'
'''
#Importing the required libraries
import pandas as pd
import glob
import os

#combining the data
path_to_review_files= os.path.abspath(".\P2a Labels\P2a Labels")
list_of_files= glob.glob(os.path.join(path_to_review_files, "*.xlsx"))

#create a data frame to store combined data
crowdsource_data = pd.DataFrame()

#Concatenating the columns
data= [pd.read_excel(excel_file) for excel_file in list_of_files]
crowdsource_data = pd.concat(data, axis=1)
crowdsource_data.reset_index(drop=True, inplace=True)

#create a new dataframe with only 'title' and 'review' 
title_review= crowdsource_data[['title','review']]

#remove the duplicates of 'title' and 'review'
title_review= title_review.loc[:,~title_review.columns.duplicated()]

'''print(list(title_review.columns))'''

#Drop all the 'title' and 'review' columns
crowdsource_data.drop(columns=['title', 'review'], inplace=True)

#Concate removed 'title and 'review'
crowdsource_data=pd.concat([title_review,crowdsource_data],axis=1)
crowdsource_data.drop(columns=['Unnamed: 5'], inplace=True) # found some unnamed columns and dropped them.

#Finally storing the data frame to a .csv/.xlxs file for ref
crowdsource_data.to_csv('crowdsource_data.csv',index=False)

#print the columns of the combined data frame
print(list(crowdsource_data.columns))
print(crowdsource_data.head(5))




