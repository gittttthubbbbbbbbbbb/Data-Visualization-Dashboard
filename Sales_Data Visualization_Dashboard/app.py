import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
@st.cache_data
def load_data(file):
    data = pd.read_csv(file, parse_dates=['Date'])
    return data

# Main function to run the app
def main():
    st.title(" Data Visualization Dashboard")

    # Message about CSV format
    st.markdown(
    """
     *Important:* Your CSV file should follow this format:
    - Columns required: Date, Product, Category, Sales, Profit  
    - Date must be in YYYY-MM-DD format  
    - Sales and Profit must be numeric values  
    """)

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
    else:
        # Load sample data if no file is uploaded
        data = load_data('sales.csv')

    # Sidebar filters
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
    end_date = st.sidebar.date_input("End Date", value=data['Date'].max())
    categories = st.sidebar.multiselect("Select Categories", options=data['Category'].unique())
    products = st.sidebar.multiselect("Select Products", options=data['Product'].unique())

    # Filter data based on user input
    filtered_data = data[
        (data['Date'] >= pd.to_datetime(start_date)) &
        (data['Date'] <= pd.to_datetime(end_date)) &
        (data['Category'].isin(categories) if categories else True) &
        (data['Product'].isin(products) if products else True)
    ]

    # KPIs
    total_sales = filtered_data['Sales'].sum()
    average_sales = filtered_data['Sales'].mean()
    total_profit = filtered_data['Profit'].sum()

    st.header("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Average Sales", f"${average_sales:,.2f}")
    col3.metric("Total Profit", f"${total_profit:,.2f}")

    # Visualizations
    st.header("Visualizations")

    # Line Chart: Sales over Time
    line_chart = px.line(filtered_data, x='Date', y='Sales', title='Sales Over Time')
    st.plotly_chart(line_chart)

    # Bar Chart: Sales by Category
    bar_chart = px.bar(filtered_data.groupby('Category', as_index=False)['Sales'].sum(), 
                        x='Category', y='Sales', title='Sales by Category')
    
    # Pie Chart: Category-wise Sales Distribution
    pie_chart = px.pie(filtered_data, values='Sales', names='Category', title='Category-wise Sales Distribution')

    # Arrange Bar and Pie Chart side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart)
    with col2:
        st.plotly_chart(pie_chart)

    # Scatter Plot: Sales vs Profit
    scatter_plot = px.scatter(filtered_data, x='Sales', y='Profit', title='Sales vs Profit', 
                               labels={'Sales': 'Sales', 'Profit': 'Profit'})
    st.plotly_chart(scatter_plot)

    # Download Button for filtered data
    if st.button("Download Filtered Data"):
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='filtered_sales_data.csv',
            mime='text/csv',
        )

if __name__ == "__main__":

    main()
