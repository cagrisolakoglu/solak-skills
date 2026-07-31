# Veri Giriş Formu

## Gruplama ve ritim

Alanları anlamsal gruplara ayır (`fieldset` + `legend`); grup arası boşluk alan arası boşluğun **en az iki katı**. Tek tip aralık, uzun formu okunmaz bir liste yapar.

```css
.form-field { margin-block-end: var(--space-field); }  /* 16px */
.form-group { margin-block-end: var(--space-group); }  /* 40px */
```

## Etiket üstte

Etiket alanın üstünde, sola hizalı. Tarama hızı en yüksek yerleşim budur ve uzun etiketlerde bozulmaz.

Sol yerleşim (etiket solda, alan sağda) kolon genişliğini etikete esir eder. Yer içi (placeholder) etiket ise **etiket değildir** — odaklanınca kaybolur, kullanıcı ne girdiğini doğrulayamaz. Placeholder yalnızca biçim ipucu için: `GG.AA.YYYY`.

## Zorunluluk işaretlemesi

**Alanların çoğu zorunluysa, isteğe bağlı olanı işaretle** — tersi değil. Her alanın yanında yıldız görmek hiçbir bilgi taşımaz.

```html
<label for="note">Not <span class="field-optional">(isteğe bağlı)</span></label>
```

## Doğrulama zamanlaması

- **`blur`'da doğrula** — her tuş vuruşunda değil. Yazarken hata göstermek kullanıcıyı cümlesinin ortasında suçlar.
- Bir alan hatalıysa ve kullanıcı düzeltiyorsa, doğru hale geldiği anda hatayı **kaldır** — bu durumda anlık geri bildirim doğrudur.
- Gönderimde tüm hataları göster ve ilk hataya odaklan.
- Sunucu tarafı doğrulama sonucu da aynı yere, aynı biçimde düşmeli; ayrı bir hata kanalı kurma.

## Hata mesajı

Alanın **altında**, alana `aria-describedby` ile bağlı, ne yapılacağını söyleyen tonda.

| ❌ | ✅ |
|----|-----|
| "Geçersiz değer" | "Tarih GG.AA.YYYY biçiminde olmalı" |
| "Hata: alan zorunlu" | "Tesis seçilmeli" |
| "Format hatalı" | "Vergi numarası 10 haneli olmalı — şu an 9 hane" |

```html
<input id="tax" aria-describedby="tax-error" aria-invalid="true">
<p id="tax-error" class="field-error">Vergi numarası 10 haneli olmalı — şu an 9 hane.</p>
```

Hata rengi tek gösterge olamaz: ikon veya metin eşlik etmeli.

Uzun formda ayrıca üstte özet blok: kaç hata var, her biri ilgili alana bağlantı.

## disabled ile read-only ayrımı

| Durum | Ne demek | Görsel |
|-------|----------|--------|
| `disabled` | Şu an değiştirilemez, **nedeni belirtilmeli** | Soluk, odaklanılamaz |
| `readonly` | Değer bilgi olarak var, değiştirilemez | Normal kontrast, odaklanılabilir, kopyalanabilir |

Gösterilen bir değeri `disabled` yapmak okunmaz hale getirir — bilgi amaçlıysa `readonly` kullan. `disabled` bir alanın yanında neden kapalı olduğu yazılmalı: "Tesis seçilmeden birim seçilemez".

### İkisini aynı griye boyamak en sık yapılan hata

Her ikisine "çökmüş yüzey + soluk kenar" verilirse ayrım yalnızca metin renginde kalır, gözle görünmez. Ayrımı **üç ayrı eksene** dağıt:

```css
/* readonly = basılı değer, kontrol değil: dolgu yok, tam kontrast mürekkep */
input[readonly] { background: transparent; border-color: var(--line); color: var(--ink-strong); }
input[readonly]:hover { border-color: var(--line); }   /* kontrol gibi tepki vermez */

/* disabled = kapalı kontrol: çökmüş dolgu + soluk mürekkep + KESİKLİ kenar */
input[disabled], select[disabled] {
  background: var(--surface-sunken);
  border: 1px dashed var(--line-strong);
  color: var(--ink-muted);
  cursor: not-allowed;
}
```

