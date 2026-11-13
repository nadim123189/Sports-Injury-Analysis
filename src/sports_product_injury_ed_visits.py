#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DS2500
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

# Note: the Consumer Product Injury excel file has 12 sheets
# 1 with a Product Grouping Summary and 11 sheets each by a year's data (2013 to 2023)
# The sheets for each year have more detailed data on sports equipment types for 
# the Sports & Recreation Product Grouping
from pathlib import Path
FILEPATH = Path(__file__).resolve().parent.parent / 'data' / 'Consumer Product Injury Tables.xlsx'

'''
Loading, Filtering, and Cleaning Data Functions
'''
def load_product_data(file_path):
    """
    Loads the data into a dataframe and sorts by sheet_name (product summary)
    """
    sheet_name = 'Product Category Summary'
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    return data

def load_year_data(file_path, sheet_name):
    """
    Loads the data into a dataframe where you can input sheet name for the year
    """
    # Skip first 2 lines
    data = pd.read_excel(file_path, sheet_name=sheet_name, header=[2])
    return data

def load_all_year_data(file_path, years=range(2013, 2024)):
    """
    Loads data from all year sheets into a dataframe 
    """
    all_data = []
    for year in years:
        # Read the data for each year (sheet names are years)
        data = pd.read_excel(file_path, sheet_name=str(year), header=[2])
        all_data.append(data)
    
    # Concatenate all years into a single df
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data

def filter_sports_recreation(data):
    """
    Filterrs the dataframe to get sports and recreation data using sports group names
    """
    # Create a regex pattern for the sports group names to be sorted
    sports_pattern = r'ATVs, Mopeds, Minibikes, etc\.|Baseball|Amusement Attractions \(incl\. Rides\)|Barbecue Grills, Stoves, Equipment|Baseball, Softball|Basketball|Beach, Picnic, Camping Equipment|Bicycles & Accessories|Bowling|Boxing|Exercise, Exercise Equipment|Fishing|Football|Golf|Hockey|Horseback Riding|Lacrosse, Rugby, Misc\. Ball Games|Martial Arts'
    
    # Filter rows where 'Product Groupings' contains one of the sports group names
    sports_data = data[data['Product Groupings'].str.contains(sports_pattern, na=False)]
    
    # Create dataframe with renaming
    sports_df = pd.DataFrame({
        'Sport': sports_data['Product Groupings'],
        'Injuries': sports_data['Estimated Number of Injuries'],
        'Hosp. & DOA': sports_data['Hosp. & DOA'],
        '0-4': sports_data['0-4'],
        '5-14': sports_data['5-14'],
        '15-24': sports_data['15-24'],
        '25-64': sports_data['25-64'],
        '65+': sports_data['65+'],
        'Male': sports_data['Male'],
        'Female': sports_data['Female']
    })
    
    # Calculate the percentage of injuries that resulted in hospitalization or death
    sports_df['Hosp. & DOA %'] = (sports_df['Hosp. & DOA'] / sports_df['Injuries']) * 100
    
    # Sort in descending order of injuries
    sorted_sports_df = sports_df.sort_values('Injuries', ascending=False)
    
    return sorted_sports_df

def clean_data(data):
    """
    Cleans data by removing empty columns and rows and removing trailing spaces
    """
    # Remove columns with all NaN values
    data = data.dropna(axis=1, how='all')
    # Remove rows with all NaN values
    data = data.dropna(how='all')
    # Remove '*' in columns
    data.columns = data.columns.str.replace('*', '', regex=False)
    # Remove leading/trailing spaces
    data.columns = data.columns.str.strip()
    
    return data
    
