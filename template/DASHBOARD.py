# setup
import streamlit as st
import pandas as pd
import numpy as np
import cryptocompare as cc
from datetime import datetime
import plotly.graph_objects as go
from datetime import date
from PIL import Image
import plotly.express as px
from requests import Request, Session
from bs4 import BeautifulSoup
import requests
import json


#set variable
coinlist=np.array(['BTC','ETH','BUSD','USDC','SOL','USDT','XRP','BNB','MATIC','ADA'])
api_key="631999bf0b5310a37e876c6773310f46c097dddcb6fdeb252ca3c17e25f0bf81"
ccobj=cc.cryptocompare._set_api_key_parameter(api_key)

#url coinmarketcap:
cmc = requests.get('https://coinmarketcap.com')
soup = BeautifulSoup(cmc.content, 'html.parser')

## Function to color changes: increase = green, decrease = red
def render_diff(diff, is_pct):
  if diff > 0:
    if is_pct:
      return f'''<td class='text-success'><i class="fa-solid fa-caret-up mr-1"></i>{abs(diff)}%</td>'''
    else:
      return f'''<td class='text-success'><i class="fa-solid fa-caret-up mr-1"></i>{abs(diff)}</td>'''
  if diff < 0:
    if is_pct:
      return f'''<td class='text-danger'><i class="fa-solid fa-caret-down mr-1"></i>{diff}%</td>'''
    else:
      return f'''<td class='text-danger'><i class="fa-solid fa-caret-down mr-1"></i>{diff}</td>'''
  return f"<td>{diff}</td>"

## Function to plot line chart, candlesticks chart for price, and bar chart for volume
def myplot(df, time_period, margin_setup, C, sma_name, ema_name):
    ## C = chart type, sma_no = SMA indecator
    if C=='Candlestick chart':
        ##candelstick-price
        figprice = go.Figure(data=[go.Candlestick(name='Prices', x=time_period, open=df['open'], high=df['high'],low=df['low'], close=df['close'])])
        figprice.add_trace(go.Scatter(name=sma_name, x=time_period, y=df[sma_name],line_color='#2e6902'))
        figprice.add_trace(go.Scatter(name=ema_name, x=time_period, y=df[ema_name],line_color='#d1025c'))
        figprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500, hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ##linechart-price
        figprice=go.Figure(go.Scatter(name='Prices', x=time_period, y=df['close'],line_color='#100269'))
        figprice.add_trace(go.Scatter(name=sma_name, x=time_period, y=df[sma_name],line_color='#2e6902'))
        figprice.add_trace(go.Scatter(name=ema_name, x=time_period, y=df[ema_name],line_color='#d1025c'))
        figprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)

    ##barchar-volumn
    figvol=px.bar(df, x=time_period, y=df['volumeto'])
    figvol.update_layout(xaxis_rangeslider_visible=False,width=1000, height=300, hovermode='x unified', margin=margin_setup)
    return figprice, figvol

## Function to add SMA and EMA indecators on dataframe of coin historical prices
def sma_ema(df, sma_no, ema_no):
    ## calculate SMA: Simple Moving Average
    sma_name = 'SMA'+str(sma_no)
    df[sma_name] = df.close.rolling(sma_no).mean()
    ## calculate ema: Exponential Moving Average
    ema_name = 'EMA'+str(ema_no)
    df[ema_name] = df.close.ewm(span=ema_no, adjust=False).mean()
    return df, sma_name, ema_name

