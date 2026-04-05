# ⌨ LLMRank 2026

> Every major AI model ranked for coding — intelligence, speed, latency & cost.

A Streamlit dashboard that lets you filter, compare, and explore **188 LLMs from 37 AI labs** across key metrics relevant to coding use cases.

---

## Features

- **Leaderboard** — sortable table of all models with intelligence index, price, speed, latency, and estimated response time
- **Analytics** — charts for top models, cost vs intelligence, speed vs latency, models per lab, price distribution, and context window breakdown
- **Compare** — head-to-head comparison of up to 4 models with a normalised radar chart and side-by-side bar charts
- **Insights** — key market findings including top model, fastest models, lowest latency, free models, and 1M+ context window models
- **Sidebar filters** — filter by lab, context window, max price, min speed, and output token count

---

## Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Plotly](https://plotly.com/python/) — interactive charts
- [Pandas](https://pandas.pydata.org/) — data handling
- [Matplotlib](https://matplotlib.org/) — required by pandas Styler for heatmaps

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/CodeWithPriyankaMukherjee/LLMrank.git
cd llmrank
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

---

## Data

The app reads from `aimodels.csv` in the project root. The CSV should contain the following columns:

| Column | Description |
|--------|-------------|
| `Model` | Model name |
| `Creator` | Lab / company |
| `Context Window` | Token context size (e.g. `128k`, `1m`) |
| `Intelligence Index` | Numeric intelligence score |
| `Price (Blended USD/1M Tokens)` | Blended input+output price |
| `Speed(median token/s)` | Median output speed in tokens/second |
| `Latency (First Answer Chunk /s)` | Time to first token in seconds |

---

## Deployment

Deployed on [Streamlit Cloud](https://streamlit.io/cloud). To deploy your own:

1. Push the repo to GitHub (make sure `app.py`, `aimodels.csv`, and `requirements.txt` are all in the root)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set the main file to `app.py`
4. Deploy

**`requirements.txt`**
```
streamlit
pandas
numpy
plotly
matplotlib
```

---

## License

MIT
