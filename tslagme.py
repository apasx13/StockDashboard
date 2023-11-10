import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#####################
### Question 1: Use yfinance to Extract TSLA Stock Data
tesla = yf.Ticker("TSLA")

# Extract stock information
tesla_data = tesla.history(period="max")

#**Reset the index** 
tesla_data.reset_index(inplace=True)
tesla_data.head()

###  Question 2: Use Webscraping to Extract Tesla Revenue Data

#Download the Webpage
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
response = requests.get(url)
html_data = response.text

#Parse the HTML Data
soup = BeautifulSoup(html_data, 'html.parser')

#Extract the Tesla Revenue Table
tesla_revenue = pd.read_html(html_data, flavor='bs4')[0] #or tesla_revenue = pd.read_html(html_data)[0]
tesla_revenue.columns = ['Date', 'Revenue']

#remove the comma and dollar sign from the `Revenue` column. 
#tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")

#remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
# last 5 row
tesla_revenue.tail()

### Question 3: Use yfinance to Extract GME Stock Data

gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

###  Question 4: Use Webscraping to Extract GME Revenue Data
url = ' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, 'html.parser')

gme_revenue = pd.read_html(html_data)[0]
gme_revenue.columns = ['Date', 'Revenue']

gme_revenue.tail()

###  Question 5/6: PLOT

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)
    
    #  sorted by date
    stock_data = stock_data.sort_values(by='Date')
    revenue_data = revenue_data.sort_values(by='Date')
    
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data['Date'], y=revenue_data['Revenue'], name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()


make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GameStop')
