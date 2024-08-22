import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt

# Custom CSS for full-page borders and top bar
st.markdown("""
    <style>
    /* Your custom CSS here */
    </style>
    <div class="money-border-left"></div>
    <div class="money-border-right"></div>
    <div class="money-border-top">
        <div class="top-bar-content">
            Your Top Bar Content Here
        </div>
    </div>
    <div class="content">
        <div class="title">Credit Value Calculator</div>
    """, unsafe_allow_html=True)

# Streamlit input elements
range1 = st.number_input("First Range", min_value=300, max_value=850)
percent1 = st.number_input("Percent Increase for First Range", min_value=0, max_value=100)
range2 = st.number_input("Second Range", min_value=range1 + 1, max_value=850)
percent2 = st.number_input("Percent Increase for Second Range", min_value=percent1 + 1, max_value=100)
range3 = st.number_input("Third Range", min_value=range2 + 1, max_value=850)
percent3 = st.number_input("Percent Increase for Third Range", min_value=percent2 + 1, max_value=100)
range4 = st.number_input("Fourth Range", min_value=850, max_value=850)
percent4 = st.number_input("Percent Increase for Fourth Range", min_value=percent3 + 1, max_value=100)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file into a DataFrame
        dataframe = pd.read_csv(uploaded_file)

        # Display the DataFrame immediately after upload
        st.write("Uploaded DataFrame:")
        st.write(dataframe)

        # Check if the required columns exist
        if 'risk_score' not in dataframe.columns:
            st.error("The uploaded file does not contain a 'risk_score' column.")
        elif 'credit_line' not in dataframe.columns:
            st.error("The uploaded file does not contain a 'credit_line' column.")
        else:
            # Add a button to apply changes
            apply_changes = st.button("Apply Changes")

            if apply_changes:
                # Define the function to calculate the linear percent increase based on risk_score
                def calculate_linear_increase(risk_score):
                    if risk_score <= range1:
                        return percent1
                    elif risk_score <= range2:
                        return percent1 + ((percent2 - percent1) / (range2 - range1)) * (risk_score - range1)
                    elif risk_score <= range3:
                        return percent2 + ((percent3 - percent2) / (range3 - range2)) * (risk_score - range2)
                    elif risk_score <= range4:
                        return percent3 + ((percent4 - percent3) / (range4 - range3)) * (risk_score - range3)
                    else:
                        return percent4

                # Calculate the percentage increase and new credit value
                dataframe['percent_increase'] = dataframe['risk_score'].apply(calculate_linear_increase)
                dataframe['new_credit_value'] = dataframe.apply(
                    lambda row: row['credit_line'] * (1 + row['percent_increase'] / 100),
                    axis=1
                )

                x = 0
                # Calculate the total money spent when the new credit value is increased
                for index, row in dataframe.iterrows():
                    old = row["credit_line"]
                    new = row["new_credit_value"]
                    x += (new - old)
                st.write(f"Total Money Spent: {x}")

                y = 0
                # Calculate the total number of credit lines increased
                for index, row in dataframe.iterrows():
                    percentff = row["percent_increase"]
                    if percentff != 0:
                        y += 1
                st.write("Credit Lines Increased: " + str(y))

                z = 0
                # Calculate the total credit line amount
                for index, row in dataframe.iterrows():
                    clff = row["credit_line"]
                    z += clff
                totalamm = z + x
                w = ((totalamm - z) / z) * 100
                st.write("Total Spending Percent Increase: +" + str(w) + "%")

                # Matplotlib Plot with only dots (no connecting lines)
                fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure with size (10, 6)
                x = dataframe["risk_score"]
                y = dataframe["percent_increase"]

                ax.plot(x, y, 'o', color='red')  # 'o' indicates markers only, no lines
                ax.set_title('Percentage Increase vs Risk Score')
                ax.set_xlabel('Risk Score')
                ax.set_ylabel('Percentage Increase')
                ax.grid(True)

                st.pyplot(fig)  # Display the plot

                # Display the updated DataFrame
                st.write("Updated DataFrame with Applied Changes:")
                st.write(dataframe)

                # Convert DataFrame to CSV and provide a download button
                def convert_df_to_csv(df):
                    buffer = io.StringIO()
                    df.to_csv(buffer, index=False)
                    return buffer.getvalue()

                csv_data = convert_df_to_csv(dataframe)
                st.download_button(
                    label="Download Updated CSV",
                    data=csv_data,
                    file_name="updated_credit_data.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"Error reading the file: {e}")

# Close the HTML container
st.markdown("""
        </div>
    """, unsafe_allow_html=True)
