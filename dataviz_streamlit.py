import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# Set Seaborn style for plots
sns.set_style("whitegrid")

# Sidebar for "About Me"
st.sidebar.title("About Me")
st.sidebar.write("""
    **Name**: Axel Aouizerate  
    **Age**: 21  
    **Education**: Master's in Data - Business Intelligence & Analytics at EFREI Paris  
    **Interests**: Data Science, Machine Learning, Political Analysis  
    **GitHub**: [AxelAouizerate](https://github.com/AxelAouizerate)  
    **LinkedIn**: [Axel Aouizerate](https://www.linkedin.com/in/axel-aouizerate-9a1946221/)  
""")
st.sidebar.write("Feel free to connect with me!")

# Title and Introduction
st.title("French Presidential Election 2022 - 1st Round: Analyzing Voting Patterns by Socio-Demographic Factors")
st.markdown("""
    This analysis is structured into multiple parts where we explore how various socio-economic and demographic factors influence voting patterns in the 2022 French presidential elections.
""")

# Plan of the analysis
st.header("Plan of the Presentation")
st.write("""
    1. **Wealth and Vote**:
       Do rich people actually vote for the right-wing and center, and do poor people vote for the left-wing? We will explore the relationship between wealth and voting behavior.
       
    2. **Abstention and Access to Education**:
       Is abstention higher in departments with less access to education? We will investigate how education levels impact voter participation.

    3. **Youth and Extremism**:
       Do departments with younger populations tend to vote for more extreme parties, both on the far-left and far-right? We will explore the relationship between age and extreme political preferences.

    4. **Diversity and Vote**:
       How do departments with high levels of diversity (religion, ethnicity, culture) vote compared to those with less diversity? We will examine if diversity correlates with certain political leanings.
""")

# Step 1: Upload the preprocessed DataFrame
uploaded_file = st.file_uploader("Upload your preprocessed dataset (CSV or Excel)", type=["csv", "xlsx"])

