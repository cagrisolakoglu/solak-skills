---
name: solak-design-ui
description: Designs and implements distinctive, production-grade UI — commits to a specific style direction, defines a deliberate palette and type pairing, builds hierarchy through scale and rhythm, and ships responsive accessible frontend code with designed interaction states. Explicitly rejects generic template output (default card grids, centered-hero-with-gradient-blob, unmodified library defaults). Use when the user asks to build or style a page, screen, component, landing page or dashboard, wants existing UI made less generic ("bu template gibi durmuş", "tasarımı iyileştir", "make this look designed"), or invokes /solak-design-ui.
metadata:
  version: 0.1.0
  author: cagrisolakoglu
  tags: [design, frontend, ui, css]
  status: draft
---

# solak-design-ui

Bir ekranı veya komponenti, belirli bir tasarım yönüne bağlı kalarak üretim kalitesinde tasarlar ve kodlar.

## When to Use

- Yeni bir sayfa, ekran veya komponent tasarlanacak (landing, dashboard, form, kart, tablo).
- Mevcut UI "default Tailwind/shadcn şablonu" gibi duruyor ve karakter kazanması gerekiyor.
- Bir komponentin hover/focus/active/empty/loading state'leri eksik veya özensiz.

Bu skill'i **kullanma**:
- Tasarım sistemi/token katmanı sıfırdan kurulacaksa → o iş daha geniş, ayrı ele al.
- Sorun görsel değil davranışsalsa (state yönetimi, veri akışı, bug) → doğrudan kodu düzelt.
- Kullanıcı sadece tek bir CSS değeri değiştirmek istiyorsa → gereksiz ağırlık, direkt yap.

## Inputs

| Girdi | Zorunlu | Açıklama |
|-------|---------|----------|
| hedef yüzey | ✅ | Hangi sayfa/komponent. Var olan dosya yolu veya sıfırdan tanım. |
| ürün bağlamı | ✅ | Ne işe yarıyor, kim kullanıyor, hangi tonu istiyor. Yoksa **sor** — bağlamsız tasarım jenerik olur. |
| stil yönü | ❌ | Verilmezse `references/style-directions.md`'den 2-3 aday öner ve onay al. Kendi başına seçip ilerleme. |
| teknoloji | ❌ | Repodan tespit et (React/Angular/plain HTML, Tailwind/CSS modules). Tespit edilemezse sor. |
| kısıt | ❌ | Mevcut palet, marka, erişilebilirlik seviyesi, performans bütçesi. |

"Clean minimal", "modern", "şık" gibi girdiler **yön değildir** — somut bir yöne çevirip onay al.

## Workflow

1. **Bağlamı oku** — Mevcut kod varsa: token dosyası, tipografi, komponent kalıpları, tema desteği. Yeni projede: teknoloji ve varsa marka kısıtları.
2. **Yön belirle** — `references/style-directions.md`'den somut bir yön seç ve **tek cümleyle gerekçelendir**. Karanlık temayı otomatik varsayma; ürünün istediği yönü seç.
3. **Paleti ve tipografiyi karara bağla** — Renkler semantik rolleriyle (surface / text / accent / danger), tipografi gerçek bir pairing stratejisiyle. En fazla iki font ailesi. Kontrast oranlarını (metin ≥ 4.5:1) burada doğrula, sonda değil.
4. **Kompozisyonu planla** — Ölçek kontrastıyla hiyerarşi, düzensiz ama kasıtlı ritim, katmanlanma (overlap/gölge/yüzey). Grid'i kırmak uygunsa editorial veya bento kompozisyon kullan. Her yere aynı padding'i dağıtma.
5. **Token'ları yaz** — Palet, type scale, spacing, duration ve easing'i CSS custom property olarak tanımla. Palet/tipografi/spacing değerlerini komponent içine hardcode etme.
6. **Komponenti kodla** — Semantik HTML (`header`/`nav`/`main`/`section`, generic `div` yığını değil). Hover, focus-visible, active, disabled, empty ve loading state'lerinin **hepsi** tasarlanmış olacak.
7. **Motion ekle (varsa)** — Yalnızca `transform`, `opacity`, `clip-path`. `width`/`height`/`top`/`margin` animasyonu yok. `prefers-reduced-motion` karşılığını yaz.
8. **Doğrula** — Aşağıdaki kontrol listesini çalıştır ve sonucu raporla. Mümkünse 320 / 768 / 1440 genişliklerinde ekran görüntüsü al (bkz. `/run`, Playwright).