'''
Bar and Line Plot Functions
'''
def plot_injury(data, injury_type, year=None, age_group=None, gender=None):
    """
    Plots injury rate or count for all years or a specific year, filtered by age group and gender.

    Parameters:
        data (DataFrame): the injury dataframe
        injury_type (str): 'rate' or 'count'
        year (int, optional): The year to filter (Defaults to None AKA all years)
        age_group (str, optional): Age group to filter by (e.g., '0-4', '25-64') Defaults to None (all ages)
        gender (str, optional): Gender to filter by ('Male', 'Female') Defaults to None (all genders)
    """
    # Filter by injury type
    filtered_data = data[data['Type'] == injury_type]

    # Filter by year, if specified
    if year is not None:
        filtered_data = filtered_data[filtered_data['Year'] == year]

    # Determine the column to plot
    column_to_plot = 'All Ages'  # Default column
    if age_group is not None:
        column_to_plot = age_group
    elif gender is not None:
        column_to_plot = gender

    # Ensure the column is numeric
    filtered_data[column_to_plot] = pd.to_numeric(filtered_data[column_to_plot], errors='coerce')

    if year is None:
        # Plot for all years (line chart)
        annual_data = filtered_data.groupby('Year')[column_to_plot].mean().reset_index()

        plt.figure(figsize=(10, 6))
        plt.plot(annual_data['Year'], annual_data[column_to_plot], marker='o', linestyle='-', label=injury_type.title())

        # Add labels and title
        plt.title(f'Estimated Injury {injury_type.title()} Over Time ({age_group or "All Ages"}, {gender or "All Genders"})', fontsize=14)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel(f'Injury {injury_type.title()}', fontsize=12)

        # Customize X-axis ticks to show every year
        years = annual_data['Year']
        plt.xticks(ticks=years, labels=years)

        # Add grid and legend
        plt.grid(alpha=0.3)
        plt.legend()
    else:
        # Plot for a specific year (bar chart)
        plt.figure(figsize=(10, 6))
        plt.bar(filtered_data['Product Groupings'], filtered_data[column_to_plot], color='skyblue' if injury_type == 'rate' else 'red')

        # Add labels and title
        plt.title(f'Estimated Injury {injury_type.title()} by Product Groupings in {year} ({age_group or "All Ages"}, {gender or "All Genders"})', fontsize=14)
        plt.xlabel('Product Groupings', fontsize=12)
        plt.ylabel(f'Injury {injury_type.title()}', fontsize=12)

        # Rotate x-axis labels for readability
        plt.xticks(rotation=45, ha='right')

        # Add grid
        plt.grid(alpha=0.3)

    # Show the chart
    plt.tight_layout()
    plt.show()
    
def compare_product_grouping(data, product_groupings, injury_type=None, age_group=None, gender=None):
    """
    Compares the injury rates or counts for specified product groupings over time using a line plot.
    
    Parameters:
        data (DataFrame): The injury data.
        product_groupings (list): A list of product groupings to compare.
        injury_type (str): Either 'rate' or 'count' to specify the type of data to plot.
        age_group (str, optional): Age group column to filter (e.g., '0-4', '25-64'). Defaults to None for all ages.
        gender (str, optional): Gender to filter ('Male' or 'Female'). Defaults to None for all genders.
    """

    # Filter data for the selected product groupings and metric
    filtered_data = data[(data['Product Groupings'].isin(product_groupings)) & (data['Type'] == injury_type)]

    # Apply age group filter
    if age_group:
        filtered_data['Value'] = pd.to_numeric(filtered_data[age_group], errors='coerce')
    else:
        filtered_data['Value'] = pd.to_numeric(filtered_data['All Ages'], errors='coerce')

    # Apply gender filter
    if gender:
        filtered_data['Value'] = pd.to_numeric(filtered_data[gender], errors='coerce')

    # Group by 'Year' and 'Product Groupings' to calculate means
    grouped_data = filtered_data.groupby(['Year', 'Product Groupings'])['Value'].mean().reset_index()

    # Plot for each product grouping
    for grouping in product_groupings:
        # Extract data for the current product grouping
        subset = grouped_data[grouped_data['Product Groupings'] == grouping]

        # Plot the data
        plt.plot(
            subset['Year'],
            subset['Value'],
            marker='o',
            linestyle='-',
            label=f'{grouping} ({injury_type.capitalize()})'
        )

    # Add labels, title, and legend
    age_label = f" ({age_group})" if age_group else ""
    gender_label = f" ({gender})" if gender else ""
    plt.title(f'Comparison of Injury {injury_type.capitalize()}s Over Time by Product Groupings{age_label}{gender_label}')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel(f'Injury {injury_type.capitalize()}')
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
    
