import pandas as pd
import re
import numpy as np
import csv

# ================= Extracting excel data into datframe ================= #
eve_data = pd.read_excel(r"C:\Users\sribalaji\OneDrive\Documents\ticketmaster.xlsx", sheet_name=0)
ven_data = pd.read_excel(r"C:\Users\sribalaji\OneDrive\Documents\ticketmaster.xlsx", sheet_name=1)
catg_data = pd.read_excel(r"C:\Users\sribalaji\OneDrive\Documents\ticketmaster.xlsx", sheet_name=2)


# ================= Deleting blanks/empty rows ================= #
def delete_blanks(data):
     data = data.replace(r"^\s*$", pd.NA, regex = True)
     return data.dropna(how ="all")
eve_data = delete_blanks(eve_data)
ven_data = delete_blanks(ven_data)
catg_data = delete_blanks(catg_data)


# ================= Deleting duplicate rows based on unique ID ================= #
eve_data = eve_data.drop_duplicates(subset="Id").reset_index(drop=True)
ven_dim = ven_data.drop_duplicates(subset="Id").reset_index(drop=True)
catg_dim = catg_data.drop_duplicates(subset="Id").reset_index(drop=True)


# ================= Converting messy string datetime to  datetime format ================= #
date_cols = ["Start_date","End_date","Artist_Start_date","Artist_End_date"]
eve_data[date_cols] = eve_data[date_cols].apply(
    lambda col: pd.to_datetime(col, errors="coerce").dt.tz_localize(None) )


# ================= trimming unwanted text ================= #
text_cols_e = ["Id", "Category_Id", "Venue_Id", "Artist_pre_sales"]
eve_data[text_cols_e] = eve_data[text_cols_e].apply(
    lambda col: col.astype("string").str.strip())

text_cols_c = ["Id","Name", "Segment", "Genre", "Sub_genre"]
catg_dim[text_cols_c] = catg_dim[text_cols_c].apply(
     lambda col: col.astype("string").str.strip())

text_cols_v = ["Id","Name","Time_zone", "City", "State", "Country", "Address"]
ven_dim[text_cols_v] = ven_dim[text_cols_v].apply(
     lambda col: col.astype("string").str.strip())


# ================= Organizing text into titles ================= #
eve_data["Artist_pre_sales"] = eve_data["Artist_pre_sales"].str.title()

title_cols_c = ["Name", "Segment", "Genre", "Sub_genre"]
catg_dim[title_cols_c] = catg_dim[title_cols_c].apply(
     lambda col: col.astype("string").str.title())

title_cols_v = ["Name", "City", "State", "Country", "Address"]
ven_dim[title_cols_v] = ven_dim[title_cols_v].apply(
     lambda col: col.astype("string").str.title())


# ================= Extracting the number from ticket limit ================= #
eve_data["Ticket_limit"] = eve_data["Ticket_limit"].apply(
     lambda x : int(re.search(r"\d+", str(x)).group()) if re.search(r"\d+", str(x)) else pd.NA
)
eve_data["Ticket_limit"] = eve_data["Ticket_limit"].astype("Int64")



# ================= Altering the fact and dimension tables ================= #

# >>>>>> Creating new dimension table for pre_Sales category:
pre_sales_dim = (eve_data[["Artist_pre_sales"]].drop_duplicates()
                         .dropna(subset = ["Artist_pre_sales"]).reset_index(drop =True))
pre_sales_dim["Pre_sales_Id"] = pre_sales_dim.index + 1 


# >>>>>> Linking the connection between two tables:
eve_data = eve_data.merge(pre_sales_dim, how = "left", on = "Artist_pre_sales")
eve_data.drop("Artist_pre_sales", axis = 1, inplace = True)
eve_data["Pre_sales_Id"] = eve_data["Pre_sales_Id"].astype("Int64")
eve_data["Pre_sales_Id"] = eve_data["Pre_sales_Id"].replace(pd.NA, None)


# ================= Handling empty strings ================= #
def empty_values(df):
    df = df.replace(r'^\s*$', np.nan, regex = True)
    return df
eve_data = empty_values(eve_data)
ven_dim = empty_values(ven_dim)
catg_dim = empty_values(catg_dim)
pre_sales_dim = empty_values(pre_sales_dim)


# ================= Data validation ================= #

