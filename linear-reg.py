import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
advertising=pd.read_csv("advertising.csv")
print(advertising.head())

print(advertising.info())
print("Data Shape : ",advertising.shape)

print('Checking For NULL Values')
print(advertising.isnull().sum()*100/advertising.shape[0])

import seaborn as sns
fig,axs=plt.subplots(3,figsize=(5,5))
plt1=sns.boxplot(advertising['TV'],ax=axs[0])
plt2=sns.boxplot(advertising['Newspaper'],ax=axs[1])
plt3=sns.boxplot(advertising['Radio'],ax=axs[2])
plt.tight_layout()

sns.pairplot(advertising,x_vars=["TV","Newspaper","Radio"],y_vars="Sales",size=4,kind="scatter")
plt.show()

sns.heatmap(advertising.corr(),cmap="YlGnBu",annot=True)
plt.show()

X=advertising["TV"]
Y=advertising["Sales"]

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=0.7,test_size=0.3,random_state=100)
print("TV Data : \n",X_train.head())
print(X_train.shape)
print(X_test.shape)
print("Sales Data : \n",Y_train.head())
print(Y_train.shape)
print(Y_test.shape)

import statsmodels.api as sm
X_train_sm=sm.add_constant(X_train)
lr=sm.OLS(Y_train,X_train_sm).fit()
print(lr.params)

print(lr.summary())

plt.scatter(X_train,Y_train)
plt.plot(X_train,6.948 + 0.054*X_train,'r')
plt.show()

X_test_sm=sm.add_constant(X_test)
y_pred=lr.predict(X_test_sm)
print("Y PREDICTION : ")
print(y_pred.head())

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
print("RMSE : ",np.sqrt(mean_squared_error(Y_test,y_pred)))
print("R-SQUARED : ",r2_score(Y_test,y_pred))

plt.scatter(X_test,Y_test)
plt.plot(X_test,6.948 + 0.054*X_test,'r')
plt.show()
