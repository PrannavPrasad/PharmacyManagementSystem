import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
from streamlit_option_menu import option_menu
import datetime as dt
page="""" 
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://wallpaperaccess.com/full/8405347.jpg");
 background-size: cover;
 }


</style>    
"""
#st.markdown(page,unsafe_allow_html=True)
cnx = mysql.connector.connect(user='root', password='Password', host='localhost', database='Pharmacy')
cursor = cnx.cursor()
option = st.sidebar.selectbox("menu:",["login","sign up"])
import sqlite3


def sign_up():
    
    name = st.sidebar.text_input("Name")
    username = st.sidebar.text_input("Username")
    empID = int(st.sidebar.number_input("Employee_ID"))
    password = st.sidebar.text_input("Password", type='password')
    password2 = st.sidebar.text_input("Confirm Password", type='password')
    if(st.sidebar.button("submit") ):
            # Check if passwords match
        if password != password2:
            st.error("Passwords do not match")
        else:
                # Insert new user into the MySQL database
            insert_query = "INSERT INTO Employees (Employee_ID, Employee_Name, Employee_Username, Employee_password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (empID,name,username, password))
            cnx.commit()
            st.success("Account created!")
    # Close the connection

def Home():
    selected=option_menu(menu_title=None,options=['customers','orders','medicines'],orientation="horizontal")
    if(selected == 'customers'):
        sel=option_menu(menu_title=None,options=['new customer','customer history'],orientation='horizontal')
        if(sel=='new customer'):
            cus_id=int(st.number_input("customer id"))
            cus_name=st.text_input("enter the name")
            cus_num = int(st.number_input("enter the number"))
            cus_add=st.text_area("enter the address")
            if st.button("Submit"):
                Insert_Customer = 'INSERT INTO Customers (Customer_ID,Customer_Name,Customer_Number,Customer_address) VALUES (%s, %s, %s, %s)'
                cursor.execute(Insert_Customer,(cus_id,cus_name,cus_num,cus_add))
                cnx.commit()
                st.success("Inserted successfully!")

            
        if(sel=='customer history'):
            cus_id=int(st.number_input("enter the customer id"))
            if st.button("Submit"):                
                customer_history = 'select * from Orders where Customer_ID = %s'
                cursor.execute(customer_history,(cus_id,))
                result = cursor.fetchall()
                cnx.commit()
                coloumn_name=["Order_ID","Order_date","Medicine_ID1","Medicine_ID2","Medicine_ID3","Medicine_ID4","Medicine_ID5","Medicine_ID6","Total_Price","Customer_ID","Doctor_ID"]
                df=pd.DataFrame(result,columns=coloumn_name)
                st.table(df)
                st.success("Orders retreived")

    if(selected=='orders'):
        sel1=option_menu(menu_title=None,options=['new order','order history'],orientation='horizontal')
            
        if(sel1=='new order'):
            ord_id=st.text_input('enter order id')
            ord_date=st.date_input('order date')
            tot=st.text_input('enter totla price')
            med_id1=st.text_input('entet med id1')
            med_id2=st.text_input('entet med id2')
            med_id3=st.text_input('entet med id3')
            med_id4=st.text_input('entet med id4')
            med_id5=st.text_input('entet med id5')
            med_id6=st.text_input('entet med id6')
            cus_id=st.text_input('enter custmer is')
            doc_id=st.text_input('doctor id')
            if st.button("Submit"):
                Insert_Customer = 'INSERT INTO Orders (Order_ID,Order_date,Medicine_ID1,Medicine_ID2,Medicine_ID3,Medicine_ID4,Medicine_ID5,Medicine_ID6,Total_Price,Customer_ID,Doctor_ID) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(Insert_Customer,(ord_id,ord_date,tot,med_id1,med_id2,med_id3,med_id4,med_id5,med_id6,cus_id,doc_id))
                cnx.commit()
                st.success("Inserted successfully!")
            
        if(sel1=='order history'):
            cus_id=int(st.number_input("Order id"))
            if st.button("submit"):
                Order_history = 'select * from Orders where Order_ID = %s'
                cursor.execute(Order_history,(cus_id,))
                result = cursor.fetchall()
                coloumn_name=["Order_ID","Order_date","Medicine_ID1","Medicine_ID2","Medicine_ID3","Medicine_ID4","Medicine_ID5","Medicine_ID6","Total_Price","Customer_ID","Doctor_ID"]
                df = pd.DataFrame(result,columns=coloumn_name)
                st.table(df)
                cnx.commit()
                
    if(selected=='medicines'):
        med_id=int(st.number_input('enter med id'))
        if st.button("Submit"):
            medicine = 'select * from Medicines where Medicine_ID = %s'
            cursor.execute(medicine,(med_id,))
            result = cursor.fetchall()
            column_names = ["Medicine_ID","Name","Packet_Size","Rating_Count","Rating","Price","MRP"]
            df = pd.DataFrame(result,columns=column_names)
            st.table(df)
            cnx.commit()
            st.success("Medicine received")
if(option == "login"):
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')

            # Check if user exists in the MySQL database
        select_query = "SELECT * FROM Employees WHERE Employee_Username = %s AND Employee_password = %s"
        cursor.execute(select_query, (username, password))
        results = cursor.fetchall()
        if st.sidebar.checkbox("Log in"):
            if results:
                st.sidebar.success("Logged in!")
                Home()
            else:
                st.error("Incorrect username or password")


if(option=="sign up"):
    sign_up()