import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
diabetes=load_diabetes()
X,y=diabetes.data, diabetes.target
print(X)
print(y)
y_binary=(y>np.median(y)).astype(int)
print("after convert into 0 and 1")
print(y_binary)

X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)

scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

model=LogisticRegression()
model.fit(X_train,y_train)

y_pred=model.predict(X_test)
accuracy=accuracy_score(y_test,y_pred)
print("ACCURACY : {:.2f}%".format(accuracy*100))

print("CONFUSION MATRIX :\n",confusion_matrix(y_test,y_pred))
print("CLASSIFICATION REPORT :\n",classification_report(y_test,y_pred))

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_test[:,2],y=X_test[:,8],hue=y_test, palette={0: 'blue', 1: 'red'},marker='o')
plt.xlabel("BMI")
plt.ylabel("AGE")
plt.title("LOGISTIC REGRESSION DECISION BOUNDARY\nACCURACY : {:.2f}%".format(accuracy*100))
plt.legend(title="DIABETES",loc="upper right")
plt.show()
