import requests
import json
import pandas as pd

url = "https://app.ticketmaster.com/discovery/v2/events.json" 

all_events =[]

page = 0
while True:

    params = {
    "apikey" : "e29aA4aEYmuJ43s3EYpU6y6QlvC3JTx5",
    "size"   : 50,
    "page"   : page
    }

    try:
        response = requests.get(url,params= params,timeout= 120)
    except requests.exceptions.Timeout as error:
        print(f"Timed out at page {page}, status: {error}")
    except requests.exceptions.ConnectionError as c_error:
        print(f"Request failed at page {page}: {c_error}")
        break
    
    if response.status_code == 400:
        print(f"No more events at page {page}")
        break
    if response.status_code != 200:
        print(f"Error {response.status_code} at page {page}")
        break

    data = response.json()

    total_pages = data["page"]["totalPages"]
    if not data.get("_embedded") or not data["_embedded"].get("events"):
        break
    events = data["_embedded"]["events"]
    all_events.extend(events)

    if page >= total_pages-1:
        break 

    page += 1

print(f"Fetched content: {len(all_events)} events")

cleaned_events = []
cleaned_venues= []
cleaned_categories = []

for events in all_events:
    categories_list = events.get("_embedded",{}).get("attractions", [])
    categories = categories_list[0] if categories_list else {}
    external_links = categories.get("externalLinks", {})

    sales = events.get("sales",{}).get("public", {})
    pre_sales = events.get("sales", {}).get("presales", [])
    artist_pre = pre_sales[0] if len(pre_sales) > 0 else {}
    classification = events.get("classifications", [{}])[0]

    venues_list = events.get("_embedded",{}).get("venues", [])
    venue = venues_list[0] if venues_list else {}

    categories_data = {
        "Id"    : categories.get("id", ""),
        "Name" : categories.get("name", ""),
        "Websites" : ", ".join(external_links.keys()),
        "Segment": classification.get("segment", {}).get("name", ""),
        "Genre": classification.get("genre", {}).get("name", ""),
        "Sub_genre": classification.get("subGenre", {}).get("name", "")
    }
    cleaned_categories.append(categories_data)


    venues_data = {
        "Name" : venue.get("name", ""),
        "Id" : venue.get("id", ""),
        "locale" : venue.get("locale", ""),
        "Postalcode" : venue.get("postalCode", ""),
        "Time_zone" : events.get("dates",{}).get("timezone", ""),
        "City" : venue.get("city",{}).get("name", ""),
        "State" : venue.get("state", {}).get("name", ""),
        "Country" : venue.get("country", {}).get("name", ""),
        "Address" : venue.get("address", {}).get("line1", "")
        }
    cleaned_venues.append(venues_data)


    events_data = {
        "Id" : events.get("id",""),
        "Category_Id" : categories.get("id", ""),
        "Venue_Id" : venue.get("id", ""),

        "Start_date" : sales.get("startDateTime", ""),
        "End_date" : sales.get("endDateTime", ""),

        "Artist_Start_date" : artist_pre.get("startDateTime", ""),
        "Artist_End_date" : artist_pre.get("endDateTime", ""),
        "Artist_pre_sales" : artist_pre.get("name", ""),

        "Ticket_limit" : events.get("ticketLimit",{}).get("info","")
        }
    cleaned_events.append(events_data)



print(f'''The sample data of cleaned_events looks like this:
       { json.dumps(cleaned_events[0],indent = 2)}''')
print(f'''The sample data of cleaned_venues looks like this:
      {json.dumps(cleaned_venues[0],indent = 2)}''')
print(f'''The sample data of cleaned_categories looks like this:
      {json.dumps(cleaned_categories[0],indent = 2)}''')

df_events = pd.DataFrame(cleaned_events)
df_venues = pd.DataFrame(cleaned_venues)
df_categories = pd.DataFrame(cleaned_categories)

with pd.ExcelWriter(r"C:\Users\sribalaji\OneDrive\Documents\ticketmaster.xlsx") as writer:
    df_events.to_excel(writer, sheet_name="Events", index=False)
    df_venues.to_excel(writer, sheet_name="Venues", index=False)
    df_categories.to_excel(writer, sheet_name="Categories", index=False)