# Plot 1h
def plot_1h(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_minute(coin,'USD',limit=59, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append(datetime.fromtimestamp(df.iloc[i,0]))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)
    
    return figprice, figvol



# Plot 1day
def plot_1day(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_minute(coin,'USD',limit=1440, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol



# Plot 1week
def plot_1week(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_hour(coin,'USD',limit=167, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Plot 1month
def plot_1month(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_hour(coin,'USD',limit=720, exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Plot 6 months
def plot_6months(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_day(coin,'USD',limit=181,exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Plot 1 year
def plot_1year(coin, margin_setup, C, sma_no, ema_no):
    ## C = chart type, sma_no = SMA indecator
    df = pd.DataFrame(cc.get_historical_price_day(coin,'USD',limit=364,exchange='CCCAGG',toTs=datetime.now()))
    time_period=[]
    for i in range(df.shape[0]):
        time_period.append((datetime.fromtimestamp(df.iloc[i,0])))
    ## add SMA and EMA indecators on current dataframe
    df, sma_name, ema_name = sma_ema(df, sma_no, ema_no)

    figprice, figvol = myplot(df, time_period, margin_setup, C, sma_name, ema_name)    
    return figprice, figvol


# Function to retrieve data for market indecators
def get_signal(from_sym):
    
    url = 'https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest'
    
    parameters = {'fsym': from_sym}    
    # response comes as json
    response = requests.get(url, params=parameters)   
    
    data = response.json()['Data'] 
    
    return data


# Funrtion to plot indecator: in The Money
def in_the_money(data_indecators, margin_setup1, w, h):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = round(data_indecators['inOutVar']['score'],2),
        mode = "gauge+number",
        gauge = {'axis': {'range': [0, 1]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, data_indecators['inOutVar']['score_threshold_bearish']], 'color': "red"},
                    {'range': [data_indecators['inOutVar']['score_threshold_bearish'], 
                               data_indecators['inOutVar']['score_threshold_bullish']], 'color': '#F7E31D'},
                    {'range': [data_indecators['inOutVar']['score_threshold_bullish'], 1], 'color': "green"}]}))
    fig.update_layout(width=w, height=h, hovermode='closest', margin=margin_setup1, font=dict(size=20))
    return fig

# Funrtion to plot indecator: Net Network Growth
def network_growth(data_indecators, margin_setup1, w, h):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = round(data_indecators['addressesNetGrowth']['score'],2),
        mode = "gauge+number",
        gauge = {'axis': {'range': [0, 1]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, data_indecators['addressesNetGrowth']['score_threshold_bearish']], 'color': "red"},
                    {'range': [data_indecators['addressesNetGrowth']['score_threshold_bearish'], 
                               data_indecators['addressesNetGrowth']['score_threshold_bullish']], 'color': '#F7E31D'},
                    {'range': [data_indecators['addressesNetGrowth']['score_threshold_bullish'], 1], 'color': "green"}]}))
    fig.update_layout(width=w, height=h, hovermode='closest', margin=margin_setup1, font=dict(size=20))
    return fig

# Funrtion to plot indecator: Concentration
def concentration(data_indecators, margin_setup1, w, h):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = round(data_indecators['concentrationVar']['score'],2),
        mode = "gauge+number",
        gauge = {'axis': {'range': [0, 1]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, data_indecators['concentrationVar']['score_threshold_bearish']], 'color': "red"},
                    {'range': [data_indecators['concentrationVar']['score_threshold_bearish'], 
                               data_indecators['concentrationVar']['score_threshold_bullish']], 'color': '#F7E31D'},
                    {'range': [data_indecators['concentrationVar']['score_threshold_bullish'], 1], 'color': "green"}]}))
    fig.update_layout(width=w, height=h, hovermode='closest', margin=margin_setup1, font=dict(size=20))
    return fig

# Funrtion to plot indecator: Large Transactions
def large_transaction(data_indecators, margin_setup1, w, h):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = round(data_indecators['largetxsVar']['score'],2),
        mode = "gauge+number",
        gauge = {'axis': {'range': [0, 1]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, data_indecators['largetxsVar']['score_threshold_bearish']], 'color': "red"},
                    {'range': [data_indecators['largetxsVar']['score_threshold_bearish'], 
                               data_indecators['largetxsVar']['score_threshold_bullish']], 'color': '#F7E31D'},
                    {'range': [data_indecators['largetxsVar']['score_threshold_bullish'], 1], 'color': "green"}]}))
    fig.update_layout(width=w, height=h, hovermode='closest', margin=margin_setup1, font=dict(size=20))
    return fig



