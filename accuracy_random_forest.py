import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


def find_acc_rf():
    data=pd.read_csv(r"C:\Users\shahma fathima\OneDrive\project\Autism_spectrum_disorder\static\Toddler Autism dataset July 2018.csv")

    #   Extract attributes and labels
    attributes=data.values[:, :14]
    labels=data.values[:, 14]

    #   Split attributes and labels
    X_train, X_test, Y_train, Y_test = train_test_split(attributes, labels, test_size=0.2)
    rf=RandomForestClassifier()
    rf.fit(X_train, Y_train)

    #   Predict result
    pred=rf.predict(X_test)

    print("Original Result\t\tPredicted Result")
    for i in range(len(pred)):
        print(Y_test[i], "\t\t", pred[i])



    #   Find accuracy score
    acc=accuracy_score(Y_test, pred)
    print("\nAccuracy : ", round(acc*100, 2), "%")



find_acc_rf()