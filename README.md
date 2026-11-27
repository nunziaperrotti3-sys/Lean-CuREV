# Lean-CuREV: Un approccio pratico e sostenibile alla pulizia dei dataset di Code Review

Progetto realizzato per il corso di Intelligenza Artificiale, ispirato allo studio *"Towards Better Code Reviews: Using LLM-as-a-Judge for Dataset Curation"* (`CuREV` / `CuREV+`).

---

## 🎯 Obiettivo e Razionale del Progetto
La metodologia proposta dagli autori originali offre un eccellente rigore scientifico, ma presenta un elevato costo computazionale: utilizza un modello di grandi dimensioni (**Llama-3.1-70B**) per generare commenti di riferimento, giustificazioni testuali e riscritture su larga scala.

L'obiettivo di **Lean-CuREV** è individuare un **compromesso pratico (trade-off efficienza/qualità)**: coprire tutti e tre i criteri qualitativi dello studio (**Educatezza, Concisione e Chiarezza**) riducendo drasticamente tempi e risorse hardware, così da rendere la pipeline eseguibile su una singola GPU gratuita (Google Colab T4).

---

## ⚙️ Architettura della Pipeline Snella (3 Fasi)
Al posto di un singolo modello gigante invocato su tutti i dati, la nostra soluzione adotta un **filtraggio a imbuto** (*right-sizing*):

1. **Fase 1 – Filtro deterministico anti-rumore (Zero AI):**
   Eliminazione istantanea tramite regole Python dei convenevoli privi di valore informativo (es. *"LGTM"*, *"thanks"*, *"done"*, *"+1"*), preservando i suggerimenti tecnici brevi ma utili.
2. **Fase 2 – Smistamento mirato sui 3 pilastri qualitativi:**
   * **Educatezza (*Civility*):** Classificazione leggera tramite `unitary/toxic-bert` (preferito a un modello di *sentiment* generico che fraintende il lessico tecnico come *error*, *bug*, *fail*).
   * **Concisione (*Conciseness*):** Rimozione tramite regex dei blocchi di codice (`` `...` ``) per contare **solo le parole di testo naturale** ed evitare falsi positivi, intercettando i commenti realmente prolissi (`> 25 parole`).
   * **Chiarezza (*Clarity*):** Intercettazione delle domande brevi e vaghe prive di contesto (`< 8 parole` terminanti con `?`).
3. **Fase 3 – Riscrittura contestuale con Small LLM (`Qwen/Qwen2.5-3B-Instruct`):**
   Solo i commenti selezionati nella Fase 2 vengono riscritti da un modello agile da **3 miliardi di parametri** (23 volte più piccolo rispetto a Llama-70B). Passando al modello un estratto del `code_diff`, l'AI riesce a disambiguare anche i commenti vaghi in massimo 2 frasi, senza bisogno di esempi few-shot o giustificazioni prolisse.

---

## 📊 Risultati Sperimentali (Campione di 500 commenti da `CuREV+`)
Test eseguito su un campione estratto dal dataset originale `OussamaBS/CuREV-plus` su singola GPU **NVIDIA T4**:

| Metrica / Fase | Risultato Ottenuto | Dettaglio / Impatto Pratico |
| :--- | :--- | :--- |
| **Campione analizzato** | 500 commenti reali | Base di confronto diretta con `CuREV+` |
| **Tempo Fase 1 + Fase 2** | **12.45 secondi** | Analisi e classificazione quasi istantanee |
| **Commenti già buoni (originali)** | **356 (71.2%)** | Nessun costo generativo per oltre il 70% dei dati |
| **Commenti selezionati per riscrittura** | **144 (28.8%)** | **86** per Prolissità · **58** per Chiarezza · **0** per Tossicità |
| **Velocità riscrittura (`Qwen-3B`)** | **1.98 sec / commento** | Riscrittura contestuale (con `code_diff`) su hardware consumer |

*(Nota: sul campione estratto da `CuREV-plus` il filtro di tossicità rileva 0 casi gravi, confermando la pulizia di base del dataset d'origine, mentre la pipeline interviene attivamente su concisione e chiarezza).*

---

## 📁 Struttura della Repository
* `pipeline_lean_curev.ipynb` — Notebook Python completo con l'implementazione delle 3 fasi e i test su GPU.
* `risultati_confronto_lean_curev_v2.xlsx` — Tabella con i confronti diretti tra commenti originali, motivazione del filtro (`esito_filtro`), dataset `CuREV+` e riscritture contestuali generate dal nostro approccio.