# >>>>>> Checking invalid / incosistent dates:
invalid_dates = eve_data[eve_data["End_date"] < eve_data["Start_date"]]
invalid_pre_dates = eve_data[eve_data["Artist_End_date"] < eve_data["Artist_Start_date"]]

if invalid_dates.empty:
    print("No invalid general_dates found ✅")
else:
    print(f"Found {len(invalid_dates)} invalid dates:")
    print(invalid_dates)

if invalid_pre_dates.empty:
    print("No invalid pre_dates found ✅")
else:
    print(f"Found {len(invalid_pre_dates)} invalid dates:")
    print(invalid_pre_dates)

# >>>>>> Checking if venue and attraction tables Id's are present in events table:
ven_check= eve_data[~eve_data["Venue_Id"].isin(ven_dim["Id"])]
catg_check = eve_data[~eve_data["Category_Id"].isin(catg_dim["Id"])]

if ven_check.empty:
    print("No missing Venue_Id's found ✅ ")
else:
    print(f"Found {len(ven_check)} missing Venue_id's")

if catg_check.empty:
    print("No missing Category_Id's found ✅")
else:
    print(f"Found {len(catg_check)} missing Category_id's")


# ================= Data validation ================= #

# >>>>>> Removing invalid dates: 
eve_data = eve_data[
    (eve_data["End_date"].isna()) |
    (eve_data["Start_date"].isna()) |
    (eve_data["End_date"] >= eve_data["Start_date"])
]
eve_data = eve_data[
    (eve_data["Artist_End_date"].isna()) |
    (eve_data["Artist_Start_date"].isna()) |
    (eve_data["Artist_End_date"] >= eve_data["Artist_Start_date"])
]

# >>>>>> Removing rows with empty dates: 
eve_data = eve_data.dropna(
    subset=date_cols,
    how="all"
)


# >>>>>> Removing broken venue and events cardinality:
eve_data = eve_data[eve_data["Venue_Id"].isin(ven_dim["Id"])]

# >>>>>> Removing broken attraction and events cardinality:
eve_data = eve_data[eve_data["Category_Id"].isin(catg_dim["Id"])]


# ================= Sorting the events table ================= #
eve_data = eve_data[["Id", "Category_Id","Venue_Id", "Pre_sales_Id", "Start_date", "End_date", "Artist_Start_date",
       "Artist_End_date", "Ticket_limit"]]
ven_dim = ven_dim[["Id", "Name", "locale","Postalcode","Time_zone", "City", "State", "Country", "Address"]]
catg_dim = catg_dim[["Id", "Name","Websites", "Segment", "Genre", "Sub_genre"]]
pre_sales_dim = pre_sales_dim[["Pre_sales_Id", "Artist_pre_sales"]]



# ================= Total empty values in each column  ================= #
print(f"Total empty values in events table: \n {eve_data.isna().sum()} \n")
print(f"Total empty values in venues table: \n{ven_dim.isna().sum()} \n")
print(f"Total empty values in categories table: \n {catg_dim.isna().sum()} \n")
print(f"Total empty values in pre_sales_dimension table: \n {pre_sales_dim.isna().sum()} \n")


# ================= Cleaned and Filtered tables preview ================= #
print(f'''
The sample data of events looks like this:
      {eve_data.head(5)}
''')
print(f'''
The sample data of venues looks like this:
      {ven_dim.head(5)}
''')
print(f'''
The sample data of categories looks like this:
      {catg_dim.head(5)}
''')
print(f'''
The sample data of pre sales dimension looks like this:
      {pre_sales_dim.head(5)}
''')


# ================= Saving the cleaned data into new excel files ================= #
eve_data.to_csv(r"C:\Users\sribalaji\OneDrive\Documents\excel shreesha\Project_1.0\events_fact.csv", index= False,encoding = "utf-8-sig")
ven_dim.to_csv(r"C:\Users\sribalaji\OneDrive\Documents\excel shreesha\Project_1.0\ven_dim.csv", index= False, encoding = "utf-8-sig")
catg_dim.to_csv(r"C:\Users\sribalaji\OneDrive\Documents\excel shreesha\Project_1.0\catg_dim.csv", index= False, encoding = "utf-8-sig")
pre_sales_dim.to_csv(r"C:\Users\sribalaji\OneDrive\Documents\excel shreesha\Project_1.0\pre_sales_dim.csv", index= False, encoding = "utf-8-sig")