import csv

filename = "/home/antonio/coding/DCRIDs.csv"

def load_id(filename):
    ids = set()
    with open(filename, newline='') as f:
        next(f)
        for row in csv.reader(f):
            if row:
                ids.add(row[0].strip())
    return ids

def craft_dcr(ids):
    sec1 = "Security!*System["
    sec2 = "Security!*System["
    sec3 = "Security!*System["
    sec4 = "Security!*System["
    sec5 = "Security!*System["
    sec6 = "Security!*System["
    sec7 = "Security!*System["

    for x in range(20):
        sec1 += "(EventID=" + str(ids[x]) +")or"
    
    for x in range(20, 40):
        sec2 += "(EventID=" + str(ids[x]) +")or"
    
    for x in range(40, 60):
        sec3 += "(EventID=" + str(ids[x]) +")or"

    for x in range(60, 80):
        sec4 += "(EventID=" + str(ids[x]) +")or"

    for x in range(80, 100):
        sec5 += "(EventID=" + str(ids[x]) +")or"

    for x in range(100, 120):
        sec6 += "(EventID=" + str(ids[x]) +")or"

    for x in range(120, 140):
        sec7 += "(EventID=" + str(ids[x]) +") or "

    return sec1, sec2, sec3, sec4, sec5, sec6, sec7

def main():
    ids = load_id(filename)
    ids = sorted(list(ids))
    #print(ids)

    dcr = craft_dcr(ids)
    print(dcr)

main()