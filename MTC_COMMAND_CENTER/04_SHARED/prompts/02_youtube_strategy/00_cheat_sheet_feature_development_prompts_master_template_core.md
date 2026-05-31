# 00 Cheat Sheet Feature Development Prompts Master Template Core

AmaÃ§:
MASTER_TEMPLATE_COREâ€™a **yeni Ã¶zellikler (filter, ana sinyal, SL/TP/risk modu)** eklerken
Ã§ok-LLMâ€™li, kontrollÃ¼ bir workflow kullanmak.

Genel prensip:
- Yeni modÃ¼l â†’ her zaman `use_*` input ile aÃ§Ä±lÄ±p kapanÄ±r.
- `use_* = false` iken strateji eski versiyonla **aynÄ± davranÄ±ÅŸÄ±** korur.
- Mimari korunur: Signal Plugin / Engine / Filters / Visualization ayrÄ±mÄ± bozulmaz.

---

## STEP 1 â€“ YouTube â†’ Teknik Rapor (Gemini)

### Prompt 1A â€“ FILTER Report
**Dosya Ã¶nerisi:**  
`30_PROMPTS/Gemini_YouTube_Filter_Report_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- YouTube strateji videosunu analiz eder.  
- Stratejinin tamamÄ±nÄ± raporlar ama Ã¶zellikle **filter** mantÄ±ÄŸÄ±nÄ± ayrÄ±ntÄ±lÄ± Ã§Ä±karÄ±r.  
- MASTER_TEMPLATE_CORE iÃ§in:
  - Hangi yeni filter modÃ¼lÃ¼ eklenebilir?
  - LONG / SHORT iÃ§in koÅŸullar ne?
  - Mevcut filtrelerle Ã§akÄ±ÅŸma / benzerlik var mÄ±?
- Ek olarak:
  - Bu filter iÃ§in TradingView koduna ihtiyaÃ§ var mÄ±?
  - â€œCODE_SOURCE_NEEDED: YES / NOâ€ ÅŸeklinde raporlar.

---

### Prompt 1B â€“ MAIN SIGNAL MODULE Report
**Dosya Ã¶nerisi:**  
`30_PROMPTS/Gemini_YouTube_MainSignal_Report_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- YouTube stratejisinin **ana giriÅŸ/sinyal** mantÄ±ÄŸÄ±nÄ± Ã§Ä±karÄ±r.  
- Supertrend Ã¶rnek bloÄŸunu ileride deÄŸiÅŸtirebileceÄŸimiz bir **Signal Plugin taslaÄŸÄ±** Ã¼retir.  
- `longSignal_raw` / `shortSignal_raw` ve edge mantÄ±ÄŸÄ±na nasÄ±l map edileceÄŸini anlatÄ±r.  
- TradingView kodu gerekiyorsa bunu da â€œCODE_SOURCE_NEEDEDâ€ ile belirtir.

---

### Prompt 1C â€“ SL/TP & RISK Module Report
**Dosya Ã¶nerisi:**  
`30_PROMPTS/Gemini_YouTube_SLTPrisk_Report_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- Stratejinin Ã§Ä±kÄ±ÅŸ (SL, TP, Multi-TP, Trailing, BE) ve risk yÃ¶netimini detaylÄ± Ã§Ä±karÄ±r.  
- BunlarÄ± MASTER_TEMPLATE_COREâ€™daki:
  - SL modu,
  - TP modu,
  - Trailing / BE,
  - Risk engineâ€™e nasÄ±l ekleneceÄŸini tarif eder.  
- Ek olarak:
  - Bu SL/TP/risk yapÄ±sÄ± iÃ§in orijinal Pine Scriptâ€™e ihtiyaÃ§ var mÄ±, raporlar.

---

## STEP 2 â€“ Feature Module Design (6Ã— LLM)

### Prompt 2 â€“ Feature Module Design for MASTER_TEMPLATE_CORE
**Dosya Ã¶nerisi:**  
`30_PROMPTS/LLM_Feature_Module_Design_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- Input:
  - FEATURE_TYPE = FILTER / MAIN_SIGNAL / SL_TP_RISK  
  - 1A / 1B / 1Câ€™den gelen teknik rapor  
  - (Varsa) orijinal Pine kodu  
