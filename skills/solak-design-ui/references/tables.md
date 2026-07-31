# Tablo / Veri Grid'i

Yoğunluk kararı için önce `density-and-direction.md`.

## Hizalama tipe göre

| Veri tipi | Hizalama | Not |
|-----------|----------|-----|
| Metin, etiket | Sola | — |
| Sayı, para, yüzde | **Sağa** + `font-variant-numeric: tabular-nums` | Basamaklar dikey hizalanır, karşılaştırma mümkün olur |
| Tarih, saat | Sola, sabit genişlik | Format tutarlı: tek tabloda karışık format yok |
| Durum, etiket (badge) | Sola | Renk **tek gösterge olamaz** — metin veya ikon eşlik eder |
| Eylem | Sağa, en sağ kolon | Sıralanamaz; yatay kaydırmada sticky olabilir |

```css
.cell-numeric {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
```

Sayıyı sola hizalamak veya proportional font kullanmak, tablonun tek işini — karşılaştırmayı — bozar. Başlık hücresi de gövdeyle **aynı** hizada olmalı; sağa hizalı sayı kolonunun başlığı sola hizalıysa göz iki farklı eksen takip eder.

## Kolon önceliği ve daralma

Kolonları üç önceliğe ayır: **kimlik** (hangi kayıt), **karar** (kullanıcının aradığı değer), **detay** (gerisi).

Ekran daraldığında **kolonu sıkıştırmak yasak.** Üç meşru strateji:

1. **Gizle** — detay kolonlarını kaldır, satır genişletmeyle erişilebilir kıl
2. **Katla** — kimlik + karar kolonlarını iki satırlı tek hücreye topla (mobil kart görünümü)
3. **Yatay kaydır** — kimlik kolonu sticky, gerisi kayar

Hangisi seçildiyse **çıktı raporunda açıkça beyan et.** Beyan edilmemiş daralma davranışı doğrulama kapısını geçmez.

### Yatay kaydırmanın çöktüğü eşik: kimlik bloğu > %40

Sticky kimlik bloğu görünür genişliğin **%40'ından fazlasını** alıyorsa strateji teknik olarak çalışır ama pratikte işe yaramaz: 320px'te 34px checkbox + 132px ad = 166px, kalan ~150px'e tek veri kolonu sığar. Kullanıcı her değeri görmek için ayrı bir kaydırma yapar.

Bu genişlikte tek meşru seçenek **katlamadır** (2. strateji): satır bir karta döner, kimlik başlık olur, karar kolonları etiketli satırlara iner, detay kolonları "Detay" bağlantısına kalır.

Beyan yeterli değil: "yatay kaydırma seçildi" demek 320px'te kullanılabilir olduğunu kanıtlamaz. **Ölç:** kimlik bloğu genişliği ÷ görünür genişlik. Eşiği aşıyorsa ya bu genişlik için katlama yaz, ya yüzeyin desteklenen alt sınırını (örn. 560px) açıkça bildir.

## Sticky

- Başlık satırı: `position: sticky; top: 0` — 15+ satırda zorunlu
- Kimlik kolonu: yatay kaydırma varsa `position: sticky; left: 0` zorunlu
- Sticky yüzeyin arkası **opak** olmalı; yarı saydam başlık altındaki metni okunmaz yapar
- Sticky öğeye `z-index` ver; kesişimde (başlık × ilk kolon) köşe hücresi en üstte kalmalı
- Sticky kimlik sınırı (dikey çizgi) yalnızca **yatay kaydırma varken** anlam taşır; kaydırma yoksa gerekçesiz bir dikey çizgidir

### İki zorunlu tablo ayarı — yoksa sticky sessizce bozulur

```css
table {
  table-layout: fixed;          /* 1 */
  border-collapse: separate;    /* 2 */
  border-spacing: 0;
  inline-size: 100%;
  min-inline-size: 1216px;      /* altında yatay kaydırma başlar */
}
```

