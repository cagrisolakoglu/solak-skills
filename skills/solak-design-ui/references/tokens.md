# Token Katmanı

Token katmanı, komponentin hiçbir renk/ölçü/süre değerini kendi içinde tutmadığı anlamına gelir. Yoğunluk (`density-and-direction.md`) ve kolon grid'i (`grid.md`) de bu katmanın parçasıdır — komponent kararı değil.

## Önce mevcut katmanı ara

**Paralel bir sistem kurmak, hiç token kullanmamaktan kötüdür.** İki sistem varsa ikisi de bozulur. Yazmadan önce ara:

```bash
rg -l "^\s*--[a-z-]+:" --type css --type scss -g '!node_modules'   # CSS custom property tanımları
rg -l "tailwind.config|theme\s*:|createTheme|defineTheme"           # JS/TS tema nesnesi
fd -g "*variables*.{css,scss,sass}" -g "*tokens*" -E node_modules   # adlandırılmış token dosyası
fd -g "quasar.variables.*" -g "_variables.scss"                     # framework tema dosyası
```

Bulursan:
- **Oku, isim şemasını çıkar** (`--color-*`, `$brand-*`, `theme.palette.*` — hangisi?)
- Eksik token'ı **aynı şemaya** ekle; yeni bir isim ailesi başlatma
- Değer değil **rol** eşleştir: mevcut `--bg-elevated` varsa `--surface-card` yazma, onu kullan
- Katman yetersizse (ör. semantik durum rengi yok) eksik olanı ekle ve raporda söyle

Bulamazsan aşağıdaki katmanı yaz.

## Rol adı, değer adı değil

```css
--surface-card: …      /* ✅ nerede kullanılacağını söyler */
--gray-100: …          /* ❌ ne olduğunu söyler, tema değişince yalan olur */
--ink-muted: …         /* ✅ */
--text-gray-500: …     /* ❌ koyu temada gri-500 değil */
```

Değer adlı token koyu temada anlamını kaybeder: `--gray-100` açık temada yüzey, koyu temada metindir. Rol adı iki temada da doğru kalır.

## Katman: dokuz grup

Aşağıdaki set sayaç okuma formunda iki temada ekran görüntüsüyle doğrulandı. Değerler `oklch` — açıklığı (ilk sayı) doğrudan okunabilir olduğu için kontrast hesabı gözle yapılabilir hale gelir.

```css
:root {
  color-scheme: light dark;

  /* 1 · Yüzey — üç seviye yeter: sayfa, kart, çökmüş */
  --surface-page:   oklch(97.5% 0.003 250);
  --surface-card:   oklch(100% 0 0);
  --surface-sunken: oklch(95.5% 0.004 250);
  --surface-field:  oklch(100% 0 0);

  /* 2 · Mürekkep — üç seviye: güçlü, gövde, soluk. Yorumu yanına yaz. */
  --ink-strong:   oklch(21% 0.012 260);   /* kart üzerinde 14.6:1 */
  --ink-body:     oklch(34% 0.010 260);   /* 9.4:1 */
  --ink-muted:    oklch(46% 0.010 260);   /* 5.6:1 — 4.5 sınırının üstünde */
  --ink-onaccent: oklch(99% 0 0);

  /* 3 · Çizgi — iki seviye: ayırıcı ve kenar */
  --line:        oklch(88% 0.005 260);
  --line-strong: oklch(72% 0.008 260);

  /* 4 · Accent — TEK işlevsel accent. İkincisi hiyerarşiyi böler. */
  --accent:       oklch(46% 0.14 252);
  --accent-hover: oklch(39% 0.14 252);
  --accent-quiet: oklch(95% 0.03 252);
  --focus-ring:   oklch(52% 0.17 252);

  /* 5 · Semantik durum — her biri ikon/metinle eşlenir, renk tek gösterge değil */
  --danger: oklch(45% 0.17 27);   --danger-quiet:  oklch(96% 0.03 27);
  --success: oklch(43% 0.11 155); --success-quiet: oklch(96% 0.03 155);
  --warn: oklch(48% 0.11 75);     --warn-quiet:    oklch(96% 0.04 75);

  /* 6 · Tipografi — tek aile, hiyerarşi ağırlık ve ölçekle */
  --font-ui: ui-sans-serif, "Segoe UI Variable Text", "Segoe UI", system-ui, sans-serif;
  --text-micro: 0.75rem;
  --text-label: 0.8125rem;
  --text-body:  0.875rem;
  --text-title: clamp(1.25rem, 1.05rem + 0.9vw, 1.6rem);
  --weight-label: 550;

  /* 7 · Yoğunluk — dikey ritim (density-and-direction.md) */
  --field-height: 36px;
  --field-pad-x:  10px;
  --space-field:  16px;
  --space-group:  40px;   /* alan arasının ~2.5 katı */
  --space-card:   clamp(20px, 2vw, 32px);

  /* 8 · Grid — yatay ritim (grid.md) */
  --grid-cols:   12;
  --grid-gutter: 20px;
  --content-max: 76ch;

  /* 9 · Biçim — kenar yarıçapı ve hareket */
  --radius: 5px;  --radius-sm: 3px;
  --duration: 120ms;
  --ease: cubic-bezier(0.2, 0, 0.2, 1);
}
```

