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

## Sticky

- Başlık satırı: `position: sticky; top: 0` — 15+ satırda zorunlu
- Kimlik kolonu: yatay kaydırma varsa `position: sticky; left: 0` zorunlu
- Sticky yüzeyin arkası **opak** olmalı; yarı saydam başlık altındaki metni okunmaz yapar
- Sticky öğeye `z-index` ver; kesişimde (başlık × ilk kolon) köşe hücresi en üstte kalmalı

## Tek ayırıcı sistemi

Zebra şeritleri **veya** yatay çizgiler — ikisi birden değil. İkisi birlikte gürültü üretir ve hiçbiri işini yapmaz.

- **Zebra**: `dense` seviyede, çok kolonlu tabloda göz kaymasını engeller
- **Çizgi**: `comfortable`/`compact` seviyede daha temiz
- **Dikey çizgi**: yalnızca kolon grupları varsa

Zebra kullanılıyorsa hover ve seçili durum zebradan **daha güçlü** olmalı, yoksa görünmez.

## Taşan hücre

Uzun metin: tek satırda kısalt (`text-overflow: ellipsis`) **ve** tam değeri erişilebilir kıl — `title` özniteliği veya tooltip. Kısaltıp tam değeri hiç göstermemek veri kaybıdır.

Satır yüksekliğini içeriğe göre büyütmek `dense`/`compact` seviyede tarama ritmini bozar; sabit yükseklik + kısaltma tercih edilir.

## Sıralama ve seçim

- Sıralanabilir başlık `button` olmalı (klavye erişimi); hover'da göstergeyi belli et
- Aktif sıralamada yön oku **ve** hangi kolon olduğu görünür kalsın; `aria-sort` özniteliğini kullan
- Satır tıklaması ile checkbox seçimi **çakışmasın** — tıklama detaya gidiyorsa checkbox ayrı hedef olmalı
- Toplu seçimde kaç kayıt seçildiği ve "tümünü seç" kapsamı (bu sayfa mı, tüm sonuç mu) açıkça yazılmalı

## Toplam satırı

Varsa `position: sticky; bottom: 0`, gövdeden farklı ağırlıkta, sayı hizası gövdeyle **birebir aynı**. Toplam filtreye mi tüm veriye mi ait, belirt.

## Durumlar — hepsi tasarlanacak

| Durum | Tasarım |
|-------|---------|
| İlk kullanım (hiç veri yok) | Ne olduğunu açıkla + ilk eylemi öner. "Kayıt yok" yetersiz. |
| Sonuç yok (filtre sonucu) | **İlk kullanımdan ayrı.** Hangi filtrenin gevşetileceğini öner. |
| Yükleniyor | İskelet satırlar, yüksekliği gerçek satırla **aynı** — yoksa layout shift |
| Kısmi yükleme | Yüklenmiş satırlar görünür, devamı için gösterge |
| Hata | Ne olduğu + tekrar dene eylemi; tabloyu boşaltıp tek satır hata yazma |
| Tek satır | Tablo yerine detay görünümü daha uygun olabilir — sorgula |

İlk kullanım ile "sonuç yok" durumunu aynı bileşenle çözmek en sık yapılan hatadır: kullanıcı sistemin boş mu olduğunu yoksa filtresinin mi kötü olduğunu anlayamaz.

## Erişilebilirlik

- `<table>` + `<th scope="col">` kullan; `div` grid'i ancak sanallaştırma zorunluysa ve `role="grid"` ile
- Klavye: `Tab` ile eylemlere ulaşılır; sıralanabilir başlıklar `button`
- Sanallaştırılmış tabloda toplam satır sayısını ekran okuyucuya bildir — DOM'daki satır sayısı gerçeği yansıtmaz
- Yalnızca hover'da görünen eylem **klavyeyle erişilemez**; `focus-within` ile de görünür olmalı
