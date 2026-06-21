> **REPO PLACEMENT NOTE (added 2026-06-20 by Claude Opus 4.8).** Filed at
> `MTC_COMMAND_CENTER/09_DOCS/AI_TOOLING/MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md`.
> The folder names this document assumes (`00_DOCS`, `00_KNOWLEDGE_BASE`, `09_TOOLS`,
> `09_AUTOMATION`, `00_PLANS`) **do not exist** in this repo. The real path mapping, the
> phased plan with acceptance criteria, and a critical review of the decisions below live
> in two sibling files — read them before acting on any "Önerilen aksiyon" path here:
> - `AI_TOOL_INTEGRATION_PLAN.md` — how/where to actually integrate (real repo paths + gates).
> - `CLAUDE_REVIEW_OF_CODEX_BACKLOG.md` — where Claude disagrees with this backlog.

# MTC Command Center — AI Tools Master Integration Backlog + Claude Code Prompt

**Prepared for:** MTC Command Center / QuantLens / TradingView LAB  
**Prepared date:** 2026-06-20  
**Purpose:** Tek bir kalıcı dosyada bu sohbet kapsamında incelenen tüm AI araçlarını, transcriptlerden öğrenilen detayları, repo adreslerini, MTC için kararları, beklenen faydaları, riskleri, eksik araştırma ihtiyaçlarını ve Claude Code'a verilecek uygulama promptunu toplamak.

---

## 0. Bu dosyanın amacı

Bu sohbet içinde birçok video transcripti üzerinden Claude Code / Codex / AI workflow aracı değerlendirildi. Amaç, bu kararların chat içinde kaybolmaması ve MTC repo içinde kalıcı bir entegrasyon backlog'una dönüşmesidir.

Bu dosya daha sonra repo içine koyulduğunda, herhangi bir LLM şu soruya cevap verebilmelidir:

```text
MTC Command Center'a sırayla hangi AI araçları entegre edilmeli, hangileri pilot yapılmalı, hangileri dış servis olarak kullanılmalı, hangileri hiç kullanılmamalı?
```

Bu dosya ayrıca şu ikinci amacı taşır:

```text
Claude Code, bu dosyayı repo içine uygun yere koysun, _AI_MEMORY dosyalarını güncellesin, araç entegrasyon planını unutulmayacak şekilde iş akışına bağlasın ve gelecekteki LLM oturumları bu roadmap'i otomatik bulsun.
```

---

## 1. Karar sınıfları

| Karar | Anlamı |
|---|---|
| **Hemen entegre et** | MTC workflow'una kısa sürede kontrollü şekilde eklenmeli. |
| **Yan servis olarak entegre et** | Core repo davranışına gömülmeden dış/local servis olarak çalışmalı. |
| **Pattern olarak pilot** | Repo/tool doğrudan kurulmasın; mantığı MTC'ye özel workflow'a dönüştürülsün. |
| **Kontrollü pilot** | Ayrı branch/folder/test akışında denenmeli, sonra karar verilmeli. |
| **İleride değerlendir** | İlginç ama şu an MTC önceliği değil. |
| **Şimdilik alma / kullanma** | MTC core için düşük değer, yüksek risk veya dikkat dağıtıcı. |

---

# Grup A — Hemen entegre edilmesi önerilenler

Bu grup MTC'nin en acil problemlerine doğrudan dokunur: repo hafızası, agent disiplini, maliyet takibi, doküman ingestion, model routing ve Claude/Codex koordinasyonu.

---

## A1. `CLAUDE.md` / `AGENTS.md` / `CODEX.md` — repo içi agent kuralları

**Repo / kaynak:**  
- https://github.com/multica-ai/andrej-karpathy-skills  
- https://developers.openai.com/codex/skills

**Karar:** Hemen entegre et.

**Ne işe yarar:**  
Claude Code, Codex ve diğer agent'lara repo içinde nasıl davranacaklarını söyleyen kalıcı kurallar. Karpathy tarzı yaklaşımda temel prensipler: kodlamadan önce düşün, basitlik, cerrahi değişiklik, hedef odaklı doğrulama.

**Transcriptlerden öğrenilen detay:**  
Karpathy `CLAUDE.md` yaklaşımı basit ama etkili: agent'ın hızlıca büyük refactor yapmasını değil, dikkatli ve küçük adımlarla ilerlemesini sağlar. MTC gibi çok parçalı bir repo için bu kritik.

**MTC faydası:**

- `MTC_V2.pine` gibi korunması gereken dosyalara gereksiz dokunmayı azaltır.
- Registry/schema kontratlarını korur.
- Dashboard API ve UI değişikliklerinde veri kontratını hatırlatır.
- Büyük işlerden önce plan çıkarmayı zorunlu hale getirir.
- İş sonunda `_AI_MEMORY` güncellemesini hatırlatır.
- Claude, Codex, Antigravity, OpenCode, Hermes gibi araçların aynı kurallarla çalışmasını sağlar.

**Önerilen aksiyon:**

```text
CLAUDE.md
AGENTS.md
CODEX.md
```

dosyaları oluştur veya mevcutsa güncelle.

Eklenecek MTC özel kurallar:

```text
- Do not modify MTC_V2.pine unless explicitly required.
- Do not change registry schemas without a written migration plan.
- Prefer surgical changes over broad refactors.
- Before major work, create or update PLAN.md.
- After major work, update _AI_MEMORY files.
- No live trading, broker execution, or credential exposure.
- Verify dashboard API contracts after UI/API changes.
```

**İlave araştırma:**  
Repo içinde zaten `CLAUDE.md`, `AGENTS.md`, `CODEX.md` veya benzeri dosya var mı incelenmeli. Varsa yenisi yaratılmamalı; mevcut dosya geliştirilmelidir.

---

## A2. MTC-specific Grill-Me Plan Workflow

**Repo / kaynak:**  
- https://github.com/mattpocock/skills  
- https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md  
- https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md  
- Video: https://youtu.be/ENCRw5-uJBA?si=X2m2AAPAMpg5hoBo

**Karar:** Hemen entegre et, ama MTC'ye özel pattern olarak.

**Ne işe yarar:**  
Normal plan mode yerine agent'ın kodlamadan önce seni sorgulamasını sağlar. Belirsiz istekleri uygulanabilir plana dönüştürür.

**Transcriptlerden öğrenilen detay:**  
Video, normal plan mode'un yetmediğini söylüyor. Asıl problem, kullanıcının fuzzy fikrini Claude'un yanlış anlaması. Grill-Me, bu boşluğu kapatmak için daha derin sorular soruyor. Grill-with-docs ise mevcut doküman/domain model ile planı karşılaştırıyor.

**MTC faydası:**

