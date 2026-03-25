# Import python packages.
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd



# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want un your custom Smoothie!
  """
)

# option = st.selectbox(
#     "What is your favorite fruits?",
#     ("Banana", "Strawberries", "Peaches"),
# )
# st.write("your favorite fruit is: ", option)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(f"{fruit_chosen} Nutrition Information ")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        af_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                    values ('""" + ingredients_string + """')"""
    # st.write(my_insert_stmt)

    time_to_insert = st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# ------------------------------------------------------------- desde aqui se realizan  nuevos cambios ------------------------------------------------------------------

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
    #st.write(smoothiefroot_response.json())
    #time_to_insert = st.button('Submit Order')
    #if time_to_insert:
        #session.sql(my_insert_stmt).collect()
        # New section to display smoothiesfroot nutrition information
        #import requests  
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
        #st.text(smoothiefroot_response.json())
        #st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
sf_df = st.dataframe(data=smoothiefroot_response.json() ,use_container_width=True)