Kesikli kenar süs değil, **koyu tema zorunluluğu.** Açık temada dolgu farkı işi görür; koyu temada girdi yüzeyi %27.5, kart %24, çökmüş yüzey %21 olur — üçü aynı koyu griye çıkar, parlaklık farkı yok olur. Kapalılığı renkten bağımsız bir ipucu (kesik kenar, kilit ikonu, neden metni) taşımak zorundadır. Aynı gerekçe gri tonlamalı çıktı ve düşük parlaklıklı ekran için de geçerli.

Doğrulaması tek adım: **koyu temada ekran görüntüsü al, readonly ile disabled alanı yan yana karşılaştır.** Ayırt edemiyorsan kullanıcı da edemez.

## Alan genişliği içerikle eşleşir

Posta kodu, vergi no, tutar gibi sabit uzunluklu alanlar **tam genişlik olmaz.** Genişlik beklenen karakter sayısını gösterir ve hata yapmayı azaltır.

Bu kural kolon hizasını **bozmaz**: hücrenin sol kenarını grid belirler, `max-inline-size` alanın hücre içinde ne kadarını doldurduğunu. Görev bölüşümü için `grid.md`.

```css
.field-postcode { inline-size: 8ch; }
.field-amount   { inline-size: 12ch; font-variant-numeric: tabular-nums; text-align: right; }
.field-name     { inline-size: 100%; max-inline-size: 40ch; }
```

## Eylem hiyerarşisi

- Birincil eylem (Kaydet) vurgulu ve **tek**
- İkincil (İptal) düşük vurgulu; birincilin yanında ama yanlışlıkla tıklanmayacak mesafede
- **Yıkıcı eylem (Sil) ayrı yerde**, birincilin yanında değil; onay ister
- Uzun formda kaydet sticky olabilir; o zaman kaydedilmemiş değişiklik göstergesi de olmalı
- Gönderim sırasında butonu devre dışı bırak ve durumu göster — çift gönderimi engelle

## Otomatik kaydetme

Otomatik kaydediliyorsa **durumu göster**: "Kaydedildi · 14:32". Sessiz otomatik kayıt, kullanıcının işinin kaybolduğunu düşünmesine yol açar. Açık kaydetme varsa, kaydedilmemiş değişiklikle sayfadan ayrılma uyarısı ver.

## Durumlar

| Durum | Tasarım |
|-------|---------|
| Boş form | Varsayılanlar makul ve görünür; gizli varsayılan yok |
| Yükleniyor (mevcut kaydı getirme) | Alan iskeletleri, yükseklik gerçek alanla aynı — **etiket iskelet değil** |
| Gönderiliyor | Buton meşgul durumu; form kilitli ama içerik okunur |
| Kısmi hata (sunucu) | Hangi alanların kaydedildiği, hangilerinin kaydedilmediği açık |
| Kaydedildi | Onay görünür ve kalıcı; kaybolan toast yeterli değil |

### İskelet yalnızca bilinmeyeni gizler

Etiket yüklenmiyor — zaten bilinir. Etiketi gri bir çubuğa çevirmek kullanıcıya neyin geldiğini saklar ve yükleme bitince metin belirince layout titrer.

```html
<!-- ❌ etiket de iskelet, alan ekran okuyucudan tamamen saklanmış -->
<div class="field" aria-hidden="true">
  <span class="skeleton-label"></span>
  <span class="skeleton"></span>
</div>

<!-- ✅ etiket gerçek metin; yalnızca değer bekliyor -->
<div class="field">
  <label for="avg">Geçmiş Dönem Ortalaması (kWh)</label>
  <div id="avg" aria-busy="true" aria-describedby="avg-hint">
    <span class="skeleton w-index"></span>
  </div>
  <p class="field-hint" id="avg-hint">Son 6 dönem ortalaması getiriliyor…</p>
</div>
```

`aria-hidden` yerine `aria-busy`: ekran okuyucu alanın var olduğunu ve beklediğini bilir. `aria-hidden` ile alan hiç yokmuş gibi davranır, veri gelince aniden ortaya çıkar.

İskeletin genişliği de beklenen değere uymalı — 16ch'lik bir endeks alanı için tam genişlik iskelet, gelmeyecek bir şey vaat eder.

## Erişilebilirlik

- Her alan `label` ile `for`/`id` üzerinden bağlı
- Hata `aria-describedby` + `aria-invalid`
- Grup `fieldset`/`legend`
- Klavye ile baştan sona doldurulabilir; odak sırası görsel sırayla aynı
- Otomatik odak yalnızca formun tek işi olduğu ekranda; yoksa ekran okuyucu kullanıcısını bağlamdan koparır