**1 · `table-layout: fixed` + `<colgroup>`.** `auto` düzende `td`/`th` üzerindeki `inline-size` yalnızca bir *öneridir*; tarayıcı kolonu içeriğe göre büyütür. Sticky `left` offset'i ise kesin bir sayıdır. İkisi uyuşmayınca sticky kolonun **altından kaydırılan içerik sızar** — ekranda, checkbox'ın yanında komşu kolonun son haneleri belirir.

Aynı ayar `text-overflow: ellipsis`'i de çalışır hale getirir: `auto` düzende kolon içeriğe göre genişlediği için kırpma hiç tetiklenmez.

```html
<colgroup>
  <col class="c-select"><col class="c-point"><col class="c-meter">…
</colgroup>
```

Genişlikler tek yerde (`colgroup`) durur; sticky offset'ler aynı token'lardan türetilir:

```css
.c-select { inline-size: var(--w-select); }
.c-point  { inline-size: var(--w-point); }
.col-select { position: sticky; left: 0; }
.col-point  { position: sticky; left: var(--w-select); }   /* offset = önceki kolonun GERÇEK genişliği */
```

**2 · `border-collapse: separate`.** `collapse` ile kenarlar hücreye ait olmaz; sticky hücre kaydırılırken kenarları geride kalır ve kaybolur. Ayırıcı görevini zebra veya `::after` ile çizilen sahte kenar üstlenir.

### z-index katmanları

| Katman | Öğe |
|--------|-----|
| 1 | Gövdedeki sticky kolonlar |
| 2 | `thead th` ve `tfoot td` |
| 3 | Kesişim: `thead .col-point`, `tfoot .col-point` |

Kesişim hücresi en üstte olmazsa köşede iki sticky yüzey üst üste biner ve metin okunmaz.

Her sticky hücre **kendi opak dolgusunu** taşımak zorunda. Zebra kuralı `tr`'ye değil `td`'ye yazılırsa bu kendiliğinden sağlanır:

```css
tbody tr:nth-child(even) td { background: var(--surface-zebra); }
tbody tr:nth-child(odd)  td { background: var(--surface-card); }
```

## Tek ayırıcı sistemi

Zebra şeritleri **veya** yatay çizgiler — ikisi birden değil. İkisi birlikte gürültü üretir ve hiçbiri işini yapmaz.

- **Zebra**: `dense` seviyede, çok kolonlu tabloda göz kaymasını engeller
- **Çizgi**: `comfortable`/`compact` seviyede daha temiz
- **Dikey çizgi**: yalnızca kolon grupları varsa

Zebra kullanılıyorsa hover ve seçili durum zebradan **daha güçlü** olmalı, yoksa görünmez.

**Zebra deltası ≥ ~%3 açıklık.** `oklch(100%)` ile `oklch(98.2%)` arası fark ekranda kaybolur — kod zebra yazar, kullanıcı düz tablo görür. Yoğun ve çok kolonlu tabloda gözle ayırt edilebilir en az fark yaklaşık %3'tür; koyu temada da ayrıca ölç, açık temada yeten delta koyuda yetmez.

## Taşan hücre

Uzun metin: tek satırda kısalt (`text-overflow: ellipsis`) **ve** tam değeri erişilebilir kıl — `title` özniteliği veya tooltip. Kısaltıp tam değeri hiç göstermemek veri kaybıdır.

Kırpma yalnızca `table-layout: fixed` ile çalışır (yukarı bak). `auto` düzende kolon içeriğe göre büyür, kırpma hiç tetiklenmez.

Satır yüksekliğini içeriğe göre büyütmek `dense`/`compact` seviyede tarama ritmini bozar; sabit yükseklik + kısaltma tercih edilir.

### Başlık kırpılamaz

`OKUMA T…` bir başlık değildir — kolonun anahtarını yok eder. Hücre kırpılır, başlık **asla**. İki çıkış yolu: kolonu başlığı alacak kadar genişlet, veya başlığı kısalt ("Okuma Tipi" → "Tip"). Kırpılmış başlık, kırpılmış hücreden çok daha pahalıdır: hücrede tek bir kaydı, başlıkta bütün kolonu okunamaz yapar.

