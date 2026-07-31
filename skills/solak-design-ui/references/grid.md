# Kolon Grid'i

Yoğunluk **dikey** ritmi kurar, grid **yatay** ritmi. İkisinden biri eksikse yüzey dağınık görünür — alanlar tek tek doğru boyutta olsa bile.

Belirti: her alanın genişliği kendi içeriğine göre makul ama hiçbir alanın sol veya sağ kenarı bir diğeriyle hizalı değil; geniş ekranda yüzeyin sağ yarısı ölü alan. Bu **içerik genişlikli flex** ile kurulmuş formun imzasıdır.

## Token'lar

Kolon sayısı ve oluk (gutter) yoğunluk gibi kök seviye token'dır, komponent kararı değil.

```css
:root {
  --grid-cols: 12;
  --grid-gutter: 20px;
  --grid-row-gap: var(--space-field);
  --content-max: 76ch;        /* okuma kolonu tavanı */
}

[data-density="dense"]       { --grid-gutter: 12px; }
[data-density="comfortable"] { --grid-gutter: 24px; }

.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols), minmax(0, 1fr));
  gap: var(--grid-row-gap) var(--grid-gutter);
}
/* span daima grid-column-END üzerinden verilir — nedeni aşağıda */
.col-2  { grid-column-end: span 2; }
.col-3  { grid-column-end: span 3; }
.col-4  { grid-column-end: span 4; }
.col-6  { grid-column-end: span 6; }
.col-12 { grid-column-end: span 12; }
.start-1 { grid-column-start: 1; }   /* yeni satır başlatır */
```

`minmax(0, 1fr)` zorunlu: `1fr` tek başına taşan içeriği (uzun seçenek metni, kesilmemiş sayı) kolon dışına çıkarır.

## Tuzak: `grid-column: span N` ile satır başlatma birbirini yer

`grid-column: span 6` shorthand'i `span 6`'yı **start** değerine yazar, end'i `auto` bırakır. Aynı elemana satır başlatmak için `grid-column-start: 1` verildiğinde span bilgisi silinir ve alan **1 kolona** düşer. Belirti: bütün alanlar aynı, absürt derecede dar genişlikte; seçici ve girdi metinleri kırpılır.

```css
/* ❌ span, .start-1 tarafından eziliyor */
.col-6  { grid-column: span 6; }
.start-1 { grid-column-start: 1; }

/* ✅ start ve end ayrı özellikler, çakışmaz */
.col-6  { grid-column-end: span 6; }
.start-1 { grid-column-start: 1; }
```

Bu kırılma yalnızca ekran görüntüsüyle yakalanır — CSS geçerli, hata vermez. Grid'e geçtikten sonra **mutlaka görüntü al.**

## Tuzak: `max-inline-size` bir media query özelliği değildir

Komponent CSS'inde mantıksal özellikler (`inline-size`, `max-inline-size`) doğrudur; **media query'de** karşılığı yoktur — `@media (max-inline-size: 900px)` sessizce hiç eşleşmez. Media query'de `max-width`, kap sorgusunda `inline-size` kullan.

```css
@media (max-width: 900px) { :root { --grid-cols: 6; } }            /* ✅ */
@container (max-inline-size: 900px) { :root { --grid-cols: 6; } }  /* ✅ kap sorgusu */
```

## Uzlaşma: kolon hizası ile karakter genişliği çelişmez

Form referansı "alan genişliği içerikle eşleşir" der (posta kodu tam genişlik olmaz), grid ise "kenarlar hizalanır" der. İkisi çelişmez — **görev bölüşümü** vardır:

| Kim | Neyi belirler |
|-----|---------------|
| Grid kolonu | Hücrenin **sol kenarını** ve tahsis edilen yeri |
| `max-inline-size: Nch` | Alanın hücre içinde **ne kadarını doldurduğunu** |