# If the user uploads a file, use the preprocessed data
if uploaded_file is not None:
    # Detect file type and load DataFrame
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Show a preview of the DataFrame
    st.write("Here’s a preview of the 2022 presidential elections by department:")
    st.dataframe(df.head())

    # Group parties: left, right, extreme, center (including all candidates in percentage terms)
    left_parties_pct = ['% Voix/Exp MÉLENCHON', '% Voix/Exp HIDALGO', '% Voix/Exp JADOT', '% Voix/Exp ROUSSEL', '% Voix/Exp ARTHAUD', '% Voix/Exp POUTOU']
    right_parties_pct = ['% Voix/Exp LE PEN', '% Voix/Exp ZEMMOUR', '% Voix/Exp PÉCRESSE', '% Voix/Exp DUPONT-AIGNAN']
    center_parties_pct = ['% Voix/Exp MACRON']

    # Add calculated columns for grouped votes as percentages
    df['left_votes_pct'] = df[left_parties_pct].sum(axis=1)
    df['right_votes_pct'] = df[right_parties_pct].sum(axis=1)
    df['center_votes_pct'] = df[center_parties_pct].sum(axis=1)


    # Step 1: Reshape the data to long format (for Altair compatibility)
    df_melted = df.melt(id_vars=['Libellé du département'], 
                        value_vars=['left_votes_pct', 'right_votes_pct'], 
                        var_name='Political_Spectrum', value_name='Vote_Percentage')

    # Step 2: Create an interactive line chart
    line_chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x='Libellé du département:O',  # Department names on the x-axis
        y='Vote_Percentage:Q',  # Vote percentage on the y-axis
        color='Political_Spectrum:N',  # Color based on political spectrum (left, right, center)
        tooltip=['Libellé du département', 'Political_Spectrum', 'Vote_Percentage']  # Hover tooltip
    ).interactive().properties(
        title='Voting Patterns by Political Spectrum Across Departments'
    )

    # Step 3: Display the chart in Streamlit
    st.altair_chart(line_chart, use_container_width=True)


    # PART 1: Wealth and Vote
    st.header("Part 1: Wealth and Vote")
    st.write("Let's explore the voting trends in rich and poor departments based on the percentage of votes.")

    # Plot for Top 5 departments voting most for left-wing parties by percentage
    st.subheader("Top 5 Departments Voting Most for Left-Wing Parties (%)")
    top_left_departments_pct = df[['Libellé du département', 'left_votes_pct']].sort_values(by='left_votes_pct', ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='left_votes_pct', data=top_left_departments_pct, palette='Blues_d')
    plt.title('Top 5 Departments Voting Most for Left-Wing Parties (%)')
    plt.xlabel('Department')
    plt.ylabel('Left Votes (%)')
    st.pyplot(plt.gcf())

    st.write("""
             These departements are generally poor. For example Seine Saint Denis and Guadeloupe have 30% poverty rate, way more than the national average which is 14.5%. We can deduce a correlation between voting left and poverty levels.
             """)

    # Plot for Top 5 departments voting least for left-wing parties by percentage
    st.subheader("Top 5 Departments Voting Least for Left-Wing Parties (%)")
    least_left_departments_pct = df[['Libellé du département', 'left_votes_pct']].sort_values(by='left_votes_pct', ascending=True).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='left_votes_pct', data=least_left_departments_pct, palette='Reds_d')
    plt.title('Top 5 Departments Voting Least for Left-Wing Parties (%)')
    plt.xlabel('Department')
    plt.ylabel('Left Votes (%)')
    st.pyplot(plt.gcf()) 

    st.write("""
             Based on clichés, we could expect that rich departements would be here. However we see that the departements who don't vote for the left are poor too. It's hard to conclude a trend between poverty level and voting for the left.
             """)

    # Plot for Top 5 departments voting most for right-wing parties by percentage
    st.subheader("Top 5 Departments Voting Most for Right-Wing Parties (%)")
    top_right_departments_pct = df[['Libellé du département', 'right_votes_pct']].sort_values(by='right_votes_pct', ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='right_votes_pct', data=top_right_departments_pct, palette='Greens_d')
    plt.title('Top 5 Departments Voting Most for Right-Wing Parties (%)')
    plt.xlabel('Department')
    plt.ylabel('Right Votes (%)')
    st.pyplot(plt.gcf())

    st.write("""
             The departement voting for the right do not belong to the same wealth category. Some like Corse and Var have low poverty index, whereas Mayotte has the highest poverty index in France equal to 70%, or 5 times the national average.
             The cliché saying that rich departement tend to vote for the right doesn't seem to be true """)

    # Plot for Top 5 departments voting most for centrist parties (Macron) by percentage
    st.subheader("Top 5 Departments Voting Most for Centrist Parties (%)")
    top_center_departments_pct = df[['Libellé du département', 'center_votes_pct']].sort_values(by='center_votes_pct', ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='center_votes_pct', data=top_center_departments_pct, palette='Purples_d')
    plt.title('Top 5 Departments Voting Most for Centrist Parties (%)')
    plt.xlabel('Department')
    plt.ylabel('Center Votes (%)')
    st.pyplot(plt.gcf())

    st.write("""
             The wealth of these departements is variable. Some rich and poor departements voted for the center""")
    
    st.header("""
             Conclusion of Part 1 
            """)
    
    st.write("""
            Based on the data, we couldn't conclude with confidence that there is a correlation between wealth and vote. The cliché that poor people vote for the left and rich people vote for the right doesn't seem to be right.
             """)


    # PART 2: Abstention and Access to Education
    st.header("Part 2: Abstention and Access to Education")
    st.write("We’ll examine whether there is a correlation between abstention rates and access to education.")

    # Plot for Top 5 departments with the most abstention
    st.subheader("Top 5 Departments with the Highest Abstention")
    top_abstention_departments = df[['Libellé du département', '% Abs/Ins']].sort_values(by='% Abs/Ins', ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='% Abs/Ins', data=top_abstention_departments, palette='Oranges_d')
    plt.title('Top 5 Departments with the Highest Abstention (%)')
    plt.xlabel('Department')
    plt.ylabel('Abstention Rate (%)')
    st.pyplot(plt.gcf())

    st.write("""
        The above departements have weak access to education : In Guyane, the drop out rate before completing high school is 40%. These departements also lack universities infrastructures for the population. )
    """)

    # Plot for Top 5 departments with the lowest abstention
    st.subheader("Top 5 Departments with the Highest Participation")
    low_abstention_departments = df[['Libellé du département', '% Abs/Ins']].sort_values(by='% Abs/Ins', ascending=True).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='% Abs/Ins', data=low_abstention_departments, palette='Oranges_d')
    plt.title('Top 5 Departments with the Highest Abstention (%)')
    plt.xlabel('Department')
    plt.ylabel('Abstention Rate (%)')
    st.pyplot(plt.gcf())

    st.write("""
        The above departements have weak access to education, but have high participation, somehow. This is due to other factors such as political tradition. For example many agricultural unions have been created in Le Gers.   
    """)

    st.write("""
             To conclude, there is a strong correlation between access to education and abstention rates, but there are outliers
             """)

    # PART 3: Youth and Extremism
    st.header("Part 3: Youth and Extremism")
    st.write("We will explore the relationship between youth population and votes for extreme parties.")