## Başlıkta birim ve büyük harf

Başlıklarda `text-transform: uppercase` yaygın bir Swiss kalıbı, ama iki şeyi sessizce bozar:

**1 · Birim sembolleri.** `kWh` → `KWH` yanlıştır: `k` kilo, `W` Watt, `h` saat — büyük/küçük harf anlam taşır. `MWh`, `mA`, `kV` aynı şekilde. Birimi ayrı bir öğeye al:

```html
<th class="is-num">Tüketim <span class="unit">(kWh)</span></th>
```
```css
th { text-transform: uppercase; }
th .unit { text-transform: none; letter-spacing: 0; }
```

**2 · Türkçe `i`.** `text-transform: uppercase` Türkçe kuralını yalnızca `lang="tr"` varsa uygular. Eksikse `Tip` → `TIP`, `İtirazlı` → `ITIRAZLI` olur. Kök öğede `<html lang="tr">` **zorunlu** — bu bir erişilebilirlik ayarı değil, doğru harf üretme koşulu.

## Sıralama ve seçim

- Sıralanabilir başlık `button` olmalı (klavye erişimi)
- **Sıralanabilirlik göstergesi hover'a bağlanamaz** — dokunmatikte hover yoktur, gösterge hiç görünmez. Kalıcı ama sessiz olsun: `opacity: 0.3` "sıralanabilir", `0.6` hover, `1` sıralanmış
- Aktif sıralamada yön oku **ve** hangi kolon olduğu görünür kalsın; `aria-sort` özniteliğini kullan
- Satır tıklaması ile checkbox seçimi **çakışmasın** — tıklama detaya gidiyorsa checkbox ayrı hedef olmalı
- Toplu seçimde kaç kayıt seçildiği ve "tümünü seç" kapsamı (bu sayfa mı, tüm sonuç mu) açıkça yazılmalı

## Hücre içi işaretçi sayı hizasını bozar

Aykırı bir değeri (endeks geri gitmiş, imkansız negatif, eşik aşımı) işaretlemek gerekir — eksi işaretini yoğun bir kolonda tek gösterge bırakmak onu kaçırılır kılar. Ama sağa hizalı bir kolonda **glif işe yaramaz**, iki denemenin ikisi de başarısız:

```css
/* ❌ 1: akışa girer → sayıyı sola kaydırır, kolonun basamak hizası biter */
.is-anomaly::after { content: " ⚠"; }

/* ❌ 2: akış dışına alınır → hizayı korur ama sağa hizalı kolonun boş sol
   tarafında durur ve KOMŞU KOLONA aitmiş gibi okunur ("40 ⚠" gibi) */
.is-anomaly { position: relative; }
.is-anomaly::after { content: "⚠"; position: absolute; left: var(--cell-pad-x); }
```

Doğru cevap **hücre vurgusu**: hizayı bozmaz, sahipliği belirsiz bırakmaz.

```css
/* ✅ hücrenin tamamı işaretli; zebra kuralını ezmek için tr td özgüllüğü gerekir */
tbody tr td.is-anomaly {
  background: var(--danger-quiet);
  box-shadow: inset 2px 0 0 var(--danger);
  color: var(--danger);
  font-weight: 650;
}
```

Renk tek gösterge olmadığı için eksi işareti ve satırın durum etiketi ("İtirazlı") eşlik etmeli; ayrıca `title` ile nedenini yaz ("Güncel endeks öncekinden küçük — sayaç değişimi veya hatalı okuma").

Aynı kural para birimi simgesi, dipnot yıldızı ve trend oku için de geçerli: sağa hizalı bir kolonda sayının yanına eklenen her karakter ya hizayı kaydırır ya sahipliği belirsizleştirir. Rakamların sağ kenarı **tek** bir dikey çizgide kalmalı; ek bilgi hücre vurgusu, ayrı kolon veya tooltip ile verilir.

## Toplam satırı

Varsa `position: sticky; bottom: 0`, gövdeden farklı ağırlıkta, sayı hizası gövdeyle **birebir aynı**.

