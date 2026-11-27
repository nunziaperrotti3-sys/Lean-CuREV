# Lean-CuREV: Un approccio pratico e sostenibile alla pulizia dei dataset di Code Review

Progetto realizzato per il corso di Intelligenza Artificiale, ispirato allo studio *"Towards Better Code Reviews: Using LLM-as-a-Judge for Dataset Curation"* (`CuREV` / `CuREV+`).

---

## 🎯 Obiettivo e Razionale del Progetto
La metodologia proposta dagli autori originali offre un eccellente rigore scientifico, ma presenta un elevato costo computazionale: utilizza un modello di grandi dimensioni (**Llama-3.1-70B**) per generare commenti di riferimento, giustificazioni testuali e riscritture su larga scala.

L'obiettivo di **Lean-CuREV** è individuare un **compromesso pratico (trade-off efficienza/qualità)**: ridurre drasticamente tempi e risorse hardware (rendendo la pipeline eseguibile anche su una singola GPU gratuita come Google Colab T4), mantenendo al contempo un'elevata qualità e naturalezza dei commenti per l'addestramento dei modelli.

---

## ⚙️ Architettura della Pipeline Snella (3 Fasi)
Al posto di un singolo modello gigante usato su tutti i dati, la nostra soluzione adotta un **filtraggio a imbuto** (*right-sizing*):

1. **Fase 1 – Filtro deterministico anti-rumore (Zero AI):**
   Eliminazione istantanea tramite regole Python dei convenevoli privi di valore informativo (es. *"LGTM"*, *"thanks"*, *"done"*, *"+1"*), preservando però i commenti tecnici brevi ma utili (es. correzioni di refusi o suggerimenti puntuali).
2. **Fase 2 – Classificazione leggera della tossicità (`unitary/toxic-bert`):**
   Al posto di un modello generico di *sentiment analysis* (che tende a fraintendere il lessico tecnico come *error*, *bug*, *fail*), utilizziamo un classificatore leggero dedicato alla tossicità/maleducazione, abbinato a una soglia di lunghezza (`> 25 parole`), per individuare **solo** i commenti realmente da migliorare.
3. **Fase 3 – Riscrittura essenziale con Small LLM (`Qwen/Qwen2.5-3B-Instruct`):**
   Solo i commenti selezionati nella Fase 2 vengono riscritti da un modello agile da **3 miliardi di parametri** (23 volte più piccolo rispetto a Llama-70B), utilizzando un prompt diretto senza pesanti esempi few-shot o giustificazioni testuali prolisse.

---

## 📊 Risultati Sperimentali (Campione di 500 commenti da `CuREV+`)
Test eseguito su un campione estratto dal dataset originale `OussamaBS/CuREV-plus` utilizzando una singola GPU **NVIDIA T4**:

| Metrica / Fase | Risultato Ottenuto | Impatto Pratico |
| :--- | :--- | :--- |
| **Campione analizzato** | 500 commenti reali | Base di confronto diretta con `CuREV+` |
| **Tempo Fase 1 + Fase 2** | **18.83 secondi** | Analisi quasi istantanea dell'intero campione |
| **Commenti salvati originali** | **398 (79.6%)** | Nessun costo LLM necessario per quasi l'80% dei dati |
| **Commenti selezionati per riscrittura** | **102 (20.4%)** | Riduzione drastica delle chiamate al modello generativo |
| **Velocità riscrittura (`Qwen-3B`)** | **2.20 sec / commento** | Eseguibile su hardware consumer / cloud gratuito |

### Esempio di Confronto Qualitativo
* **🔴 Originale:** *"per current error handling best practices, its fine to continue for other resources in this action, but we want to stop policy exec by raising at the end of processing..."*
* **🟢 Lean-CuREV (`Qwen-3B`):** *"It is acceptable to continue processing other resources upon encountering an error. However, following best practices, it is recommended to raise an exception at the end of the processing to halt further execution."*

---

## 📁 Struttura della Repository
* `pipeline_lean_curev.ipynb` — Notebook Python completo con l'implementazione delle 3 fasi e i test su GPU.
* `risultati_confronto_lean_curev.xlsx` — Tabella con i confronti diretti tra commenti originali, dataset `CuREV+` e riscritture generate dal nostro approccio snello.
