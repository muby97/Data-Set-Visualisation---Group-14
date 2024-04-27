import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joypy
from matplotlib_venn import venn3

# Load the dataset
df = pd.read_csv("disease_outbreaks_nigeria.csv")

# Data preprocessing: Drop corrupt or inaccurate records
# Assuming 'id' column uniquely identifies each record
df.dropna(subset=['id'], inplace=True)

# 1. Disease Prevalence by State: Bar Chart
def visualize_disease_prevalence_by_state():
    try:
        state_counts = df['state'].value_counts()
        plt.figure(figsize=(10, 6))
        state_counts.plot(kind='bar', color='skyblue')
        plt.xlabel('State')
        plt.ylabel('Cases')
        plt.title('1. Disease Prevalence by State')
        plt.xticks(rotation=45)
        plt.show()
        print("Disease Prevalence by State: This visualization displays the number of disease cases in each state of Nigeria.")
    except Exception as e:
        print(f"Error in Disease Prevalence by State visualization: {e}")

# 2. Gender Disparity in Disease Cases: Pie Chart
def visualize_gender_disparity():
    try:
        gender_counts = df['gender'].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
        plt.title('2. Gender Disparity in Disease Cases')
        plt.show()
        print("Gender Disparity in Disease Cases: This visualization illustrates the distribution of disease cases between male and female patients.")
    except Exception as e:
        print(f"Error in Gender Disparity visualization: {e}")

# 3. Age Distribution of Patients: Histogram
def visualize_age_distribution():
    try:
        plt.figure(figsize=(8, 6))
        plt.hist(df['age'], bins=20, color='salmon', edgecolor='black')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.title('3. Age Distribution of Patients')
        plt.show()
        print("Age Distribution of Patients: This histogram shows the distribution of patients across different age groups.")
    except Exception as e:
        print(f"Error in Age Distribution visualization: {e}")

# 4. Trend Analysis Over Time: Area Chart
def visualize_trend_analysis_over_time():
    try:
        df.groupby('report_year').size().plot(kind='area', color='green', figsize=(10, 6))
        plt.xlabel('Year')
        plt.ylabel('Confirmed Cases')
        plt.title('4. Trend Analysis Over Time')
        plt.show()
        print("Trend Analysis Over Time: This area chart depicts the trend in confirmed disease cases over the years.")
    except Exception as e:
        print(f"Error in Trend Analysis Over Time visualization: {e}")

# 5. Child vs. Adult Affected Groups: Stacked Bar Chart
def visualize_child_vs_adult_affected_groups():
    try:
        age_groups = df.groupby(['child_group', 'adult_group']).size().unstack()
        age_groups.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'], figsize=(8, 6))
        plt.xlabel('Child vs. Adult')
        plt.ylabel('Count')
        plt.title('5. Child vs. Adult Affected Groups')
        plt.legend(title='Age Group')
        plt.show()
        print("Child vs. Adult Affected Groups: This stacked bar chart compares the number of disease cases between children and adults.")
    except Exception as e:
        print(f"Error in Child vs. Adult Affected Groups visualization: {e}")

# 6. Distribution of Cases by Age and Disease: Bubble Chart
def visualize_disease_distribution_bubble_top():
    try:
        # Sample a smaller subset of data (adjust sample size)
        sample_df = df.sample(100, random_state=500)  # Random sampling with fixed seed for reproducibility

        # Assuming a numeric variable (e.g., age) is available
        numeric_var = 'age'  # Replace with the desired numeric variable
        diseases_to_plot = sample_df['disease'].unique()  # All unique diseases in the sample

        sns.scatterplot(x=numeric_var, y='id', size=numeric_var, hue='disease', data=sample_df, palette='hls')
        plt.xlabel(numeric_var)  # Adjust label based on variable name
        plt.ylabel('Number of Cases')
        plt.title('6. Distribution of Cases by Age and Disease')
        plt.legend(title='Disease', loc='upper left', bbox_to_anchor=(1, 0.5))
        plt.show()
        print("Disease Age Distribution: This bubble chart shows the distribution of cases across age groups, with bubble size representing '{}' and color-coded by disease.".format(numeric_var))
    except Exception as e:
        print(f"Error in Disease Distribution visualization: {e}")


