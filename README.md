# Lean-CuREV: Un approccio pratico e sostenibile alla pulizia dei dataset di Code Review

📓 **[Visualizza il Notebook Python completo (Codice e Output)](https://github.com)**

Progetto realizzato per il corso di Intelligenza Artificiale, ispirato allo studio *"Towards Better Code Reviews: Using LLM-as-a-Judge for Dataset Curation"* (`CuREV` / `CuREV+`).

---

## 🎯 Obiettivo e Razionale del Progetto
Lo studio originale offre un contributo metodologico di grande valore e rigore scientifico, esplorando le massime prestazioni raggiungibili attraverso modelli di grandi dimensioni (**Llama-3.1-70B**).

Partendo da questa solida base, **Lean-CuREV** nasce con l'obiettivo di esplorare un adattamento complementare orientato all'accessibilità e alla sostenibilità: verificare se sia possibile ottenere un buon compromesso tra efficienza e qualità su hardware consumer (come una singola GPU gratuita su Google Colab T4), mantenendo l'attenzione sui tre criteri qualitativi dello studio (**Educatezza, Concisione e Chiarezza**).

L'intero flusso preserva comunque un'**automazione completa (*end-to-end*, senza alcun intervento manuale)**, adottando un'architettura a cascata in cui regole deterministiche, classificatori leggeri e modelli generativi collaborano in sequenza per rendere il processo agile e facilmente replicabile.

---

## ⚙️ Architettura della Pipeline (3 Fasi)
Per ottimizzare i tempi di calcolo e l'impiego di risorse, la pipeline adotta un **filtraggio progressivo a imbuto** (*right-sizing*), riservando il modello generativo solo ai casi che richiedono una riformulazione:

1. **Fase 1 – Filtro deterministico iniziale (Zero AI):**
   Rimozione tramite regole Python dei convenevoli privi di contenuto tecnico (es. *"LGTM"*, *"thanks"*, *"done"*, *"+1"*), preservando i suggerimenti tecnici brevi ma informativi.
2. **Fase 2 – Smistamento mirato sui 3 pilastri qualitativi:**
   * **Educatezza (*Civility*):** Classificazione leggera tramite `unitary/toxic-bert`, scelto per distinguere efficacemente il tono maleducato dal lessico tecnico della programmazione (come *error*, *bug*, *fail*).
   * **Concisione (*Conciseness*):** Rimozione tramite regex dei blocchi di codice (`` `...` ``) per contare **solo le parole di testo naturale** ed evitare falsi positivi, individuando i commenti più estesi (`> 25 parole`).
   * **Chiarezza (*Clarity*):** Individuazione delle domande brevi prive di contesto (`< 8 parole` terminanti con `?`) che possono beneficiare di una riformulazione più esplicita.
3. **Fase 3 – Riscrittura contestuale con Small LLM (`Qwen/Qwen2.5-3B-Instruct`):**
   I commenti selezionati nella Fase 2 vengono riformulati tramite un modello leggero da **3 miliardi di parametri**. Fornendo al modello un estratto del `code_diff` e un prompt essenziale, è possibile chiarire anche i commenti più sintetici in massimo 2 frasi, contenendo i tempi di elaborazione.

---

## 📊 Risultati Sperimentali (Campione di 500 commenti da `CuREV+`)
Test eseguito su un campione estratto dal dataset `OussamaBS/CuREV-plus` su singola GPU **NVIDIA T4**:

| Metrica / Fase | Risultato Ottenuto | Dettaglio / Impatto Pratico |
| :--- | :--- | :--- |
| **Campione analizzato** | 500 commenti reali | Base di confronto diretta con `CuREV+` |
| **Tempo Fase 1 + Fase 2** | **12.45 secondi** | Analisi e smistamento su GPU T4 |
| **Commenti mantenuti originali** | **356 (71.2%)** | Nessuna riformulazione necessaria per oltre il 70% dei dati |
| **Commenti selezionati per riscrittura** | **144 (28.8%)** | **86** per Concisione · **58** per Chiarezza · **0** per Tossicità |
| **Velocità riscrittura (`Qwen-3B`)** | **1.98 sec / commento** | Riscrittura contestuale (con `code_diff`) su hardware consumer |

*(Nota: sul campione estratto da `CuREV-plus` il filtro di tossicità rileva 0 casi gravi, confermando l'efficacia della pulizia già presente nel dataset d'origine, mentre la pipeline interviene principalmente su concisione e chiarezza).*

---

## 📁 Struttura della Repository
* `Untitled4.ipynb` — Notebook Python completo con l'implementazione delle 3 fasi e i test su GPU.
* `risultati_confronto_lean_curev_v2.xlsx` — Tabella con i confronti diretti tra commenti originali, motivazione del filtro (`esito_filtro`), dataset `CuREV+` e riscritture contestuali generate dal modello.