- Yanlış mimari kararları koddan önce yakalar.
- Registry/schema/backtest/dashboard contract etkilerini baştan sorgulatır.
- `MTC Light`, naked vs MTC-enhanced backtest, scoring, Strategy Detail Page gibi konularda yanlış kapsamı azaltır.
- Kullanıcı onayı öncesi `PLAN.md` oluşmasını sağlar.

**Önerilen aksiyon:**

Repo-local skill olarak yaz:

```text
.claude/skills/mtc-grill-plan/SKILL.md
.agents/skills/mtc-grill-plan/SKILL.md
```

Zorunlu kullanılacağı işler:

```text
- registry/schema changes
- dashboard API changes
- dashboard data contract changes
- MTC Light / MTC_v2 integration
- scoring system changes
- backtest engine changes
- multi-file architecture changes
```

**Risk:**  
`grill-with-docs` ADR yazabiliyor. Uygulanmamış kararların `accepted ADR` gibi kaydedilmesi MTC hafızasını kirletir.

**Kural:**

```text
Draft ADR allowed.
Accepted ADR only after implementation + audit + user approval.
```

**İlave araştırma:**  
Repo içinde mevcut plan/ADR yapısı incelenmeli. Eğer `00_PLANS`, `docs/adr`, `_AI_MEMORY/PLANS` gibi bir yapı varsa ona uyulmalı.

---

## A3. Codex as Read-Only Reviewer / Codex Plugin for Claude Code

**Repo / kaynak:**  
- https://github.com/openai/codex-plugin-cc  
- https://developers.openai.com/codex/cli  
- https://developers.openai.com/codex/windows  
- Video: https://youtu.be/ENCRw5-uJBA?si=X2m2AAPAMpg5hoBo  
- Video: https://youtu.be/8kWONfT_-H8?si=P_Rx2_6PmlGLJyf8

**Karar:** Hemen entegre et.

**Ne işe yarar:**  
Claude'un yaptığı planı veya diff'i Codex ikinci göz olarak inceler. Claude'un kendi işini kendisinin onaylaması engellenir.

**Transcriptlerden öğrenilen detay:**  
Grill-Me-Codex videosunda Claude plan çıkarıyor, Codex read-only review yapıyor, Claude planı revize ediyor ve roundlar sonunda plan onaylanıyor. Codex Desktop videosu ise Claude Code kullanıcılarının Codex'e kolay geçebileceğini ve iki aracın birlikte kullanılmasının vendor lock-in riskini azalttığını anlatıyor.

**MTC faydası:**

- Claude'un kaçırdığı schema/API/backtest risklerini yakalar.
- Claude kredisi bittiğinde iş Codex'e devredilebilir.
- Codex final diff audit yapabilir.
- Tek vendor'a bağımlılığı azaltır.
- Büyük işlerde kalite kontrol döngüsü oluşturur.

**Önerilen aksiyon:**

Oluştur:

```text
00_DOCS/AI_WORKFLOW/CODEX_REVIEW_PROMPTS.md
00_DOCS/AI_WORKFLOW/CODEX_CLAUDE_WORKFLOW.md
CODEX.md
```

Standart workflow:

```text
Claude plans / implements
→ Codex read-only review
→ Claude fixes valid findings
→ tests / verification
→ _AI_MEMORY update
```

**İlave araştırma:**  
Repo içinde Codex plugin/config var mı kontrol edilmeli. Codex Windows/CLI kurulumu repo dışı dokümante edilmeli.

---

## A4. Graphify — repo architecture knowledge graph

**Repo / kaynak:**  
- https://github.com/safishamsi/graphify  
- https://graphify.net/

**Karar:** Hemen entegre et, read-only architecture intelligence layer olarak.

**Ne işe yarar:**  
Repo dosyalarını, fonksiyonlarını, class/import ilişkilerini, docs/media kaynaklarını knowledge graph'a çevirir. Agent'ların repo'yu tekrar tekrar grep/explore yapmadan anlamasına yardım eder.

**Transcriptlerden öğrenilen detay:**  
Graphify üç pass mantığıyla anlatıldı: deterministic code structure extraction, audio/video transcription, docs/images semantic processing. Özellikle codebase için Obsidian ile full RAG arasında bir yerde konumlanıyor. Token tasarrufu iddiaları çok yüksek olsa da gerçek faydası repo haritasıdır.

**MTC faydası:**

- Strategy metadata → registry → dashboard akışını izler.
- Dashboard API/frontend ilişkilerini gösterir.
- `pipeline_reader.py`, `STRATEGY_REGISTRY.json`, schema dosyalarının etkisini bulur.
- Claude/Codex repo'yu daha hızlı anlar.
- Büyük değişiklik öncesi impact analysis sağlar.

**Önerilen aksiyon:**

```text
00_DOCS/ARCHITECTURE_GRAPH/
09_TOOLS/graphify/
```

İlk test soruları:

```text
- How does strategy metadata flow into the dashboard?
- Which files produce STRATEGY_REGISTRY.json?
- What dashboard files depend on pipeline_reader.py?
- Which files are central to MTC backtest workflow?
```

Exclude edilecekler:

```text
.git/
node_modules/
.venv/
raw market data
large optimization outputs
.env
secrets
API keys
broker credentials
```

**İlave araştırma:**  
Gerçek MTC repo üzerinde çalıştırılıp çıktı kalitesi değerlendirilmeli. `graph.json` commit edilecek mi kararlaştırılmalı.

---

## A5. MarkItDown — document-to-Markdown ingestion

**Repo / kaynak:**  
- https://github.com/microsoft/markitdown

**Karar:** Hemen entegre et.

**Ne işe yarar:**  
PDF, DOCX, PPTX, XLSX, image/audio gibi dosyaları LLM dostu Markdown'a çevirir.

**Transcriptlerden öğrenilen detay:**  
Videoda MarkItDown PDF'i temiz heading ve tablo yapısıyla Markdown'a çevirdi. Microsoft aracı olduğu ve extensible olduğu vurgulandı.

**MTC faydası:**

- YouTube transcript, PDF, Excel backtest sonuçları ve proje dokümanlarını tek formatta toplar.
- `00_KNOWLEDGE_BASE/raw` için temiz kaynak üretir.
- Claude/Codex'e ham PDF/XLSX vermek yerine düşük token, yüksek kalite input sağlar.
- Teknik rapor, packing list, strateji dokümanı ingestion için uygundur.

**Önerilen aksiyon:**

```text
09_TOOLS/document_ingestion/markitdown/
```

veya QuantLens içinde:

```text
03_QUANTLENS/tools/document_ingestion/markitdown/
```

**İlave araştırma:**  
Gerçek MTC PDF/XLSX dosyalarında test edilmeli. LiteParse ile karşılaştırılmalı.

---

