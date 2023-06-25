import pandas as pd
import requests
import json
import os
import mysql.connector
import streamlit as st
import plotly.express as px
from PIL import Image

#setting up sql connection to retrieve data
mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="BH7@ravi$",db="phonepedata")
mycursor = mydb.cursor()

icon = Image.open("spotlight.jpg")
st.set_page_config(page_title = "PhonePe Pulse Data-Visualization |by Bhuvaneswari Ravindran",
                   page_icon=icon)

st.title(":violet[PhonePE Pulse Data-Visualisation by-bhuvana]")
st.image(icon)
st.subheader(":chart: Explore India's Larrgest Digital Transaction APP Phonepe's Statistics and Visualisation :money_with_wings:")

if st.button("About"):
    txt=('''PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.
                       The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.
                       When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?
                       This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.
                       ''')
    st.write(txt)



with st.sidebar:
    option = st.selectbox('**What do you like to explore?**',
                          ("Statistics and Charts","Map"))
if option=="Statistics and Charts":    
    stats = st.sidebar.selectbox("**Stats of**",("Transactions","user"))
    if stats=="Transactions":
        tab1,tab2,tab3 = st.tabs(["State","District","Pincode"])
        with tab1:
                st.markdown(":blue[State]")
                yr=st.slider("Year",2018,2022)
                qtr=st.slider("Quater",min_value=1,max_value=4)
                mycursor.execute(f"select State,sum(Transaction_count)as Total_transaction, sum(Transaction_amount)as Total_amount from agg_trans where year={yr} and quater={qtr} group by State order by Total_amount desc limit 10")
                df=pd.DataFrame(mycursor.fetchall(),columns=["State","Transaction_count","Transaction_amount"])
                fig=px.bar(df,y='Transaction_amount',
                                x="State",
                                title="Top10 Total_amount of Transaction done, State-wise",
                                hover_data=["Transaction_count"],color="State")
                st.plotly_chart(fig,use_container_width=True)

        with tab2:
            st.markdown(":blue[District]")
            mycursor.execute(f'select District,sum(Transaction_count) as Total_transaction,sum(Transaction_amount)as Total_amount from map_trans where year={yr} and quater={qtr} group by District order by Total_amount desc limit 10')
            df=pd.DataFrame(mycursor.fetchall(),columns=["District","Transaction_count","Transaction_amount"])
            fig=px.bar(df,y='Transaction_amount',
                            x="District",
                            title="Top10 Total_amount of Transaction done, District-wise",
                            color_discrete_sequence=(["#d966ff"]),
                            hover_data=["Transaction_count"],color="District")
            st.plotly_chart(fig,use_container_width=True)

        with tab3:
            st.markdown(":blue[Pincode]")
            mycursor.execute(f'select Pincode, sum(Transaction_count)as Total_Transaction,sum(Transaction_amount) as Total_amount from top_trans where year={yr} and quater={qtr} group by Pincode order by Total_amount desc limit 10')
            df=pd.DataFrame(mycursor.fetchall(),columns=["Pincode","Transaction_count","Transaction_amount"])
            fig=px.scatter(df,y="Transaction_amount",
                    x="Pincode",
                    title="Top10 Total_amount of Transaction done, Pincode-wise",
                    color_discrete_sequence="#ffcc66",
                    hover_data=["Transaction_count"],color="Pincode")
            st.plotly_chart(fig,use_container_width=True)

    if stats=="user":
        tab1,tab2,tab3=st.tabs(["State","Brand","District"])
        with tab1:
            st.markdown("**:blue[State]**")
            yr=st.slider("Year",2018,2022)
            qtr=st.slider("Quater",min_value=1,max_value=4)
            mycursor.execute(f'select State,sum(Registered_user)as Users ,sum(App_opening)as Apps from map_user where year={yr} and quater={qtr} group by State order by Users desc limit 15')
            df=pd.DataFrame(mycursor.fetchall(),columns=["State","Registered_user","App_opening"])
            fig=px.pie(df,values="Registered_user",
                        names="State",
                        title="Top 15 Registered_users,State-wise",
                        hover_data=["Registered_user"],color="State",
                        )
            st.plotly_chart(fig,use_container_width=True)
            
        with tab2:
            st.markdown("**:blue[Brands]**")
            mycursor.execute(f'select Brand as Brands ,sum(Brand_count)as Total_users from agg_user where year={yr} and quater={qtr} group by Brand order by Total_users desc limit 10')
            df=pd.DataFrame(mycursor.fetchall(),columns=["Brand","Brand_count"])
            fig=px.pie(df,values="Brand_count",
                        names="Brand",
                        title="Top Brands of Mobile Phone used by users",
                        hover_data=["Brand_count"],color="Brand")
                        
            st.plotly_chart(fig,use_container_width=True)           
        
        with tab3:
            st.markdown("**:blue[District]**")
            mycursor.execute(f'select District ,sum(RegisteredUser)as Total_users from top_user where year={yr} and quater={qtr} group by District order by Total_users desc limit 10')
            df=pd.DataFrame(mycursor.fetchall(),columns=["District","RegisteredUser"])
            fig=px.pie(df,values="RegisteredUser",
                        names="District",
                        title="Top Registered users District-wise ",
                        hover_data=["RegisteredUser"],color="District")
                        
            st.plotly_chart(fig,use_container_width=True)

if option=="Map":
    yr=st.radio("Year",[2018,2019,2020,2021,2022])
    qtr=st.slider("Quater",min_value=1,max_value=4)
    type=st.selectbox("**Type**",("Transactions","User"))
    col1,col2=st.columns(2)

  #Visulaizing Transactions 
    if type=="Transactions":
        #state Transactions in India Map
        with col1:
            st.markdown("**:violet[States of India in Transaction]**")
            mycursor.execute(f'select State,sum(Transaction_count)asTotal_transaction,sum(Transaction_amount)asTotal_amount from map_trans where year={yr} and quater={qtr} group by State order by State ')
            df=pd.DataFrame(mycursor.fetchall(),columns=["State","Transaction_count","Transaction_amount"])
            df1=pd.read_csv("Stateslatlong.csv")
            df1=df1.rename(columns={"state":"State"})
            df2=pd.merge(df,df1,on=["State"],how="left")
            df1.State=df2


            fig= px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                               featureidkey='properties.ST_NM',
                               locations='State',
                               color='Total_transaction',
                               color_continuous_scale='Inferno',
                               title="Total Transactions in India",
                               height=2000)
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

            st.markdown("## :violet[Select any State to explore more]")
            state_name= st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
            mycursor.execute(f"select State, District,Year,Quater, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_trans where year = {yr} and quater = {qtr} and State = '{state_name}' group by State, District,Year,Quater order by State,District")
        
            df = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
            fig = px.bar(df,
                     title=state_name,
                     x="District",
                     y="Total_Transactions",
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

           
    

           
    

        

        
          

          
