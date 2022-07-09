import streamlit as st
from multiapp import MultiApp
from apps import home, data, model,newone # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Stock Trend", newone.app)
app.add_app("Stock Forcasting", home.app)
app.add_app("Total assets prediction", data.app)
app.add_app("Liabilities Prediction", model.app)
# The main app
app.run()
