import pandas as pd
data_set=pd.read_csv(r'statedata.csv')
print(data_set)

x=data_set.iloc[:,:-1].values
print(x)

y=data_set.iloc[:,3].values
print(y)

from sklearn.impute import SimpleImputer
import numpy as np
imputer=SimpleImputer(missing_values=np.nan,strategy='mean')
imputerimputer=imputer.fit(x[:,1:3])
x[:,1:3]=imputer.transform(x[:,1:3])
print(x)

from sklearn.preprocessing import LabelEncoder
label_encoder_x=LabelEncoder()
x[:,0]=label_encoder_x.fit_transform(x[:,0])
print(x)

data_set=pd.get_dummies(data_set,columns=['State'],dtype='int')
print("Dummy variable using one hot encoding : ")
#print(data_set)
print(data_set.head())

labelencoder_y=LabelEncoder()
y=labelencoder_y.fit_transform(y)
print("Purchased Variable : ",y)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
print(x_train)

from sklearn.preprocessing import StandardScaler
st_x=StandardScaler()
x_train=st_x.fit_transform(x_train)
x_test=st_x.transform(x_test)
print("Feature Scaling Of X_Train Data: ",x_train)
print("Feature Scaling Of X_Test Data: ",x_test)