```css
.field { min-inline-size: 0; }              /* grid hücresinde taşmayı önler */
.field input { inline-size: 100%; }
.field--code   { max-inline-size: 11ch; }   /* dönem, çarpan */
.field--date   { max-inline-size: 13ch; }
.field--index  { max-inline-size: 16ch; }
```

Böylece sol kenarlar kolon çizgisine oturur, genişlik hâlâ beklenen karakter sayısını söyler. Sağ kenarları hizalamak için alanı gereksiz genişletmek **yanlıştır** — hizalanan şey kolon çizgisidir, alan kutusu değil.

## Hücrenin span'ini girdi değil, en geniş içerik belirler

Hücrede üç içerik var: etiket, girdi, yardım/hata metni. Span'i **en geniş ölçü isteyen** belirler — bu çoğu zaman girdi değil, metindir.

Belirti: 11 karakterlik alana `col-2` verilmiş, altındaki yardım metni 28 karakterlik dar bir şeride sıkışıp iki satıra kırılıyor, hemen sağında **boş kolonlar** duruyor. Metin dar hendekte akarken yanında yer varsa span yanlış seçilmiştir.

```html
<!-- ❌ span girdiye göre: yardım metni kırılır, sağda 9 boş kolon -->
<div class="field col-2">
  <label for="period">Dönem</label>
  <input class="w-code" id="period" value="2026-07" readonly>
  <p class="field-hint">Açık dönem. Kapalı döneme okuma girilemez.</p>
</div>

<!-- ✅ span metne göre; girdi max-inline-size ile 11ch kalır -->
<div class="field col-4">…aynı içerik…</div>
```

```css
.field-hint, .field-error { max-inline-size: 46ch; }   /* geniş hücrede de okuma ölçüsünü aşmaz */
```

Kural: **yardım veya hata metni taşıyan hücreye en az ~34ch ayır.** Metnin ölçüsü hücrenin, girdinin ölçüsü `max-inline-size`'ın işidir; ikisi aynı sayı değildir.

Yardım metnini satır sonuna kadar yaymak alternatif değil: metin girdinin sol kenarından başlar ama hiçbir şeyle hizalanmayan bir sağ kenarda biter.

## Span seçimi

Aynı satırdaki alanlar toplamda kolon sayısını doldurur; artan yer boş kolonda bırakılır, alanlara dağıtılmaz.

```html
<div class="grid">
  <div class="field col-6">…Tesis…</div>
  <div class="field col-4">…Ölçüm Noktası…</div>
  <!-- kalan 2 kolon kasıtlı boş -->

  <div class="field col-2">…Dönem…</div>
  <div class="field col-2">…Okuma Tarihi…</div>
  <div class="field col-4">…Okuyan…</div>
</div>
```

Kural: **satır sonunda artan yeri son alana verme.** "Okuyan" alanını 6 kolona yaymak onu Tesis kadar önemli gösterir; hiyerarşi span ile konuşur.

## İlişkili alanlar aynı span'i paylaşır

Karşılaştırılacak alanlar (önceki endeks / güncel endeks, başlangıç / bitiş tarihi, min / maks tutar) **eşit span** alır. Farklı span, kullanıcıya olmayan bir önem farkı bildirir.

## Satır anlamsal bir birimdir

Aynı satırdaki alanlar kullanıcıya "bunlar aynı türden" der. Tür karışırsa satır bilgi taşımaz, yalnızca yer doldurur.

Sayaç okuma formunda üç tür var, her biri kendi satırını alıyor:

| Satır | Alanlar | Neden birlikte |
|-------|---------|----------------|
| Cihaz sabitleri | Sayaç Seri No, Çarpan | Okumadan bağımsız, kayıt boyunca değişmez |
| Okumalar | Önceki Endeks, Güncel Endeks | Karşılaştırılacak çift → **eşit span** |
| Türetilmiş | Hesaplanan Tüketim, Geçmiş Ortalama | Girdi değil, sonuç |

