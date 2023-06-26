# Phonepe-pulse-project
In this project we will be seeing how to extract data from the Phonepe pulse repo using github cloning, store it in a data base and retrieve it ,do visualization for analysis of digital transactions happened till last year in phonepe. We will be using Mysql database,and plotly, for visualization and streamlit to deploy the web app.

Approach:
1. Data extraction: Clone the Github using scripting to fetch the data from the
Phonepe pulse Github repository and store it in a suitable format such as CSV
or JSON.

3. Data transformation: Use a scripting language such as Python, along with
libraries such as Pandas, to manipulate and pre-process the data. This may
include cleaning the data, handling missing values, and transforming the data
into a format suitable for analysis and visualization.

4. Database insertion: Use the "mysql-connector-python" library in Python to
connect to a MySQL database and insert the transformed data using SQL
commands.

5.Dashboard creation: Use the Streamlit and Plotly libraries in Python to create
an interactive and visually appealing dashboard. Plotly's built-in geo map
functions can be used to display the data on a map and Streamlit can be used
to create a user-friendly interface with multiple dropdown options for users to
select different facts and figures to display.

6. Data retrieval: Use the "mysql-connector-python" library to connect to the
MySQL database and fetch the data into a Pandas dataframe. Use the data in
the dataframe to update the dashboard dynamically.

Overall, the result of this project will be a comprehensive and user-friendly solution
for extracting, transforming, and visualizing data from the Phonepe pulse Github
repository.
