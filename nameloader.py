import csv
import pickle

# Load random first and last names
first = []
last = []
with open('randomNames.csv', 'rb') as csvfile:
    names = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in names:
        first.append(row[0])
        last.append(row[1])

first = list(set(first))
last = list(set(last))

pickle.dump({'first': first, 'last': last}, open('names.p', 'wb'))


# Load random websites

with open('websites.csv', 'rb') as csvfile:
    sites = csv.reader(csvfile, delimiter=',', quotechar='|')

pickle.dump([s[1] for s in sites], open('sites.p', 'wb')
