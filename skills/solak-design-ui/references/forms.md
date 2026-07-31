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

## Alan genişliği içerikle eşleşir

Posta kodu, vergi no, tutar gibi sabit uzunluklu alanlar **tam genişlik olmaz.** Genişlik beklenen karakter sayısını gösterir ve hata yapmayı azaltır.

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
| Yükleniyor (mevcut kaydı getirme) | Alan iskeletleri, yükseklik gerçek alanla aynı |
| Gönderiliyor | Buton meşgul durumu; form kilitli ama içerik okunur |
| Kısmi hata (sunucu) | Hangi alanların kaydedildiği, hangilerinin kaydedilmediği açık |
| Kaydedildi | Onay görünür ve kalıcı; kaybolan toast yeterli değil |

## Erişilebilirlik

- Her alan `label` ile `for`/`id` üzerinden bağlı
- Hata `aria-describedby` + `aria-invalid`
- Grup `fieldset`/`legend`
- Klavye ile baştan sona doldurulabilir; odak sırası görsel sırayla aynı
- Otomatik odak yalnızca formun tek işi olduğu ekranda; yoksa ekran okuyucu kullanıcısını bağlamdan koparır
