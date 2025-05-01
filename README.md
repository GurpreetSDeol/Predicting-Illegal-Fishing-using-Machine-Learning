# 🚢 Predicting Illegal Fishing Using Random Forest

This project applies Random Forest classification and spatial analysis to identify potential illegal fishing activity using Automatic Identification System (AIS) data. It detects fishing behaviour and flags vessels that may be operating inside Marine Protected Areas (MPAs).

🔗 **Live App**: [Streamlit Dashboard](https://predicting-illegal-fishing-using-machine-learning.streamlit.app)

---

## 🌍 Overview

Using data from the Global Fishing Watch API, this application processes vessel movement events and predicts whether a vessel is fishing. If fishing is detected within protected marine zones, the event is flagged as potentially illegal.

The original model was retrained and optimised to reduce file size for deployment, resulting in slightly lower accuracy than the original version, but still performing reliably.

### 🧠 Model Performance

- **Training set class distribution**:  
  `{0: 240,702 (Not Fishing), 1: 202,382 (Fishing)}`
- **Test set class distribution**:  
  `{0: 60,064, 1: 50,707}`

| Class         | Precision | Recall | F1-score |
|---------------|-----------|--------|----------|
| Not Fishing   | 0.97      | 0.91   | 0.94     |
| Fishing       | 0.90      | 0.96   | 0.93     |
| **Accuracy**  |           |        | **0.94** |

---

## 🚀 Streamlit Dashboard

The **Streamlit app** is the final interactive product. It allows users to:

- Fetch and process real-time vessel event data from the Global Fishing Watch API.
- Apply a trained Random Forest model to classify vessel behaviour.
- Filter results spatially to highlight suspected illegal fishing activity within MPAs.
- Visualise results on an interactive map with colour-coded vessel behaviour.

👉 **Try it live**: [https://predicting-illegal-fishing-using-machine-learning.streamlit.app](https://predicting-illegal-fishing-using-machine-learning.streamlit.app)

---

## ⚙️ How It Works

1. **Data Retrieval**: Vessel event data is pulled from the Global Fishing Watch API.
2. **Fishing Prediction**: A trained Random Forest model predicts whether a vessel is engaged in fishing.
3. **Spatial Filtering**: Events are filtered based on ocean and MPZ (Marine Protected Zone) boundaries using GeoPandas and spatial joins.
4. **Visualisation**: Results are plotted on an interactive map to highlight potential violations.

---

## 📁 Repository Structure

```
├── Python files/
│   ├── Filter_Fishing_data.ipynb      # Data preprocessing and cleaning
│   ├── Machine_Learning_Model.ipynb   # Random Forest model development and evaluation
│   └── Main.ipynb                     # Initial functions for API fetch, filtering, prediction and plotting
│
├── Streamlit/
│   ├── app.py                         # Streamlit frontend interface
│   ├── Main.py                        # Final Core class (API, prediction, filtering, map)
│   └── Data/                          # Geographical boundaries and trained Random Forest model
```

---

## 📦 Features

- ✅ Accesses recent vessel event data via Global Fishing Watch API  
- ✅ Predicts fishing behaviour using a Random Forest classifier  
- ✅ Identifies activity inside Marine Protected Areas (MPAs)  
- ✅ Visualises spatial patterns using interactive maps  
- ✅ Built with GeoPandas, scikit-learn, matplotlib, and PostGIS  

---

## 📚 Data Sources

- **Global Fishing Watch** – Vessel movement data and fishing activity labels  
- **Natural Earth Data** – Ocean and land boundaries  
- **Protected Planet** / **Marine Conservation Institute** – Marine Protected Zone (MPZ) boundaries  

---

## 📌 Future Improvements

- Improve Random Forest model size without compromising accuracy  
- Add support for multi-vessel tracking and filtering  
- Schedule regular data fetching via cloud functions or cron  
- Add downloadable reports or flag exports for authorities
