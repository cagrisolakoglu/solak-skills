# Tipografi

Yoğun veri yüzeyinde tipografi süs değil **okuma aracıdır**: yanlış figür seti kolon hizasını, yanlış font ailesi tarama hızını, yanlış ağırlık okunurluğu bozar. Sayı biçimi ve yerel ayar (`1.284.690`, ondalık virgül) `formatting.md`'de; burada font, figür ve ağırlık kararları var.

## 1 · Önce mevcut sistemi kullan

Projede tipografi token'ları varsa **onları kullan**, paralel bir ölçek kurma. Arama yöntemi `tokens.md`'de. Bir framework varsayılanı da bir sistemdir: Quasar/Vuetify projesinde Roboto, Material tabanlı bir üründe kendi ölçeği zaten vardır — ürünün fontunu değiştirmek tipografi kararı değil, marka kararıdır ve bu skill'in işi değildir.

## 2 · Sistem yoksa: Inter Variable

```css
:root {
  --font-ui: "Inter Variable", "Inter var", Inter,
             ui-sans-serif, "Segoe UI Variable Text", "Segoe UI", system-ui, sans-serif;
}
```

Inter yoğun UI için tasarlandı: geniş x-height, `1`/`l`/`I` ve `0`/`O` ayrımı net, tabular figür seti tam. Variable sürümü 400-600 arasını tek dosyada verir.

**Fallback zinciri kuralın parçasıdır.** Inter kurulu değilse ve self-host edilmemişse tarayıcı sessizce Arial'a düşer — kural uygulanmış görünür, sonuç uygulanmamıştır. Üç yol, sırayla:

1. **Self-host** (tercih edilen) — `woff2` dosyasını projeye koy, `@font-face` + `font-display: swap`. Tek ağırlık dosyası (variable) yeterli; ayrı ayrı 400/500/600 indirme.
2. **Kurulu varsay** — yalnızca kurumsal imaj yönetimiyle dağıtıldığı biliniyorsa.
3. **Sistem fontuna düş** — Inter yoksa `Segoe UI Variable` / `system-ui` kabul edilebilir; ama o zaman **figür setini doğrula** (aşağı bak), çünkü fallback fontun tabular desteği farklı olabilir.

Hangisi seçildiyse çıktı raporunda yaz. "Inter kullanıldı" demek, gerçekten yüklendiğini kanıtlamaz — ekran görüntüsünde harf formlarına bak.

## 3 · Tablo ve metriklerde monospace yok

Ölçülen sayıda, metrikte, KPI değerinde monospace **kullanma**. Mono her karaktere eşit yer verir; yoğun tabloda kolon gereksiz genişler ve rakamlar seyrekleşerek tarama yavaşlar. `tabular-nums`'lı bir sans zaten basamakları hizalar — mono'nun tek faydasını sağlar, bedelini ödemeden.

## 4 · Sayısal hücrelerde üç ayar birlikte

```css
.num {
  font-variant-numeric: tabular-nums lining-nums;
  text-align: right;
}
```

- **`tabular-nums`** — her rakam eşit genişlik; basamaklar dikey hizalanır
- **`lining-nums`** — rakamlar aynı yükseklikte oturur. Bazı font aileleri **oldstyle** (alçalan `3`, `4`, `7`, `9`) figürleri varsayılan kullanır; `tabular-nums` tek başına bunu düzeltmez, kolon hizalı ama satır zıplayan görünür
- **Sağa hizalama** — tipe göre hizalama tablosu `tables.md`'de
- **Tutarlı ondalık basamak** — kolon boyunca sabit; gerekçesi ve nicelik tablosu `formatting.md`'de

Üçü birlikte olmadan hiçbiri işini yapmaz. Doğrulama: kolonda `1.284.690` ile `98.440`'ın **son hanesi** aynı dikey çizgide mi?

## 5 · Mono yalnızca teknik kimlikte

Monospace'in yeri, karakteri **tek tek** okunan ve dikte edilen değerlerdir:

| Mono | Mono değil |
|------|------------|
| UUID | Tüketim, tutar, yüzde |
| EIC / ETSO kodu | Tarih, saat, dönem (`2026-07`) |
| Sayaç seri no | Kişi adı, tesis adı |
| Endpoint, URL yolu | Durum etiketi |
| Hash, commit sha | Sayfa/kayıt sayısı |
| Log satırı, stack trace | Sıralama/filtre değeri |

```css
:root { --font-mono: "Cascadia Mono", Consolas, ui-monospace, "SF Mono", monospace; }
.ident-tech { font-family: var(--font-mono); font-variant-numeric: tabular-nums lining-nums; letter-spacing: 0; }
```

### 3 ile 5 çakışırsa: içerik kazanır, kap değil

Sayaç seri no bir **tablo kolonunda** yaşar. Kural 3 "tabloda mono yok", kural 5 "sayaç kodu mono" der — çelişki görünür, değildir:

