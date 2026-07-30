# solak-design-ui v0.2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `solak-design-ui` skill'ini genel tasarım öğüdünden veri-yoğun kurumsal UI uzmanlığına (tablo, filtre, form, dashboard) taşımak; `frontend-design` ve global `web/design-quality.md` ile olan tekrarı ortadan kaldırmak.

**Architecture:** İnce `SKILL.md` (~90 satır) ortak temeli ve yönlendirmeyi taşır; yüzeye özel bilgi `references/` altında beş dosyaya ayrılır. Model çalışma anında yalnızca ilgili yüzeyin referansını okur. Global kurallarda ve `dataviz` skill'inde zaten yazan bilgi tekrar edilmez, işaret edilir.

**Tech Stack:** Markdown + YAML frontmatter. Doğrulama: PowerShell 7 (`ConvertFrom-Json`, `Select-String`, `Measure-Object`). Referans içindeki kod örnekleri teknoloji-bağımsız: semantik HTML + CSS custom property.

**Spec:** `docs/specs/2026-07-30-solak-design-ui-design.md`

**Çalışma dizini:** `C:\Users\CagriSolakoglu\solak-skills` — tüm yollar bu köke göredir.

**Sıra neden bu:** referanslar önce yazılır, `SKILL.md` sonra — çünkü `SKILL.md` bu dosyalara isimle atıf yapar ve var olmayan dosyaya atıf yapan bir skill kırıktır.

---

### Task 1: Yoğunluk ve yön referansı

Yoğunluk ölçeği bu skill'in çekirdek kararı; diğer dört referans buna atıf yapar, o yüzden ilk.

**Files:**
- Create: `skills/solak-design-ui/references/density-and-direction.md`
- Delete: `skills/solak-design-ui/references/style-directions.md`

- [ ] **Step 1: Yoğunluk ölçeğini yaz**

`references/density-and-direction.md` dosyasını oluştur, şu içerikle başla:

```markdown
# Yoğunluk ve Yön

Veri-yoğun UI'da **yoğunluk kararı yön seçiminden daha belirleyicidir.** Aynı tablo
`comfortable` ile `dense` arasında farklı bir üründür. Bu kararı önce ver.

## Yoğunluk ölçeği

| Seviye | Satır/alan yüksekliği | Gövde metni | Ne zaman |
|--------|----------------------|-------------|----------|
| `comfortable` | 44px | 15-16px | < 20 kayıt, okuma odaklı, dokunmatik kullanım |
| `compact` | 36px | 14px | 20-100 kayıt, karışık kullanım (varsayılan) |
| `dense` | 28px | 13px + `tabular-nums` | 100+ kayıt, tarama ve karşılaştırma odaklı |

```css
:root {
  /* compact — varsayılan */
  --row-height: 36px;
  --row-padding-x: 12px;
  --text-body: 0.875rem;
  --table-border: 1px solid oklch(88% 0 0);
}

[data-density="comfortable"] { --row-height: 44px; --row-padding-x: 16px; --text-body: 0.9375rem; }
[data-density="dense"]       { --row-height: 28px; --row-padding-x: 8px;  --text-body: 0.8125rem; }
```

## Seviye nasıl seçilir

Üç soru:

1. **Kaç kayıt gösterilecek?** Tipik durumda, en kötü durumda.
2. **Kullanıcı tarıyor mu, okuyor mu?** Tarama (bir değeri bulmak, karşılaştırmak) yoğunluğu artırır; okuma azaltır.
3. **Hangi ekran ve girdi?** Dokunmatik veya sahada kullanım en az `comfortable` gerektirir (dokunma hedefi ≥ 44px).

Cevaplar bilinmiyorsa **sor.** Varsayılana kaçmak bu skill'in engellemek için var olduğu şey.

## Temel ilke: yoğunluk sıkıştırma değildir

Satır yüksekliği düşerken şunlar **artmak** zorunda:

- Hizalama disiplini — `dense`'te göz kaymasını önleyen tek şey sütun hizası
- Ayırıcı netliği — yükseklik azaldıkça satırları ayıran ipucu güçlenmeli
- Sayı okunurluğu — `tabular-nums` `dense`'te zorunlu, opsiyonel değil

Sadece padding kısıp font küçültmek yoğunluk değil, okunmazlıktır.

## Üç yön

| Yön | Ne zaman | Tipografi | Renk | Kompozisyon |
|-----|----------|-----------|------|-------------|
| **Swiss / International** (varsayılan) | Operasyonel ekran: tablo, filtre, form | Tek grotesk aile, ağırlıkla hiyerarşi | Nötr + tek işlevsel accent + semantik durum renkleri | Katı kolon grid, sola hizalı |
| **Editorial-dense** | Rapor, analiz, anlatı taşıyan ekran | Serif başlık + grotesk gövde/veri | Kağıt yüzey, koyu mürekkep, tek accent | Asimetrik: anlatı kolonu + veri bloğu |
| **Bento** | Metrik özeti, dashboard | Kompakt, sayı odaklı, tabular figür | Nötr yüzey + semantik eşik renkleri | **Eşit olmayan** hücreler (2x1, 1x2, 2x2) |

Yönü kullanıcıya **onaylat**; geri alınması pahalı karardır. Karanlık tema varsayılan değildir.
```

