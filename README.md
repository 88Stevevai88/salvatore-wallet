
# 🧠 CronoWatch Pro

**CronoWatch Pro** è una web app interattiva per il monitoraggio automatico delle transazioni su Cronos, con particolare attenzione alle vendite di token in WCRO.  
Ti consente di tracciare e analizzare ogni conversione con eleganza, chiarezza e funzionalità evolute.

🔗 **Live App**: [Apri CronoWatch Pro](https://cronowatch-pro-aph2yejxnlz7xzzwhleqos.streamlit.app/)

---

## ✨ Funzionalità

- 🔄 Rilevamento automatico degli swap su Cronos
- 💰 Calcolo WCRO ricevuti e conversione in EUR
- 📆 Dashboard completa con grafici giornalieri e mensili
- 🎯 Tracker dei token venduti (LION, BARA, AGENTFUN…)
- 🧠 Grafico a torta + linea cumulativa + barre mensili
- 📤 Esportazione CSV
- 🖤 Tema dark personalizzato
- 📊 Icone token in tabella e grafici
- ⚡ Spinner animato durante il caricamento

---

## 📦 Requisiti

- Python 3.9 o superiore
- Librerie:
  ```bash
  streamlit
  pandas
  requests
  plotly
  ```

---

## 🚀 Come usarla localmente

```bash
git clone https://github.com/tuo-username/cronowatch-pro.git
cd cronowatch-pro
streamlit run app.py
```

---

## 🔐 Configurazione API Key

Crea un file `.streamlit/secrets.toml` oppure configura le secrets su [Streamlit Cloud](https://streamlit.io/cloud):

```toml
API_KEY = "LA_TUA_API_KEY_CRONOSCAN"
CMC_API_KEY = "LA_TUA_API_KEY_COINMARKETCAP"
```

---

## 👨‍💻 Autore

Realizzato con amore da **[Piero Pasquariello](https://github.com/tuo-username)**  
🧠 Powered by Python, Streamlit & Plotly

---

## 📌 Licenza

MIT License. Usala, clonala, personalizzala! 🚀
