SideBarLinks()

try:
  st.dataframe(hotel_clicks)
except:
  st.write("Could not connect to database to get hotel clicks.")

num_hotel_clicks = requests.get('http://api:4000/hc/top_hotel_clicks').json()