def plot_sports_injury_counts(sports_data):
    """
    Plots bar chart of sports injuries for each sports type and hospital death %
    
    Parameters:
        sports_data (DataFrame): The sports dataframe containing injuries and hospital/death data
    """
    # Calculate the "Non-Hosp. & DOA" injuries (total injuries minus Hosp. & DOA)
    sports_data['Treated & Rel.'] = sports_data['Injuries'] - sports_data['Hosp. & DOA']
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Stacked bar chart: first plot Non-Hosp. & DOA (blue), then Hosp. & DOA (red)
    ax.bar(sports_data['Sport'], sports_data['Treated & Rel.'], color='blue', label='Treated & Rel.')
    ax.bar(sports_data['Sport'], sports_data['Hosp. & DOA'], bottom=sports_data['Treated & Rel.'], color='red', label='Hosp. & DOA')

    # Labels and title
    ax.set_xlabel('Sport/Equipment')
    ax.set_ylabel('Number of Injuries')
    ax.set_title('Sports and Recreational Equipment Injuries in 2023')
    
    # Add legend
    ax.legend()
    
    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Show the plot
    plt.show()

'''
Linear Regression Model Functions
'''
def linear_regression_rmse(x, y, random_state=0, test_size=0.2):
    """
    Creates a linear regression model based on training and test data to 
    calculate RMSE using MSE
    
    Parameters:
        x: x-axis variable
        y: y-axis variable
        random_state (int): Random seed
        test_size (float): Proportion of data to be used for testing
    """
    # Use train_test_split to define training and testing data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
    
    # Create model using LinearRegression() and fit to training data
    model = LinearRegression()
    model.fit(x_train, y_train)
    
    # Predict using testing data
    y_pred = model.predict(x_test)
    
    # Calculate RMSE using MSE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Calculate R-squared value
    r_squared = model.score(x, y)
    
    # Return the model, RMSE, R-squared, and test/prediction data
    return model, rmse, r_squared, x_test, y_test, y_pred

def plot_sports_age_rmse(data):
    """
    Plots the relationship between age groups and injury rates for the
    Sports and Recreation product grouping using linear regression model
    
    Parameters:
        data (DataFrame): the data
    """
    # Filter for Sports & Recreational Equipment category and 'rate' type
    sports_data = data[
        (data['Product Groupings'].str.contains('SPORTS AND RECREATION EQUIPMENT', na=False)) &
        (data['Type'] == 'rate')
    ]

    # Extract age group columns
    age_columns = ['0-4', '5-14', '15-24', '25-64', '65+']
    
    # Reshape the DataFrame for modeling (one row per age group and entry)
    reshaped_data = sports_data.melt(
        id_vars=['Product Groupings'], 
        value_vars=age_columns, 
        var_name='Age Group', 
        value_name='Injury Rate'
    )
    
    # Encode age groups as numerical values (for regression)
    reshaped_data['Age Group Encoded'] = reshaped_data['Age Group'].map({
        '0-4': 0, '5-14': 1, '15-24': 2, '25-64': 3, '65+': 4
    })
    
    # Drop rows with missing injury rates
    reshaped_data = reshaped_data.dropna(subset=['Injury Rate'])
    
    # Define x (age group encoded) and y (injury rates)
    x = reshaped_data[['Age Group Encoded']]
    y = reshaped_data['Injury Rate']
    
    # Fit the linear regression model and calculate RMSE and R-squared
    model, rmse, r_squared, x_test, y_test, y_pred = linear_regression_rmse(x, y)
    
    # Print RMSE and R-squared
    print(f"RMSE: {rmse}")
    print(f"R-squared: {r_squared}")
    
    # Plot the data and regression line
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', label='Actual Data', alpha=0.7)
    plt.plot(sorted(x['Age Group Encoded']), 
             model.predict(sorted(x['Age Group Encoded'].values.reshape(-1, 1))), 
             color='red', label='Regression Line')
    
    # Add R-squared to the legend
    plt.legend(title=f'R-squared: {r_squared:.3f}', loc='upper left')
    
    # Title and labels
    plt.title('Age Groups vs. Injury Rates (Sports & Recreation)', fontsize=15)
    plt.xlabel('Age Group (Encoded)', fontsize=12)
    plt.ylabel('Injury Rate', fontsize=12)
    plt.xticks(ticks=range(len(age_columns)), labels=age_columns, rotation=45)
    plt.tight_layout()
    plt.show()
    
    return model
    
