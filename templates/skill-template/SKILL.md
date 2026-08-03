---
name: solak-<eylem>-<hedef>
description: <Skill'in ne yaptığı ve NE ZAMAN devreye girmesi gerektiği. Üçüncü şahıs, tek paragraf. Tetikleyici ifadeleri açıkça yaz — model bu alana bakarak skill'i seçer. "Use when the user ..." kalıbıyla bitir.>
metadata:
  version: 0.1.0
  author: cagrisolakoglu
  tags: [<etiket>, <etiket>]
  status: draft   # draft → beta (temiz oturumda koşuldu) → stable (gerçek işte dayandı)
---

<!-- Aşağıdaki bölümlerden When to Use / Inputs / Workflow / Output / Guardrails / Examples
     ZORUNLUDUR. "Kapsam sınıflandırması", "TODO", "Doğrulama kapıları" bölümleri
     KOŞULLUDUR: skill'in yanlış çalışması ne kadar pahalıysa o kadarı gerekir.
     Merdiven docs/skill-development-guide.md → "Aşamalı yürütme" bölümünde.
     Gerekmeyen bölümü sil — boş bırakma. -->

# solak-<eylem>-<hedef>

<Bir cümlelik amaç.>

## When to Use

- <Tetikleyici durum 1>
- <Tetikleyici durum 2>

Bu skill'i **kullanma**: <kapsam dışı kalan, karışabilecek durum>.

## Kapsam sınıflandırması

<!-- KOŞULLU: yalnızca istek küçük de büyük de gelebiliyorsa. Tek bir iş yapan
     skill'de bu bölümü sil. -->

İşe başlamadan önce isteğin büyüklüğünü belirle. **Yanlış süreç gerçek bir hatadır.**

| Kapsam | Tipik istek | Süreç |
|--------|-------------|-------|
| **<küçük>** | <örnek> | <en kısa yol: incele → düzelt → doğrula> |
| **<orta>** | <örnek> | <yerel kontrol → TODO → uygula> |
| **<büyük>** | <örnek> | <tam akış> |
| **<kapsam dışı>** | <örnek> | <neden dışarıda, nereye yönlendirilir> |

Kapsam **isteğin sözlerine değil, gereken işe** göre belirlenir. İkisi çelişiyorsa bunu söyleyip devam et.

## Inputs

| Girdi | Zorunlu | Açıklama |
|-------|---------|----------|
| `<arg>` | ✅ | <ne beklendiği> |
| `<arg>` | ❌ | <varsayılan davranış> |

Girdi eksikse: <sor mu, varsayılanla devam mı — açıkça yaz>.

<!-- Kapsam sınıflandırması varsa: hangi girdinin hangi kapsamda zorunlu olduğunu yaz.
     Küçük bir düzeltme için kullanıcıyı sorguya çekme. -->

## Workflow

1. **<Adım adı>** — <yapılacak iş, kullanılacak araç.> *Kapı: <bu adım bitmeden sonrakine geçilmemesini sağlayan somut koşul.>*
2. **<Adım adı>** — <...>
3. **<Uygulama listesi>** — Bağımlılık sırasına dizilmiş, dosya düzeyinde, her kalemi tek doğrulanabilir sonuç üreten liste. **Beş kalem ve üstü ayrı dosyaya, altı satır içi listeye.** *Kapı: liste yoksa kod yazılmaz.*
4. **<Kalem kalem yürüt>** — Her kalem için: dosyaları oku → kabul ölçütünü yeniden söyle → en küçük değişikliği yap → kontrolleri çalıştır → doğrula → tamamlandı işaretle.
5. **Doğrula ve raporla** — <çıktının doğru olduğu nasıl kanıtlanır: komut, test, kontrol listesi.>

<!-- Kapılar ve TODO yalnızca merdivenin üst basamaklarında gerekir. Tek adımlık,
     geri alınabilir bir işte 1 ve 5 yeter. -->

## Doğrulama kapıları

<!-- KOŞULLU: geri alınması pahalı iş yapan skill'lerde zorunlu. -->

**Bloke edici** — biri geçmezse iş **bitmemiştir**; neyin eksik olduğunu açıkça söyle:

- [ ] <somut, kontrol edilebilir koşul>
- [ ] <...>

**Raporlanan** — eksikse söyle, iş durmaz:

- [ ] <...>

Kapsam sınıflandırması varsa kapılar da kapsamlanır: küçük bir düzeltme yalnızca **kendi değişiminin dokunduğu** kapıları yanıtlar. **Kontrol edilmemiş bir kapıyı iddia etmek, kontrol edilmedi demekten kötüdür.**

## Output

<Kullanıcının eline ne geçiyor: dosya, rapor, PR yorumu, tablo. Varsa format örneği ver.>

```
<çıktı örneği>

Doğrulanmadı: <neyin denenmediği — bu satır raporun en değerli kısmı>
```

## Guardrails

- <Yapılmaması gereken şey (dosya silme, force push, secret yazma vb.).>
- <Onay gerektiren adım.>
- Belirsizlik varsa tahmin etme; kullanıcıya sor — ama sormaya bağlı olmayan işi önce bitir.
- Her mikro adımda onay isteme; pahalı ve geri alınamaz kararları tek mesajda topla.
- Neyi doğrulamadığını raporla; geçmiş gibi gösterme.

## Examples

```
/solak-<eylem>-<hedef> <örnek argüman>
```

<Beklenen davranışın kısa anlatımı.>
