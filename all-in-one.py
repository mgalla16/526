from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
dirpath = "C:/Users/Matt/Documents/526/reuters"
tuples = []
relevant = ['money', 'fx', 'crude', 'grain', 'trade', 'interest', 'wheat', 'ship', 'corn', 'oil', 'dlr', 'gas', 'oilseed', 'supply', 'sugar', 'gnp', 'coffee', 'veg', 'gold', 'soybean', 'bop', 'livestock', 'cpi']
x = 1
for file in os.listdir(dirpath):
    if file.startswith("reut2-"):
        print("Working on file "+str(x))
        filepath = os.path.join(dirpath, file).replace("\\","/")
        with open(filepath) as f:
            file1 = f.read()
        soup = BeautifulSoup(file1, 'lxml')

        #Create a list of all articles
        reuters = soup.find_all('reuters')
        for article in reuters:
            #get all topics from 1 article
            topics = []
            for topic in article.find('topics').findChildren():
                split = topic.contents[0].split("-")
                for seg in split:
                    topics.append(seg)
            topics = list(set(topics))
            if len(set(relevant).intersection(set(topics)))>0:
                #get body from 1 article
                body = article.find('text')
                try:
                    body.title.extract()
                except AttributeError:
                    pass
                try:
                    body.dateline.extract()
                except AttributeError:
                    pass
                body_text = body.text
                t = topics, body_text
                tuples.append(t)
        x+=1
#create df with empty labels
df = pd.DataFrame(tuples, columns=['topics','body'])
labels = pd.DataFrame(np.random.randint(low=0, high=1, size=(len(tuples), len(relevant))), columns=['money', 'fx', 'crude', 'grain', 'trade', 'interest', 'wheat', 'ship', 'corn', 'oil', 'dlr', 'gas', 'oilseed', 'supply', 'sugar', 'gnp', 'coffee', 'veg', 'gold', 'soybean', 'bop', 'livestock', 'cpi'])
data_complete = df.join(labels)

#fill in labels
for row in data_complete.itertuples():
    tops = row[1]
    index = row[0]
    for item in tops:
        if item in relevant:
            data_complete.at[row[0], item] = 1
data_complete.head()