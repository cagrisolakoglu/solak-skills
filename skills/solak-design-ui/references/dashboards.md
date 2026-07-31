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

Eşit grid bento değil, sadece grid'dir. `minmax(0, 1fr)` önemli: `1fr` tek başına taşan içerikte kolonu şişirir.

## KPI anatomisi

Dört parça, sırasıyla:

1. **Etiket** — ne ölçülüyor, birimiyle
2. **Değer** — en büyük ölçek, `tabular-nums`
3. **Değişim** — yön + miktar; **renk tek gösterge olamaz** (ok ikonu veya işaret eşlik eder)
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

**Bağlamsız sayı bilgi değildir.** "184.320" tek başına kullanıcıya hiçbir karar verdirmez.

## Eşik renkleri semantik, ve renk tek gösterge olamaz

```css
:root {
  --status-ok:       oklch(62% 0.15 150);
  --status-warn:     oklch(72% 0.16  75);
  --status-critical: oklch(58% 0.20  25);
}
```

Her durum rengi bir **ikon veya metinle** eşlenir. Renk körlüğü bir yana, gri tonlamalı çıktıda ve düşük parlaklıkta ekranda renk kaybolur.

Ayrıca: bir metriğin "yukarı" gitmesi her zaman iyi değildir (maliyet, arıza sayısı, gecikme). **Yönü ok taşır, iyi/kötü durumunu renk taşır** — ikisini karıştırma.

## Sparkline

- Eksen ve etiket yok; işi trendin şeklini göstermek
- Son değer noktayla işaretlenir
- Tek başına sayı yerine geçmez — her zaman değerle birlikte
- Yükseklik 24-40px; daha küçüğü şekli okunmaz yapar
- Y ekseni sıfırdan başlamıyorsa bunu belli et; yoksa küçük dalgalanma dramatik görünür

## Grafik işi geldiğinde

Grafik tipi seçimi, kategorik/sıralı palet, eksen ve tooltip kuralları için **`dataviz` skill'ini kullan.** O bilgi burada tekrar edilmez.

## Durumlar

| Durum | Tasarım |
|-------|---------|
| Veri yok | Tile yapısı korunur; değer yerine "veri yok" + nedeni |
| Kısmi veri | Hangi dönemin eksik olduğu yazılır |
| Yükleniyor | Tile boyutunda iskelet — layout shift olmaz |
| Bayat veri | Son güncelleme zamanı görünür; canlı sanılmasın |
| Hata | Tile içinde, tüm dashboard'u boşaltmadan |

**Eksik veriyi sıfır olarak gösterme.** Dashboard'lardaki en pahalı hata budur: yanlış karara yol açar. Sıfır bir ölçümdür, veri yokluğu değildir.

## Düzen ve okuma sırası

- Sol üst en önemli metrik (soldan sağa okuma)
- İlgili metrikler komşu
- Dashboard bir ekrana sığmalı; kaydırma gerekiyorsa muhtemelen iki farklı dashboard var
- `320px`'te tek kolona iner; sıra önem sırasıyla aynı kalır

## Erişilebilirlik

- Her tile `article` + başlık (`h3`); ekran okuyucu tile'ları listeleyebilmeli
- Dekoratif ikon `aria-hidden="true"`; anlam taşıyan ikonun metin karşılığı olmalı
- Otomatik yenilenen değerler `aria-live="polite"` — ama sık yenilemede kapat, sürekli okuma rahatsız eder
- Sparkline `aria-hidden`; trendi metinle de söyle ("son 7 günde artış")
