---
name: solak-design-ui
description: Designs and implements data-dense enterprise UI — tables and data grids, filter and query panels, data-entry forms, and metric dashboards. Decides row/field density deliberately, aligns numbers and text by type, designs the states real data produces (empty, loading, partial, error, overflow, too-many-results), and keeps everything on the project's token layer. Tech-agnostic: semantic HTML + CSS custom properties, adapted to the detected framework. Use when the user works on a table, grid, filter panel, form, report screen or dashboard — "tabloyu düzelt", "filtre paneli tasarla", "bu ekran kalabalık", "dashboard yap" — or invokes /solak-design-ui. For marketing pages, landing pages and brand surfaces, prefer `frontend-design`.
metadata:
  version: 0.2.0
  author: cagrisolakoglu
  tags: [design, frontend, ui, data-dense, enterprise]
  status: draft
---

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

1. **Bağlamı oku** — Token katmanı, mevcut tablo/form kalıpları, tema desteği, framework tespiti (dosya uzantıları ve paket dosyası).
2. **Yüzeyi tespit et** — Hangi yüzey olduğunu belirle ve **yalnızca ilgili referansı oku**:
   - Tablo / veri grid'i → `references/tables.md`
   - Filtre / arama / sorgu paneli → `references/filters.md`
   - Veri giriş formu → `references/forms.md`
   - Dashboard / metrik özeti → `references/dashboards.md`
   Yüzeyden bağımsız **kesişen** referanslar:
   - `references/grid.md` — çok alanlı/çok kolonlu her yüzeyde zorunlu (yatay ritim)
   - `references/formatting.md` — sayı, tarih, birim veya para görünen her yüzeyde zorunlu
   - `references/tokens.md` — token katmanı yoksa veya mevcut katman okunacaksa
3. **Yoğunluğu karara bağla** — `references/density-and-direction.md`: `comfortable` / `compact` / `dense`. Karar üç sorudan çıkar (kayıt sayısı, tarama mı okuma mı, ekran ve girdi). Gerekçeyi çıktı raporunda yaz.
   Yoğunluk **dikey** ritmi kurar, grid **yatay** ritmi; çok alanlı yüzeyde ikisi birlikte karara bağlanır.
4. **Yön seç** — Aynı referanstan üç yön (Swiss / editorial-dense / bento). Tek cümleyle gerekçelendir ve **kullanıcıya onaylat**. Karanlık temayı varsayma.
5. **Token'ları kullan veya yaz** — Mevcut token katmanı varsa **onu kullan**, paralel sistem kurma. Yoksa `references/tokens.md`'ye göre palet, type scale, spacing, yoğunluk, **kolon sayısı ve oluk**, duration/easing'i CSS custom property olarak tanımla.
6. **Kodla** — Semantik HTML (`table`/`th`/`fieldset`/`label`, generic `div` yığını değil). Yüzey referansındaki durumların **hepsi** ve etkileşim state'leri: hover, `focus-visible`, active, disabled/readonly, seçili.
7. **Motion (varsa)** — Yalnızca `transform`, `opacity`, `clip-path`. `prefers-reduced-motion` karşılığını yaz.
8. **Doğrula** — Aşağıdaki kapıları çalıştır, sonucu raporla. Mümkünse 320/768/1440 ekran görüntüsü al (`/run`, Playwright).

Anti-template kalıpları ve genel tasarım kalitesi nitelikleri için global `web/design-quality.md` kuralı geçerlidir; burada tekrar edilmez.

## Doğrulama kapıları

**Bloklayan** — biri geçilmezse iş **tamamlanmadı**, eksiği açıkça yaz:

- [ ] Metin kontrastı ≥ 4.5:1 (büyük metin ≥ 3:1); durum renkleri dahil
- [ ] Renk tek gösterge değil — ikon veya metin eşlik ediyor
- [ ] Klavye ile gezinilebiliyor, `focus-visible` görünür; grid/form içi gezinme dahil
- [ ] Boş / yükleniyor / hata durumları var
- [ ] Ölçülen sayılar `tabular-nums` ve sağa hizalı; kimlik numaraları sola (`references/formatting.md`)
- [ ] Sayı/tarih biçimi yerel ayara uygun ve elle kurulmamış (`Intl`); ondalık basamak kolon boyunca sabit
- [ ] Eksik veri sıfırdan ayırt edilebiliyor (`—`), hesaba dahil edilmemiş
- [ ] Komponentte hardcoded palet / spacing / type değeri yok
- [ ] 320px'te taşma yok **veya** daralma stratejisi açıkça beyan edilmiş
- [ ] Alanlar/kolonlar ortak grid çizgilerinden başlıyor — içerik genişlikli flex ile dizilmiş "her biri kendi genişliğinde" yerleşim yok (`references/grid.md`)
- [ ] `readonly` ile `disabled` **koyu temada da** ayırt edilebiliyor

**Bildirilen** — eksikse raporla, iş durmaz:

- [ ] Kısmi veri / çok fazla sonuç / taşan hücre durumları
- [ ] `prefers-reduced-motion` karşılığı
- [ ] İki tema da kasıtlı duruyor
- [ ] Yoğunluk seçimi gerekçelendirilmiş
- [ ] Toplam ham değerlerden hesaplanmış; yuvarlama farkı beyan edilmiş

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