## A6. LiteParse — local PDF/layout parser

**Repo / kaynak:**  
- https://github.com/run-llama/liteparse

**Karar:** Hemen entegre et / kontrollü pilot.

**Ne işe yarar:**  
PDF ve dokümanları lokal, layout-aware şekilde parse eder. Kolonlar, tablolar, spatial text gibi durumlarda faydalı olabilir.

**Transcriptlerden öğrenilen detay:**  
LiteParse, dış API kullanmadan lokal çalışan PDF parser olarak anlatıldı. Özellikle hassas PDF'leri Opus/OpenAI'a göndermeden işlemek için değerli.

**MTC faydası:**

- Elektrik proje PDF'leri ve teknik tablolar için lokal parsing.
- Backtest PDF/raporları için layout koruma.
- Hassas dokümanlarda privacy.
- MarkItDown'a alternatif veya tamamlayıcı.

**Önerilen aksiyon:**

MarkItDown ile A/B test:

```text
same PDF → MarkItDown
same PDF → LiteParse
compare: tables, headings, layout, LLM usability
```

**İlave araştırma:**  
Kendi packing list PDF'leri, proje PDF'leri ve strateji PDF'leriyle test edilmeli.

---

## A7. CodeBurn — AI cost observability

**Repo / kaynak:**  
- https://github.com/getagentseal/codeburn

**Karar:** Hemen entegre et.

**Ne işe yarar:**  
Claude Code, Codex, Cursor vb. araçlarda token, maliyet ve performans gözlemi sağlar.

**Transcriptlerden öğrenilen detay:**  
CodeBurn; activity, project, model, tool, shell command, MCP server kırılımında token ve dolar maliyeti gösteriyor. Ayrıca maliyet azaltma önerileri veriyor.

**MTC faydası:**

- Claude vs Codex maliyetini ölçer.
- Graphify, Headroom, Caveman gerçekten tasarruf sağlıyor mu gösterir.
- Uzun audit / plan / implementation maliyetlerini ayırır.
- Token optimizasyonunu sezgiyle değil veriyle yapar.

**Önerilen aksiyon:**

```text
00_DOCS/AI_WORKFLOW/COST_OBSERVABILITY.md
09_TOOLS/cost_observability/codeburn/
```

veya global local tool olarak kullanıp sonuçları MTC raporlarına yaz.

**İlave araştırma:**  
Mevcut provider/proxy fiyatları doğru okunuyor mu kontrol edilmeli. API/proxy routing durumlarında fiyat hatası olabilir.

---

## A8. Caveman Light — concise agent outputs

**Repo / kaynak:**  
- https://github.com/JuliusBrussee/caveman

**Karar:** Hemen entegre et, ama Light modda.

**Ne işe yarar:**  
Claude/Codex cevaplarını kısa, direkt ve daha az verbose hale getirir.

**Transcriptlerden öğrenilen detay:**  
Caveman düşünme token'larını değil, görünen output uzunluğunu azaltır. Toplam tasarruf iddia edildiği kadar büyük değildir; transcriptte yaklaşık %5 genel tasarruf daha gerçekçi görüldü. Asıl faydası okunabilirliktir.

**MTC faydası:**

- Audit/status çıktıları kısalır.
- Uzun Claude/Codex cevapları daha takip edilebilir olur.
- Kullanıcı ve agent daha az noise ile çalışır.

**Önerilen aksiyon:**

```text
Caveman Light = progress updates, audit summaries, terminal recaps
Caveman Off = final technical reports, detailed implementation plans
```

**İlave araştırma:**  
Bir audit ve bir implementation recap üzerinde test edilmeli.

---

## A9. MTC Knowledge Base — self-improving research/wiki system

**Kaynak video:**  
- https://youtu.be/ib74sLgjIBM?si=0sNpZ3IyvWCGZ8lr

**Karar:** Hemen entegre et.

**Ne işe yarar:**  
Claude-managed folder-based knowledge base. Obsidian, vector database veya RAG gerektirmeden çalışır.

**Transcriptlerden öğrenilen detay:**  
Video şu yapıyı önerdi:

```text
raw/     = ham bilgi
wiki/    = Claude'un düzenlediği bilgi tabanı
outputs/ = soru cevaplarından üretilen raporlar
CLAUDE.md = sistem kuralları
```

Ayrıca monthly health check ile çelişkiler, kaynak eksikleri, stale articles, broken links, işlenmemiş raw dosyalar ve yeni makale adayları bulunuyor.

**MTC faydası:**

- Bu sohbetten çıkan tüm tool raporlarını tek yerde tutar.
- Aynı tool farklı videoda tekrar gelirse hızlı elenir.
- “Neden Graphify uygula, Headroom pilot, MoneyPrinter alma demiştik?” sorusu cevaplanır.
- MTC architecture/tool decision hafızası oluşur.
- `_AI_MEMORY` operasyonel kalır, knowledge base araştırma/hafıza katmanı olur.

**Önerilen yapı:**

```text
00_KNOWLEDGE_BASE/
  CLAUDE.md
  raw/
    ai_tools/
    youtube_transcripts/
    architecture_notes/
  wiki/
    ai_tool_decision_matrix.md
    mtc_agent_workflow.md
    document_ingestion_workflow.md
    codebase_mapping_workflow.md
    cost_optimization_workflow.md
  outputs/
  CHANGELOG.md
  INGESTION_REGISTRY.md
  HEALTH_CHECK_REPORTS/
```

**İlave araştırma:**  
Repo içinde zaten knowledge base benzeri klasör var mı incelenmeli. Varsa bu yapı ona entegre edilmeli.

---

# Grup B — Yan servis olarak entegre edilecekler

Bu araçlar MTC core koduna gömülmemeli. Ayrı servis, watchdog, automation veya local helper olarak kullanılmalı.

---

## B1. n8n MCP / n8n watchdog

**Repo / kaynak:**  
- https://docs.n8n.io/advanced-ai/mcp/accessing-n8n-mcp-server/  
- https://blog.n8n.io/n8n-mcp-server/

**Karar:** Yan servis olarak entegre et.

**Ne işe yarar:**  
n8n MCP, Claude/Codex'in n8n workflow'larıyla çalışmasına imkan verir. n8n ise log izleme, Telegram/email bildirme, rapor gönderme gibi otomasyonlar için güçlüdür.

**Transcriptlerden öğrenilen detay:**  
n8n MCP'nin yeni versiyonu TypeScript ile workflow oluşturup validate ediyor, sonra JSON'a çevirip n8n instance içine koyuyor. Eski hacky MCP yaklaşımlarından daha güvenilir anlatıldı.

**MTC faydası:**

