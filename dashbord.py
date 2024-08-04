import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Load data function
@st.cache_data
def load_data():
    df = pd.read_excel('flight.xlsx')
    df.columns = [str(name).lower() for name in df.columns.tolist()]
    return df

# Plot functions
def plot_airline_counts(df):
    airline_counts = df['airline'].value_counts()
    colors = plt.cm.tab10.colors
    plt.figure(figsize=(10, 6))
    plt.barh(airline_counts.index, airline_counts.values, color=colors[:len(airline_counts)])
    plt.xlabel('Number of counts')
    plt.ylabel('Airline')
    plt.title('Count of Airlines')
    st.pyplot(plt)

def plot_top_airlines(df):
    top_airline = df['airline'].value_counts().nlargest(10)
    plt.figure(figsize=(10, 6))
    ax = top_airline.plot(kind="bar")
    plt.title("Top Airlines")
    plt.xlabel("Airlines")
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    st.pyplot(plt)

def plot_avg_dep_delays(df):
    avg_dep_delays = df.groupby("airline")["dep_delay"].mean().sort_values()
    plt.figure(figsize=(10, 6))
    plt.bar(avg_dep_delays.index, avg_dep_delays, color='purple')
    plt.xlabel('Airline')
    plt.ylabel('Mean DEP Delay')
    plt.xticks(rotation=90)
    plt.title('Average Departure Delays by Airline')
    st.pyplot(plt)

def plot_airline_pie_chart(df):
    airline_counts = df['airline'].value_counts()
    plt.figure(figsize=(10, 7))
    plt.pie(airline_counts, labels=airline_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Airlines by Share of Domestic Flight Volume')
    st.pyplot(plt)

def plot_top_origins(df):
    top_origin_counts = df['origin'].value_counts().head(30)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_origin_counts.index, y=top_origin_counts.values, color='purple')
    plt.xlabel('Origin Airport Name')
    plt.ylabel('Count')
    plt.title('Top Airports by Outgoing Flight Count')
    plt.xticks(rotation=80)
    st.pyplot(plt)

def plot_cities_flight_share(df):
    dest_city_counts = df['dest_city'].value_counts().head(30)
    top_origin_counts = df['origin'].value_counts().head(30)
    combined_city_count = dest_city_counts.add(top_origin_counts, fill_value=0)
    sorted_combine_count = combined_city_count.sort_values(ascending=False)
    top_cities = sorted_combine_count.head(40)
    others_count = sorted_combine_count[40:].sum()
    top_cities['Others'] = others_count

    plt.figure(figsize=(10, 7))
    plt.pie(top_cities, labels=top_cities.index, autopct='%1.1f%%', startangle=90)
    plt.title('Cities by Share of Flight Count')
    st.pyplot(plt)


def main():
    st.set_page_config(
        layout='wide',
        page_title='Flight Data Analysis',
        page_icon='✈️'
    )
    st.title('Flight Data Analysis ')

    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
        st.sidebar.success("Data loaded successfully")
    
    # Display raw data
    st.write("## Flight Data")
    st.dataframe(df)

    # Sidebar for navigation
    st.title("Navigation")
    options = st.selectbox("Go to", ["Airline Counts", "Top Airlines", "Average Departure Delays", "Airline Pie Chart", "Top Origins", "Cities Flight Share"])

    # Display plots based on sidebar selection
    if options == "Airline Counts":
        plot_airline_counts(df)
    elif options == "Top Airlines":
        plot_top_airlines(df)
    elif options == "Average Departure Delays":
        plot_avg_dep_delays(df)
    elif options == "Airline Pie Chart":
        plot_airline_pie_chart(df)
    elif options == "Top Origins":
        plot_top_origins(df)
    elif options == "Cities Flight Share":
        plot_cities_flight_share(df)

if __name__ == '__main__':
    main()

    
  
