#! python3

from pandas import read_csv

data = [{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-08"
}, {
    "name": "Kavey",
    "gender": "female",
    "birthday": "1995-05-12"
}]    


with open('data.csv', 'a', newline='') as csvfile:
    fieldnames = ['name', 'gender', 'birthday']
    writer = read_csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    writer.writerows(data)

with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

df = read_csv('data.csv', encoding='gbk')
print(df)