### MAIN FUNCTION
def dashboard(coin: str):
    light_mode = st.checkbox('Dark mode')
    if light_mode:
        with open('template/style2.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        with open('template/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    #### download data from coinmarketcap
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coin_data = json.loads(data.contents[0])

    listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']
    market_cap_name = 'quote.USD.marketCap'
    for i in listings[1:]:
        coin_symbol = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'symbol'][0]]
        if coin_symbol==coin:
            coin_vol24h = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.volume24h'][0]]
            coin_cap = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == market_cap_name][0]]
            coin_cap_pct = round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.dominance'][0]],3)
            break
    coin_vol24h = '$'+str(f"{round(coin_vol24h/1e6,3):,}" + 'M')
    coin_cap_pct=str(f"{coin_cap_pct}" + "%")
    coin_cap='$'+str(f"{round(coin_cap/1e9,3):,}" + 'B')

    #----infor part
    coin_data = cc.get_avg(coin, currency='USD')
    pricecoin ='$'+str(f"{coin_data['PRICE']:,}")
    change24h = round(coin_data['CHANGE24HOUR'], 3)
    change24hpct= round(coin_data['CHANGEPCT24HOUR'], 3)
    openprice='$'+str(f"{coin_data['OPEN24HOUR']:,}")
    highprice='$'+str(f"{coin_data['HIGH24HOUR']:,}")
    lowprice='$'+ str(f"{coin_data['LOW24HOUR']:,}")

    # Introduction:
    icon, sym_alg, price, vol, cap, cap_pct = st.columns([1,1,1,1,1,1])
    img_path = './icons/'+ coin + '.jpg'
    icon.image(Image.open(img_path))
    
    sym_alg.text('Symbol: ' + coin)
    
    coin_list=cc.get_coin_list()
    sym_alg.text('Algo: ' + coin_list[coin]['Algorithm'])
    

    price.metric(label='Price', value= pricecoin, delta=change24h)
    vol.metric(label='Volume 24h', value=coin_vol24h)

    cap.metric(label='Coin market cap', value=coin_cap)
    cap_pct.metric(label='Market cap proportion', value=coin_cap_pct)

    Description = st.checkbox('Description')
    if Description:
        st.write(coin_list[coin]['Description'])

    
    #Summary column a1 : information
    st.markdown(
      """
      <h1>Coin price statistics and pairs</h1>
      """
    , unsafe_allow_html=True)

    infor, pair = st.columns(2)
    
    infor.subheader(coin + ' Price Statistics')
    table1_html = """<table class="table table-striped table-hover table-borderless text-right">
      <thead>
          <tr>
            <th class="text-left pl-5" scope="col">Information</th>
            <th scope="col">Value</th>
          </tr>
      </thead>
      <tbody>
    """
    table1_html += f"""<tr>
            <td class="text-left pl-5">Price</td>
            <td>{pricecoin}</td>
        </tr>
    """
    table1_html += f"""<tr>
            <td class="text-left pl-5">Change 24h</td>
            {render_diff(change24h, False)}
        </tr>
    """
    table1_html += f"""<tr>
            <td class="text-left pl-5">Change 24h (%)</td>
            {render_diff(change24hpct, True)}
        </tr>
    """
    table1_html += f"""<tr>
            <td class="text-left pl-5">Open price</td>
            <td>{openprice}</td>
        </tr>
    """
    table1_html += f"""<tr>
            <td class="text-left pl-5">Highest price 24h</td>
            <td>{highprice}</td>
        </tr>
    """
    table1_html += f"""<tr>
            <td class="text-left pl-5">Lowest price 24h</td>
            <td>{lowprice}</td>
        </tr>
    """
        
    table1_html += """</tbody>
    </table>"""

    
    infor.markdown(table1_html, unsafe_allow_html=True)

    
    #----pair part:
    currencyunit = np.setdiff1d(coinlist, coin)
    Pairs=[]
    Prices=[]
    for i in range(6):
        Pairs.append(coin+'/'+currencyunit[i])
        Prices.append(f"{round(cc.get_price(coin,currency=currencyunit[i])[coin][currencyunit[i]],2):,}")
    pairprice=pd.DataFrame({'Pairs':Pairs,'Price':Prices})

    pair.subheader(coin + ' Price Pairs')
    table2_html = """<table class="table table-striped table-hover table-borderless text-right">
      <thead>
          <tr>
            <th class="text-left pl-5" scope="col">Pairs</th>
            <th scope="col">Price</th>
          </tr>
      </thead>
      <tbody>
    """
    for idx, pairi in enumerate(Pairs):
        table2_html += f"""<tr>
              <td class="text-left pl-5">{pairi}</td>
              <td>{Prices[idx]}</td>
            </tr>
        """
    table2_html += """</tbody>
    </table>"""  
    pair.markdown(table2_html, unsafe_allow_html=True)


    # Chart
    title="Historical Data of " + coin
    st.title(title)


    Time, Chart, sma_indecators, ema_indecators = st.columns(4)
    T = Time.selectbox('Select time',('1 Hour','1 Day','1 Week','1 Month','6 Months','1 Year'))
    C = Chart.selectbox('Select chart type',('Candlestick chart','Line chart'))
    sma_inde = sma_indecators.selectbox('SMA indicators',('SMA 5','SMA 10', 'SMA 20', 'SMA 30', 'SMA 60'))
    ema_inde = ema_indecators.selectbox('EMA indicators',('EMA 5','EMA 12', 'EMA 26', 'EMA 50'))
    sma_no = int(sma_inde[3:])
    ema_no = int(ema_inde[3:])

    margin_setup = dict(l=20, r=20, t=40, b=20)
    if T == '1 Hour':
        figprice, figvol = plot_1h(coin, margin_setup, C, sma_no, ema_no)
    elif T=='1 Day':
        figprice, figvol = plot_1day(coin, margin_setup, C, sma_no, ema_no)
    elif T=='1 Week':
        figprice, figvol = plot_1week(coin, margin_setup, C, sma_no, ema_no)
    elif T=='1 Month':
        figprice, figvol = plot_1month(coin, margin_setup, C, sma_no, ema_no)
    elif T=='6 Months':
        figprice, figvol = plot_6months(coin, margin_setup, C, sma_no, ema_no)
    else:
        figprice, figvol = plot_1year(coin, margin_setup, C, sma_no, ema_no)
        
    st.markdown(
        """
        <h2>Historical Price</h2>
        """
    , unsafe_allow_html=True)

    st.plotly_chart(figprice, use_container_width=True)

    st.markdown(
        """
        <h2>Volume</h2>
        """
    , unsafe_allow_html=True)
    st.plotly_chart(figvol,use_container_width=True)

    ### plot indecators: Net Network Growth, in The Money, Concentration, Large Transactions
    margin_setup1 = dict(l=2, r=2, t=2, b=2)
    data_indecators = get_signal(coin)
    if len(data_indecators)>0:
        fig_network_gr = network_growth(data_indecators, margin_setup1, 400, 200)
        fig_inthe_money = in_the_money(data_indecators, margin_setup1, 400, 200)

        fig_concentration = concentration(data_indecators, margin_setup1, 400, 200)
        fig_large_trans = large_transaction(data_indecators, margin_setup1, 400, 200)
        
        st.markdown(
            """
            <h1>Signal Information</h2>
            """
        , unsafe_allow_html=True)

        Signal_des = st.checkbox('Signal descriptions')
        if Signal_des:
            st.markdown(
            """
            <ul>
                <li>Net Network Growth reflects the change in the total number of addresses for a particular coin.</li>
                <li>Large Transactions shows the score for analysing shifts in the number of transactions of over $100,000.</li>
                <li>In The Money shows the estimated ratio for the volume of tokens that make profits for a particular crypto asset.</li>
                <li>Concentration is the measured score for daily changes of addresses that hold over 1% of supply (known as whales), or the addresses that hold between 0.1% and 1% of supply (known as investors).</li>
            </ul>
            """
            , unsafe_allow_html=True)

        network , large_trans, money , concentra = st.columns(4)
        # network , large_trans = st.columns(2)
        network.subheader('Net Network Growth')
        network.plotly_chart(fig_network_gr, use_container_width=True)

        large_trans.subheader('Large Transactions')
        large_trans.plotly_chart(fig_large_trans, use_container_width=True)

        # money , concentra = st.columns(2)
        money.subheader('In The Money')
        money.plotly_chart(fig_inthe_money, use_container_width=True)

        concentra.subheader('Concentration')
        concentra.plotly_chart(fig_concentration, use_container_width=True)
    

    