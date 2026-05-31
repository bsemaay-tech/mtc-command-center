# MTC V2 Architecture Pending Audit

Date: 2026-03-14
Scope: `00_MASTER_TEMPLATE/MTC_V2` altindaki onceki audit/report dosyalarindan kalan ve `MTC_V2_ARCHITECTURE.md` icine henuz yansimamis oneriler.

Bu dosya yalnizca henuz uygulanmamis maddeleri tutar. Asagidaki aileler architecture icinde artik mevcut oldugu icin bu rapora yeniden alinmadi:

- base same-bar reason matrix (`OPP_SIGNAL`, `FILTER_BLOCK`, `TIME_STOP`, `EOD`, `EOW`)
- `working_exit_reference_qty`, `completed_exit_ids`, working-exit rebasing
- `event_seq_in_bar`, `fill_type`, `is_pessimistic_sl`, `execution_profile_id`
- `guard_recovery_owner` single-owner semantigi
- HTF `shift(1)`, session-aware carry, DST/holiday/half-day kurallari
- warmup seeding, `effective_history_start`, `warmup_seed_provenance`
- config naming/scale kurallari, schema/manifest source-of-truth yonu
- runner tarafinda `gate_results` uretimi ve raw `OPP_SIGNAL` kontrati

## Pending Recommendations

| ID | Henuz uygulanmayan onerı | Ana kaynaklar | Neden hala acik | Durum |
|---|---|---|---|---|
| P01 | Section 2 diyagramini dogrudan exit-first yap ve ayni gorsele HTF snapshot build adimini ekle | `Pipline/pipeline_audit_report.md`, `Pipline/pipeline_audit_report_claude_opus.md`, `Pipline/pipeline_audit_report_roo.md`, `Pipline/gemini_code_assist.md`, `Pipline/VSCODE .md` | Section 2 hala gorsel olarak `Position Manager -> Position Sizing -> Entry Execution -> Exit Rules` akisini gosteriyor. Sonradan eklenen canonical-order notu dogru, ama diyagramin kendisi hala yanlis okunabilir. HTF snapshot build de ust gorselde acik stage olarak gorunmuyor. | APPLY |
| P02 | Transform state-awareness kontratini tutarli hale getir: ya `portfolio_state`/flat-state girdisini `SignalTransform` kontratina ekle ya da `conf_gate_only_when_flat` benzeri davranislari transform kapsamindan cikar. Ayrica Section 2 output'unda `TransformResult.source` alani da gosterilsin | `Pipline/gemini_code_assist.md`, `Pipline/pipeline_audit_report_claude_opus.md` | Architecture metni `conf_gate_only_when_flat=True` iken pozisyon acikken transform pass-through derken, Section 6.2 `SignalTransform.on_bar(...)` imzasi yalniz `signal + bar` aliyor. Section 2 de `source` alanini gostermiyor. Bu, dokuman icinde kalan gercek bir kontrat drift'i. | APPLY |
| P03 | Section 2 PositionManager girisini canonical runner kontratiyla hizala: `gated_signal` adini kullan, `close_reason_this_bar` ve `block_new_entries_this_bar` alanlarini acikca ekle | `Pipline/gemini_code_assist.md` | Section 6.5 ve Section 8 bu alanlari kullaniyor; Section 2 Step 4 ise hala yalniz `filtered_signal + PortfolioState/Position` gibi daha zayif bir kontrat gosteriyor. | APPLY |
| P04 | `execution_profile_id` yanina gercek bir `ExecutionProfile` schema/object katmani ekle | `AUDIT_6/gpt-5-codex.md`, `AUDIT_6/AUDIT_6_CONSOLIDATED_CODEX_READONLY_20260310.md`, `MTC_V2_DEEP_AUDIT_R2_Codex_GPT5.md` | Architecture artik base profile ve `execution_profile_id` tasiyor; fakat farkli same-bar/fill/workbook varyantlarini tasiyan yapisal bir profile objesi hala yok. | DEFER / ADVANCED PARITY |
| P05 | `ExitResult + continue_evaluation_this_bar` modelini tam `ExitPlan/ExitEvent[]` soyutlamasina yukselt | `AUDIT_6/gpt-5-codex.md`, `Pipline/chatgbt.md`, `AUDIT_6/AUDIT_6_CONSOLIDATED_CODEX_READONLY_20260310.md` | Ordered same-bar lifecycle bugun loop ve metadata ile tasiniyor; tam event-plan modeli architecture'a alinmis degil. Mevcut dokuman bunu bilincli olarak daha hafif bir modelde birakiyor. | DEFER / ONLY IF IMPLEMENTATION PAIN APPEARS |
| P06 | `time_stop_cooldown_bars` alanini en azindan optional/profile-scoped policy veya explicit limit-notu olarak ekle | `AUDIT_6/claude-opus-4-6.md`, `AUDIT_6/Gemini`, `AUDIT_6/grok`, `AUDIT_6/Chatgbt`, `AUDIT_6/deepseek` | Architecture base scope'ta pulse producer + `cooldown_bars_after_exit` modeline dayaniyor. Ayrik time-stop cooldown halen bilincli olarak yok; bu karar dokumanda daha net sinirlanabilir. | OPTIONAL / LOW |
| P07 | `SignalProducer` icin `semantic_kind` / `output_mode = pulse` benzeri explicit capability alanini ekle | `AUDIT_6/gpt-5-codex.md`, `AUDIT_6/Chatgbt` | Pulse semantigi dokumanda anlatiliyor ama type/contract seviyesinde capability olarak gorunmuyor. | OPTIONAL |
| P08 | Exit fazi handoff'unu daha sikilastir: ya adli bir `ExitPhaseResult`/handoff modeli tanimla ya da `ExitContext` icin daraltilmis/frozen erisim kurallari koy | `Pipline/chatgbt.md`, `Pipline/Claude.md`, `Pipline/pipeline_audit_report_claude_opus.md`, `AUDIT_6/Gemini`, `AUDIT_6/claude-opus-4-6.md` | Architecture bugun `closed_this_bar_reason` ve `block_new_entries_this_bar` state'i ile ilerliyor, ama exit kurallarinin genis `ExitContext` icinde yanlis tier'a erismesini tip seviyesinde engelleyen bir kontrat yok. | OPTIONAL / DESIGN HARDENING |

## Recommended Interpretation

- `P01-P03` architecture dokumani tekrar revize edilirse dogrudan uygulanmali.
- `P04-P05` aktif base-core blocker degil; ama V2 birden fazla parity/execution profiline genislerse ilk buyuyecek borc burada.
- `P06-P08` bilinclı olarak disarida birakilmis veya dusuk oncelikli tasarim sertlestirmeleridir.

## Final Note

Bu dosya, eski audit/report yigininin yerine gecen tek kalan ozet dosyadir.
Eski raporlar bu konsolidasyondan sonra silinebilir.