- Gece çalışan backtest/optimization işlerini izler.
- Hata olursa telefona bildirir.
- Progress raporu gönderir.
- Bitince result path / summary yollar.
- Claude/Codex sürekli açık kalmadan izleme yapılır.

**Önerilen aksiyon:**

```text
09_AUTOMATION/n8n/
  README.md
  workflows/
  backtest_watchdog.example.json
  report_sender.example.json
  .env.example
```

**Kritik kural:**  
Bunu “agent hatırlarsa çalıştırır” şeklinde bırakma. Tam otomasyon için backtest runner düzenli log/progress dosyası üretmeli, n8n bunu otomatik izlemeli.

**İlave araştırma:**  
Mevcut MTC backtest log formatı ve result output klasörü incelenmeli. Telegram/email route seçilmeli.

---

## B2. Zapier — managed permission middle layer

**Kaynak:**  
- https://zapier.com/

**Karar:** Yan servis / watchlist.

**Ne işe yarar:**  
AI agent'lara Gmail, Calendar, Notion gibi SaaS araçlarına kontrollü erişim verme katmanı.

**MTC faydası:**

- SaaS permission yönetimi.
- Agent'lara sınırlı yetki verme.
- Gmail/Calendar/Notion işlerindeki güvenlik.

**Önerilen aksiyon:**  
MTC'nin local/backtest ihtiyacı için öncelik n8n. Zapier ancak SaaS tarafı büyürse değerlendirilmeli.

**İlave araştırma:**  
Şimdilik yok.

---

## B3. Webwright — browser automation/testing

**Repo / kaynak:**  
- https://github.com/microsoft/webwright  
- https://playwright.dev/

**Karar:** DROPPED 2026-06-20 (Barış) — kullanılmayacak. Mevcut `Claude-in-Chrome` / `Claude_Preview` MCP'leri ile çakışıyor (redundant). Dashboard QA için onlar kullanılacak. (Orijinal Codex kararı: kontrollü pilot.)

**Ne işe yarar:**  
Agent'ın browser'ı pixel/screenshot yerine daha düşük seviye Playwright mantığıyla kontrol etmesini sağlar.

**Transcriptlerden öğrenilen detay:**  
Webwright, browser automation için daha hızlı ve token-efficient yaklaşım olarak anlatıldı. Agent sayfayı pixel olarak değil, page element/tree yapısı üzerinden anlayabilir.

**MTC faydası:**

- Local dashboard E2E testleri.
- Strategy Detail Page açılıyor mu?
- Registry filtreleri çalışıyor mu?
- Missing Metadata paneli görünüyor mu?
- Console error var mı?

**Önerilen aksiyon:**  
Sadece local dashboard için:

```text
http://localhost:xxxx
```

**Yasak:**

```text
Binance / broker / TradingView live account üzerinde kullanma.
Gerçek emir, alert, credential formu, canlı işlem yok.
```

**İlave araştırma:**  
Önce Playwright tek başına yeterli mi değerlendirilmeli.

---

# Grup C — Pattern olarak pilot yapılacaklar

Bu araçların mantığı değerli; ama doğrudan kurmak yerine MTC'ye özel uygulanmalı.

---

## C1. Grill-Me-Codex

**Repo / kaynak:**  
- https://github.com/chaseai-yt/grill-me-codex  
- Video: https://youtu.be/ENCRw5-uJBA?si=X2m2AAPAMpg5hoBo

**Karar:** Pattern olarak pilot.

**Ne işe yarar:**  
Claude önce kullanıcıyla planı netleştirir, `PLAN.md` oluşturur, Codex `PLAN-REVIEW-LOG.md` içinde read-only adversarial review yapar, Claude planı revize eder.

**Transcriptlerden öğrenilen detay:**  
Demo'da Codex ilk roundda 11 issue buldu, sonraki roundlarda sayı azaldı ve üçüncü roundda approve verdi. Ayrıca false fix'leri de yakaladı.

**MTC faydası:**

- High-risk planlarda ikinci göz.
- Plan audit trail.
- Schema/API/security/backtest risklerini koddan önce bulma.

**Önerilen aksiyon:**  
Doğrudan kurma. MTC versiyonunu oluştur:

```text
00_PLANS/active/PLAN.md
00_PLANS/active/PLAN-REVIEW-LOG.md
```

Default:

```text
max review rounds = 3
critical architecture work = 5 allowed
```

**İlave araştırma:**  
Repo çok genç görünüyor. Kopyalamadan önce içeriği incelenmeli.

---

## C2. Compound Engineering Plugin

**Repo / kaynak:**  
- https://github.com/everyinc/compound-engineering-plugin

**Karar:** Pattern olarak incele, komple kurma.

**Ne işe yarar:**  
Every Inc. tarafından hazırlanmış engineering skill/plugin seti. Git, debug, commit, frontend, project workflows gibi alanlarda kurallar içerir.

**Transcriptlerden öğrenilen detay:**  
Büyük skill paketleri başka insanların mühendislik tercihlerini agent context'ine sokar. Kör kurulum doğru değil; içindeki iyi fikirler seçilmeli.

**MTC faydası:**

- commit discipline fikirleri
- debug workflow fikirleri
- review process fikirleri
- frontend workflow fikirleri

**Önerilen aksiyon:**  
Skill dosyalarını oku, MTC'ye uygun olanları `CLAUDE.md` / `AGENTS.md` içine uyarlayarak ekle.

**İlave araştırma:**  
Hangi skill'ler gerçekten faydalı tek tek incelenmeli.

---

## C3. Stop-Slop / anti-AI writing rules

**Repo / kaynak:**  
- https://github.com/hardikpandya/stop-slop

**Karar:** Pattern olarak pilot, hazır haliyle kurma.

**Ne işe yarar:**  
AI yazılarındaki klişe kalıpları azaltmaya çalışır.

**Transcriptlerden öğrenilen detay:**  
Hazır kurallardan bazıları fazla kaba: tüm adverb'leri silmek, bazı soru cümlesi başlangıçlarını yasaklamak gibi. Bu metni bozabilir.

**MTC faydası:**

- daha iyi İngilizce promptlar
- daha temiz raporlar
- daha az “AI slop” doküman stili

**Önerilen aksiyon:**

```text
00_DOCS/AI_WORKFLOW/MTC_WRITING_STYLE.md
```

içinde MTC özel style guide oluştur.

Kurallar:

```text
clear
technical
no marketing hype
no fake certainty
preserve engineering detail
English prompts by default
```

**İlave araştırma:**  
Gerek yok; MTC'nin kendi yazım stili tanımlanmalı.

---

## C4. Cheaper sub-agent/model routing — DeepSeek / xAI / OpenRouter

**Kaynak:**  
- Kullanıcının mevcut MTC workflow notları  
- DeepSeek / xAI / OpenRouter API docs ileride doğrulanmalı

