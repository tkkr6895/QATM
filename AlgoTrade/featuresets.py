from pandas.io.data import DataReader
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.metrics import mean_squared_error
import numpy as np


name = raw_input("Enter company name\n")

mydata = DataReader(name,'yahoo',datetime(2008,1,1),datetime(2016,4,10)) #Which data to pull

#print (mydata.shape) #rows,col

mydata = mydata.dropna(axis = 0) #drop rows with missing values

kmeans_model = KMeans(n_clusters = 5, random_state = 1)

good_columns = mydata._get_numeric_data() #get only numeric columns

kmeans_model.fit(good_columns)

labels = kmeans_model.labels_

pca_2 = PCA(2) #create PCA Model
plot_columns = pca_2.fit_transform(good_columns)
plt.scatter(x = plot_columns[:,0],y = plot_columns[:,1],c = labels)

#plt.show()

columns = mydata.columns.tolist()

columns = [c for c in columns if c not in ["Open","Date"]]

target = "Open"
#split data
train = mydata.sample(frac = 0.8,random_state = 1)
test = mydata.loc[~mydata.index.isin(train.index)]

#print(train.shape)
#print(test.shape)
#clf = svm.SVC(kernel = 'rbf', C = 10000)
model = LinearRegression()
model.fit(train[columns],train[target])
#clf.fit(train[columns],train[target])
predictions = model.predict(test[columns])

#acc = accuracy_score(test[target],predictions)
acc = 100 - int(mean_squared_error(predictions, test[target]))
print acc,"%"
print predictions
