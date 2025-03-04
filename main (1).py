import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
import statsmodels.api as sm

# Set a page config for better visuals
st.set_page_config(page_title="Statistical Analysis", layout="wide")

# Page Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Statistical Analysis</h1>", unsafe_allow_html=True)

# Data upload
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading the file: {e}")
    else:
        # Show a sample of the dataframe using columns
        st.markdown("### Data Preview")
        with st.expander("Expand to see the data"):
            st.write(data.head(10))

    # Sidebar for analysis selection
    with st.sidebar:
        st.markdown("<h3 style='color: #4CAF50;'>Choose your Analysis:</h3>", unsafe_allow_html=True)
        analysis_type = st.selectbox(
            'Select the type of analysis',
            ('Basic Statistics', 'Basic Plots', 'Regression Analysis')
        )

        # Customization based on selected analysis type
        if analysis_type == 'Basic Plots':
            x_axis = st.selectbox('Select X-axis', data.columns)
            y_axis = st.selectbox('Select Y-axis', data.columns)

        # Variable selection for regression in the sidebar
        if analysis_type == 'Regression Analysis':
            st.markdown("#### Regression Variables")
            y_var = st.selectbox('Select Dependent Variable (y)', data.columns)
            x_vars = st.multiselect('Select Independent Variable(s) (x)', data.columns)

    # Column layout for visual appeal
    col1, col2 = st.columns([1, 3])

    # Show selections only for Basic Plots
    if analysis_type == 'Basic Plots':
        with col1:
            st.markdown("### Your Selections")
            st.write(f"**Analysis Type:** {analysis_type}")
            st.write(f"**X-axis:** {x_axis}")
            st.write(f"**Y-axis:** {y_axis}")
    
    with col2:
        # Generate visualizations based on user selection
        if analysis_type == 'Basic Statistics':
            with st.expander("Expand to view Basic Statistics"):
                st.markdown("#### Basic Statistics")
                st.write(data.describe())
        
        elif analysis_type == 'Basic Plots':
            graph_type = st.selectbox(
                'Select the type of graph you want to visualize:',
                ('Bar Plot', 'Line Plot', 'Scatter Plot', 'Histogram', 'Box Plot')
            )

            if graph_type == 'Bar Plot':
                st.markdown("#### Bar Plot")
                fig, ax = plt.subplots()
                sns.barplot(x=data[x_axis], y=data[y_axis], ax=ax, palette="viridis")
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                st.pyplot(fig)

            elif graph_type == 'Line Plot':
                st.markdown("#### Line Plot")
                fig, ax = plt.subplots()
                sns.lineplot(x=data[x_axis], y=data[y_axis], ax=ax, palette="coolwarm")
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                st.pyplot(fig)

            elif graph_type == 'Scatter Plot':
                st.markdown("#### Scatter Plot")
                scatter_plot = px.scatter(data, x=x_axis, y=y_axis, color=data.columns[0], hover_data=data.columns, color_continuous_scale='Bluered')
                st.plotly_chart(scatter_plot)

            elif graph_type == 'Histogram':
                st.markdown("#### Histogram")
                num_bins = st.slider('Number of bins', min_value=5, max_value=50, value=10)
                fig, ax = plt.subplots()
                sns.histplot(data[x_axis], bins=num_bins, kde=True, ax=ax, color="skyblue")
                ax.set_xlabel(x_axis)
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

            elif graph_type == 'Box Plot':
                st.markdown("#### Box Plot")
                fig, ax = plt.subplots()
                sns.boxplot(x=data[x_axis], y=data[y_axis], ax=ax, palette="Set2")
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                st.pyplot(fig)

        elif analysis_type == 'Regression Analysis':
            st.markdown("#### Linear Regression Analysis")
            
            if x_vars:  # Only perform regression if x variables are selected
                X = data[x_vars]
                X = sm.add_constant(X)
                y = data[y_var]

                model = sm.OLS(y, X).fit()
                predictions = model.predict(X)

                # Display regression summary
                st.write(model.summary())

                # Plot if single independent variable is selected
                if len(x_vars) == 1:
                    fig, ax = plt.subplots()
                    sns.regplot(x=data[x_vars[0]], y=data[y_var], ax=ax, scatter_kws={"color": "black"}, line_kws={"color": "red"})
                    ax.set_xlabel(x_vars[0])
                    ax.set_ylabel(y_var)
                    st.pyplot(fig)