**Karar:** Hemen workflow'a entegre edilmeli, ama implementation repo incelendikten sonra.

**Ne işe yarar:**  
Claude/Codex'in bazı düşük riskli işleri daha ucuz modellere devretmesini sağlar.

**Mevcut problem:**  
Kullanıcıya göre repo içinde daha önce Claude/Codex'in DeepSeek/xAI'ya alt ajan gibi iş aktarması için workflow kurulmuştu; ancak kullanıcı hatırlatmazsa kullanılmıyor.

**MTC faydası:**

- token maliyeti düşer
- premium modeller high-value decision için saklanır
- büyük log summarization / research / audit pass işleri ucuz modele gider

**Önerilen aksiyon:**

```text
00_DOCS/AI_WORKFLOW/MODEL_ROUTING_POLICY.md
```

Otomatik karar kuralı:

```text
Use cheaper sub-agent/model for:
- large summarization
- broad research
- repeated audit passes
- long log summarization
- draft critique
- non-final classification

Do not use cheaper model for:
- final architecture decision
- registry/schema migration approval
- security-sensitive review
- live trading/broker logic
- final verdict without premium review
```

Bu politika şuralara referans olarak eklenmeli:

```text
CLAUDE.md
AGENTS.md
CODEX.md
_AI_MEMORY/GLOBAL_HANDOFF.md
_AI_MEMORY/NEXT_STEPS.md
```

**İlave araştırma:**  
Repo içinde mevcut DeepSeek/xAI/OpenRouter delegation scriptleri aranmalı. API key varsayılmamalı, secret basılmamalı.

---

# Grup D — Dashboard/UI için kontrollü pilotlar

Bu araçlar dashboard kalitesi için değerli olabilir; ancak data contract, registry veya backtest logic değiştirmemelidir.

---

## D1. Impeccable

**Repo / kaynak:**  
- https://github.com/pbakaus/impeccable

**Karar:** Kontrollü UI pilot.

**Ne işe yarar:**  
Frontend design skill. Typography, spacing, layout, motion, polish, live browser mode gibi komutlar içerir.

**Transcriptlerden öğrenilen detay:**  
Impeccable 23 command içeren tek skill olarak anlatıldı. Yeni live mode ile browser içinde frontend tasarım düzenleme yapılabiliyor.

**MTC faydası:**

- Strategy Detail Page daha okunur olur.
- Research Lab / Registry Browser / Backtest Results daha profesyonel görünür.
- “AI slop” dashboard görünümü azalır.

**Önerilen aksiyon:**

```text
feature/ui-impeccable-pilot
```

Sadece UI branch'te dene. API/data contract değiştirme.

**İlave araştırma:**  
Bir ekran üzerinde test edilmeli.

---

## D2. Design-Extract

**Repo / kaynak:**  
- https://github.com/Manavarya09/design-extract

**Karar:** Kontrollü UI pilot.

**Ne işe yarar:**  
Herhangi bir web sitesinden design system çıkarır: layout, responsiveness, component anatomy, brand voice, motion, interaction states.

**Transcriptlerden öğrenilen detay:**  
Awesome Design MD gibi sınırlı repo yerine herhangi bir siteyi headless browser ile analiz edip tasarım sistemi çıkarabiliyor.

**MTC faydası:**

- TradingView / Grafana / Linear / Vercel / Datadog gibi sistemlerden ilham alınabilir.
- Dashboard data-density ve UI düzeni iyileşir.

**Önerilen aksiyon:**

```text
design-extract → design reference markdown → Claude/Codex UI prompt
```

Kopyalama değil, ilham.

**İlave araştırma:**  
2–3 dashboard sitesinde test edilmeli.

---

## D3. Taste-Skill

**Repo / kaynak:**  
- https://github.com/leonxlnx/taste-skill

**Karar:** Kontrollü UI pilot.

**Ne işe yarar:**  
AI-generated frontend'in generic Claude görünümünü azaltmaya çalışan tasarım taste skill seti.

**Transcriptlerden öğrenilen detay:**  
Tasarım “taste” alanında başkasının fikirlerini denemek daha kabul edilebilir; çünkü beğenilmezse kolayca atılır. Ancak aynı tropelar tekrarlayabilir.

**MTC faydası:**

- Dashboard'a daha özgün görünüm.
- Strategy Detail / Research Lab sayfalarında daha iyi görsel hiyerarşi.

**Önerilen aksiyon:**

```text
feature/ui-taste-skill-pilot
```

Impeccable ile kıyasla.

**İlave araştırma:**  
Impeccable yeterli mi önce görülmeli.

---

## D4. Open-Design

**Repo / kaynak:**  
- https://github.com/nexu-io/open-design

**Karar:** İleride UI/prototype pilot.

**Ne işe yarar:**  
Local/open-source Claude Design benzeri prototip, slide deck, artifact, UI üretim ortamı.

**MTC faydası:**

- Dashboard prototipleri.
- Yönetim sunumu / slide deck mockup.
- UI konsept denemeleri.

**Neden şimdi değil:**  
MTC'nin şu an önceliği veri doğruluğu, registry/backtest workflow ve agent memory. UI/prototype aracı şu an core bottleneck değil.

**İlave araştırma:**  
Codex Desktop + Impeccable yeterli mi kıyaslanmalı.

---

# Grup E — Research/video input pilotları

---

## E1. Claude-Video

**Repo / kaynak:**  
- https://github.com/bradautomates/claude-video

**Karar:** Kontrollü pilot.

**Ne işe yarar:**  
Videodan frame çıkarır, audio transcript üretir, Claude'a video içeriğini görsel+metin olarak analiz ettirir.

**Transcriptlerden öğrenilen detay:**  
Claude doğrudan video ingest edemediği için araç ffmpeg ile kare çıkarıyor, Whisper/caption ile audio alıyor. Uzun videolarda frame budget seyrekleşiyor.

**MTC faydası:**

- Trading strateji videolarında sadece transcriptte olmayan ayarları yakalar.
- Grafik üstündeki SL/TP çizgileri, indicator settings, TradingView panel ayarlarını görselden çıkarabilir.
- YouTube strategy ingestion kalitesini artırır.

**Önerilen aksiyon:**

```text
03_QUANTLENS/tools/research_assist/video_review/
```

Pilot:

```text
same strategy video:
transcript-only analysis vs claude-video analysis
compare missing indicator/settings/rules
```

**İlave araştırma:**  
YouTube download/caption durumu, token maliyeti ve frame seçimi test edilmeli.

---

## E2. NotebookLM-py

**Repo / kaynak:**  
- https://github.com/teng-lin/notebooklm-py

