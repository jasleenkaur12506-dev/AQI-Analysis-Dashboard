# 🌍 Air Quality Index (AQI) Analysis & Visualization

A data analysis and visualization project that analyzes air quality data across different cities and states of India. The project uses Python, Pandas, NumPy, Plotly, and Streamlit to clean, analyze, visualize, and present AQI data through an interactive dashboard.

**Python • Pandas • NumPy • Plotly • Streamlit**

## 📝 Project Overview

Air pollution is one of the major environmental challenges affecting human health and the environment. The purpose of this project is to analyze Air Quality Index (AQI) data and identify pollution patterns across different locations and time periods.

The project provides an interactive web dashboard where users can explore AQI values, compare locations, observe trends, and understand the severity of air pollution through charts, graphs, and maps.

The system focuses on transforming raw AQI data into meaningful visual insights that can help users understand air quality conditions more easily.

## ✨ Key Features & Architecture

**Interactive Dashboard:**
Displays important AQI statistics such as average AQI, highest AQI, lowest AQI, and pollution levels.

**AQI Trends:**
Analyzes changes in AQI over time and helps identify increasing or decreasing pollution patterns.

**India AQI Map:**
Uses an interactive geographical map to visualize AQI levels across different Indian states.

**AQI Analysis:**
Provides detailed comparison of AQI values between different cities, states, and pollutants.

**Data Filtering:**
Allows users to filter the data according to location, date, and other available parameters.

**Interactive Visualizations:**
Uses Plotly charts and graphs to make AQI patterns easier to understand.

## 💻 Tech Stack & Dependencies

### Core Language

**Python:**
The primary programming language used for data processing, analysis, visualization, and dashboard development.

### Data Processing & Analysis

**Pandas:**
Used for loading datasets, cleaning data, handling missing values, filtering records, and performing statistical analysis.

**NumPy:**
Used for numerical calculations and efficient manipulation of data.

### Data Visualization

**Plotly:**
Used to create interactive line charts, bar charts, pie charts, and geographical maps for AQI visualization.

### Dashboard Development

**Streamlit:**
Used to build the interactive web-based dashboard and provide navigation between different project pages.

### Geographical Visualization

**GeoJSON:**
Used with Plotly to display AQI information for different states of India on an interactive map.

## 📊 Dataset

The project uses an AQI dataset containing air-quality measurements collected from different locations.

| Column | Description                           |
| ------ | ------------------------------------- |
| City   | Name of the city                      |
| State  | Name of the state                     |
| Date   | Date of the recorded observation      |
| AQI    | Air Quality Index value               |
| PM2.5  | Fine particulate matter concentration |
| PM10   | Particulate matter concentration      |
| NO2    | Nitrogen dioxide concentration        |
| SO2    | Sulphur dioxide concentration         |
| CO     | Carbon monoxide concentration         |
| O3     | Ozone concentration                   |

*The exact columns may vary depending on the dataset used in the project.*

## ⚙️ Detailed Workflow & Steps

### 1. Data Loading

The AQI dataset is imported using Pandas. The dataset is examined to understand its structure, columns, data types, and available records.

### 2. Data Cleaning

The raw dataset is cleaned before analysis.

* Missing values are identified and handled.
* Duplicate records are removed where required.
* Date columns are converted into appropriate date formats.
* Numerical columns are converted into suitable data types.
* Unnecessary columns are removed.

### 3. Exploratory Data Analysis

The cleaned data is analyzed to understand pollution patterns.

The project calculates:

* Average AQI
* Maximum AQI
* Minimum AQI
* City-wise AQI
* State-wise AQI
* Monthly AQI
* Pollutant levels
* AQI categories

### 4. AQI Classification

AQI values are categorized according to their pollution severity, such as:

* Good
* Satisfactory
* Moderate
* Poor
* Very Poor
* Severe

This makes it easier for users to understand the health and environmental implications of different AQI values.

### 5. AQI Trends

The AQI Trends page analyzes how air quality changes over time.

Line and bar charts are used to visualize:

* Daily AQI trends
* Monthly average AQI
* City-wise AQI trends
* Pollutant trends

This helps identify periods and locations where pollution levels are particularly high.

### 6. Interactive AQI Map

An interactive map of India is created using Plotly and GeoJSON.

Different states can be compared based on their AQI values, allowing users to quickly identify areas with higher or lower pollution levels.

### 7. AQI Analysis

The AQI Analysis page provides detailed statistical and visual analysis of the dataset.

It can be used to:

* Compare cities and states
* Identify highly polluted locations
* Compare different pollutants
* Find highest and lowest AQI values
* Understand overall pollution patterns

### 8. Streamlit Dashboard

The complete project is converted into an interactive Streamlit web application.

The dashboard contains three main navigation pages:

**🏠 Home:**
Provides an overall AQI dashboard and interactive India AQI map.

**📈 AQI Trends:**
Displays AQI changes over time and pollutant trends.

**📊 AQI Analysis:**
Provides detailed comparisons, statistics, and pollution analysis.

## 📈 Results

The project successfully transforms raw air-quality data into an interactive analytical dashboard. It helps users identify pollution trends, compare air quality across locations, and understand the severity of AQI levels through visualizations and an interactive map.

The dashboard provides a simple and user-friendly way to explore large AQI datasets and gain meaningful insights into air pollution.