# Check if the required columns are in the dataset before proceeding
required_columns_extreme = ['% Voix/Exp MÉLENCHON', '% Voix/Exp LE PEN', '% Voix/Exp ZEMMOUR', '% Voix/Exp ROUSSEL']
required_columns_center = ['% Voix/Exp MACRON', '% Voix/Exp PÉCRESSE', '% Voix/Exp HIDALGO']

if all(col in df.columns for col in required_columns_extreme) and all(col in df.columns for col in required_columns_center):
    
    # Group candidates into extremist and centrist categories
    extremist_parties = ['% Voix/Exp MÉLENCHON', '% Voix/Exp LE PEN', '% Voix/Exp ZEMMOUR', '% Voix/Exp ROUSSEL']
    centrist_parties = ['% Voix/Exp MACRON', '% Voix/Exp PÉCRESSE', '% Voix/Exp HIDALGO']

    # Calculate the total percentage of votes for extremist and centrist parties
    df['extreme_votes_pct'] = df[extremist_parties].sum(axis=1)
    df['center_votes_pct'] = df[centrist_parties].sum(axis=1)

    # Get the top 5 departments for extremist parties
    top_extremist_departments = df[['Libellé du département', 'extreme_votes_pct']].sort_values(by='extreme_votes_pct', ascending=False).head(5)

    # Get the top 5 departments for centrist parties
    top_centrist_departments = df[['Libellé du département', 'center_votes_pct']].sort_values(by='center_votes_pct', ascending=False).head(5)

    # Plot for Top 5 departments voting for extremist parties by percentage
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='extreme_votes_pct', data=top_extremist_departments, palette='Reds_d')
    plt.title('Top 5 Departments Voting for Extremist Parties (%)')
    plt.xlabel('Department')
    plt.ylabel('Extremist Votes (%)')
    plt.tight_layout()
    st.pyplot(plt.gcf())

    st.write("""
            Guyane, la Réunion and Mayotte have a very young population whereas Martinique and Guadeloupe have old populations. Based on the data, we can't make a correlation between age and voting for extremist parts.
             """)


    # Plot for Top 5 departments voting for centrist parties by percentage
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Libellé du département', y='center_votes_pct', data=top_centrist_departments, palette='Purples_d')
    plt.title('Top 5 Departments Voting for Centrist Parties (%)')
    plt.xlabel('Department')
    plt.ylabel('Centrist Votes (%)')
    plt.tight_layout()
    st.pyplot(plt.gcf())

else:
    st.error("The dataset doesn't contain the required columns for extremist and centrist votes.")

    st.write("""
            Here again, we have some departements with younger people, and some with older people voting heavily for the center. We can't see a correlation between age and vote based on this plot.
             """)
    
    st.write("""
            We can try to make another plot.
             """)


# Grouping extreme parties (adjust based on your dataset columns)
extreme_parties = ['% Voix/Exp MÉLENCHON', '% Voix/Exp LE PEN', '% Voix/Exp ZEMMOUR']

# Create a new column for total votes for extreme parties
df['extreme_votes_pct'] = df[extreme_parties].sum(axis=1)

# Define the youngest departments (use actual age data if available)
youngest_departments = ['Mayotte', 'Guyane', 'Seine-Saint-Denis', 'Réunion', 'Guadeloupe']

# Filter the DataFrame for these departments
top_youngest_df = df[df['Libellé du département'].isin(youngest_departments)]

# Define the national average for extreme votes (adjust based on your data)
national_average_extreme = df['extreme_votes_pct'].mean()

# Create a DataFrame for plotting, including the national average
plot_data = top_youngest_df[['Libellé du département', 'extreme_votes_pct']]
plot_data['national_average_extreme'] = national_average_extreme

# Plot the top 5 youngest departments voting for extreme parties vs national average
plt.figure(figsize=(10, 6))
sns.barplot(x='Libellé du département', y='extreme_votes_pct', data=plot_data, color='red', label='Department Extreme Votes (%)')
sns.lineplot(x='Libellé du département', y='national_average_extreme', data=plot_data, color='blue', label='National Average (%)', marker='o')

# Add titles and labels
plt.title('Top 5 Youngest Departments Votes for Extreme Parties vs National Average')
plt.xlabel('Department')
plt.ylabel('Votes for Extreme Parties (%)')
plt.legend()

# Show the plot
plt.tight_layout()
st.pyplot(plt.gcf())

st.header("""
          Conclusion
          """)

st.write("""
         We see a significant correlation between youth and extreme votes.
         """)


    # PART 4: Diversity and Vote
st.header("Part 4: Diversity and Vote")
st.write("In this part, we will analyze how diversity, inside regions impacts the vote. We will plot the votes for the 5 most diverse and 5 least diverse departements (according to INSEE) ")