**Karar:** DROPPED 2026-06-20 (Barış) — kullanılmayacak. Unofficial/undocumented API; Google değiştirince kırılır, bakım tuzağı. (Orijinal Codex kararı: kontrollü research pilot.)

**Ne işe yarar:**  
NotebookLM kaynak işleme özelliklerini CLI/API ile kullanmaya çalışır. YouTube, PDF, docs, slide gibi kaynakları işleyebilir.

**Transcriptlerden öğrenilen detay:**  
NotebookLM Google tarafında video ve doküman işleme için güçlü; ancak `notebooklm-py` unofficial/undocumented API kullanır, kırılabilir.

**MTC faydası:**

- YouTube strategy research offload.
- Büyük kaynak summarization.
- Research package oluşturma.

**Risk:**  
Unofficial API kırılabilir. Core pipeline bağımlılığı olamaz.

**İlave araştırma:**  
Kullanmadan önce repo/API güncelliği kontrol edilmeli.

---

# Grup F — Cost/token optimizasyon pilotları

---

## F1. Headroom

**Repo / kaynak:**  
- https://github.com/chopratejas/headroom

**Karar:** DROPPED 2026-06-20 (Barış) — kullanılmayacak. Agent↔LLM arasına MITM compression proxy (tüm prompt/repo içeriğini görür); gerçek tasarruf ~%5. Güvenlik/accuracy riski faydadan büyük. (Orijinal Codex kararı: kontrollü pilot.)

**Ne işe yarar:**  
Agent ile LLM arasına girip logs, JSON, tool output, repeated content gibi inputları sıkıştırır.

**Transcriptlerden öğrenilen detay:**  
Başlık %60–95 token tasarrufu iddia ediyor; fakat transcriptte median saving yaklaşık %4.8 olarak belirtildi. Yüksek tasarruf daha çok log-heavy debugging durumlarında olabilir.

**MTC faydası:**

- Büyük backtest log analizinde maliyet azaltma.
- Uzun JSON/tool outputlarını sıkıştırma.
- Claude/Codex'e daha temiz hata özeti verme.

**Önerilen aksiyon:**  
Sadece log/debug pilot:

```text
large backtest log → direct analysis
large backtest log → Headroom compressed analysis
compare cost + diagnosis accuracy
```

**Risk:**  
Agent ile LLM arasına proxy koymak güvenlik/accuracy riski getirir.

**İlave araştırma:**  
Security/privacy ve Claude/Codex uyumluluğu incelenmeli.

---

# Grup G — Repo anlama / codebase intelligence alternatifleri

---

## G1. Understand-Anything

**Repo / kaynak:**  
- https://github.com/Lum1104/Understand-Anything

**Karar:** Graphify ile A/B kontrollü pilot.

**Ne işe yarar:**  
Codebase'i interactive knowledge graph / visual intelligence formatına getirir.

**Transcriptlerden öğrenilen detay:**  
Büyük kod projelerini anlamak için görsel yapı çıkarıyor. Ancak transcriptte GitHub star kalitesi/şüpheli yıldız tartışması da geçti.

**MTC faydası:**

- MTC architecture visualization.
- Guided tour.
- Impact analysis.
- Business/domain view.

**Önerilen aksiyon:**  
Graphify varsa ikisini birden standart yapma. A/B test:

```text
- strategy metadata flow
- dashboard API dependencies
- registry schema impact
- MTC backtest architecture
```

Kazananı seç.

**İlave araştırma:**  
Repo olgunluğu ve output kalitesi kontrol edilmeli.

---

# Grup H — Memory / personal knowledge sistemleri

Bunlar MTC core için şimdilik bekletilmeli. MTC için önerilen ana bilgi sistemi `00_KNOWLEDGE_BASE` + `_AI_MEMORY` olmalı.

---

## H1. Supermemory

**Repo / kaynak:**  
- https://github.com/supermemoryai/supermemory

**Karar:** İleride değerlendir.

**Ne işe yarar:**  
Araçlar arası persistent memory service/API.

**MTC faydası:**  
Geniş cross-project memory için ileride faydalı olabilir.

**Neden beklet:**  
MTC'de explicit `_AI_MEMORY` ve `00_KNOWLEDGE_BASE` daha kontrollü. Ek memory service çakışma yaratabilir.

---

## H2. GBrain

**Repo / kaynak:**  
- https://github.com/garrytan/gbrain

**Karar:** İleride değerlendir.

**Ne işe yarar:**  
Kişiler, şirketler, timeline, meeting/email/voice gibi bilgileri organize eden AI brain.

**MTC faydası:**  
Çok sayıda müşteri/kişi/proje yönetimi için ileride faydalı olabilir.

**Neden beklet:**  
MTC'nin ihtiyacı şu an deterministic repo-local memory.

---

## H3. Claude-Obsidian

**Repo / kaynak:**  
- https://github.com/AgriciDaniel/claude-obsidian

**Karar:** Repo dışı research vault olarak ileride değerlendir.

**Ne işe yarar:**  
Claude ile Obsidian vault organize etme.

**MTC faydası:**  
Dış research vault için yararlı olabilir.

**Neden core'a alma:**  
MTC içinde `00_KNOWLEDGE_BASE` varken ikinci knowledge source karışıklık yaratır.

**Önerilen konum:**

```text
C:\LAB\MTC_RESEARCH_VAULT\
```

---

# Grup I — Şimdilik alma / MTC core'a entegre etme

Bu araçlar düşük alakalı, yüksek riskli veya MTC'nin ana hedefinden saptırıcıdır.

---

## I1. MoneyPrinterTurbo

**Repo / kaynak:**  
- https://github.com/harry0703/MoneyPrinterTurbo

**Karar:** Şimdilik alma.

**Neden:**  
AI short-video generator. MTC'nin strategy research/backtest/dashboard problemlerini çözmez. “AI slop” üretme riski yüksek.

**Ayrı kullanım:**  
MTC sonuçlarından tanıtım videosu üretmek istenirse repo dışı content project olarak düşünülebilir.

---

## I2. VoxCPM

**Repo / kaynak:**  
- https://github.com/OpenBMB/VoxCPM

**Karar:** Şimdilik alma.

**Neden:**  
Voice cloning / TTS. MTC core değeri yok.

**Etik/güvenlik:**  
Sadece kendi sesin veya açık izinli seslerle kullanılmalı. Başkasının sesini klonlama riski yüksek.

---

## I3. Career-Ops

**Repo / kaynak:**  
- https://github.com/santifer/career-ops  
- https://career-ops.org/

**Karar:** MTC'ye alma.

**Neden:**  
Job search command center. MTC ile doğrudan alakalı değil.

**Ayrı kullanım:**  
Kişisel kariyer projesi olarak ayrı klasörde değerlendirilebilir.

---

## I4. Odysseus

