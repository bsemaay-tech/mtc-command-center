# 00 Cheat Sheet Performance Prompts Master Template Core

AmaÃ§:  
MASTER_TEMPLATE_CORE.pine iÃ§in **4 adÄ±mlÄ±, Ã§ok-LLMâ€™li** bir performans workflowâ€™u:

1) Multi-LLM Performance Audit  
2) Consolidation / Merge (ChatGPT)  
3) Performance Refactor (VS Code Chat)  
4) Double-Check Behavior (VS Code Chat)

---

## 1ï¸âƒ£ PERFORMANCE AUDIT (multi-LLM)

**Prompt file Ã¶nerisi:**  
`30_PROMPTS/LLM_Performance_Audit_MASTER_TEMPLATE_CORE.md`

**KullanÄ±ldÄ±ÄŸÄ± yer:**  
- ChatGPT, Gemini, DeepSeek, Grok, Claude, Perplexity vb.  
- Her birine aynÄ± prompt veriliyor.

**Ne yapar?**  
- Kodu deÄŸiÅŸtirmez, sadece **performans audit raporu** Ã¼retir.  
- Her model:
  - Ã‡Ä±ktÄ±nÄ±n baÅŸÄ±na `MODEL: <name>` yazar.  
  - Performance issues & fixes listesi Ã§Ä±karÄ±r.  
  - Her Ã¶neriye Priority (HIGH/MEDIUM/LOW) ve Safety (SAFE / RISKY) etiketi koyar.  

**Ne zaman kullanÄ±lÄ±r?**  
- Performans aÃ§Ä±sÄ±ndan â€œneresi ÅŸiÅŸman, neresi pahalÄ± Ã§alÄ±ÅŸÄ±yor?â€ gÃ¶rmek istediÄŸinde.  
- FarklÄ± LLMâ€™lerden fikir toplayÄ±p, sonrasÄ±nda ortak noktalarÄ± birleÅŸtirmek istediÄŸinde.

---

## 2ï¸âƒ£ CONSOLIDATION / MERGE (ChatGPT)

**Prompt file Ã¶nerisi:**  
`30_PROMPTS/LLM_Performance_Audit_MERGE_MASTER_TEMPLATE_CORE.md`

**KullanÄ±ldÄ±ÄŸÄ± yer:**  
- Sadece ChatGPT iÃ§inde.

**Ne yapar?**  
- 4â€“8 farklÄ± LLMâ€™den gelen audit raporlarÄ±nÄ± okur.  
- AynÄ± problemi iÅŸaret eden Ã¶nerileri **tek bir FIX** altÄ±nda birleÅŸtirir.  
- Her FIX iÃ§in:
  - KaÃ§ LLMâ€™in Ã¶nerdiÄŸini (Count)  
  - Hangi modellerin Ã¶nerdiÄŸini (Models)  
  - Priority ve Safety bilgisini  
  - VS Codeâ€™un uygulayabileceÄŸi net bir â€œRecommended Changeâ€ metnini verir.  
- Sadece **dÃ¼zeltme Ã¶nerileri** kalÄ±r; â€œsorun yokâ€ bÃ¶lÃ¼mleri atÄ±lÄ±r.

**Ne zaman kullanÄ±lÄ±r?**  
- 6 farklÄ± LLMâ€™den audit raporlarÄ± aldÄ±ktan sonra.  
- VS Codeâ€™a verilecek **tek, temiz bir â€œplanâ€** oluÅŸturmak istediÄŸinde.

---

## 3ï¸âƒ£ PERFORMANCE REFACTOR (VS Code Chat)

**Prompt file Ã¶nerisi:**  
`30_PROMPTS/VSCode_Performance_Refactor_MASTER_TEMPLATE_CORE.md`

**KullanÄ±ldÄ±ÄŸÄ± yer:**  
- VS Code Chat iÃ§inde, repo aÃ§Ä±kken.

**Ne yapar?**  
- Bir Ã¶nceki adÄ±mda ChatGPTâ€™den gelen  
  **â€œConsolidated Performance Audit â€“ Fixes Onlyâ€** raporunu okur.  