# Grouping left-wing and right-wing parties
left_parties = ['% Voix/Exp MÉLENCHON', '% Voix/Exp HIDALGO', '% Voix/Exp JADOT', '% Voix/Exp ROUSSEL', '% Voix/Exp ARTHAUD', '% Voix/Exp POUTOU']
right_parties = ['% Voix/Exp LE PEN', '% Voix/Exp ZEMMOUR', '% Voix/Exp PÉCRESSE', '% Voix/Exp DUPONT-AIGNAN']

# Create new columns for total left and right votes
df['left_votes_pct'] = df[left_parties].sum(axis=1)
df['right_votes_pct'] = df[right_parties].sum(axis=1)

# Define the most and least diverse departments
most_diverse_departments = ['Seine-Saint-Denis', 'Paris', 'Val-de-Marne', 'Bouches-du-Rhône', 'Rhône']
least_diverse_departments = ['Creuse', 'Cantal', 'Lot', 'Lozère', 'Aveyron']

# Filter the DataFrame for these departments
most_diverse_df = df[df['Libellé du département'].isin(most_diverse_departments)]
least_diverse_df = df[df['Libellé du département'].isin(least_diverse_departments)]

# Calculate national averages for left and right votes
national_avg_left = df['left_votes_pct'].mean()
national_avg_right = df['right_votes_pct'].mean()

# Prepare the data for plotting, including the national average
plot_data_most_diverse = most_diverse_df[['Libellé du département', 'left_votes_pct', 'right_votes_pct']]
plot_data_most_diverse['national_avg_left'] = national_avg_left
plot_data_most_diverse['national_avg_right'] = national_avg_right

plot_data_least_diverse = least_diverse_df[['Libellé du département', 'left_votes_pct', 'right_votes_pct']]
plot_data_least_diverse['national_avg_left'] = national_avg_left
plot_data_least_diverse['national_avg_right'] = national_avg_right

# Plot for most diverse departments
plt.figure(figsize=(12, 6))

# Left votes
sns.barplot(x='Libellé du département', y='left_votes_pct', data=plot_data_most_diverse, color='blue', label='Department Left Votes (%)')
sns.lineplot(x='Libellé du département', y='national_avg_left', data=plot_data_most_diverse, color='black', label='National Avg Left Votes (%)', marker='o')

plt.title('Left Votes in Most Diverse Departments vs National Average')
plt.xlabel('Department')
plt.ylabel('Left Votes (%)')
plt.legend()
plt.tight_layout()
st.pyplot(plt.gcf())

# Right votes
plt.figure(figsize=(12, 6))
sns.barplot(x='Libellé du département', y='right_votes_pct', data=plot_data_most_diverse, color='red', label='Department Right Votes (%)')
sns.lineplot(x='Libellé du département', y='national_avg_right', data=plot_data_most_diverse, color='black', label='National Avg Right Votes (%)', marker='o')

plt.title('Right Votes in Most Diverse Departments vs National Average')
plt.xlabel('Department')
plt.ylabel('Right Votes (%)')
plt.legend()
plt.tight_layout()
st.pyplot(plt.gcf())

# Plot for least diverse departments
plt.figure(figsize=(12, 6))

# Left votes
sns.barplot(x='Libellé du département', y='left_votes_pct', data=plot_data_least_diverse, color='blue', label='Department Left Votes (%)')
sns.lineplot(x='Libellé du département', y='national_avg_left', data=plot_data_least_diverse, color='black', label='National Avg Left Votes (%)', marker='o')

plt.title('Left Votes in Least Diverse Departments vs National Average')
plt.xlabel('Department')
plt.ylabel('Left Votes (%)')
plt.legend()
plt.tight_layout()
st.pyplot(plt.gcf())

# Right votes
plt.figure(figsize=(12, 6))
sns.barplot(x='Libellé du département', y='right_votes_pct', data=plot_data_least_diverse, color='red', label='Department Right Votes (%)')
sns.lineplot(x='Libellé du département', y='national_avg_right', data=plot_data_least_diverse, color='black', label='National Avg Right Votes (%)', marker='o')

plt.title('Right Votes in Least Diverse Departments vs National Average')
plt.xlabel('Department')
plt.ylabel('Right Votes (%)')
plt.legend()
plt.tight_layout()
st.pyplot(plt.gcf())

st.write("We can see a correlation between left vote and diversity of the departments.")

st.header("CONCLUSION")
st.write("Through this data analysis, we showed that some clichés relatives to vote are partly true, but that there are also outliers. The question : Does your vote tell me who you are ? Can be answered by no. Indeed factors like age, wealth and diversity are not enough to predict the votes. In reality, we demonstrated that the vote is more complex and multifactorial.")