- [ ] **Step 2: Eski yön dosyasını sil**

Bu dosyanın sekiz stil yönünden hiçbiri (retro-futurism, glassmorphism, neo-brutalism…) kurumsal veri ekranında kullanılmayacak. Kullanılabilir kısmı Step 1'e taşındı.

```powershell
Remove-Item skills\solak-design-ui\references\style-directions.md
```

- [ ] **Step 3: Doğrula**

Run:
```powershell
Test-Path skills\solak-design-ui\references\style-directions.md
Test-Path skills\solak-design-ui\references\density-and-direction.md
```
Expected: `False` sonra `True`

- [ ] **Step 4: Commit**

```bash
git add skills/solak-design-ui/references/
git commit -m "feat: replace style-directions with density-and-direction reference"
```

---

### Task 2: Tablo referansı

**Files:**
- Create: `skills/solak-design-ui/references/tables.md`

- [ ] **Step 1: Dosyayı yaz**

```markdown
# Tablo / Veri Grid'i

Yoğunluk kararı için önce `density-and-direction.md`.

## Hizalama tipe göre

| Veri tipi | Hizalama | Not |
|-----------|----------|-----|
| Metin, etiket | Sola | — |
| Sayı, para, yüzde | **Sağa** + `font-variant-numeric: tabular-nums` | Basamaklar dikey hizalanır, karşılaştırma mümkün olur |
| Tarih, saat | Sola, sabit genişlik | Format tutarlı: tek satırda karışık format yok |
| Durum, etiket (badge) | Sola | Renk **tek gösterge olamaz** — metin veya ikon eşlik eder |
| Eylem | Sağa, en sağ kolon | Sıralanamaz, sticky olabilir |

```css
.cell-numeric {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
```

Sayıyı sola hizalamak veya proportional font kullanmak, tablonun tek işini (karşılaştırma) bozar.

## Kolon önceliği ve daralma

Kolonları üç önceliğe ayır: **kimlik** (hangi kayıt), **karar** (kullanıcının aradığı değer), **detay** (gerisi).

Ekran daraldığında **kolonu sıkıştırmak yasak.** Üç meşru strateji:

1. **Gizle** — detay kolonlarını kaldır, satır genişletmeyle erişilebilir kıl
2. **Katla** — kimlik + karar kolonlarını iki satırlı tek hücreye topla (mobil kart görünümü)
3. **Yatay kaydır** — kimlik kolonu sticky, gerisi kayar

Hangisi seçildiyse **çıktı raporunda açıkça beyan et.** Beyan edilmemiş daralma davranışı, doğrulama kapısını geçmez.

## Sticky

- Başlık satırı: `position: sticky; top: 0` — 15+ satırda zorunlu
- Kimlik kolonu: yatay kaydırma varsa `position: sticky; left: 0` zorunlu
- Sticky yüzeyin arkası **opak** olmalı; yarı saydam başlık altındaki metni okunmaz yapar

## Tek ayırıcı sistemi

Zebra şeritleri **veya** yatay çizgiler — ikisi birden değil. İkisi birlikte gürültü üretir ve hiçbiri işini yapmaz.

- Zebra: `dense` seviyede, çok kolonlu tabloda göz kaymasını engeller
- Çizgi: `comfortable`/`compact` seviyede daha temiz
- Dikey çizgi: yalnızca kolon grupları varsa

## Taşan hücre

Uzun metin: tek satırda kısalt (`text-overflow: ellipsis`) **ve** tam değeri erişilebilir kıl — `title` özniteliği veya tooltip. Kısaltıp tam değeri hiç göstermemek veri kaybıdır.

Satır yüksekliğini içeriğe göre büyütmek `dense`/`compact` seviyede tarama ritmini bozar; sabit yükseklik + kısaltma tercih edilir.

## Sıralama ve seçim

- Sıralanabilir başlık: hover'da göstergeyi belli et, aktif sıralamada yön oku **ve** hangi kolon olduğu görünür kalsın
- Seçim: satır tıklaması ile checkbox seçimi **çakışmasın** — tıklama detaya gidiyorsa checkbox ayrı hedef olmalı
- Toplu seçimde kaç kayıt seçildiği ve "tümünü seç" kapsamı (sayfa mı, tüm sonuç mu) açıkça yazılmalı

## Toplam satırı

Varsa `position: sticky; bottom: 0`, gövdeden farklı ağırlıkta, sayı hizası gövdeyle **birebir aynı**.

## Durumlar — hepsi tasarlanacak

| Durum | Tasarım |
|-------|---------|
| İlk kullanım (hiç veri yok) | Ne olduğunu açıkla + ilk eylemi öner. "Kayıt yok" yetersiz. |
| Sonuç yok (filtre sonucu) | **İlk kullanımdan ayrı.** Hangi filtrenin gevşetileceğini öner. |
| Yükleniyor | İskelet satırlar, yüksekliği gerçek satırla **aynı** — yoksa layout shift |
| Kısmi yükleme | Yüklenmiş satırlar görünür, devamı için gösterge |
| Hata | Ne olduğu + tekrar dene eylemi; tabloyu boşaltıp tek satır hata yazma |
| Tek satır | Tablo yerine detay görünümü daha uygun olabilir — sorgula |

İlk kullanım ile "sonuç yok" durumunu aynı bileşenle çözmek en sık yapılan hatadır; kullanıcı sistemin boş mu olduğunu yoksa filtresinin mi kötü olduğunu anlayamaz.

## Erişilebilirlik

- `<table>` + `<th scope="col">` kullan; `div` grid'i ancak sanallaştırma zorunluysa ve `role="grid"` ile
- Klavye: `Tab` ile eylemlere, sıralanabilir başlıklar `button` olmalı
- Sanallaştırılmış tabloda toplam satır sayısını ekran okuyucuya bildir
```

- [ ] **Step 2: Doğrula**

Run:
```powershell
(Get-Content skills\solak-design-ui\references\tables.md | Measure-Object -Line).Lines
Select-String -Path skills\solak-design-ui\references\tables.md -Pattern 'TBD|TODO|<\.\.\.>'
```
Expected: satır sayısı yazılır; `Select-String` **hiçbir şey döndürmez**

- [ ] **Step 3: Commit**

```bash
git add skills/solak-design-ui/references/tables.md
git commit -m "feat: add tables reference for solak-design-ui"
```

---

### Task 3: Filtre referansı

**Files:**
- Create: `skills/solak-design-ui/references/filters.md`

- [ ] **Step 1: Dosyayı yaz**

```markdown
# Filtre / Arama / Sorgu Paneli

## Aktif filtre tek doğruluk kaynağı

Kullanıcı **her an** neyin uygulandığını görmeli. Uygulanmış filtreler, panel kapalıyken de görünen chip'ler olarak listelenir; her chip tek tek kaldırılabilir.

Panelin içine gömülü, kapatınca kaybolan filtre durumu en sık yapılan hatadır: kullanıcı eksik veriye bakıp doğru sanır.

```html
<div class="applied-filters" aria-live="polite">
  <span class="filter-chip">
    Tesis: Ankara-2
    <button type="button" aria-label="Tesis filtresini kaldır">×</button>
  </span>
  <button type="button" class="filter-clear">Tümünü temizle</button>
</div>
```

`aria-live="polite"` önemli: filtre değişimi ekran okuyucuya bildirilmeli.

## Durum URL'de

Filtre, sıralama, sayfa ve arama sorgusu URL'e yazılır. Kazandırdığı üç şey: ekran paylaşılabilir, geri tuşu beklendiği gibi çalışır, yenilemede durum kaybolmaz.

Filtre durumunu yalnızca bileşen state'inde tutmak bu üçünü de kaybettirir.

## Filtre ile arama ayrı işlerdir

- **Arama**: serbest metin, birden çok alanda eşleşir, yazarken sonuç daralır
- **Filtre**: bilinen alanda bilinen değer kümesi, kasıtlı seçim

İkisini tek girdiye bindirmek ikisini de belirsizleştirir. Her ikisi de gerekiyorsa görsel olarak ayır.

## Sonuç sayısı geri bildirimi

Uygulanan filtrenin etkisi **sayıyla** görünür: "1.284 kayıt · 3 filtre aktif". Mümkünse filtre uygulanmadan önce tahmini sayıyı göster — kullanıcı sonucu boş bir listede keşfetmesin.

## Pahalı filtre

Sunucuya giden veya yavaş filtrede:

- Yazma girdisinde debounce (250-400ms), her tuş vuruşunda sorgu yok
- **Beklemede olduğunu göster** — mevcut sonucu soluklaştır, iskelete dönme
- Eski sonucu ekranda tutup yeni sonuç gelince değiştir (stale-while-revalidate); boşaltıp bekletme

## "Sonuç yok" durumu — çıkmaz sokak bırakma

Sonuç boşsa **hangi filtrenin sorumlu olduğunu** söyle ve bir çıkış yolu ver:

> Bu kriterlerle kayıt bulunamadı. **Tarih aralığı** (son 7 gün) en çok daraltan filtre — genişletmeyi dene.
> [Tarihi son 30 güne genişlet] [Tüm filtreleri temizle]

Kullanıcıyı hangi filtreyi kaldıracağını tahmin etmeye bırakmak, en sık terk noktasıdır.

## Sıfırlama ve kayıtlı görünüm

- "Tümünü temizle" her zaman erişilebilir, tek eylem
- Tekrar eden sorgular varsa kayıtlı görünüm: adlandırılır, paylaşılabilir (URL zaten durumu taşıyor)
- Varsayılan görünüm açıkça belirtilir — kullanıcı "temiz duruma" nasıl döneceğini bilmeli

## Erişilebilirlik

- Filtre grubu `fieldset` + `legend`
- Chip kaldırma butonu `aria-label` ile hangi filtreyi kaldırdığını söyler
- Sonuç sayısı `aria-live` bölgesinde
- Panel açılır-kapanırsa `aria-expanded` ve odak yönetimi
```

- [ ] **Step 2: Doğrula**

Run:
```powershell
Select-String -Path skills\solak-design-ui\references\filters.md -Pattern 'TBD|TODO|<\.\.\.>'
```
Expected: hiçbir çıktı yok

- [ ] **Step 3: Commit**

```bash
git add skills/solak-design-ui/references/filters.md
git commit -m "feat: add filters reference for solak-design-ui"
```

---

### Task 4: Form referansı

**Files:**
- Create: `skills/solak-design-ui/references/forms.md`

- [ ] **Step 1: Dosyayı yaz**

```markdown
# Veri Giriş Formu

## Gruplama ve ritim

Alanları anlamsal gruplara ayır (`fieldset` + `legend`); grup arası boşluk alan arası boşluğun **en az iki katı**. Tek tip aralık, uzun formu okunmaz bir liste yapar.

```css
.form-field  { margin-block-end: var(--space-field);  }  /* 16px */
.form-group  { margin-block-end: var(--space-group);  }  /* 40px */
```

## Etiket üstte

Etiket alanın üstünde, sola hizalı. Tarama hızı en yüksek yerleşim budur ve uzun etiketlerde bozulmaz.

Sol yerleşim (etiket solda, alan sağda) kolon genişliğini etikete esir eder; yer içi (placeholder) etiket ise **etiket değildir** — odaklanınca kaybolur, kullanıcı ne girdiğini doğrulayamaz.

## Zorunluluk işaretlemesi

**Alanların çoğu zorunluysa, isteğe bağlı olanı işaretle** — tersi değil. Her alanın yanında yıldız görmek hiçbir bilgi taşımaz.

```html
<label for="note">Not <span class="field-optional">(isteğe bağlı)</span></label>
```

## Doğrulama zamanlaması

- `blur`'da doğrula — her tuş vuruşunda değil. Yazarken hata göstermek kullanıcıyı cümlesinin ortasında suçlar.
- Bir alan hatalıysa ve kullanıcı düzeltiyorsa, doğru hale geldiği anda hatayı kaldır (bu durumda anlık geri bildirim doğru).
- Gönderimde tüm hataları göster, ilk hataya odaklan.

## Hata mesajı

Alanın **altında**, alana `aria-describedby` ile bağlı, ne yapılacağını söyleyen tonda.

| ❌ | ✅ |
|----|-----|
| "Geçersiz değer" | "Tarih GG.AA.YYYY biçiminde olmalı" |
| "Hata: alan zorunlu" | "Tesis seçilmeli" |
| "Format hatalı" | "Vergi numarası 10 haneli olmalı — şu an 9 hane" |

```html
<input id="tax" aria-describedby="tax-error" aria-invalid="true">
<p id="tax-error" class="field-error">Vergi numarası 10 haneli olmalı — şu an 9 hane.</p>
```

Uzun formda ayrıca üstte özet blok: kaç hata var, her biri ilgili alana bağlantı.

## disabled ile read-only ayrımı

| Durum | Ne demek | Görsel |
|-------|----------|--------|
| `disabled` | Şu an değiştirilemez, **neden'i belirtilmeli** | Soluk, odaklanılamaz |
| `readonly` | Değer bilgi olarak var, değiştirilemez | Normal kontrast, odaklanılabilir, kopyalanabilir |

Gösterilen bir değeri `disabled` yapmak okunmaz hale getirir — bilgi amaçlıysa `readonly` kullan. `disabled` bir alanın yanında neden kapalı olduğu yazılmalı ("Tesis seçilmeden birim seçilemez").

## Alan genişliği içerikle eşleşir

Posta kodu, vergi no, tutar gibi sabit uzunluklu alanlar **tam genişlik olmaz.** Genişlik beklenen karakter sayısını gösterir ve hata yapmayı azaltır.

```css
.field-postcode { inline-size: 8ch; }
.field-amount   { inline-size: 12ch; }
.field-name     { inline-size: 100%; max-inline-size: 40ch; }
```

## Eylem hiyerarşisi

- Birincil eylem (Kaydet) vurgulu ve tek
- İkincil (İptal) düşük vurgulu, birincilin yanında ama karışmayacak mesafede
- **Yıkıcı eylem (Sil) ayrı yerde**, birincilin yanında değil; onay ister
- Uzun formda kaydet butonu sticky olabilir; o zaman kaydedilmemiş değişiklik göstergesi de olmalı

## Otomatik kaydetme

Otomatik kaydediliyorsa **durumu göster** ("Kaydedildi · 14:32"). Sessiz otomatik kayıt, kullanıcının işinin kaybolduğunu düşünmesine yol açar. Açık kaydetme varsa, kaydedilmemiş değişiklikle sayfadan ayrılma uyarısı ver.

## Erişilebilirlik

- Her alan `label` ile `for`/`id` üzerinden bağlı
- Hata `aria-describedby` + `aria-invalid`
- Grup `fieldset`/`legend`
- Klavye ile baştan sona doldurulabilir; odak sırası görsel sırayla aynı
```

- [ ] **Step 2: Doğrula**

Run:
```powershell
Select-String -Path skills\solak-design-ui\references\forms.md -Pattern 'TBD|TODO|<\.\.\.>'
```
Expected: hiçbir çıktı yok

- [ ] **Step 3: Commit**

```bash
git add skills/solak-design-ui/references/forms.md
git commit -m "feat: add forms reference for solak-design-ui"
```

---

### Task 5: Dashboard referansı

**Files:**
- Create: `skills/solak-design-ui/references/dashboards.md`

- [ ] **Step 1: Dosyayı yaz**

```markdown
# Dashboard / Metrik Özeti

## Her tile tek bir soruyu cevaplar

Bir tile eklerken sorusunu yaz: "Bu ay hedefin ne kadar gerisindeyiz?" Soruyu yazamıyorsan tile'ı çıkar.

Aynı ağırlıkta on iki kutu hiyerarşi değil, envanterdir. Dashboard'un işi kullanıcının **bir sonraki eylemini** belirlemek.

## Eşit olmayan kompozisyon

Bento düzeni eşit hücrelerden oluşmaz — önem farkı boyut farkıyla görünür.

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-tile);
}
.tile--primary { grid-column: span 2; grid-row: span 2; }  /* ana metrik */
.tile--wide    { grid-column: span 2; }                    /* trend */
.tile--unit    { grid-column: span 1; }                    /* destek metrik */
```

Eşit grid bento değil, sadece grid'dir.

## KPI anatomisi

Dört parça, sırasıyla:

1. **Etiket** — ne ölçülüyor, birimiyle
2. **Değer** — en büyük ölçek, `tabular-nums`
3. **Değişim** — yön + miktar, **renk tek gösterge olamaz** (ok ikonu veya işaret eşlik eder)
4. **Bağlam** — neye göre: "geçen aya göre", "hedefin %8 altında"

```html
<article class="tile">
  <h3 class="tile-label">Aylık tüketim <span class="tile-unit">kWh</span></h3>
  <p class="tile-value">184.320</p>
  <p class="tile-delta tile-delta--up">
    <svg aria-hidden="true"><!-- yukarı ok --></svg>
    %12,4 <span class="tile-context">geçen aya göre</span>
  </p>
</article>
```

**Bağlamsız sayı bilgi değildir.** "184.320" tek başına kullanıcıya hiçbir karar vermez.

## Eşik renkleri semantik, ve renk tek gösterge olamaz

```css
:root {
  --status-ok:       oklch(62% 0.15 150);
  --status-warn:     oklch(72% 0.16  75);
  --status-critical: oklch(58% 0.20  25);
}
```

Her durum rengi bir **ikon veya metinle** eşlenir. Renk körlüğü bir yana, gri tonlamalı çıktıda ve düşük parlaklıkta ekranda renk kaybolur.

Ayrıca: bir metriğin "yukarı" gitmesi her zaman iyi değildir (maliyet, arıza sayısı). Yön ile iyi/kötü ayrımını karıştırma — artış yönünü ok, iyi/kötü durumunu renk taşır.

## Sparkline

- Eksen ve etiket yok; işi trendin şeklini göstermek
- Son değer noktayla işaretlenir
- Tek başına sayı yerine geçmez — her zaman değerle birlikte
- Yükseklik 24-40px; daha küçüğü şekli okunmaz yapar

## Grafik işi geldiğinde

Grafik tipi seçimi, kategorik/sıralı palet, eksen ve tooltip kuralları için **`dataviz` skill'ini kullan.** O bilgi burada tekrar edilmez.

## Durumlar

| Durum | Tasarım |
|-------|---------|
| Veri yok | Tile yapısı korunur, değer yerine "veri yok" + nedeni |
| Kısmi veri | Hangi dönemin eksik olduğu yazılır; eksik veriyi sıfır gibi gösterme |
| Yükleniyor | Tile boyutunda iskelet — layout shift olmaz |
| Bayat veri | Son güncelleme zamanı görünür; canlı sanılmasın |
| Hata | Tile içinde, tüm dashboard'u boşaltmadan |

Eksik veriyi sıfır olarak göstermek dashboard'larda en pahalı hatadır: yanlış karara yol açar.

## Düzen ve okuma sırası

- Sol üst en önemli metrik (soldan sağa okuma)
- İlgili metrikler komşu
- Dashboard bir ekrana sığmalı; kaydırma gerekiyorsa muhtemelen iki farklı dashboard var
- `320px`'te tek kolona iner, sıra önem sırasıyla aynı kalır
```

- [ ] **Step 2: Doğrula**

Run:
```powershell
Select-String -Path skills\solak-design-ui\references\dashboards.md -Pattern 'TBD|TODO|<\.\.\.>'
Select-String -Path skills\solak-design-ui\references\dashboards.md -Pattern 'dataviz'
```
Expected: ilk komut boş; ikinci komut `dataviz` devir satırını bulur

- [ ] **Step 3: Commit**

```bash
git add skills/solak-design-ui/references/dashboards.md
git commit -m "feat: add dashboards reference for solak-design-ui"
```

---

### Task 6: SKILL.md'yi yeniden yaz

Referanslar hazır olduğu için `SKILL.md` artık var olan dosyalara atıf yapabilir.

**Files:**
- Modify: `skills/solak-design-ui/SKILL.md` (tam yeniden yazım)

- [ ] **Step 1: Mevcut dosyayı oku**

Üzerine yazmadan önce oku — mevcut guardrail'lerin korunacak kısmı var.

```powershell
Get-Content skills\solak-design-ui\SKILL.md
```

- [ ] **Step 2: Frontmatter'ı değiştir**

`version` 0.1.0 → 0.2.0, `tags`'e iki etiket eklenir, `description` tamamen yenilenir:

```yaml
---
name: solak-design-ui
description: Designs and implements data-dense enterprise UI — tables and data grids, filter and query panels, data-entry forms, and metric dashboards. Decides row/field density deliberately, aligns numbers and text by type, designs the states real data produces (empty, loading, partial, error, overflow, too-many-results), and keeps everything on the project's token layer. Tech-agnostic: semantic HTML + CSS custom properties, adapted to the detected framework. Use when the user works on a table, grid, filter panel, form, report screen or dashboard — "tabloyu düzelt", "filtre paneli tasarla", "bu ekran kalabalık", "dashboard yap" — or invokes /solak-design-ui. For marketing pages, landing pages and brand surfaces, prefer `frontend-design`.
metadata:
  version: 0.2.0
  author: cagrisolakoglu
  tags: [design, frontend, ui, data-dense, enterprise]
  status: draft
---
```

Son cümle (`For marketing pages… prefer frontend-design`) **çıkarılamaz** — iki skill arasındaki seçim belirsizliğini bitiren şey odur.

- [ ] **Step 3: Gövdeyi yaz**

````markdown
# solak-design-ui

Veri-yoğun kurumsal yüzeyleri — tablo, filtre paneli, veri giriş formu, metrik dashboard — yoğunluğu ve durumları kasıtlı seçerek tasarlar ve kodlar.

## When to Use

- Tablo/veri grid'i tasarlanacak veya mevcut biri okunmuyor ("400 kayıt var, kalabalık")
- Filtre/sorgu paneli, veri giriş formu, rapor ekranı veya metrik dashboard işi
- Gerçek verinin ürettiği durumlar eksik: boş, yükleniyor, kısmi, hata, taşma, çok fazla sonuç

Bu skill'i **kullanma**:
- Pazarlama sayfası, landing page, marka yüzeyi → `frontend-design`
- Grafik tipi ve palet kararı → `dataviz`
- Tasarım sistemi/token katmanının sıfırdan kurulması → ayrı ve daha geniş iş
- Sorun görsel değil davranışsalsa (veri akışı, state, bug) → doğrudan kodu düzelt

## Inputs

| Girdi | Zorunlu | Açıklama |
|-------|---------|----------|
| hedef yüzey | ✅ | Hangi ekran/komponent. Dosya yolu veya sıfırdan tanım. |
| ürün bağlamı | ✅ | Ne işe yarıyor, kim kullanıyor. Yoksa **sor**. |
| veri hacmi ve kullanım | ✅ | Kaç kayıt (tipik/en kötü), kullanıcı tarıyor mu okuyor mu. Yoğunluk kararı buna bağlı; yoksa **sor**. |
| stil yönü | ❌ | Verilmezse 3 adaydan öner ve onay al. |
| teknoloji | ❌ | Repodan tespit et; edilemezse sor. |
| kısıt | ❌ | Mevcut token/palet, erişilebilirlik seviyesi, performans bütçesi. |

"Clean minimal", "modern", "şık" **yön değildir** — somut bir yöne çevirip onay al.

## Workflow

1. **Bağlamı oku** — Token katmanı, mevcut tablo/form kalıpları, tema desteği, framework tespiti (repodaki dosya uzantıları ve paket dosyası).
2. **Yüzeyi tespit et** — Hangi yüzey olduğunu belirle ve **yalnızca ilgili referansı oku**:
   - Tablo / veri grid'i → `references/tables.md`
   - Filtre / arama / sorgu paneli → `references/filters.md`
   - Veri giriş formu → `references/forms.md`
   - Dashboard / metrik özeti → `references/dashboards.md`
3. **Yoğunluğu karara bağla** — `references/density-and-direction.md`: `comfortable` / `compact` / `dense`. Karar üç sorudan çıkar (kayıt sayısı, tarama mı okuma mı, ekran ve girdi). Gerekçeyi çıktı raporunda yaz.
4. **Yön seç** — Aynı referanstan üç yön (Swiss / editorial-dense / bento). Tek cümleyle gerekçelendir ve **kullanıcıya onaylat**. Karanlık temayı varsayma.
5. **Token'ları kullan veya yaz** — Mevcut token katmanı varsa **onu kullan**, paralel sistem kurma. Yoksa palet, type scale, spacing, yoğunluk, duration/easing'i CSS custom property olarak tanımla.
6. **Kodla** — Semantik HTML (`table`/`th`/`fieldset`/`label`, generic `div` yığını değil). Yüzey referansındaki durumların **hepsi** ve etkileşim state'leri: hover, `focus-visible`, active, disabled/readonly, seçili.
7. **Motion (varsa)** — Yalnızca `transform`, `opacity`, `clip-path`. `prefers-reduced-motion` karşılığını yaz.
8. **Doğrula** — Aşağıdaki kapıları çalıştır, sonucu raporla. Mümkünse 320/768/1440 ekran görüntüsü al.

Anti-template kalıpları ve genel tasarım kalitesi nitelikleri için global `web/design-quality.md` kuralı geçerlidir; burada tekrar edilmez.

## Doğrulama kapıları

**Bloklayan** — biri geçilmezse iş **tamamlanmadı**, eksiği açıkça yaz:

- [ ] Metin kontrastı ≥ 4.5:1 (büyük metin ≥ 3:1); durum renkleri dahil
- [ ] Renk tek gösterge değil — ikon veya metin eşlik ediyor
- [ ] Klavye ile gezinilebiliyor, `focus-visible` görünür; grid/form içi gezinme dahil
- [ ] Boş / yükleniyor / hata durumları var
- [ ] Sayılar `tabular-nums` ve sağa hizalı
- [ ] Komponentte hardcoded palet / spacing / type değeri yok
- [ ] 320px'te taşma yok **veya** daralma stratejisi açıkça beyan edilmiş

**Bildirilen** — eksikse raporla, iş durmaz:

- [ ] Kısmi veri / çok fazla sonuç / taşan hücre durumları
- [ ] `prefers-reduced-motion` karşılığı
- [ ] İki tema da kasıtlı duruyor
- [ ] Yoğunluk seçimi gerekçelendirilmiş

## Output

```
Yüzey: veri grid'i · Yoğunluk: dense · Yön: Swiss/International
Gerekçe: 400+ kayıt, saha mühendisi değer tarıyor, masaüstü birincil

Dosyalar
  + src/styles/tokens.css        palet, type scale, yoğunluk seviyeleri
  ~ src/components/ConsumptionTable.*

Kararlar
  - dense (28px satır) + tabular-nums; sayı kolonları sağa hizalı
  - Daralma stratejisi: kimlik kolonu sticky, detay kolonları yatay kaydırmada
  - Tek ayırıcı: zebra (çok kolonlu, göz kayması riski yüksek)
  - "Sonuç yok" ile "ilk kullanım" ayrı bileşen

Doğrulama
  ✅ kontrast 7.1:1 · ✅ klavye + focus-visible · ✅ tabular-nums
  ✅ boş/yükleniyor/hata · ✅ hardcoded değer yok · ✅ 320px strateji beyan edildi
  ⚠️  reduced-motion eklendi, gerçek cihazda denenmedi
  ⚠️  koyu tema token'ları var, gözle doğrulanmadı
```

## Guardrails

- **Bağlam yoksa tasarlama.** Ürün/kullanıcı/veri hacmi bilinmiyorsa sor.
- **Yön seçimini onaylat.** Geri alınması pahalı karardır.
- Mevcut token/palet varsa onu kullan; ikinci bir sistem kurma.
- Mevcut stil dosyalarını **okumadan üzerine yazma**.
- Erişilebilirliği estetik uğruna feda etme — kontrast ve odak göstergesi pazarlık konusu değil.
- Grafik tipi/palet gerektiğinde `dataviz`'e, pazarlama yüzeyinde `frontend-design`'a devret; kapsam dışına taşma.
- Bağımlılık ekleme (grid/UI kütüphanesi) **istenmediyse**; CSS ile çözülüyorsa CSS ile çöz.
- **Eksik veriyi sıfır gibi gösterme.** Yanlış karara yol açar.

## Examples

```
/solak-design-ui src/app/consumption/page.tsx "400+ kayıt, saha mühendisi değer tarıyor"
/solak-design-ui "tesis filtre paneli, 6 kriter, sonuçlar yavaş geliyor"
/solak-design-ui src/components/InvoiceTable.tsx "bu tablo okunmuyor, kalabalık"
```

Üçüncü örnekte skill tüm sayfayı yeniden tasarlamaz; kapsamı tabloyla ve token uyumuyla sınırlı tutar.
````

- [ ] **Step 4: Satır sayısını ve isim eşleşmesini doğrula**

Run:
```powershell
(Get-Content skills\solak-design-ui\SKILL.md | Measure-Object -Line).Lines
(Select-String -Path skills\solak-design-ui\SKILL.md -Pattern '^name:').Line
Select-String -Path skills\solak-design-ui\SKILL.md -Pattern 'TBD|TODO|<eylem>|<hedef>'
```
Expected: satır sayısı **150'nin altında**; `name: solak-design-ui`; yer tutucu taraması boş

- [ ] **Step 5: Referans atıflarının gerçek dosyalara gittiğini doğrula**

`SKILL.md` beş referansa isimle atıf yapıyor; hiçbiri kırık olmamalı.

Run:
```powershell
'density-and-direction','tables','filters','forms','dashboards' | ForEach-Object {
  "$_`: " + (Test-Path "skills\solak-design-ui\references\$_.md")
}
```
Expected: beş satır, hepsi `True`

- [ ] **Step 6: Commit**

```bash
git add skills/solak-design-ui/SKILL.md
git commit -m "feat: reposition solak-design-ui onto data-dense enterprise UI"
```

---

### Task 7: registry.json ve README güncellemesi

**Files:**
- Modify: `registry.json`
- Modify: `README.md`

- [ ] **Step 1: registry.json girişini güncelle**

`skills` dizisindeki `solak-design-ui` nesnesini bul ve `version`, `tags`, `description` alanlarını değiştir:

```json
    {
      "name": "solak-design-ui",
      "path": "skills/solak-design-ui",
      "version": "0.2.0",
      "status": "draft",
      "tags": ["design", "frontend", "ui", "data-dense", "enterprise"],
      "description": "Designs and implements data-dense enterprise UI: tables and data grids, filter panels, data-entry forms and metric dashboards. Decides density deliberately, designs real-data states, stays on the project's token layer."
    }
```

- [ ] **Step 2: README skill tablosunu güncelle**

Mevcut satırı:

```markdown
| [solak-design-ui](skills/solak-design-ui/SKILL.md) | Jenerik olmayan, üretim kalitesinde UI tasarlar ve kodlar | 🚧 draft |
```

şununla değiştir:

```markdown
| [solak-design-ui](skills/solak-design-ui/SKILL.md) | Veri-yoğun kurumsal UI: tablo, filtre, form, dashboard | 🚧 draft |
```

- [ ] **Step 3: JSON geçerliliğini doğrula**

Run:
```powershell
$r = Get-Content registry.json -Raw | ConvertFrom-Json
"skill sayisi: $($r.skills.Count)"
($r.skills | Where-Object name -eq 'solak-design-ui').version
```
Expected: `skill sayisi: 2` ve `0.2.0`

- [ ] **Step 4: Commit**

```bash
git add registry.json README.md
git commit -m "chore: update registry and README for solak-design-ui v0.2"
```

---

### Task 8: Bütünsel doğrulama ve tetikleme sınaması

Yapısal kontroller geçse bile skill **tetiklenmiyorsa işe yaramaz.** Bu task davranışı sınar.

**Files:**
- Modify: `skills/solak-design-ui/SKILL.md` (yalnızca sınama başarısız olursa, `description` düzeltmesi için)

- [ ] **Step 1: Yapısal kontrollerin tamamını çalıştır**

Run:
```powershell
cd C:\Users\CagriSolakoglu\solak-skills
$ok = $true
$r = Get-Content registry.json -Raw | ConvertFrom-Json
if ($r.skills.Count -ne 2) { "HATA: skill sayisi $($r.skills.Count)"; $ok = $false }
$lines = (Get-Content skills\solak-design-ui\SKILL.md | Measure-Object -Line).Lines
if ($lines -gt 150) { "HATA: SKILL.md $lines satir"; $ok = $false }
$name = (Select-String -Path skills\solak-design-ui\SKILL.md -Pattern '^name: (.+)$').Matches.Groups[1].Value
if ($name -ne 'solak-design-ui') { "HATA: name '$name'"; $ok = $false }
Get-ChildItem skills\solak-design-ui -Recurse -Filter *.md | ForEach-Object {
  $hit = Select-String -Path $_.FullName -Pattern 'TBD|TODO|FIXME'
  if ($hit) { "HATA: yer tutucu $($_.Name)"; $ok = $false }
}
if (Test-Path skills\solak-design-ui\references\style-directions.md) { "HATA: eski yon dosyasi silinmedi"; $ok = $false }
if ($ok) { "TUM YAPISAL KONTROLLER GECTI" }
```
Expected: `TUM YAPISAL KONTROLLER GECTI`

- [ ] **Step 2: Skill'i kur**

```powershell
Copy-Item -Recurse -Force skills\solak-design-ui "$env:USERPROFILE\.claude\skills\"
Test-Path "$env:USERPROFILE\.claude\skills\solak-design-ui\references\tables.md"
```
Expected: `True`

- [ ] **Step 3: Pozitif tetikleme sınaması**

**Yeni bir Claude Code oturumu aç** (mevcut oturumda skill listesi tazelenmez) ve skill adını **anmadan** şunu yaz:

```
bu tabloda 400 kayıt var, hiç okunmuyor
```

Expected: `solak-design-ui` skill'i devreye girer, veri hacmini ve kullanım biçimini sorar.

Tetiklenmezse: sorun `description` alanındadır — tetikleyici ifadeleri (`tablo`, `okunmuyor`, `kalabalık`) güçlendir, `SKILL.md`'yi güncelle, yeniden kur ve tekrar dene.

- [ ] **Step 4: Devir sınaması (negatif)**

Yeni oturumda:

```
ürün için bir landing page tasarla
```

Expected: `solak-design-ui` **devreye girmez**; `frontend-design` seçilir. Girerse `description`'daki devir cümlesi yetersiz — güçlendir.

- [ ] **Step 5: Uçtan uca gerçek kullanım**

Gerçek bir ekranda skill'i çalıştır (bir VGen rapor tablosu uygun). Kontrol et:

- Yoğunluk kararı soruldu ve gerekçelendirildi mi?
- Yön onayı istendi mi?
- Bloklayan kapılar raporlandı mı, biri geçilmediyse "tamamlandı" demedi mi?
- Yalnızca ilgili referansı mı okudu (dördünü birden değil)?

- [ ] **Step 6: Sonucu kaydet ve commit**

Sınamalar geçtiyse `SKILL.md` ve `registry.json`'da `status: draft` → `status: stable`.

Geçmediyse `draft` kalır ve eksik `docs/specs/2026-07-30-solak-design-ui-design.md` dosyasının "Açık konular" bölümüne yazılır.

```bash
git add -A
git commit -m "test: verify solak-design-ui v0.2 triggering and gates"
git push
```

---

## Tamamlanma kriterleri

- [ ] Beş referans dosyası var, `style-directions.md` silinmiş
- [ ] `SKILL.md` 150 satırın altında, `name` klasör adıyla eşleşiyor, yer tutucu yok
- [ ] `SKILL.md`'deki beş referans atfı gerçek dosyalara gidiyor
- [ ] Anti-template listesi kopyası yok; global kurala işaret ediliyor
- [ ] `dataviz` ve `frontend-design` devirleri hem `description`'da hem guardrail'lerde yazılı
- [ ] `registry.json` geçerli JSON, sürüm `0.2.0`
- [ ] README tablosu güncel
- [ ] Pozitif tetikleme ve negatif devir sınamaları geçti
- [ ] Gerçek bir ekranda uçtan uca çalıştırıldı
