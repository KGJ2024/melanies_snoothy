# Import python packages
import streamlit as st
import pandas as pd

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(f"Customize your Smoothie ")
st.write(
  """Choose the fruit you want in your smoothie..
  """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name will be", name_on_order)

##option = st.selectbox(
  ##  "What is your favourite food?",
    ##("Banana", "Strawberries", "Peaches"),
##)

##st.write("Your favourite food is:", option)

# smootiefroot



#st.text(smoothiefroot_response.json())





#st.write("You selected:", options)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Panda

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
    "Choose upto 5 ingrdients"  ,  my_dataframe, max_selections=6
)

submitted = st.button('Submit')
if submitted:
    st.success('Someone clicked the button', icon = '👍')
    
    if ingredients_list:
        st.write (ingredients_list)
        st.text (ingredients_list)
    
        ingredients_String = ''
    
        for fruit_chosen in ingredients_list:
            ingredients_String += fruit_chosen + ' '

            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            
            st.subheader(fruit_chosen + 'Nutrition Information')

            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
            sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
    
        st.write (ingredients_String)
    
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_String + """', 
                '""" + name_on_order + """')"""
    
        st.write(my_insert_stmt)
    
        if ingredients_String:
            session.sql(my_insert_stmt).collect()
        
            st.success('Your Smoothie is ordered!', icon="✅")