Sayı disiplini: üç yüzey, üç mürekkep, iki çizgi, bir accent. Beşinci gri tonu eklemek istiyorsan önce mevcut dördünün hangisinin işini yapmadığını söyle.

## Yoğunluk ve tema aynı katmanda devralınır

```css
[data-density="comfortable"] { --field-height: 44px; --field-pad-x: 14px; --text-body: 0.9375rem;
                               --space-field: 20px; --space-group: 48px; --grid-gutter: 24px; }
[data-density="dense"]       { --field-height: 28px; --field-pad-x: 8px;  --text-body: 0.8125rem;
                               --space-field: 12px; --space-group: 32px; --grid-gutter: 12px; }
```

Komponent `--field-height`'ı okur; hangi yoğunlukta olduğunu bilmez. Yoğunluk seviyesi eklemek komponente dokunmadan olur — olmuyorsa token katmanı sızmış.

## Koyu tema ters çevirme değildir

```css
@media (prefers-color-scheme: dark) {
  :root {
    --surface-page:   oklch(19% 0.012 260);
    --surface-card:   oklch(24% 0.013 260);   /* kart sayfadan YÜKSEK */
    --surface-sunken: oklch(21% 0.012 260);
    --surface-field:  oklch(27.5% 0.014 260); /* girdi en yüksek yüzey */

    --ink-strong: oklch(97% 0.004 260);
    --ink-body:   oklch(88% 0.005 260);
    --ink-muted:  oklch(72% 0.008 260);

    --accent:       oklch(72% 0.13 252);      /* doygunluk düşer, açıklık yükselir */
    --ink-onaccent: oklch(18% 0.02 260);      /* accent üzerindeki mürekkep de döner */
  }
}
```

Üç kural:

1. **Açıklığı çevir, doygunluğu düşür.** Koyu zeminde aynı chroma titrer ve kenarları parlar.
2. **Yükseklik sırası korunur ama değerler yeniden seçilir** — açık temada kart sayfadan *beyaz*, koyu temada sayfadan *açık*.
3. **Accent üstündeki mürekkep de temaya bağlıdır.** `--ink-onaccent` sabit beyaz kalırsa koyu temada açık accent üzerinde okunmaz.

Koyu temada yüzey açıklıkları 19-27.5% arasına sıkışır: **parlaklık farkıyla anlam taşımak burada işlemez.** `readonly`/`disabled` gibi ayrımları renksiz bir ipucuyla (kesik kenar, ikon) desteklemek zorunludur — `forms.md`.

Kullanıcı tercihi varsa media query'yi tek kaynak yapma:

```css
:root[data-theme="dark"]  { /* koyu değerler */ }
:root[data-theme="light"] { /* açık değerler */ }
```

## Token olmayan şeyler

- Tek komponentte bir kez kullanılan ölçü — orada dursun
- İçerikten gelen renk (grafik serisi paleti → `design-quality.md`, semantik durum renklerinden türetilir)
- Yüzeye özgü kompozisyon ölçüsü (bir tile'ın span'i)

Her sayıyı token yapmak katmanı okunmaz bir sözlüğe çevirir. Ölçüt: **iki farklı yerde aynı kararı vermek gerekiyorsa token.**

## Doğrulama

```bash
# Komponentte kalmış hardcoded değer
rg -n "#[0-9a-fA-F]{3,8}|rgba?\(|oklch\(" src/components -g '!*tokens*'
rg -n ":\s*\d+px" src/components -g '!*tokens*'
```

- [ ] Komponent dosyalarında palet/spacing/type sabiti yok; hepsi `var(--…)`
- [ ] Token adları rol tabanlı (`--surface-card`), değer tabanlı değil (`--gray-100`)
- [ ] Mürekkep token'larının yanında kontrast oranı yazılı, ≥ 4.5:1
- [ ] Tek işlevsel accent; semantik durum renkleri ondan ayrı
- [ ] Yoğunluk ve grid token'ları kökte, komponentte değil
- [ ] Koyu tema ayrı ayrı seçilmiş; ters çevirme değil, `--ink-onaccent` dahil
- [ ] Mevcut bir token katmanı varsa **o** kullanılmış, ikinci sistem kurulmamış