Seri no ile önceki endeksi aynı satıra koymak ikisini aynı cins gösterir; biri kimlik, öbürü ölçüm. Satırı bölmek yer kaybı değil, bilgi kazancıdır.

Tersi de geçerli: bir satırda tek başına duran dar alan **kasıtlı bir sınır** bildirir. Bir grupta böyle iki-üçten fazla satır varsa sınır değil dağınıklık üretilmiş; gruplama yeniden düşünülmeli.

## Daralma: kolon sayısı düşer, span'ler yeniden eşlenir

Alanları tek tek `100%` yapmak grid'i çözmez, yok eder. Kolon sayısını azalt; span'ler otomatik uyumlanır.

```css
@media (max-width: 900px) { :root { --grid-cols: 6; }
  .col-4 { grid-column-end: span 3; }
  .col-5, .col-6, .col-7, .col-12 { grid-column-end: span 6; } }
@media (max-width: 560px) { :root { --grid-cols: 1; }
  [class*="col-"] { grid-column-end: span 1; } }
```

**Kolon sayısından büyük kalan her span sessizce taşırır.** 6 kolonlu grid'de eşlenmemiş `span 7` örtük bir kolon yaratır; grid 7 kolona çıkar, yüzey kabından dışarı sarkar. Hata vermez, konsola bir şey yazmaz — yalnızca ekran görüntüsünde görünür. Daralma yazarken **her** span sınıfını say, kullandığın en büyüğünü unutma.

Tek kolona düşen alanlarda `max-inline-size` **kalır** — sayaç seri no alanı telefonda da tam genişlik olmamalı, aksi halde dokunmatik klavyede yanlış hizalama hissi verir. Yalnızca yardım metni ve hata metni tam genişliğe yayılır.

## Ölü alan bir grid sorunudur

Geniş ekranda içerik solda toplanıp sağ yarı boş kalıyorsa iki meşru çözüm var; **üçüncüsü yok** (alanları gereksiz genişletmek çözüm değildir):

1. **Kabı daralt** — form kartını `--content-max` ile sınırla, ortala veya sola sabitle. Uzun formda tercih edilen.
2. **Yan kolonu doldur** — özet, geçmiş kayıt, doğrulama listesi gibi **gerçek** bir içerik koy. Doldurmak için içerik uyduruluyorsa 1. seçeneğe dön.

Henüz yüklenmemiş gerçek bir alan da içeriktir: "Geçmiş Dönem Ortalaması" iskeleti, hesaplanan tüketim bloğunun yanındaki boş kolonları meşru şekilde doldurur — kullanıcı o değerin geleceğini bilir. Ama yalnızca boşluğu kapatmak için eklenen bir tile veya tekrar eden bir özet içerik değil, dolgudur.

## Etiket ve alan hizası

Etiket üstte yerleşimde etiketin sol kenarı alanın sol kenarıyla, yani kolon çizgisiyle **aynı** olmalı. `padding-inline-start` ile içe alınmış etiket grid'i gözle bozar.

## Doğrulama

- [ ] Her alan bir kolon çizgisinden başlıyor (tarayıcı grid overlay ile bak)
- [ ] Karşılaştırılan alanlar eşit span
- [ ] Satır sonu artan yer boş kolonda, son alana yayılmış değil
- [ ] Yardım/hata metni taşıyan hücre ≥ 34ch; metin dar şeride kırılmıyor
- [ ] Her satır tek türden alan taşıyor (kimlik / ölçüm / türetilmiş karışmamış)
- [ ] Daralma kolon sayısıyla yapılıyor, alan başına `100%` ile değil
- [ ] Daralmada **her** span sınıfı yeniden eşlenmiş; kolon sayısından büyük span kalmamış
- [ ] Geniş ekranda ölü alan yok: ya kap daraltılmış ya yan kolonda gerçek içerik var