# 7. Health Status of Patients: Donut Chart
def visualize_health_status_of_patients():
    try:
        health_counts = df['health_status'].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(health_counts, labels=health_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], wedgeprops=dict(width=0.3))
        plt.title('7. Health Status of Patients')
        plt.show()
        print("Health Status of Patients: This donut chart shows the distribution of health statuses (alive or dead) among patients.")
    except Exception as e:
        print(f"Error in Health Status of Patients visualization: {e}")

# 8. Confirmation Status of Cases: Box Plot
def visualize_confirmation_status_of_cases():
    try:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, x='report_outcome', y='confirmed', palette='pastel')
        plt.xlabel('Confirmation Status')
        plt.ylabel('Cases')
        plt.title('8. Confirmation Status of Cases')
        plt.show()
        print("Confirmation Status of Cases: This box plot illustrates the confirmation status of disease cases.")
    except Exception as e:
        print(f"Error in Confirmation Status of Cases visualization: {e}")

# 9. Time span of Cases: Time series
def visualize_disease_time_series():
    try:
        # Assuming daily data in report_date with potential invalid dates
        def try_convert_date(date_str):
            try:
                return pd.to_datetime(date_str, format='%d/%m/%Y')  # Specify the correct format
            except ValueError:
                return None  # Handle invalid dates

        df['report_date'] = df['report_date'].apply(try_convert_date)  # Apply custom conversion function
        df.dropna(subset=['report_date'], inplace=True)  # Drop rows with invalid dates

        disease_to_plot = 'malaria'  # Replace with the disease of interest
        daily_cases = df.groupby(['report_date', disease_to_plot])['id'].count().unstack()  # Count cases by disease per day
        daily_cases.plot(kind='line', figsize=(10, 6))
        plt.xlabel('Report Date')
        plt.ylabel('Number of Cases')
        plt.title('9. Time Series of Cases for {}'.format(disease_to_plot))
        plt.show()
        print("Time Series of Cases: This line chart shows the number of cases for '{}' over time.".format(disease_to_plot))
    except Exception as e:
        print(f"Error in Disease Time Series visualization: {e}")

# 10. Disease Mortality Rates: Violin Plot
def visualize_disease_mortality_rates():
    try:
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df, x='disease', y='dead', palette='husl')
        plt.xlabel('Disease')
        plt.ylabel('Dead')
        plt.title('10. Disease Mortality Rates')
        plt.xticks(rotation=90)
        plt.show()
        print("Disease Mortality Rates: This violin plot shows the distribution of mortality rates for different diseases.")
    except Exception as e:
        print(f"Error in Disease Mortality Rates visualization: {e}")

# 11. Temporal Patterns: Line Chart
def visualize_temporal_patterns():
    try:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df.groupby('report_year').size().reset_index(name='count'), x='report_year', y='count', color='green')
        plt.xlabel('Year')
        plt.ylabel('Confirmed Cases')
        plt.title('11. Temporal Patterns')
        plt.show()
        print("Temporal Patterns: This line chart illustrates the temporal patterns in confirmed disease cases over the years.")
    except Exception as e:
        print(f"Error in Temporal Patterns visualization: {e}")

# 12. Health Outcome by Settlement Type: Pairplot
def visualize_health_outcome_by_settlement_type():
    try:
        sns.pairplot(df[['settlement', 'health_status', 'confirmed']], hue='settlement', palette='husl')
        plt.suptitle('12. Health Outcome by Settlement Type', y=10.02)
        plt.title('12. Health Outcome by Settlement Type')
        plt.show()
        print("Health Outcome by Settlement Type: This pairplot compares the health outcomes between different settlement types.")
    except Exception as e:
        print(f"Error in Health Outcome by Settlement Type visualization: {e}")

