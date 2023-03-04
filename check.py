import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class autism_pred:
    def predict(self, feats):
        data=pd.read_csv(r"D:\ASWIN\2022-2023 workspace\LBS\Autism_spectrum_disorder\static\Toddler Autism dataset July 2018.csv")
        attributes=data.values[1:200, :14]
        labels=data.values[1:200, 14]

        x_train, x_test, y_train, y_test =train_test_split(attributes, labels, test_size=0.2)
        rf=RandomForestClassifier()
        rf.fit(x_train, y_train)
        y_pred=rf.predict(x_test)
        acc=accuracy_score(y_test, y_pred)
        print("Accuracy : ", round(acc * 100, 2))

        # lst=[0,1,1,1,0,0,0,0,0,0,30,1,0,0]
        # pred=rf.predict([lst])
        pred=rf.predict([feats])
        print(pred)
        if pred[0] == '0':
            print("Non austistic")
            return "Non austistic"
        else:
            print("Autistic")
            return "Autistic"

