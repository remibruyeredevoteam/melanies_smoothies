# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie !
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))  
# st.dataframe(data=my_dataframe, use_container_width=True)

name = st.text_input("Name on the smoothie:", key="name_input")

ingredients_list = st.multiselect(
    "Select 5 fruits for your smoothie:",
    my_dataframe,
    max_selections=5
)


if ingredients_list and len(ingredients_list) == 5 and name:
    
    insert = st.button("Place Order")
    if insert:
      ingredients_string = " ".join(ingredients_list)
      
      order_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order,order_filled) VALUES ('{ingredients_string}', '{name}', false)"""

      session.sql(order_stmt).collect()
      st.success(f"Your smoothie order has been placed , {name}!", icon="✅")

