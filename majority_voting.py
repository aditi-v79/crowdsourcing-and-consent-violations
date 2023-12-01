
#Importing the required libraries
from cgitb import text
import pandas as pd
import glob
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer

# for the first time only
#nltk.download('all')

#combining the data(removing the fake files: 47.xlsx, 12.xlsx, 3.xlsx, 27.xlsx, 11.xlsx)
path_to_review_files= os.path.abspath(".\P2a Labels\P2a Labels")
list_of_files= glob.glob(os.path.join(path_to_review_files, "*.xlsx"))

exclude_files = ["47.xlsx", "12.xlsx", "3.xlsx", "27.xlsx", "11.xlsx"]
list_of_files = [file for file in list_of_files if os.path.basename(file) not in exclude_files]
# for file in list_of_files:
#     print(file)


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

#print(list(title_review.columns))

#Drop all the 'title' and 'review' columns
crowdsource_data.drop(columns=['title', 'review'], inplace=True)

#Concate removed 'title and 'review'
crowdsource_data=pd.concat([title_review,crowdsource_data],axis=1)
crowdsource_data.drop(columns=['Unnamed: 5'], inplace=True) # found some unnamed columns and dropped them.


#Finally storing the data frame to a .csv/.xlxs file for ref
crowdsource_data.to_csv('crowdsource_data.csv',index=False)


#print the columns of the combined data frame
#print(list(crowdsource_data.columns))
#print(crowdsource_data.head(5))

'''Majority Voting'''
df= pd.read_csv("crowdsource_data.csv")
#print(df.head(5))
all_violations= df.drop(columns=['title', 'review'])
finalviolation_df=pd.DataFrame()

#print(all_violations.head(3))

for index, row in all_violations.iterrows():

    #count all unique values and store their count in dict
    count_dict= row.value_counts().to_dict()
    #print(count_dict)

    #sort the dictionary to pick the top 3 violations
    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    majority_violations = [item[0] for item in sorted_items[:3]]
    #print(majority_violations)

    #create a dictionary to store the top three violations 
    final_dict={
    'First violation': majority_violations[0],
    'Second violation': majority_violations[1] if (len(majority_violations) > 1) and (majority_violations[0]!="No violation") and (majority_violations[1]!="No violation") else ' ',
    'Third violation': majority_violations[2] if (len(majority_violations) > 2) and (majority_violations[0]!="No violation") and (majority_violations[2]!="No violation") else ' '
    }
    violation_df = pd.DataFrame([final_dict])
    finalviolation_df = pd.concat([finalviolation_df, violation_df], ignore_index=True)

#print final data frame
finalviolation_df=pd.concat([df['title'],df['review'], finalviolation_df], axis=1)
print(finalviolation_df.head(15))

#save it as a csv
finalviolation_df.to_csv('finalviolation.csv',index=False)


################################################################################################################################################################################################################
################################################################################################################################################################################################################


'''Analyse top 3 prominent categories to build word clouds for each
   1. Find the top-3 prominent violations in the final dataset
   2. Analyse the words from the reviews related to each of the top-3 violations
   3. Build the word clouds for each of the top-3 violations '''

final_cat= finalviolation_df[['First violation', 'Second violation', 'Third violation']]

concat_data= pd.concat([finalviolation_df['First violation'],finalviolation_df['Second violation']])
concat_data= pd.concat([concat_data,finalviolation_df['Third violation']])
#print(concat_data)

count_viol= concat_data.str.lower().value_counts().to_dict()
#print(count_viol)

new_count_viol = defaultdict(int)
for key, value in count_viol.items():
    new_count_viol[key.strip().lower()] += value

# Convert defaultdict to a regular dictionary
new_count_viol = dict(new_count_viol)
new_count_viol.pop('') # remove empty values
#print(new_count_viol)

 #sort the dictionary to pick the top 3 violations
sort_viol = sorted(new_count_viol.items(), key=lambda x: x[1], reverse=True)
prominent_violations = [item[0] for item in sort_viol[:3]]

# print the prominent violations in the final datasets
print(prominent_violations)

#Analyse the words in the reviews associated with each of the top-3 violations
def word_analysis(text):
    tokens_temp= word_tokenize(text.lower())
    tokens=  [token for token in tokens_temp if token not in stop_words]
    return tokens

#Lemetize the words
def lemmetize(list_of_words):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in list_of_words]
    lem_text = ' '.join(lemmatized_tokens)
    return lem_text

#Visualize word clouds
def word_cloud(text,v):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f"Word Cloud for Consent Category: {v}" )
    plt.axis('off')
    plt.show()

stop_words = stopwords.words('english')

words1, words2, words3=[], [], []
x,y,z=[],[],[]
# Iterate through each review that is associated with the prominent_violations[0]
for index, row in finalviolation_df.iterrows():
    if row['First violation'].lower()== prominent_violations[0] or row['Second violation'].lower()== prominent_violations[0] or row['Third violation'].lower()== prominent_violations[0]:
        x= word_analysis(row['review'])
        words1= words1+x
#print(words1)
word_cloud(lemmetize(words1), prominent_violations[0])


# Iterate through each review that is associated with the prominent_violations[1]
for index, row in finalviolation_df.iterrows():
    if row['First violation'].lower()== prominent_violations[1] or row['Second violation'].lower()== prominent_violations[1] or row['Third violation'].lower()== prominent_violations[1]:
        y= word_analysis(row['review'])
        words2= words2+y
lemmetize(words2)
word_cloud(lemmetize(words2), prominent_violations[1])

# Iterate through each review that is associated with the prominent_violations[1]
for index, row in finalviolation_df.iterrows():
    if row['First violation'].lower()== prominent_violations[2] or row['Second violation'].lower()== prominent_violations[2] or row['Third violation'].lower()== prominent_violations[2]:
        z= word_analysis(row['review'])
        words3= words3+z
word_cloud(lemmetize(words3), prominent_violations[2])

   