**Repo / kaynak:**  
- Transcriptte PewDiePie self-hosted AI workspace olarak geçti. Repo URL ayrı doğrulanmalı.

**Karar:** Şimdilik alma.

**Neden:**  
Self-hosted ChatGPT/AI workspace yapmak MTC için side quest. Öncelik değil.

---

## I5. ECC

**Repo / kaynak:**  
- https://github.com/affaan-m/ecc

**Karar:** Komple kurma.

**Neden:**  
Çok büyük agent/skill paketi. MTC özel kurallarını bastırabilir. Ne yaptığını okumadan context'e yüklemek riskli.

**Ayrı kullanım:**  
Sadece fikir almak için incelenebilir.

---

## I6. Higgsfield CLI / MCP

**Repo / kaynak:**  
- https://higgsfield.ai/mcp

**Karar:** Şimdilik alma.

**Neden:**  
Image/video generation. MTC core engineering'e katkısı düşük.

---

## I7. Open-Design core workflow olarak

**Repo / kaynak:**  
- https://github.com/nexu-io/open-design

**Karar:** Core workflow'a alma.

**Neden:**  
Prototip için ilginç ama MTC'nin şu anki bottleneck'i görsel artifact değil.

---

# 2. Uygulama fazları

## Phase 1 — Durable instructions and memory

```text
CLAUDE.md
AGENTS.md
CODEX.md
00_DOCS/AI_WORKFLOW/
_AI_MEMORY/
```

Eklenecekler:

```text
MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md
CODEX_CLAUDE_WORKFLOW.md
CODEX_REVIEW_PROMPTS.md
MTC_GRILL_PLAN_WORKFLOW.md
MODEL_ROUTING_POLICY.md
COST_OBSERVABILITY.md
DOCUMENT_INGESTION_POLICY.md
```

---

## Phase 2 — Knowledge Base

```text
00_KNOWLEDGE_BASE/
  CLAUDE.md
  raw/ai_tools/
  wiki/
  outputs/
  CHANGELOG.md
  INGESTION_REGISTRY.md
```

İlk wiki dosyaları:

```text
wiki/ai_tool_decision_matrix.md
wiki/mtc_agent_workflow.md
wiki/document_ingestion_workflow.md
wiki/codebase_mapping_workflow.md
wiki/cost_optimization_workflow.md
wiki/dashboard_ui_tooling.md
wiki/backtest_monitoring_workflow.md
```

---

## Phase 3 — Immediate local tools

Sırayla:

```text
1. Graphify
2. MarkItDown
3. LiteParse
4. CodeBurn
5. Caveman Light
6. Codex review workflow
7. MTC Grill Plan workflow
```

---

## Phase 4 — Controlled pilots

```text
Headroom
Claude-Video
Impeccable
Design-Extract
Taste-Skill
Understand-Anything
Webwright
NotebookLM-py
```

---

## Phase 5 — Side-service automation

```text
n8n MCP / watchdog
Telegram/email notifications
Backtest log monitor
Report sender
```

---

# 3. İlave araştırma checklist'i

Her tool kurulmadan önce kontrol et:

```text
[ ] repo maintained mi?
[ ] license uygun mu?
[ ] Windows uyumlu mu?
[ ] Python/Node version requirement ne?
[ ] local mi API mi kullanıyor?
[ ] secrets/privacy riski var mı?
[ ] output dosyaları çok büyük mü?
[ ] git noise yaratıyor mu?
[ ] file modify ediyor mu?
[ ] read-only kullanılabiliyor mu?
[ ] MTC mevcut workflow ile çakışıyor mu?
```

Özel araştırma gerekenler:

```text
[ ] Current Graphify CLI syntax and Windows behavior
[ ] CodeBurn provider pricing accuracy
[ ] MarkItDown vs LiteParse on real MTC PDFs
[ ] Headroom security and real savings on MTC logs
[ ] Codex plugin current setup
[ ] n8n MCP + Telegram route
[ ] Existing DeepSeek/xAI/OpenRouter delegation implementation
[ ] Understand-Anything vs Graphify A/B quality
[ ] NotebookLM-py API stability
```

---

# 4. Claude Code Prompt — place this roadmap into the repo and integrate memory/workflow

Copy the following prompt into Claude Code while opened at the MTC Command Center repository root.