- 6 farklÄ± LLMâ€™e verilir (ChatGPT, Gemini, DeepSeek, Grok, Claude, vb.).  
- Her LLM:
  - Model adÄ±nÄ± yazar (`Model: <name>`).  
  - Ã–zelliÄŸin Ã¶zetini,  
  - MASTER_TEMPLATE_CORE entegrasyon planÄ±nÄ±,  
  - Kod deÄŸiÅŸiklik planÄ±nÄ± (CHANGE #1, #2, â€¦ formatÄ±nda),  
  - Risk & kompatibilite notlarÄ±nÄ± yazar.  
- Ã‡Ä±ktÄ±: VS Codeâ€™a verilecek taslak rapor (daha kod yazmadan).

---

## STEP 3 â€“ Consolidation (ChatGPT)

### Prompt 3 â€“ Consolidated Feature Design
**Dosya Ã¶nerisi:**  
`30_PROMPTS/LLM_Feature_Design_MERGE_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- 6 LLMâ€™in Prompt 2 Ã§Ä±ktÄ±sÄ±nÄ± alÄ±r.  
- AynÄ± fikri savunan tasarÄ±mlarÄ± birleÅŸtirir, farklÄ±lÄ±klarÄ± tespit eder.  
- En baÅŸta:
  - ALL MODELS CONSISTENT  
  - MINOR DIVERGENCES  
  - MAJOR CONFLICTS â€“ MANUAL REVIEW REQUIRED  
  ÅŸeklinde durum raporu verir.  
- SonuÃ§:
  - "Consolidated Feature Design â€“ MASTER_TEMPLATE_CORE"  
  isimli, VS Codeâ€™a hazÄ±r tek bir tasarÄ±m dokÃ¼manÄ±:
    - Yeni input listesi  
    - Yeni fonksiyonlar  
    - Kod deÄŸiÅŸiklik planÄ± (CHANGE #1, #2, â€¦)  
    - Risk & uyum Ã¶zeti  
    - Uygulama checklistâ€™i  

---

## STEP 4 â€“ VS Code: Apply Feature Changes

### Prompt 4 â€“ Apply Feature Changes (VS Code)
**Dosya Ã¶nerisi:**  
`30_PROMPTS/VSCode_Apply_Feature_Changes_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- VS Code Chatâ€™te:
  - Ãœstte "Consolidated Feature Design â€“ MASTER_TEMPLATE_CORE"  
    dokÃ¼manÄ± yapÄ±ÅŸtÄ±rÄ±lÄ±r.  
  - ArdÄ±ndan bu prompt Ã§alÄ±ÅŸtÄ±rÄ±lÄ±r.  
- MASTER_TEMPLATE_CORE.pine Ã¼zerinde:
  - Yeni inputlarÄ± ekler,  
  - Yeni fonksiyon / filter / signal / SL-TP modÃ¼lÃ¼nÃ¼ ekler,  
  - DeÄŸiÅŸiklikleri uygular.  
- Kurallar:
  - Mimariyi bozmaz (Signal Plugin / Engine / Filters / Viz).  
  - Yeni Ã¶zellik `use_*` ile aÃ§Ä±lÄ±p kapanÄ±r, defaultâ€™ta OFF.  
  - OFF iken eski davranÄ±ÅŸ bire bir korunur.  
  - JSON alert formatÄ± bozulmaz.

---

## STEP 5 â€“ VS Code: Double-Check Behavior

### Prompt 5 â€“ Double-Check Behavior After Feature Integration
**Dosya Ã¶nerisi:**  
`30_PROMPTS/VSCode_DoubleCheck_Feature_Behavior_MASTER_TEMPLATE_CORE.md`

**Ne yapar?**  
- Refactorâ€™dan sonra:
  - Nelerin deÄŸiÅŸtiÄŸini Ã¶zetler,  
  - Mimari hala doÄŸru mu (signal vs engine vs filters) kontrol eder,  
  - `use_*` OFF iken eski davranÄ±ÅŸÄ±n aynÄ± kaldÄ±ÄŸÄ±nÄ± teyit eder,  
  - `use_*` ON iken davranÄ±ÅŸÄ±n tasarÄ±mla uyumlu olup olmadÄ±ÄŸÄ±nÄ± kontrol eder.  
- Varsa:
  - Mimari ihlaller veya geri dÃ¶nÃ¼lmesi gereken deÄŸiÅŸiklikleri listeleyip Ã¶nerir.

---

## Genel Workflow Ã–zeti

1. **Gemini (1A / 1B / 1C)**  
   - YouTube videosundan MASTER_TEMPLATE_CORE uyumlu teknik rapor Ã¼retir.

2. **6Ã— LLM â€“ Feature Module Design (Prompt 2)**  
   - Teknik rapora gÃ¶re modÃ¼ler tasarÄ±m + kod planÄ± Ã¼retir.

3. **ChatGPT â€“ Consolidation (Prompt 3)**  
   - 6 raporu birleÅŸtirir â†’ â€œConsolidated Feature Design â€“ MASTER_TEMPLATE_COREâ€.

4. **VS Code â€“ Apply Feature Changes (Prompt 4)**  
   - Consolidated tasarÄ±mÄ± MASTER_TEMPLATE_CORE.pine iÃ§ine uygular.

5. **VS Code â€“ Double-Check (Prompt 5)**  
   - Mimari ve davranÄ±ÅŸ bÃ¼tÃ¼nlÃ¼ÄŸÃ¼nÃ¼ kontrol eder.

