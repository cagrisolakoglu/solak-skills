# Yoğunluk ve Yön

Veri-yoğun UI'da **yoğunluk kararı yön seçiminden daha belirleyicidir.** Aynı tablo `comfortable` ile `dense` arasında farklı bir üründür. Bu kararı önce ver.

## Yoğunluk ölçeği

| Seviye | Satır/alan yüksekliği | Gövde metni | Ne zaman |
|--------|----------------------|-------------|----------|
| `comfortable` | 44px | 15-16px | < 20 kayıt, okuma odaklı, dokunmatik kullanım |
| `compact` | 36px | 14px | 20-100 kayıt, karışık kullanım (varsayılan) |
| `dense` | 28px | 13px + `tabular-nums` | 100+ kayıt, tarama ve karşılaştırma odaklı |

```css
:root {
  /* compact — varsayılan */
  --row-height: 36px;
  --row-padding-x: 12px;
  --text-body: 0.875rem;
  --table-border: 1px solid oklch(88% 0 0);
}

[data-density="comfortable"] { --row-height: 44px; --row-padding-x: 16px; --text-body: 0.9375rem; }
[data-density="dense"]       { --row-height: 28px; --row-padding-x: 8px;  --text-body: 0.8125rem; }
```

Yoğunluk bir **token seviyesi**, tek tek komponent kararı değil. Kullanıcıya seçtirilecekse `data-density` özniteliği kök yüzeyde değişir; komponentler hesabı token'dan alır.

## Seviye nasıl seçilir

Üç soru:

1. **Kaç kayıt gösterilecek?** Tipik durumda ve en kötü durumda.
2. **Kullanıcı tarıyor mu, okuyor mu?** Tarama (bir değeri bulmak, satırları karşılaştırmak) yoğunluğu artırır; okuma azaltır.
3. **Hangi ekran ve girdi?** Dokunmatik veya sahada kullanım en az `comfortable` gerektirir — dokunma hedefi ≥ 44px.

Cevaplar bilinmiyorsa **sor.** Varsayılana kaçmak bu skill'in engellemek için var olduğu şey.

Sorular çelişirse (500 kayıt ama dokunmatik saha kullanımı) çakışmayı kullanıcıya söyle ve bir taraf seç: dokunma hedefi erişilebilirlik kısıtıdır, yoğunluk tercihtir — kısıt kazanır.

## Temel ilke: yoğunluk sıkıştırma değildir

Satır yüksekliği düşerken şunlar **artmak** zorunda:

- **Hizalama disiplini** — `dense`'te göz kaymasını önleyen tek şey sütun hizasıdır
- **Ayırıcı netliği** — yükseklik azaldıkça satırları ayıran ipucu güçlenmeli
- **Sayı okunurluğu** — `tabular-nums` `dense`'te zorunlu, opsiyonel değil

Sadece padding kısıp font küçültmek yoğunluk değil, okunmazlıktır.

## Üç yön

| Yön | Ne zaman | Tipografi | Renk | Kompozisyon |
|-----|----------|-----------|------|-------------|
| **Swiss / International** (varsayılan) | Operasyonel ekran: tablo, filtre, form | Tek grotesk aile, ağırlıkla hiyerarşi | Nötr + tek işlevsel accent + semantik durum renkleri | Katı kolon grid, sola hizalı |
| **Editorial-dense** | Rapor, analiz, anlatı taşıyan ekran | Serif başlık + grotesk gövde/veri | Kağıt yüzey, koyu mürekkep, tek accent | Asimetrik: anlatı kolonu + veri bloğu |
| **Bento** | Metrik özeti, dashboard | Kompakt, sayı odaklı, tabular figür | Nötr yüzey + semantik eşik renkleri | **Eşit olmayan** hücreler (2x1, 1x2, 2x2) |

Yönü kullanıcıya **onaylat**; geri alınması pahalı karardır. Karanlık tema varsayılan değildir — ürünün istediği neyse o.

Bir ekranda tek yön. Tablo Swiss, üstündeki özet bento ise bu iki yön değil, bir yön içinde iki bileşendir: ortak token, ortak tipografi, yalnızca kompozisyon farkı.
