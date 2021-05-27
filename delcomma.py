
import csv
import pandas as pd
from _csv import QUOTE_ALL
import os.path

for j in range(0,153):

    filename="./library/library4-review"+str(j)+".csv"
    filename1="./reviews/library/library4-review.csv"
    if os.path.exists(filename):
        with open(filename, "r",encoding="utf-8-sig") as f:

            print(filename)
            csv_data = csv.reader(f)
            print(csv_data)
            new = []
            for row in csv_data:
                new.append(row)
                    #print(row)
            print(len(new))
        for i in range(1,len(new)):
            new[i][0]=i
        print(new)


        with open(filename1, "a", encoding="utf-8-sig") as f_new:
            writer = csv.writer(f_new, delimiter=",", quotechar='"', quoting=QUOTE_ALL)
            for row in new:
                writer.writerow(row)
                print(row)
