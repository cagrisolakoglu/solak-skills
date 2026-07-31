# Filtre / Arama / Sorgu Paneli

## Aktif filtre tek doğruluk kaynağı

Kullanıcı **her an** neyin uygulandığını görmeli. Uygulanmış filtreler, panel kapalıyken de görünen chip'ler olarak listelenir; her chip tek tek kaldırılabilir.

Panelin içine gömülü, kapatınca kaybolan filtre durumu en sık yapılan hatadır: kullanıcı eksik veriye bakıp tam sanır.

```html
<div class="applied-filters" aria-live="polite">
  <span class="filter-chip">
    Tesis: Ankara-2
    <button type="button" aria-label="Tesis filtresini kaldır">×</button>
  </span>
  <button type="button" class="filter-clear">Tümünü temizle</button>
</div>
```

`aria-live="polite"` önemli: filtre değişimi ekran okuyucuya bildirilmeli.

## Durum URL'de

Filtre, sıralama, sayfa ve arama sorgusu URL'e yazılır. Kazandırdığı üç şey: ekran paylaşılabilir, geri tuşu beklendiği gibi çalışır, yenilemede durum kaybolmaz.

Filtre durumunu yalnızca bileşen state'inde tutmak bu üçünü de kaybettirir.

## Filtre ile arama ayrı işlerdir

- **Arama**: serbest metin, birden çok alanda eşleşir, yazarken sonuç daralır
- **Filtre**: bilinen alanda bilinen değer kümesi, kasıtlı seçim

İkisini tek girdiye bindirmek ikisini de belirsizleştirir. Her ikisi de gerekiyorsa görsel olarak ayır ve birlikte nasıl çalıştıklarını belli et (arama filtre içinde mi arar, filtreyi ezer mi).

## Sonuç sayısı geri bildirimi

Uygulanan filtrenin etkisi **sayıyla** görünür: "1.284 kayıt · 3 filtre aktif". Mümkünse filtre uygulanmadan önce tahmini sayıyı göster — kullanıcı sonucu boş bir listede keşfetmesin.

Sıfır sonuç üretecek seçenekleri devre dışı bırakmak veya "(0)" ile işaretlemek, boşa giden filtre denemesini baştan önler.

## Pahalı filtre

Sunucuya giden veya yavaş filtrede:

- Yazma girdisinde debounce (250-400ms); her tuş vuruşunda sorgu yok
- **Beklemede olduğunu göster** — mevcut sonucu soluklaştır, iskelete dönme
- Eski sonucu ekranda tutup yeni sonuç gelince değiştir (stale-while-revalidate); boşaltıp bekletme
- Çok pahalıysa otomatik uygulama yerine açık "Uygula" butonu; o zaman uygulanmamış değişiklik olduğunu göster

## "Sonuç yok" durumu — çıkmaz sokak bırakma

Sonuç boşsa **hangi filtrenin sorumlu olduğunu** söyle ve bir çıkış yolu ver:

> Bu kriterlerle kayıt bulunamadı. **Tarih aralığı** (son 7 gün) en çok daraltan filtre — genişletmeyi dene.
> [Tarihi son 30 güne genişlet] [Tüm filtreleri temizle]

Kullanıcıyı hangi filtreyi kaldıracağını tahmin etmeye bırakmak, en sık terk noktasıdır.

## Sıfırlama ve kayıtlı görünüm

- "Tümünü temizle" her zaman erişilebilir, tek eylem
- Tekrar eden sorgular varsa kayıtlı görünüm: adlandırılır, paylaşılabilir (URL zaten durumu taşıyor)
- Varsayılan görünüm açıkça belirtilir — kullanıcı "temiz duruma" nasıl döneceğini bilmeli
- Varsayılan olarak uygulanan gizli bir filtre varsa (örn. "yalnızca aktif kayıtlar") bunu chip olarak **göster**; gizli varsayılan filtre kullanıcıyı yanıltır

## Erişilebilirlik

- Filtre grubu `fieldset` + `legend`
- Chip kaldırma butonu `aria-label` ile hangi filtreyi kaldırdığını söyler
- Sonuç sayısı `aria-live` bölgesinde
- Panel açılır-kapanırsa `aria-expanded`; kapanınca odak tetikleyiciye döner