```text
You are working inside the MTC Command Center repository.

Goal:
Integrate the AI tools and workflows master backlog into the repository as a durable implementation roadmap, then update the repo's AI memory and agent workflow instructions so future Claude/Codex/other LLM sessions can discover, remember, and execute the roadmap without the user having to repeat it.

Critical user intent:
The user has reviewed many AI tool transcripts and wants the useful tools integrated into MTC in the correct order. The user does not want these decisions to disappear into chat history. The repo must remember them. Future LLMs should be able to find the roadmap by reading the appropriate `_AI_MEMORY` and workflow files.

Important constraints:
- Do not modify MTC_V2.pine unless explicitly required. It should not be required for this task.
- Do not change production backtest behavior.
- Do not change registry schemas.
- Do not install tools yet unless the user explicitly approves installation.
- Do not run destructive commands.
- Do not expose or read secrets, .env files, broker credentials, or API keys.
- Prefer documentation, plans, workflow files, and memory updates only.
- Preserve existing repo structure. Do not invent a parallel architecture if one already exists.
- If a similar document/folder already exists, update it instead of duplicating it.
- All prompts and workflow instructions must be written in English.

Source artifact:
The user will provide a Markdown file named:
`MTC_AI_Tools_Master_Integration_Backlog_and_Claude_Prompt.md`

Part 1 — Inspect repository:
1. Read the repo root.
2. Locate existing project instruction files:
   - CLAUDE.md
   - AGENTS.md
   - CODEX.md
   - README files
3. Locate `_AI_MEMORY` and inspect:
   - GLOBAL_HANDOFF.md
   - NEXT_STEPS.md
   - ACTIVE_FILES.md
   - SESSION_LOG.md
   - any other memory/planning files
4. Locate existing docs/plans folders:
   - 00_DOCS
   - docs
   - 00_PLANS
   - 09_TOOLS
   - 09_AUTOMATION
   - any current knowledge base or tool backlog folder

Part 2 — Place the master backlog:
1. Choose the best repo location for the master Markdown file.
2. Preferred location if available:
   `00_DOCS/AI_WORKFLOW/MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md`
3. If `00_DOCS/AI_WORKFLOW/` does not exist, create it.
4. Also copy or reference it from:
   `00_KNOWLEDGE_BASE/raw/ai_tools/`
   if the repo has or should have a knowledge base.
5. Do not create duplicate conflicting files. If an equivalent file exists, merge carefully.

Part 3 — Create / update the MTC Knowledge Base plan:
1. If `00_KNOWLEDGE_BASE/` does not exist, create a lightweight scaffold:
   - `00_KNOWLEDGE_BASE/CLAUDE.md`
   - `00_KNOWLEDGE_BASE/raw/`
   - `00_KNOWLEDGE_BASE/wiki/`
   - `00_KNOWLEDGE_BASE/outputs/`
   - `00_KNOWLEDGE_BASE/CHANGELOG.md`
   - `00_KNOWLEDGE_BASE/INGESTION_REGISTRY.md`
2. Put the master backlog under:
   `00_KNOWLEDGE_BASE/raw/ai_tools/`
3. Create or update:
   `00_KNOWLEDGE_BASE/wiki/ai_tool_decision_matrix.md`
   summarizing:
   - Immediate Integration
   - Side-Service Integration
   - Pattern Pilots
   - Controlled Pilots
   - Later / Watchlist
   - Do Not Integrate
4. The wiki must clearly say:
   `_AI_MEMORY` is operational memory.
   `00_KNOWLEDGE_BASE` is research/architecture/tool-decision memory.
   They must not conflict.

Part 4 — Update `_AI_MEMORY` so future LLMs can find this:
Update whichever `_AI_MEMORY` files exist and are appropriate. At minimum:
1. `GLOBAL_HANDOFF.md`
   Add a durable note:
   - AI tools master backlog exists
   - where it is located
   - what it is for
   - which tools are immediate priorities
2. `NEXT_STEPS.md`
   Add a clearly titled section:
   `AI Tool Integration Roadmap`
   with actionable phases:
   - Phase 1: docs/instructions/memory
   - Phase 2: knowledge base
   - Phase 3: immediate tools
   - Phase 4: pilots
   - Phase 5: side-service automation
3. `ACTIVE_FILES.md`
   Add the files created/updated in this task.
4. `SESSION_LOG.md`
   Add a dated entry summarizing this work.

If different memory files are used in this repo, adapt to the existing convention and report exactly what was updated.

Part 5 — Update agent workflow instructions:
Update `CLAUDE.md`, `AGENTS.md`, and `CODEX.md` if they exist. If one is missing, create it only if it fits repo convention.

Add a section:
`AI Tool Integration and Model Routing Policy`

This section must say:
1. Before major AI workflow/tooling work, read:
   - `00_DOCS/AI_WORKFLOW/MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md`
   - `_AI_MEMORY/GLOBAL_HANDOFF.md`
   - `_AI_MEMORY/NEXT_STEPS.md`
2. Do not install or integrate new AI tools blindly.
3. Follow the decision labels in the master backlog.
4. Use Codex as read-only reviewer for high-risk plans/diffs.
5. Use MTC Grill Plan before architecture/schema/backtest/dashboard contract changes.
6. Use Graphify for repo architecture discovery once available.
7. Use MarkItDown/LiteParse for document ingestion once available.
8. Use CodeBurn for cost observability once available.
9. Use Caveman Light only for concise progress/audit summaries, not for final detailed technical reports.
10. Use n8n/watchdog as side-service for long backtest monitoring.
11. Do not use Do-Not-Integrate tools in core MTC workflow.
12. Do not let external skills override MTC-specific rules.

Part 6 — Make cheaper sub-agent/model routing automatic:
The user says a previous workflow existed for delegating cheaper tasks to DeepSeek/xAI via Claude/Codex, but agents forget to use it unless reminded. Fix this as a durable policy.

1. Search the repo for existing DeepSeek, xAI, OpenRouter, model routing, sub-agent, delegation, or cost-saving workflow files.
2. Do not assume API keys exist.
3. Do not print secrets.
4. Create or update:
   `00_DOCS/AI_WORKFLOW/MODEL_ROUTING_POLICY.md`
5. The policy must define when to use cheaper models automatically:
   - large summarization
   - broad research
   - repeated audit passes
   - long log summarization
   - draft critique
   - non-final classification
6. The policy must define when NOT to use cheaper models:
   - final architecture decisions
   - registry/schema migration approval
   - security-sensitive review
   - live trading/broker logic
   - final user-facing verdicts without premium review
7. Add references to this policy in:
   - `CLAUDE.md`
   - `AGENTS.md`
   - `CODEX.md`
   - `_AI_MEMORY/NEXT_STEPS.md`
   - `_AI_MEMORY/GLOBAL_HANDOFF.md`
8. If there is an existing script/config for delegation, document exactly how future agents should invoke it.
9. If no working implementation exists, create a TODO with exact investigation steps, not fake implementation.

Part 7 — Create implementation plan for tools:
Create:
`00_DOCS/AI_WORKFLOW/AI_TOOL_IMPLEMENTATION_PLAN.md`

It must include:

Phase 1 — Immediate docs/workflow:
- CLAUDE.md / AGENTS.md / CODEX.md
- MTC Grill Plan
- Codex review prompts
- Knowledge base
- Model routing policy

Phase 2 — Immediate local tools:
- Graphify
- MarkItDown
- LiteParse
- CodeBurn
- Caveman Light

Phase 3 — Research and UI pilots:
- Claude-Video
- Impeccable
- Design-Extract
- Taste-Skill
- Headroom
- Understand-Anything
- NotebookLM-py

Phase 4 — Side-service automation:
- n8n MCP / watchdog
- Webwright or browser test pilot

Phase 5 — Watchlist / rejected:
- Supermemory
- GBrain
- Claude-Obsidian
- MoneyPrinterTurbo
- VoxCPM
- Career-Ops
- Odysseus
- ECC
- Higgsfield

For each tool:
- repo URL
- decision
- expected benefit
- risk
- next action
- acceptance criteria

Part 8 — Verification:
After changes, provide:
1. Files created/updated.
2. Where the master backlog was placed.
3. Which `_AI_MEMORY` files were updated.
4. Whether any existing conventions were found and followed.
5. Any unresolved questions.
6. Exact next command/prompt the user should run to start Phase 1.
7. Confirm no code/backtest/schema/live trading logic was modified.

Do not install any tool yet.
Do not implement actual integrations yet.
This task is documentation, memory, and workflow integration only.
```

---

# 5. Future retrieval query

Future user query:

```text
What AI tools should we add to MTC next, and what is the approved roadmap?
```

Future agent should answer by reading:

```text
_AI_MEMORY/GLOBAL_HANDOFF.md
_AI_MEMORY/NEXT_STEPS.md
00_DOCS/AI_WORKFLOW/MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md
00_DOCS/AI_WORKFLOW/AI_TOOL_IMPLEMENTATION_PLAN.md
00_DOCS/AI_WORKFLOW/MODEL_ROUTING_POLICY.md
00_KNOWLEDGE_BASE/wiki/ai_tool_decision_matrix.md
```
