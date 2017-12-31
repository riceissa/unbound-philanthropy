#!/usr/bin/env python3
# License: CC0

import csv
import re

def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def main():
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        first = True

        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries,
        affected_regions) values""")

        program_name = None
        year = None

        for row in reader:
            year_m = re.match(r"(\d\d\d\d) Grants", row['Grantee Name '])
            program_m = re.match(r"(\w+) program", row['Grantee Name '],
                                 re.IGNORECASE)
            if year_m:
                year = int(year_m.group(1))
            elif program_m:
                program_name = program_m.group(1)
            else:
                if row['Grantee Name '] not in ["", "Grantee Name "]:
                    amount = row['Amount Awarded']
                    if not (amount.startswith(" $") or amount.startswith(" £")):
                        print(row)


if __name__ == "__main__":
    main()
