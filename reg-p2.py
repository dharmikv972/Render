import numpy as np
from sklearn import preprocessing
data=np.array([[10,20],[2,4],[4,9]])
print(data)

data_std=preprocessing.scale(data)
print("Mean : ",data_std.mean(axis=0))
print("Standard Preprocessing : ",data_std.std(axis=0))

data_scaler=preprocessing.MinMaxScaler(feature_range=(0,1))
data_scaled=data_scaler.fit_transform(data)
print("Data Scaled : \n ",data_scaled)

data_normalized1=preprocessing.normalize(data,norm='l1')
print("Normlization : \n ",data_normalized1)

data_normalized2=preprocessing.normalize(data,norm='l2')
print("Normlization : \n ",data_normalized2)

data_normalized_column=preprocessing.normalize(data,norm='l1',axis=0)
print("Normalization With Column Wise : \n ", data_normalized_column)
data_normalized_row=preprocessing.normalize(data,norm='l2',axis=1)
print("Normalization With Row Wise : \n ", data_normalized_row)

data_binarization=preprocessing.Binarizer(threshold=1.4).transform(data)
print("Binarization : \n ",data_binarization)
