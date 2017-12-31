#!/usr/bin/env python3
# License: CC0

import csv
import re

PROG_MAP = {"UK": "United Kingdom", "US": "United States"}

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

        # We accumulate the USD and GBP grants separately, because the GBP ones
        # require some extra columns to be printed.
        usd_grants = []
        gbp_grants = []

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
                    amount = row['Amount Awarded'].strip()
                    if amount.startswith("$"):
                        usd_grants.append(converted_row(year, program_name, row))
                    elif amount.startswith("£"):
                        gbp_grants.append(converted_row(year, program_name, row))
                    else:
                        raise ValueError("We don't know this currency")

        # Print USD grants
        first = True
        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries,
        affected_regions) values""")
        for grant in usd_grants:
            print(("    " if first else "    ,") + grant)
            first = False
        print(";")

        # Print GBP grants
        first = True
        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries,
        affected_regions) values""")
        for grant in gbp_grants:
            print(("    " if first else "    ,") + grant)
            first = False
        print(";")



def converted_row(year, program_name, row):
    """Convert the given row to a SQL tuple."""

    amount = row['Amount Awarded'].strip()
    if amount.startswith("$"):
        amount = float(amount.replace("$", "").replace(",", ""))
    elif amount.startswith("£"):
        # FIXME: CONVERT FROM POUNDS
        amount = 0.0
    else:
        raise ValueError("We don't know this currency")

    month, day, year2 = (row['Date of Approval (listed as month/day/year)']
                         .split('/'))
    donation_date = year2 + "-" + month + "-" + day

    # This is a sanity check. It shows that the year we get from the way the
    # grants are grouped in the spreadsheet is identical to the year we get
    # from the "Date of Approval" column. Thankfully, this passes for our data.
    assert year == int(year2), (year, int(year2))

    # FIXME: Technical point about program country vs grantee country.
    # Unbound Philanthropy has US and UK programs. The program country is *not*
    # the same thing as the country in which the grantee resides. For example,
    # the 2014 grant to "America's Voice Education Fund (International learning
    # exchange)" is part of the UK program but the "Region" for the grant is
    # the United States. Therefore, the following assertion, if uncommented,
    # would fail. Currently we just use the "Region" column and ignore the
    # program name but we might want to use the program name in the notes
    # column, for instance..
    # assert PROG_MAP[program_name] == row['Region'], (program_name, row['Region'])

    # FIXME: There is a "Duration of Grant (Months)" column (accessed with
    # row["Duration of Grant (Months)"]) that we don't use at the moment.

    # FIXME: There are "Organization City" and "Organization State" columns
    # that we don't use at the moment.

    return ("(" + ",".join([
        mysql_quote("Unbound Philanthropy"),  # donor
        mysql_quote(row['Grantee Name ']),  # donee
        str(amount),  # amount
        mysql_quote(donation_date),  # donation_date
        mysql_quote("day"),  # donation_date_precision
        mysql_quote("donation log"),  # donation_date_basis
        mysql_quote("FIXME"),  # cause_area
        mysql_quote("https://www.unboundphilanthropy.org/who-we-fund"),  # url
        mysql_quote("FIXME"),  # donor_cause_area_url
        mysql_quote("FIXME"),  # notes
        mysql_quote(row['Region']),  # affected_countries
        mysql_quote("FIXME"),  # affected_regions
    ]) + ")")


if __name__ == "__main__":
    main()
