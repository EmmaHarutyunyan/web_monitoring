import os
import csv

FILE = "seen.csv"


def load_seen():
    if not os.path.exists(FILE):
        return set()

    seen = set()
    with open(FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                seen.add(row[0])
    return seen


def save_seen(item_id):
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([item_id])