'''
Scatterplot and K-Means Clustering Functions
'''
def plot_combined_sports_data(sports_df):
    """
    Plot all the sports data from all years onto scatterplot with # of injuries and
    hospitalizations & DOA
    
    Parameters:
        sports_df (DataFrame): Filtered DataFrame with sports injuries data from all years
    """
    # Create a color palette based on unique sports
    unique_sports = sports_df['Sport'].unique()
    sport_palette = sns.color_palette("Set2", len(unique_sports))  # You can choose a different color palette
    
    # Map each sport to a color
    sport_color_mapping = {sport: color for sport, color in zip(unique_sports, sport_palette)}
    
    # Plotting Injuries vs Hospitalizations & DOA, colored by Sport
    plt.figure(figsize=(12, 8))
    for sport in unique_sports:
        sport_data = sports_df[sports_df['Sport'] == sport]
        plt.scatter(sport_data['Injuries'], sport_data['Hosp. & DOA'], 
                    color=sport_color_mapping[sport], label=sport, alpha=0.6)

    # Adding labels and title
    plt.title('Sports Injuries and Hospitalizations/DOA by Sport (2013-2023)', fontsize=16)
    plt.xlabel('Number of Injuries', fontsize=12)
    plt.ylabel('Hospitalizations & DOA', fontsize=12)

    # Add legend with sport names
    plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def elbow_method(data, max_clusters=10):
    """
    Perform the elbow method to determine the optimal number of clusters
    
    Parameters:
        data (DataFrame): DataFrame with sports injuries data
        max_clusters (int): Maximum number of clusters to test
    
    Returns:
        inertia (list): Sum of squared distances for each number of clusters
    """
    inertia = []
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data[['Injuries', 'Hosp. & DOA']])
    
    # Calculate inertia for different numbers of clusters
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(normalized_data)
        inertia.append(kmeans.inertia_)
    
    # Plot the elbow curve
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), inertia, marker='o')
    plt.title('Elbow Method for Optimal K', fontsize=16)
    plt.xlabel('Number of Clusters (k)', fontsize=12)
    plt.ylabel('Distortion (Inertia)', fontsize=12)
    plt.xticks(range(1, max_clusters + 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    return inertia

def kmeans_clustering(data, n_clusters=3):
    """
    Normalize the data using the StandardScaler and apply k-means
    
    Parameters:
        data (DataFrame): Filtered DataFrame with sports injuries data from all years
        n_clusters (int): Number of k clusters
    """
    # Normalize the data using StandardScaler
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data[['Injuries', 'Hosp. & DOA']])
    
    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(normalized_data)
    
    return data, kmeans

def plot_kmeans_clusters(sports_df, n_clusters=3):
    """
    Plot the k-means clusters using clustered data and centroids
    
    Parameters:
        sports_df (DataFrame): Filtered DataFrame with sports injuries data from all years
        n_clusters (int): Number of k clusters
    """
    # Apply K-Means clustering to the data
    clustered_data, kmeans = kmeans_clustering(sports_df, n_clusters)
    
    # Count data points in each cluster
    cluster_counts = clustered_data['Cluster'].value_counts().sort_index()
    
    # Plotting all data in one plot with K-Means clusters
    plt.figure(figsize=(12, 8))

    # Scatter plot for Injuries vs Hosp. & DOA, colored by Cluster
    scatter = plt.scatter(clustered_data['Injuries'], clustered_data['Hosp. & DOA'], 
                           c=clustered_data['Cluster'], cmap='viridis', alpha=0.7)
    
    # Plot centroids
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x', s=200, label='Centroids')
    
    # Title and labels
    plt.title('K-Means Clustering of Sports Injuries and Hospitalizations (2013-2023)', fontsize=16)
    plt.xlabel('Number of Injuries', fontsize=12)
    plt.ylabel('Hospitalizations & DOA', fontsize=12)
    
    # Build a custom legend
    handles, _ = scatter.legend_elements()
    legend_labels = [f'Cluster {i} ({cluster_counts[i]} points)' for i in range(n_clusters)]
    plt.legend(handles, legend_labels, title="Clusters", loc='upper right', fontsize=10)
    
    # Show plot
    plt.tight_layout()
    plt.show()

def preprocess_age_group(df):
    """
    Preprocess the data to include gender-specific injury data and normalize
    
    Parameters:
        df (DataFrame): Filtered DataFrame with sports injuries data
        
    Returns:
        normalized_data (DataFrame): Normalized dataset with injuries and gender
    """
    # Create columns for Male and Female injury data
    age_group_columns = ['0-4', '5-14', '15-24', '25-64', '65+']
    age_group_data = df[age_group_columns]
    
    # Normalize the data
    scaler = StandardScaler()
    normalized_data = pd.DataFrame(
        scaler.fit_transform(age_group_data),
        columns=age_group_columns
    )

    return normalized_data

def kmeans_clustering_with_age(data, n_clusters=3):
    """
    Perform KMeans clustering on age group injury data

    Parameters:
        data (DataFrame): Normalized age group injury data
        n_clusters (int): Number of clusters

    Returns:
        tuple: Fitted k-means model and clustered data with labels
    """
    # Initialize and fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(data)
    
    # Add cluster labels to the data
    clustered_data = data.copy()
    clustered_data['Cluster'] = kmeans.labels_
    
    return kmeans, clustered_data

def visualize_age_group_clusters(clustered_data):
    """
    Visualize age group clusters using a heatmap of normalized means

    Parameters:
        clustered_data (DataFrame): Data with cluster labels
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        clustered_data.groupby('Cluster').mean(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar=True
    )
    plt.title("Normalized Mean Injury Counts by Age Group (Clustered)")
    plt.xlabel("Age Groups")
    plt.ylabel("Cluster")
    plt.tight_layout()
    plt.show()

def main():
    # Load product data, sports data for 2023, and data for all year sheets
    product_data = load_product_data(FILEPATH)
    sports_data_2023 = filter_sports_recreation(clean_data((load_year_data(FILEPATH, '2023'))))
    all_years_data = filter_sports_recreation(clean_data((load_all_year_data(FILEPATH))))
    
    cleaned_product_data = clean_data(product_data)
    
    '''
    PLOT INJURY RATES
    '''
    # Plot for all years, all ages, and all genders
    plot_injury(cleaned_product_data, injury_type='rate')
    # Plot for 2023 product groupings
    plot_injury(cleaned_product_data, injury_type='rate', year=2023)
    
    # Plot for every age group in 2023
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, age_group='0-4')
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, age_group='5-14')
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, age_group='15-24')
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, age_group='25-64')
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, age_group='65+')
    
    # Plot for gender groups in 2023
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, gender='Male')
    plot_injury(cleaned_product_data, injury_type='rate', year=2023, gender='Female')
    
    '''
    COMPARE PRODUCT GROUPINGS FROM 2013 to 2023
    '''    
    # Let's compare the top 3 product groupings with the highest injury rates
    product_groupings_to_compare = ['HOME FURNISHINGS, FIXTURES AND ACCESSORIES','SPORTS AND RECREATION EQUIPMENT','HOME STRUCTURES & CONSTRUCTION MATERIALS']
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate')
    
    # Compare injury rates for product groupings for gender over time
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', gender='Male')
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', gender='Female')
    

    # Compare rates for product groupings for age groups over time
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', age_group='0-4')
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', age_group='5-14')
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', age_group='15-24')
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', age_group='25-64')
    compare_product_grouping(cleaned_product_data, product_groupings_to_compare, injury_type='rate', age_group='65+')
    
    '''
    SPORTS TYPES BAR CHART
    '''
    # Can view the first few rows to see Hosp & DA %
    print(sports_data_2023.head())
    plot_sports_injury_counts(sports_data_2023)
    
    '''
    LINEAR REGRESSION FOR AGE AND SPORTS INJURIES
    '''
    # Plot regression for SPORTS AND RECREATION EQUIPMENT and 'rate'
    plot_sports_age_rmse(cleaned_product_data)
    
    '''
    SCATTERPLOT FOR ALL YEARS INJURY & HOSPITALIZATION
    '''
    # Plot scatterplot for data for all years for all sports types showing injury and hospitalization
    plot_combined_sports_data(all_years_data)
    
    '''
    K-MEANS CLUSTER FOR ALL YEARS INJURY & HOSPITALIZATION
    '''
    # Use elbow method for the scatterplot above
    inertia = elbow_method(all_years_data, max_clusters=10)
    # Plot kmeans clusters
    plot_kmeans_clusters(all_years_data, n_clusters=3)

    '''
    K-MEANS CLUSTER FOR AGE GROUPS AND SPORTS INJURIES (2023)
    '''
    # Preprocess data for age group clustering
    normalized_age_group_data = preprocess_age_group(sports_data_2023)
    # Perform k-means clustering
    kmeans, clustered_data = kmeans_clustering_with_age(normalized_age_group_data, n_clusters=3)
    # Visualize clusters for age groups and sports injuries
    visualize_age_group_clusters(clustered_data)
    
if __name__ == "__main__":
    main()


