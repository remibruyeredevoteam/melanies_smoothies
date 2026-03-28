# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie !
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"),col("search_on"))  
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()

name = st.text_input("Name on the smoothie:", key="name_input")

ingredients_list = st.multiselect(
    "Select 5 fruits for your smoothie:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
  for ingredient in ingredients_list:
    search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
    smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
    if smoothiefroot_response.status_code == 200:
      st.subheader(f"Nutrition information for {ingredient}:")
      st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

if ingredients_list and name:
    
    insert = st.button("Place Order")
    if insert:
      ingredients_string = " ".join(ingredients_list)
      
      order_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order,order_filled) VALUES ('{ingredients_string}', '{name}', false)"""

      session.sql(order_stmt).collect()
      st.success(f"Your smoothie order has been placed , {name}!", icon="✅")




