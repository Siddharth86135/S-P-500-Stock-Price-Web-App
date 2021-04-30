import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf


st.title('S&P 500 Analysis WebApp')

st.markdown("""
This webapp retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock price details**.
* **Python libraries used:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")



st.sidebar.header('Select Sector')

# Web scraping of S&P 500 data
#
@st.cache
def load_data():
	url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
	html = pd.read_html(url, header = 0)
	df = html[0]
	return df

df = load_data()
sector = df.groupby('GICS Sector')




# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, default = sorted_sector_unique[-4])

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('List of Companies in the selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)


# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
	href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
	return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance
top10 = ['AAPL','MSFT','AMZN','FB','GOOGL','GOOG','TSLA','BRK-B','JPM','JNJ']

title_list = ["Apple Inc. (AAPL)", "Microsoft Corp. (MSFT)", "Amazon.com Inc. (AMZN)","Facebook Inc. (FB)","Alphabet Inc. Class A Shares (GOOGL)","Alphabet Inc. Class C Shares (GOOG)","Tesla Inc.(TSLA)",
"Berkshire Hathaway Inc. (BRK.B)","JPMorgan Chase & Co. (JPM)","Johnson & Johnson (JNJ)"]

description = ["Apple is a major producer of hardware and software products, primarily for the consumer market. Its most prominent product is the Apple iPhone brand, but Apple also produces other brands including Mac computers and iPad tablets. It also operates the Apple Music and Apple TV media distribution platforms.", "Microsoft is a computer hardware and software company that makes products for both personal and enterprise use. A major player in the tech industry for decades, Microsoft is best known for its Windows operating system, the Microsoft Office suite of programs, and the Xbox game system. The company also is a major player in cloud computing services with its cloud platform, Azure.", "Amazon is an online retailer of all kinds of goods, but has increasingly diversified its business. It also has a major cloud-computing business known as Amazon Web Services (AWS), and runs the Whole Foods chain of brick-and-mortar grocery stores. On Feb. 2, 2021 Amazon announced that founder and CEO Jeff Bezos will transition to Executive Chair in Q3 2021, with current AWS CEO Andy Jassy becoming Amazon CEO at that time","Facebook runs the dominant social networking platform, by far the largest in the world. It also owns photo-sharing app Instagram, messenger app WhatsApp, and virtual reality equipment maker Oculus. Facebook rose in the rankings as people spent more time on social media to keep in touch during quarantine.","Alphabet is the parent company of search-engine giant Google. Among its other products besides the Google search engine, Alphabet runs video sharing site YouTube. It's notable that the company splits its stock into two main share classes. Google's C shares are nonvoting shares, meaning they do not entitle the holder to participate in proxy votes. The A shares usually trade for slightly more than the C shares, and carry voting rights. Each of these shares trades on the S&P 500, and each is large enough, by itself, to make the top 10 list. If the two share classes were counted together, it would place Alphabet 4th on this list and would make up 3.7% of the index. There are also B shares, which have disproportionate voting rights and are only held by Google insiders. The B shares do not trade on the open market.","Alphabet is the parent company of search-engine giant Google. Among its other products besides the Google search engine, Alphabet runs video sharing site YouTube. It's notable that the company splits its stock into two main share classes. Google's C shares are nonvoting shares, meaning they do not entitle the holder to participate in proxy votes. The A shares usually trade for slightly more than the C shares, and carry voting rights. Each of these shares trades on the S&P 500, and each is large enough, by itself, to make the top 10 list. If the two share classes were counted together, it would place Alphabet 4th on this list and would make up 3.7% of the index. There are also B shares, which have disproportionate voting rights and are only held by Google insiders. The B shares do not trade on the open market.","Tesla is primarily a maker of electric cars. It makes more than 90% of its revenue and virtually all of its profit from its car business, but it also sells solar panels and batteries for homes and businesses. Until recently Tesla has struggled to make a consistent profit, something that kept it out of the S&P 500. The S&P 500 requires a company to make four consecutive quarters of profit according to generally accepted accounting principles (GAAP).","Berkshire Hathaway is a holding company for the various investments Warren Buffett has made over the years. Among its numerous holdings are insurance businesses such as GEICO, large energy and utilities businesses, a major railroad, consumer brands such as ice cream store Dairy Queen, and manufacturers such as aerospace parts manufacturer Precision Castparts Corp. It also owns an enormous portfolio of equities, which is why Berkshire Hathaway notably fell several places in the rankings. Those equities took a huge hit when stocks dropped during the first quarter, absolutely crushing Berkshire's first-quarter profits, and dragging down the company's stock.","JPMorgan is the largest U.S. bank. JPMorgan provides banking services to a wide range of clients. It provides banking services like mortgage lending, commercial banking services like business loans, investment banking services like bond underwriting, and asset and wealth management services.","Johnson and Johnson is a medical and consumer products conglomerate. Its main three businesses are pharmaceuticals (both over the counter and prescription), medical devices, and consumer hygiene and wellness products. The last category includes notable brands such as Band-Aid bandages, Listerine mouth wash, and Neutrogena skin care products. At the end of February 2021, Johnson and Johnson received emergency use authorization from the Food and Drug Administration (FDA) for a single-dose vaccine for COVID-19."] 
data = yf.download(
		tickers = top10,
		period = "ytd",
		interval = "1d",
		group_by = 'ticker',
		auto_adjust = True,
		prepost = True,
		threads = True,
		proxy = None
	)



# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  #plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  fig, ax = plt.subplots()
  plt.plot(df.Date, df.Close, color='navy', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot(fig)



st.write('')
st.write('')
st.write('')
st.header(' **Top 10 S&P 500 Stocks by Index Weight** ')
st.write('')
st.write('')

for i in range(0,10):
		st.header(title_list[i])
		price_plot(top10[i])
		a = list(data[top10[i]].Close)
		startprice = a[0]
		prof = (a[-1] - a[0])
		percent = (prof / startprice) * 100
		st.subheader(" **YTD Growth** :point_right:"+"      " + str(percent))
		st.write(description[i])
		st.text('')














#############################################################################################################






