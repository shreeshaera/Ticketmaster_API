# 🎟️ Ticketmaster Data Pipeline using Python

## 📌 Overview

This project builds a complete data pipeline using the Ticketmaster Discovery API. It extracts raw event data, transforms and cleans complex nested JSON structures, and converts them into structured datasets ready for analysis.

The pipeline covers the full workflow: data extraction → cleaning → transformation → validation → storage, simulating real-world data engineering practices.

----

## 🚀 Key Features

## 🔗 Data Extraction:
* Fetches real-time event data using the Ticketmaster API
* Handles pagination to collect large datasets efficiently
* Manages API errors like timeouts and connection failures

## 🧹 Data Cleaning & Transformation:
* Removes blank and duplicate records
* Converts messy datetime strings into proper formats
* Cleans and standardizes text fields
* Extracts numeric values from unstructured text (e.g., ticket limits)

## 🏗️ Data Modeling
Splits data into structured tables:
* 🎫 Events (Fact Table)
* 🏟️ Venues (Dimension Table)
* 🎭 Categories (Dimension Table)
* 🎤 Pre-Sales (Dimension Table)
* Establishes relationships using unique IDs

## ✅ Data Validation
* Detects and removes invalid date ranges
* Ensures referential integrity between tables
* Handles missing and inconsistent data

----

## 🛠️ Tech Stack
* Python 
* Requests (API handling)
* Pandas (data processing)
* JSON
* NumPy
* Regex

---

## ⚙️ Workflow
* Extract Data from Ticketmaster API
* Parse JSON and collect event data
* Clean & Transform raw data into structured format
* Create Fact & Dimension Tables
* Validate Data Quality
* Export Results into Excel and CSV files

---

## 📊 Output
* 📁 Excel file (raw structured data)
* 📄 CSV files (cleaned datasets):
* events_fact.csv
* ven_dim.csv
* catg_dim.csv
* pre_sales_dim.csv

----

## 🎯 Learning Outcomes
* Working with real-world APIs and pagination
* Handling complex nested JSON data
* Data cleaning and preprocessing techniques
* Building fact and dimension tables
* Performing data validation and integrity checks
* Creating structured datasets for analytics Ticketmaster_API

----

## 🔮 Future Improvements

* Add data visualization (charts/dashboards)
* Store data in a database (SQL)
* Perform exploratory data analysis (EDA)