### Doğrulama kontrol listesi

- [ ] Yön seçimi açıkça belirtilmiş ve gerekçeli
- [ ] Palet ve type scale token olarak tanımlı; komponentte hardcoded değer yok
- [ ] Metin kontrastı ≥ 4.5:1 (büyük metin ≥ 3:1)
- [ ] hover / focus-visible / active / disabled / empty / loading state'leri var
- [ ] Klavye ile gezinilebiliyor, focus göstergesi görünür
- [ ] 320 / 768 / 1440'ta yatay taşma yok
- [ ] Motion yalnızca compositor-dostu property'lerde; `prefers-reduced-motion` karşılanmış
- [ ] Görsellerde açık `width`/`height` var (layout shift yok)
- [ ] İki tema destekleniyorsa ikisi de kasıtlı duruyor
- [ ] [Anti-template testi](#anti-template-testi) geçildi

### Anti-template testi

Aşağıdakilerden **hiçbiri** olmayacak:
- Tek tip aralıklı, hiyerarşisiz varsayılan kart grid'i
- Ortalanmış başlık + gradient blob + jenerik CTA hero'su
- Değiştirilmemiş kütüphane varsayılanlarının bitmiş tasarım gibi sunulması
- Her komponentte aynı radius, gölge ve spacing
- Tek dekoratif vurgu rengiyle güvenli gri-üstü-beyaz
- Sebepsiz varsayılan font stack

Ve şu niteliklerden **en az dördü** olacak: ölçek kontrastıyla hiyerarşi · kasıtlı ritim · katman/derinlik · karakterli tipografi pairing · semantik renk · tasarlanmış etkileşim state'leri · grid kıran kompozisyon · doku/atmosfer · akışı netleştiren motion · tasarım sistemine dahil veri görselleştirme.

## Output

Kod artı kısa bir tasarım notu:

```
Yön: editorial / high-contrast serif + grotesk pairing
Gerekçe: içerik-ağırlıklı rapor ekranı; okunabilirlik ve otorite gerekiyor

Dosyalar
  + src/styles/tokens.css          palet, type scale, spacing, easing
  + src/components/report/ReportHeader.tsx
  ~ src/components/report/report.css

Kararlar
  - Accent oklch(62% 0.19 25) — yalnızca eylem ve uyarıda, dekoratif kullanım yok
  - Başlık ölçeği 4.2x gövde — hiyerarşi ağırlıktan değil ölçekten geliyor
  - Kartlar arası ritim 1:1.6 — tek tip padding yerine kasıtlı asimetri

Doğrulama
  ✅ kontrast 7.1:1 · ✅ 320/768/1440 taşma yok · ✅ klavye + focus-visible
  ⚠️  reduced-motion karşılığı eklendi, gerçek cihazda denenmedi
```

## Guardrails

- **Bağlam yoksa tasarlama.** Ürün/kullanıcı/ton bilinmiyorsa sor; jenerik çıktı bu skill'in tam olarak engellemek için var olduğu şey.
- **Yön seçimini kullanıcıya onaylat.** Yön, geri alınması pahalı olan karardır.
- Mevcut token/palet varsa **onu kullan**; paralel ikinci bir sistem kurma.
- Mevcut stil dosyalarını okumadan üzerine yazma.
- Erişilebilirliği estetik uğruna feda etme — kontrast ve focus göstergesi pazarlık konusu değil.
- Bağımlılık ekleme (animasyon/UI kütüphanesi) **istenmediyse**; CSS ile çözülüyorsa CSS ile çöz.

## Examples

```
/solak-design-ui src/app/reports/page.tsx "enerji tüketim raporu, saha mühendisi kullanıyor, yoğun veri"
/solak-design-ui "landing page for V-Market, kurumsal alıcılar, güven vermeli"
/solak-design-ui src/components/ui/Button.tsx "bu buton kütüphane defaultu gibi, state'leri tasarla"
```

Üçüncü örnekte skill tüm sayfayı yeniden tasarlamaz; kapsamı butonun state'leri ve token uyumuyla sınırlı tutar.
