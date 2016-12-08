import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from multiprocessing import Pool
import subprocess

subprocess.Popen("aws s3 cp s3://jora-data-science/personalised-ctr-model/jora-search-clicks.csv000 jora-search-clicks.csv000".split())

df = pd.read_csv('jora-search-clicks.csv000', sep = '\t', header=None, names=['user_id', 'job_title', 'click_ind']).dropna()

users = df.user_id.value_counts().ix[lambda x: x > 200].index

def train_model(tup):
 try:
     user, group = tup
     X = group['job_title']
     y = group['click_ind']
     clf = make_pipeline(CountVectorizer(), LogisticRegression())
     clf.fit(X,y)
     coeffs = sorted(zip(clf.steps[0][1].get_feature_names(), clf.steps[1][1].coef_[0]), key = lambda t: abs(t[1]), reverse = True)
     query = " ".join("{}^{:4f}".format(k, v) for k, v in coeffs)
     return user + "\t"+ query
 except:
     return
pool = Pool()

res = pool.map(train_model, df[df.user_id.isin(users)].groupby('user_id'))

with open('models.tsv', 'w') as f:
    f.write('\n'.join([r for r in res if r]))
