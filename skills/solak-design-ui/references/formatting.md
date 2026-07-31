# Sayı, Tarih ve Birim Biçimi

Veri-yoğun ekranda biçim kozmetik değil: yanlış biçimlenmiş sayı **yanlış okunur**, yanlış okunan sayı yanlış karar üretir. Hizalama kuralları için `tables.md`, alan genişliği için `forms.md`.

## Yerel ayarı ürün belirler, kod uydurmaz

Türkçe arayüzde `tr-TR`: **binlik ayırıcı nokta, ondalık ayırıcı virgül.**

| Değer | ✅ tr-TR | ❌ |
|-------|---------|----|
| Endeks | `1.284.690` | `1,284,690` · `1 284 690` · `1284690` |
| Tüketim | `13.240,75` | `13,240.75` |
| Yüzde | `%12,4` | `12.4%` · `% 12,4` |
| Para | `1.284.690,00 ₺` | `₺1,284,690.00` |

Biçimi elle kurmak (regex, `replace`, string birleştirme) yanlış yerde yuvarlar ve negatif sayıyı bozar. **`Intl` kullan:**

```js
const kwh = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 });
const money = new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' });
const pct = new Intl.NumberFormat('tr-TR', { style: 'percent', maximumFractionDigits: 1 });

kwh.format(1284690);      // "1.284.690"
money.format(1284690);    // "1.284.690,00 ₺"
pct.format(0.124);        // "%12,4"
```

Tarayıcı diline güvenme; yerel ayar ürün ayarından (veya kullanıcı tercihinden) gelir, `navigator.language`'dan değil. Aksi halde aynı veri iki makinede iki farklı sayı gibi görünür.

Girdi tarafında **biçimi kullanıcıya dayatma.** Doğrulama `1.284.690`, `1284690` ve `1 284 690`'ı kabul eder; kaydetmeden önce normalize eder. Kullanıcıyı ayırıcı koymaya zorlamak veri girişini yavaşlatır.

## Kimlik numarası sayı değildir

Sayaç seri no, fatura no, EIC/ETSO kodu, tesis kodu, dönem (`2026-07`), vergi no — bunlar rakamdan oluşur ama **ölçüm değildir**: toplanmaz, karşılaştırılmaz, ortalaması alınmaz.

| | Ölçülen sayı | Kimlik |
|--|--------------|--------|
| Hizalama | **Sağa** | **Sola** (metin gibi) |
| Binlik ayırıcı | Var | **Yok** — `4471 0982 331` kendi bloklamasını korur |
| Tabular figür | Zorunlu | Faydalı (basamak saymayı kolaylaştırır) |
| Yuvarlama | Olabilir | Asla |

```css
.num   { font-variant-numeric: tabular-nums; text-align: right; }
.ident { font-variant-numeric: tabular-nums; text-align: left; letter-spacing: 0.02em; }
```

Kimliği sağa hizalamak onu toplanabilir bir miktar gibi gösterir; kolondaki gözü de boşa yorar.

## Hassasiyet kolon boyunca sabittir

Bir kolonda ondalık basamak sayısı **değişmez.** `13.240` ile `13.240,75` aynı kolonda görünüyorsa basamaklar hizalanmaz ve karşılaştırma biter.

```
✅ 13.240,00   ❌ 13.240
    9.180,50        9.180,5
      412,25          412,25
```

Hassasiyet niceliğin türünden gelir, verinin o anki halinden değil:

| Nicelik | Basamak | Neden |
|---------|---------|-------|
| Endeks (kWh) | 0 | Sayaç tam sayı okur |
| Tüketim (kWh) | 0 veya 2 | Çarpanla hesaplanır; kararı bir kez ver |
| Güç (MW) | 2-3 | Küçük fark anlamlı |
| Birim fiyat (₺/MWh) | 2 | Piyasa kotasyonu |
| Tutar (₺) | 2 | Kuruş |
| Oran (%) | 1 | Daha fazlası gürültü |

## Birim etiketi hücrede değil başlıkta

Birim kolon başlığında veya alan etiketinde bir kez yazılır: `Önceki Endeks (kWh)`. Her hücrede tekrarlamak (`1.284.690 kWh`) sayıyı boğar ve sağa hizalamayı bozar — göz artık rakam yerine harf kenarı takip eder.

Tek bir değer gösteriliyorsa (KPI tile, türetilmiş blok) birim değerin yanındadır ama **daha küçük ve soluk**; sayı baskın kalır.

**Bir kolonda tek birim.** Aynı kolonda kWh ile MWh karıştırmak bin kat hata üretir; birim kayıt başına değişiyorsa ya hepsini tek birime çevir ya da birimi ayrı kolona al ve bunu başlıkta belirt.

## Tarih ve saat

