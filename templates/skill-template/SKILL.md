---
name: solak-<eylem>-<hedef>
description: <Skill'in ne yaptığı ve NE ZAMAN devreye girmesi gerektiği. Üçüncü şahıs, tek paragraf. Tetikleyici ifadeleri açıkça yaz — model bu alana bakarak skill'i seçer. "Use when the user ..." kalıbıyla bitir.>
metadata:
  version: 0.1.0
  author: cagrisolakoglu
  tags: [<etiket>, <etiket>]
  status: draft   # draft | stable | deprecated
---

# solak-<eylem>-<hedef>

<Bir cümlelik amaç.>

## When to Use

- <Tetikleyici durum 1>
- <Tetikleyici durum 2>

Bu skill'i **kullanma**: <kapsam dışı kalan, karışabilecek durum>.

## Inputs

| Girdi | Zorunlu | Açıklama |
|-------|---------|----------|
| `<arg>` | ✅ | <ne beklendiği> |
| `<arg>` | ❌ | <varsayılan davranış> |

Girdi eksikse: <sor mu, varsayılanla devam mı — açıkça yaz>.

## Workflow

1. **<Adım adı>** — <yapılacak iş, kullanılacak araç.>
2. **<Adım adı>** — <...>
3. **<Adım adı>** — <...>
4. **Doğrula** — <çıktının doğru olduğu nasıl kanıtlanır: komut, test, kontrol listesi.>

## Output

<Kullanıcının eline ne geçiyor: dosya, rapor, PR yorumu, tablo. Varsa format örneği ver.>

```
<çıktı örneği>
```

## Guardrails

- <Yapılmaması gereken şey (dosya silme, force push, secret yazma vb.).>
- <Onay gerektiren adım.>
- Belirsizlik varsa tahmin etme; kullanıcıya sor.

## Examples

```
/solak-<eylem>-<hedef> <örnek argüman>
```

<Beklenen davranışın kısa anlatımı.>