Üç şeyi açıkça yaz:

1. **Neyin toplamı** — görünen sayfa mı, filtrelenmiş tüm sonuç mu: "Toplam filtrelenmiş 412 kaydın tamamına aittir, görünen 50 satıra değil."
2. **Neyin hariç tutulduğu** — "Okunamayan 7 nokta toplama dahil edilmedi." Eksik veriyi sıfır sayan toplam yanlış karar üretir.
3. **Toplanmayan kolonlar** — endeks, çarpan, tarih gibi toplamı anlamsız kolonlarda `—` göster, boş bırakma. Boş hücre "hesaplanamadı" ile "toplanmaz"ı ayırt etmez.

Yuvarlama farkı (gösterilenlerin toplamı ≠ gösterilen toplam) için `formatting.md`.

## Durumlar — hepsi tasarlanacak

| Durum | Tasarım |
|-------|---------|
| İlk kullanım (hiç veri yok) | Ne olduğunu açıkla + ilk eylemi öner. "Kayıt yok" yetersiz. |
| Sonuç yok (filtre sonucu) | **İlk kullanımdan ayrı.** Hangi filtrenin gevşetileceğini öner. |
| Yükleniyor | İskelet satırlar, yüksekliği gerçek satırla **aynı**; **başlık satırı gerçek kalır** |
| Kısmi yükleme | Yüklenmiş satırlar görünür, devamı için gösterge |
| Hata | Ne olduğu + tekrar dene eylemi; tabloyu boşaltıp tek satır hata yazma |
| Tek satır | Tablo yerine detay görünümü daha uygun olabilir — sorgula |

İlk kullanım ile "sonuç yok" durumunu aynı bileşenle çözmek en sık yapılan hatadır: kullanıcı sistemin boş mu olduğunu yoksa filtresinin mi kötü olduğunu anlayamaz.

Yükleme iskeletinde **kolon başlıkları yüklenmez** — bilinirler. Başlık satırını gri çubuklara çevirmek kullanıcıdan neyin geldiğini saklar ve metin belirince layout titrer. İskelet genişlikleri de kolon genişliklerine uymalı, rastgele olmamalı.

## Erişilebilirlik

- `<table>` + `<th scope="col">` kullan; `div` grid'i ancak sanallaştırma zorunluysa ve `role="grid"` ile
- Klavye: `Tab` ile eylemlere ulaşılır; sıralanabilir başlıklar `button`
- Kaydırılabilir kabın kendisi klavyeyle kaydırılabilmeli: `tabindex="0"` + `role="region"` + `aria-label`. Aksi halde yatay kaydırmadaki kolonlara yalnızca fare ulaşır
- Sanallaştırılmış tabloda toplam satır sayısını ekran okuyucuya bildir — DOM'daki satır sayısı gerçeği yansıtmaz
- Yalnızca hover'da görünen eylem **klavyeyle erişilemez**; `focus-within` ile de görünür olmalı

## Doğrulama

- [ ] `table-layout: fixed` + `colgroup`; sticky offset'ler kolon genişlik token'larından türüyor
- [ ] `border-collapse: separate`
- [ ] **Kaydırılmış durumda** ekran görüntüsü alındı: sticky kolonun altından içerik sızmıyor
- [ ] z-index katmanları: gövde sticky 1, thead/tfoot 2, kesişim 3
- [ ] Zebra deltası her iki temada gözle görünür (≥ ~%3)
- [ ] Hiçbir başlık kırpılmıyor
- [ ] Birim sembolleri büyük harfe çevrilmemiş; `<html lang="tr">` var
- [ ] Sıralama göstergesi hover'sız görünüyor
- [ ] Sayı kolonunda tüm rakamların sağ kenarı aynı çizgide (işaretçiler akış dışında)
- [ ] Toplam: neyin toplamı, ne hariç, hangi kolonlar toplanmıyor — üçü de yazılı
- [ ] Kimlik bloğu / görünür genişlik oranı ölçüldü; %40'ı aşan genişlikte katlama var veya alt sınır beyan edildi