- Tarih: `GG.AA.YYYY` → `31.07.2026`. Placeholder olarak da bu maskeyi göster.
- Saat: 24 saat, `HH:mm` → `14:32`. AM/PM Türkçe arayüzde yok.
- Tarih + saat: `31.07.2026 14:32`
- Dönem: `2026-07` — bu bir **kimlik**, tarih değil; sola hizalı, yerel biçime çevrilmez.
- API ve URL: ISO 8601 (`2026-07-31T14:32:00+03:00`). Yerelleştirme yalnızca görüntüde.
- Tek tabloda **tek format**. `31.07.2026` ile `2026-07-31` aynı kolonda görünmez.

```js
const dt = new Intl.DateTimeFormat('tr-TR', { dateStyle: 'short', timeStyle: 'short' });
```

### Zaman damgası ve saat dilimi

Enerji verisi saatliktir ve saat dilimi bir görüntü tercihi değil, **veri doğruluğu** meselesidir:

- Türkiye 2016'dan beri kalıcı UTC+3; yaz saati uygulaması **yok**.
- 2016 öncesi veride yaz saati geçişleri **var**: 23 saatlik ve 25 saatlik günler. Geçmiş uzlaştırma verisi gösteren ekran günün 24 saat olduğunu varsayamaz.
- Saatlik seride hangi ucun dahil olduğunu yaz: `14:00-15:00` mı, `14:00` etiketiyle o saatin tamamı mı. Belirsizlik bir saatlik kaymayla sonuçlanır.

## Eksik veri sıfır değildir

Üç farklı durum, üç farklı gösterim:

| Durum | Gösterim | Anlamı |
|-------|----------|--------|
| Ölçüldü, değer sıfır | `0` | Tüketim olmadı |
| Henüz ölçülmedi | `—` | Veri bekleniyor |
| Ölçülemedi / hatalı | `—` + neden | Arıza, erişim yok |

`—` hücresi hesaba girmez: toplam satırında ve ortalamada bu satırlar **hariç tutulur**, hariç tutulduğu da yazılır ("3 sayaç okunamadı, ortalamaya dahil değil"). Eksiği sıfır sayarak hesaplanan ortalama, kimsenin fark etmediği yanlış karardır.

## Negatif değer ve işaret

- Eksi işareti kullan (`-1.240`), muhasebe parantezi (`(1.240)`) kurumsal ekranda okunmaz.
- İşaret **renk değil** birincil göstergedir; renk ikinci kanal.
- Yön ile iyi/kötü ayrı şeyler: üretim eksiye düştüyse bu "kötü", tüketim eksiye düştüyse muhtemelen "veri hatası". Neyin beklendiğini bağlam metniyle söyle.
- Sıfırın altına düşmesi imkansız bir nicelikte eksi değer görünüyorsa bu bir **veri hatası göstergesidir**, biçim sorunu değil — sessizce `0` gösterme.

## Yuvarlama: gösterilenlerin toplamı ile gösterilen toplam

Satırları yuvarlayıp gösterirsen, kullanıcının topladığı sayı ile toplam satırındaki sayı **tutmaz**.

```
1.240,4 → 1.240        Toplam ham değerlerden: 3.720,9 → 3.721
1.240,3 → 1.240        Gösterilenlerin toplamı: 3.720
1.240,2 → 1.240        Fark: 1
```

Kural: **toplamı her zaman ham değerlerden hesapla, yuvarlamayı en son yap.** Fark kalıyorsa ve kullanıcı elle topluyorsa (fatura, uzlaştırma) dipnot düş: "Satırlar tam sayıya yuvarlanmıştır; toplam ham değerlerden hesaplanır." Sessiz bir birim fark, faturada güven kaybıdır.

## Kısaltma yalnızca dashboard'da

`1,2 mn kWh` gibi kısaltma operasyonel tabloda **yasak** — kullanıcı orada tam değeri karşılaştırıyor. KPI tile'ında kabul edilir ama:

- Birim ve büyüklük açıkça yazılır (`mn kWh`, `GWh`)
- Kesin değere erişim kalır (tooltip, detay ekranı)
- Kolon içinde kısaltma tutarlı olur; bir satır `980 bin`, öteki `1,2 mn` olmaz — ölçeği kolon seçer

## Doğrulama

- [ ] Sayılar `Intl` ile biçimlenmiş, elle string birleştirme yok
- [ ] tr-TR: binlik nokta, ondalık virgül; yüzde ve para doğru
- [ ] Kimlik numaraları sola hizalı, ayırıcı eklenmemiş, yuvarlanmamış
- [ ] Ondalık basamak sayısı kolon boyunca sabit
- [ ] Birim başlıkta bir kez; bir kolonda tek birim
- [ ] Tarih tek formatta (`GG.AA.YYYY`), saat 24 saat
- [ ] Eksik veri `—`, sıfırdan ayırt edilebilir, hesaba dahil değil
- [ ] Toplam ham değerlerden hesaplanmış; yuvarlama farkı varsa beyan edilmiş
- [ ] Operasyonel tabloda kısaltılmış sayı yok
