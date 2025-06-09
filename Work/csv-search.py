import csv

filename = "/home/antonio/Downloads/RecommendedEvents.csv"
current = "/home/antonio/Downloads/CurrentEvents.csv"
gov = "/home/antonio/Downloads/GovEvents.csv"
new = "/home/antonio/coding/NewMissingEvents.csv"

def load_id(filename, id=2):
    ids = set()
    with open(filename, newline='') as f:
        for row in csv.reader(f):
            if row:
                ids.add(row[id].strip())
    return ids

def lookup(filename, id='ID', cat='Category', name='Name'):
    lookups = {}
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lookups[row[id]] = (row[cat], row[name])
    return lookups

def main():
    ref = lookup(filename)

    missed1_ids = load_id(new, 0)
    missed2_ids = load_id(gov)

    missing_ids = sorted(missed1_ids - missed2_ids)

    header = ['ID', 'Category', 'Subcategory']
    with open('TotalMissingEvents.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for eid in missing_ids:
            cat, sub = ref.get(eid, ('<unknown>', '<unknown>'))
            writer.writerow([eid, cat, sub])

main()