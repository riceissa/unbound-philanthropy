# Unbound Philanthropy

This is for [Vipul Naik's donations site](https://github.com/vipulnaik/donations).

Data is from [this page](https://www.unboundphilanthropy.org/who-we-fund),
which has a spreadsheet linked at the bottom: https://www.unboundphilanthropy.org/sites/default/files/Full_Grants_List_December-2017.xlsx

This spreadsheet is opened in LibreOffice and saved as `data.csv` in this
repository.

The spreadsheet has a weird structure, where the country and year information
is not recorded in each row (rather, the grants are grouped together by
country, and within each country by year). The Python script knows about this
structure and deals with it, so modifying the xlsx/csv is not necessary.

## License

CC0.
