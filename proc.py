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
                # These are the regular rows containing the data we want to
                # print
                if row['Grantee Name '] not in ["", "Grantee Name "]:
                    print(("    " if first else "    ,") +
                          converted_row(year, program_name, row))
                    first = False
        print(";")


def converted_row(year, program_name, row):
    """Convert the given row to a SQL tuple."""
    amount = row['Amount Awarded']
    return ( + "(" + ",".join([
        mysql_quote("Wellcome Trust"),  # donor
        mysql_quote(donee),  # donee
        amount,  # amount
        mysql_quote(donation_date),  # donation_date
        mysql_quote("day"),  # donation_date_precision
        mysql_quote("donation log"),  # donation_date_basis
        mysql_quote("FIXME"),  # cause_area
        mysql_quote("https://wellcome.ac.uk/sites/default/files/wellcome-grants-awarded-2000-2016.xlsx"),  # url
        mysql_quote("FIXME"),  # donor_cause_area_url
        mysql_quote(notes),  # notes
        mysql_quote(country),  # affected_countries
        mysql_quote(region),  # affected_regions
    ]) + ")")


if __name__ == "__main__":
    main()