# 13. Age Distribution of Patients: Box Plot
def visualize_age_distribution_box():
    try:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, x='age', palette='husl')
        plt.xlabel('Age')
        plt.title('13. Age Distribution of Patients')
        plt.show()
        print("Age Distribution of Patients: This box plot displays the distribution of patients' ages.")
    except Exception as e:
        print(f"Error in Age Distribution Box visualization: {e}")

# 14. Correlation Analysis: Scatter Plot Matrix
def visualize_correlation_analysis():
    try:
        plt.title('14. Correlation Analysis', y=1.02)
        sns.pairplot(df[['age', 'confirmed', 'dead']], palette='viridis')
        plt.suptitle('14. Correlation Analysis', y=1.02)
        plt.show()
        print("Correlation Analysis: This scatter plot matrix shows the relationships between age, confirmed cases, and mortality.")
    except Exception as e:
        print(f"Error in Correlation Analysis visualization: {e}")


# 15. Disease Prevalenc: Venn Diagram
def visualize_disease_prevalence_venn(df):
    try:
        # Convert disease columns to categorical
        disease_columns = ['cholera', 'diarrhoea', 'measles']
        for column in disease_columns:
            df[column] = df[column].astype('category')

        # Create sets for Venn diagram
        cholera_set = set(df[df['cholera'] == 1]['id'])
        diarrhoea_set = set(df[df['diarrhoea'] == 1]['id'])
        measles_set = set(df[df['measles'] == 1]['id'])

        # Plot Venn diagram
        plt.figure(figsize=(8, 6))
        venn3([cholera_set, diarrhoea_set, measles_set], ('Cholera', 'Diarrhoea', 'Measles'))
        plt.title('15. Disease Prevalence Venn Diagram')
        plt.show()
        print("Disease Prevalence Venn Diagram: This Venn diagram visualizes the overlap and prevalence of cholera, diarrhoea, and measles among the patients.")
    except Exception as e:
        print(f"Error in Disease Prevalence Venn Diagram visualization: {e}")


# 16. Specific Disease Distribution: Radial Wheel Plot
def visualize_specific_disease_distribution_radial():
  try:
    specific_diseases = ['cholera', 'diarrhoea', 'measles', 'viral_haemmorrhaphic_fever',
                          'meningitis', 'ebola', 'marburg_virus', 'yellow_fever',
                          'rubella_mars', 'malaria']
    disease_data = df[specific_diseases].sum()
    # disease_data = df[specific_diseases].value_counts().fillna(0)  
    plt.figure(figsize=(8, 8))
    theta = np.linspace(0, 2*np.pi, len(disease_data))
    radii = disease_data.values
    plt.subplot(111, polar=True)
    plt.plot(theta, radii, marker='o', color='skyblue')
    lines, labels = plt.thetagrids(np.degrees(theta), labels=disease_data.index)
    plt.title('16. Specific Disease Distribution Radial Wheel Plot')
    plt.show()
    print("Specific Disease Distribution Radial Wheel Plot: This radial wheel plot shows the distribution of cases for specific diseases.")
  except Exception as e:
    print(f"Error in Specific Disease Distribution Radial Wheel Plot visualization: {e}")


visualize_disease_prevalence_by_state()
visualize_gender_disparity()
visualize_age_distribution()
visualize_trend_analysis_over_time()
visualize_child_vs_adult_affected_groups()
visualize_disease_distribution_bubble_top()
visualize_health_status_of_patients()
visualize_confirmation_status_of_cases()
visualize_disease_time_series()
visualize_disease_mortality_rates()
visualize_temporal_patterns()
visualize_health_outcome_by_settlement_type()
visualize_age_distribution_box()
visualize_correlation_analysis()
visualize_disease_prevalence_venn(df)
visualize_specific_disease_distribution_radial()
