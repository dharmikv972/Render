from sklearn import preprocessing
label_encoder=preprocessing.LabelEncoder()
input_classes=['suzuki','ford','suzuki','toyota','ford','bmw']
label_encoder.fit(input_classes)
print("\nClass Mapping : ")
for i, item in enumerate(label_encoder.classes_):
    print(item,'-->',i)

labels=['toyota','ford','suzuki']
encoded_labels=label_encoder.transform(labels)
print("\nLabels = ",labels)
print("Encoded Labels = ",list(encoded_labels))

encoded_labels=[3,2,0,2,1]
decoded_labels=label_encoder.inverse_transform(encoded_labels)
print("\nEncoded Labels = ",encoded_labels)
print("Decoded Labels = ",list(decoded_labels))