- Kural 3 **ölçülen sayıyı** yönetir: karşılaştırılan, toplanan, ortalaması alınan değer
- Kural 5 **kimliği** yönetir: karşılaştırılmayan, dikte edilen, kopyalanan değer

Karar hücrenin nerede durduğuna değil **ne taşıdığına** bakar. Yani: tüketim kolonu sans + tabular, sayaç no kolonu mono. Aynı tabloda ikisi bir arada olur ve bu doğrudur — kimlik kolonu görsel olarak da ayrışmalı, çünkü işi farklıdır.

Kimlik mono ise **sola hizalanır** (kimlik sayı değildir, `formatting.md`), mono zaten hizalamayı sağladığı için `letter-spacing` eklemeye gerek yoktur.

## 6 · Dense varsayılanları

| Rol | Boyut | Satır yüksekliği | Ağırlık |
|-----|-------|------------------|---------|
| Gövde / hücre | 13px | 1.35 | 400 |
| Başlık / etiket | 12px | 1.3 | 500 |

```css
[data-density="dense"] {
  --text-body:   0.8125rem;  /* 13px */
  --leading-body: 1.35;
  --text-label:  0.75rem;    /* 12px */
  --leading-label: 1.3;
  --weight-body:  400;
  --weight-label: 500;
}
```

500 **varsayılandır**, tavan değil: bir kolonun karar kolonu olduğunu belirtmek için 600 kullanmak meşru bir sapmadır — ama kasıtlı olmalı ve her başlıkta değil.

### Başlık gövdeden küçükse ikinci bir ayırıcı şart

12px başlık, 13px gövdeden küçüktür. Yoğun kurumsal UI'da bu kasıtlıdır ama **yalnızca başlık boyut dışında bir işaret taşırsa** çalışır:

```css
th { text-transform: uppercase; letter-spacing: 0.04em; color: var(--ink-strong); }
```

Uppercase + harf aralığı + güçlü mürekkep olmadan 12px/500 bir başlık, "küçük gövde metni" gibi görünür ve hiyerarşi **ters döner**. Uppercase kullanıyorsan birim sembolleri ve Türkçe `i` için `tables.md`'deki tuzaklara bak.

## 7 · 400'ün altına inme

Yoğun veri yüzeyinde 300 veya daha ince ağırlık kullanma. 13px'te ince gövde, açık zeminde griye düşer ve Windows'un gri tonlamalı yazı tipi düzleştirmesinde kırılır; koyu temada ise tersi olur, ince harf ışır ve kenarları dağılır.

Vurguyu azaltmak gerekiyorsa ağırlığı değil **mürekkebi** düşür: `--ink-body` → `--ink-muted`. Kontrast tabanı (≥ 4.5:1) korunur, harf formu bozulmaz.

## 8 · Minimalizm metni küçültmek değildir

Ekran kalabalık görünüyorsa **font küçültmek yanlış çözümdür**: kalabalığı okunmazlığa çevirir, ölçüyü değiştirir, hiyerarşiyi düzleştirir ve erişilebilirliği bozar.

Azaltılacak şeyler, bu sırayla:

1. **Renk** — kaç farklı renk var? Semantik olmayan her rengi çıkar
2. **Ayırıcı** — zebra *veya* çizgi, ikisi birlikte değil (`tables.md`); kutu içinde kutu yok
3. **Vurgu** — kaç öğe kalın/accent renkli? Her şey vurguluysa hiçbiri vurgulu değil
4. **İçerik** — bir soruyu cevaplamayan tile, kolon veya alan (`design-quality.md`)
5. **Boşluk** — grup arası korunur, süs boşluk kısılır

Yoğunluk seviyesini düşürmek (`compact` → `dense`) bir *token* kararıdır ve satır yüksekliğiyle birlikte gelir; tek başına `font-size` küçültmek yoğunluk değil, sıkıştırmadır (`density-and-direction.md`).

## Doğrulama

- [ ] Mevcut tipografi sistemi varsa kullanıldı; ikinci ölçek kurulmadı
- [ ] Sistem yoksa Inter Variable **gerçekten yüklendi** (self-host veya doğrulanmış kurulum); fallback stratejisi raporlandı
- [ ] Ölçülen sayı ve metriklerde monospace yok
- [ ] Sayısal hücrelerde `tabular-nums lining-nums` + sağa hizalama + sabit ondalık
- [ ] Kolondaki en uzun ve en kısa sayının son hanesi aynı dikey çizgide
- [ ] Mono yalnızca teknik kimlikte (UUID, EIC, sayaç no, endpoint, hash, log); kimlik sola hizalı
- [ ] Dense'te gövde 13/1.35/400, başlık 12/1.3/500; sapmalar kasıtlı
- [ ] 400 altı ağırlık yok; soluklaştırma mürekkeple yapılmış
- [ ] Kalabalık çözümü metin küçültmek değil; renk/ayırıcı/vurgu azaltılmış
