import streamlit as st
from template.MARKET import market
from template.DASHBOARD import dashboard

st.set_page_config(
    layout = "wide", 
    initial_sidebar_state = "collapsed"
)

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
""", unsafe_allow_html=True)

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css" integrity="sha512-1sCRPdkRXhBV2PBLUdRb4tMg1w2YPf37qatUFeS7zlBy7jJI8Lf4VHwWfZZfpXtYSLy85pkm9GaYVYMfw5BC1A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
""", unsafe_allow_html=True)

#### with open('template/style.css') as f:
####     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


query_params = st.experimental_get_query_params()

coin_param = query_params.get("coin")

page_title = "Crypto Analysis Dashboard"


if coin_param == None :
    st.header = "Homepage"
    market()
else:
    coin = coin_param[0]

    # breadcrumb
    st.markdown(f"""
    <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/" target="_self">Crypto Analysis Dashboard</a></li>
            <li class="breadcrumb-item active" aria-current="page">{coin}</li>
        </ol>
    </nav>
    """
    , unsafe_allow_html=True)

    dashboard(coin)
    st.experimental_set_query_params(
        coin=coin,
        action='dashboard'
    )