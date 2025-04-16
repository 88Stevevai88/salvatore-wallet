import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from token_parser import estrai_token_da_input
from token_lookup import get_token_name_from_cronoscan
st.set_page_config("CronoWatch Pro", layout="wide", page_icon="🧠")



# === CONFIG ===
WALLET = "0xbe19c5ef6289636f74ceb65ce2a618255b397977".lower()
API_KEY = "KWZWPGS5TSFCRTP9HK12RTMRUGE4R6J8AZ"
CMC_API_KEY = "d48913f8-a8ac-4ee2-b167-007b4c78e8a7"
START_DATE = datetime(2025, 3, 29)

token_names = {
    "0x9d8c68f185a04314ddc8b8216732455e8dbb7e45": "LION",
    "0xf24409d155965ca87c45ad5bc084ad8ad3be4f39": "BARA",
    "0x96733708c4157218b6e6889eb9e16b1df7873061": "AGENTFUN"
}

def get_internal_transactions():
    url = f"https://api.cronoscan.com/api?module=account&action=txlistinternal&address={WALLET}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
    return requests.get(url).json().get("result", [])

def get_transaction_input(tx_hash):
    try:
        url = f"https://api.cronoscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data and data.get("result") and isinstance(data["result"], dict):
            return data["result"].get("input", "")
    except Exception as e:
        st.warning(f"Errore durante il recupero dell'input per {tx_hash}: {e}")
    return ""

def detect_token_from_input(input_data):
    for address, name in token_names.items():
        cleaned = address.lower().replace("0x", "").rjust(64, "0")
        if cleaned in input_data.lower():
            return name
    return "Non rilevato"

def get_wcro_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {"symbol": "CRO", "convert": "EUR"}
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    try:
        response = requests.get(url, params=params, headers=headers)
        return float(response.json()["data"]["CRO"]["quote"]["EUR"]["price"])
    except:
        return 0.0

def format_line_chart(df):
    fig = px.line(df, x="Giorno", y="Valore WCRO", title="Andamento WCRO ricevuti",
                  markers=True, template="plotly_dark", line_shape="spline")
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig

def format_bar_chart(df):
    fig = px.bar(df, x="Mese", y="Totale WCRO", title="Totale WCRO per mese", template="plotly_dark")
    return fig

def format_pie_chart(df):
    fig = px.pie(df, values="Valore WCRO", names="Token", title="Distribuzione WCRO per Token", template="plotly_dark")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def main():
    st.title("🚀 Benvenuto in CronoWatch di Salvatore")
    st.markdown("<h1 style='color:#00AEEF;'>👋 Benvenuto Salvatore in CronoWatch Pro</h1><p style='color:#FAFAFA;'>Monitoraggio automatico WCRO + Analisi Token</p>", unsafe_allow_html=True)

    with st.spinner("🔄 Recupero dati da Cronoscan..."):
        # Recupero dati
        data = get_internal_transactions()
    wcro_price = get_wcro_price()

    swap_data = []
    for tx in data:
        time_stamp = datetime.fromtimestamp(int(tx["timeStamp"]))
        if time_stamp < START_DATE or tx.get("isError") != "0":
            continue
        if tx.get("to", "").lower() == WALLET and float(tx.get("value", 0)) > 0:
            value = int(tx["value"]) / 1e18
            eur = value * wcro_price
            input_data = get_transaction_input(tx["hash"])
            token = detect_token_from_input(input_data)
            swap_data.append({
                "Data": time_stamp,
                "Token": token,
                "Da": tx.get("from"),
                "Valore WCRO": value,
                "Valore EUR": eur,
                "Link": f"https://cronoscan.com/tx/{tx['hash']}"
            })

    df = pd.DataFrame(swap_data)
    if df.empty:
        st.error("Nessuna transazione WCRO trovata.")
        return

    df["Data"] = pd.to_datetime(df["Data"])
    df.sort_values("Data", inplace=True)
    df["Giorno"] = df["Data"].dt.date
    df["Mese"] = df["Data"].dt.strftime("%Y-%m")
    df["Anno"] = df["Data"].dt.year

    with st.sidebar:
        st.header("Filtri Avanzati")
        token_sel = st.multiselect("Token", options=df["Token"].unique(), default=df["Token"].unique())
        anni = sorted(df["Anno"].unique(), reverse=True)
        anno_sel = st.selectbox("Anno", options=anni)

    dff = df[(df["Token"].isin(token_sel)) & (df["Anno"] == anno_sel)]

    total_wcro = dff["Valore WCRO"].sum()
    total_eur = dff["Valore EUR"].sum()
    days_elapsed = (datetime.now() - START_DATE).days or 1
    avg_daily = total_wcro / days_elapsed

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📆 Storico Mensile", "🎯 Token Tracker"])  # Tabs con icone e colori

    with tab1:
        st.subheader("Dashboard")
        col1, col2, col3 = st.columns([1, 1, 1])
        col1.metric("💰 Totale WCRO", f"{total_wcro:.4f}")
        col1.metric("📅 Giorni Attivi", f"{days_elapsed} giorni")
        col2.metric("💶 Totale EUR", f"€ {total_eur:.2f}")
        col3.metric("📈 Media Giornaliera", f"{avg_daily:.2f} WCRO")
        st.plotly_chart(format_line_chart(dff.groupby("Giorno")["Valore WCRO"].sum().cumsum().reset_index()), use_container_width=True)
        st.markdown("### 🔍 Ultime Transazioni")
        token_icons = {
            "LION": "🦁",
            "BARA": "🍀",
            "AGENTFUN": "🧬",
            "Non rilevato": "❓"
        }
        dff["Token"] = dff["Token"].apply(lambda x: f"{token_icons.get(x, '')} {x}")
        st.dataframe(dff[["Data", "Token", "Da", "Valore WCRO", "Valore EUR", "Link"]].tail(10), use_container_width=True)


    with tab2:
        st.subheader("Storico Mensile")
        monthly = dff.groupby("Mese")["Valore WCRO"].sum().reset_index().rename(columns={"Valore WCRO": "Totale WCRO"})
        st.plotly_chart(format_bar_chart(monthly), use_container_width=True)
        st.dataframe(monthly, use_container_width=True)

    with tab3:
        st.subheader("Token Tracker")
        token_sum = dff.groupby("Token")["Valore WCRO"].sum().reset_index().sort_values("Valore WCRO", ascending=False)
        token_sum["Token"] = token_sum["Token"].apply(lambda x: f"{token_icons.get(x, '')} {x}")
        st.plotly_chart(format_pie_chart(token_sum), use_container_width=True)
        st.bar_chart(token_sum.set_index("Token"))


    st.download_button("⬇️ Scarica CSV", data=dff.to_csv(index=False), file_name="wcro_report.csv", mime="text/csv")
    st.button("🧾 Esporta Report PDF (in arrivo)", disabled=True)

if __name__ == "__main__":
    main()