- Bu raporda **Safety = SAFE_NO_BEHAVIOR_CHANGE** olan FIXâ€™leri uygular.  
- Kodu doÄŸrudan `MASTER_TEMPLATE_CORE.pine` Ã¼zerinde refactor eder.  
- Stratejinin:
  - Entry / exit davranÄ±ÅŸÄ±nÄ±  
  - Risk motorunu  
  - SL/TP, Multi-TP, BE, Trailing  
  - JSON alert formatÄ±nÄ±  
  DEÄÄ°ÅTÄ°RMEZ.

**Ne zaman kullanÄ±lÄ±r?**  
- Merge aÅŸamasÄ±ndan sonra, artÄ±k performans iyileÅŸtirmelerini **otomatik uygulamak** istediÄŸinde.

---

## 4ï¸âƒ£ DOUBLE-CHECK BEHAVIOR (VS Code Chat)

**Prompt file Ã¶nerisi:**  
`30_PROMPTS/VSCode_DoubleCheck_Behavior_MASTER_TEMPLATE_CORE.md`

**KullanÄ±ldÄ±ÄŸÄ± yer:**  
- VS Code Chat iÃ§inde, refactor tamamlandÄ±ktan SONRA.

**Ne yapar?**  
- Performans refactorâ€™undan sonra dosyayÄ± tekrar inceler.  
- Ne deÄŸiÅŸtiÄŸini bÃ¶lÃ¼m bÃ¶lÃ¼m Ã¶zetler.  
- ÅunlarÄ±n hiÃ§ deÄŸiÅŸmediÄŸini **aÃ§Ä±kÃ§a teyit eder** (yoksa uyarÄ±r):
  - Risk engine (f_calc_qty, daily loss limit, max trades per day, leverage capâ€¦)  
  - SL/TP matematiÄŸi  
  - JSON alert formatÄ±  
  - Signal API (`longSignal_*`, `shortSignal_*`, edgesâ€¦)  
  - Supertrend sinyal davranÄ±ÅŸÄ±  
- EÄŸer beklenmeyen bir davranÄ±ÅŸ deÄŸiÅŸikliÄŸi varsa:
  - Nerede olduÄŸunu sÃ¶yler  
  - Neden olduÄŸunu aÃ§Ä±klar  
  - Geri alma / dÃ¼zeltme Ã¶nerir.

**Ne zaman kullanÄ±lÄ±r?**  
- Refactor sonrasÄ±nda, â€œBu performans deÄŸiÅŸiklikleri stratejiyi bozdu mu?â€  
  sorusuna net, sistematik bir cevap almak istediÄŸinde.

---

## HÄ±zlÄ± Ã–zet â€“ Workflow

1. **Step 1 â€“ Multi-LLM Audit**  
   - 6 farklÄ± LLMâ€™e: `LLM_Performance_Audit_MASTER_TEMPLATE_CORE` promptu  
   - SonuÃ§: 6 adet STRUCTURED audit raporu.

2. **Step 2 â€“ Merge (ChatGPT)**  
   - TÃ¼m raporlarÄ± tek sohbette ChatGPTâ€™ye yapÄ±ÅŸtÄ±r.  
   - `LLM_Performance_Audit_MERGE_MASTER_TEMPLATE_CORE` promptunu kullan.  
   - SonuÃ§:  
     **â€œConsolidated Performance Audit â€“ Fixes Only (MASTER_TEMPLATE_CORE)â€**

3. **Step 3 â€“ Refactor (VS Code)**  
   - VS Code Chatâ€™te Ã¶nce Consolidated raporu yapÄ±ÅŸtÄ±r.  
   - Sonra `VSCode_Performance_Refactor_MASTER_TEMPLATE_CORE` promptunu Ã§alÄ±ÅŸtÄ±r.  
   - SonuÃ§: Performans iyileÅŸtirilmiÅŸ, davranÄ±ÅŸÄ± korunmuÅŸ yeni kod.

4. **Step 4 â€“ Double-Check (VS Code)**  
   - Refactorâ€™dan sonra aynÄ± dosya Ã¼zerinde  
     `VSCode_DoubleCheck_Behavior_MASTER_TEMPLATE_CORE` promptunu Ã§alÄ±ÅŸtÄ±r.  
   - SonuÃ§: DeÄŸiÅŸikliklerin davranÄ±ÅŸÄ± bozmadÄ±ÄŸÄ±na dair detaylÄ± bir audit raporu.
