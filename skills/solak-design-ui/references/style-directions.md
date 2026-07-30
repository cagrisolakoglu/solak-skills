# Stil Yönleri

Yön seçimi bu skill'in en belirleyici kararıdır. Aşağıdakiler başlangıç noktası; birebir kopyalanacak reçete değil. **Bir yön seç, ona bağlı kal** — iki yönü karıştırmak tutarsızlık üretir.

Her yön için: ne zaman uygun · tipografi · renk · kompozisyon · dikkat.

---

## Editorial / magazine

Yoğun içerik, rapor, blog, dokümantasyon, otorite gerektiren yüzeyler.

- **Tipografi**: yüksek kontrastlı serif başlık + nötr grotesk gövde. Başlık ölçeği gövdenin 3-5 katı.
- **Renk**: kağıt benzeri yüzey, koyu mürekkep metin, tek güçlü accent. Az renk, çok kontrast.
- **Kompozisyon**: asimetrik kolonlar, geniş boşluk, taşan görseller, pull quote, kural çizgileri.
- **Dikkat**: satır uzunluğu 60-75 karakteri geçmesin; yoksa okunmuyor.

## Neo-brutalism

Geliştirici araçları, iddialı ürünler, dikkat çekmesi gereken yüzeyler.

- **Tipografi**: kalın grotesk veya mono, sıkı tracking, büyük ölçek.
- **Renk**: saf/doygun renkler, siyah kenarlık, ofset katı gölge (blur yok).
- **Kompozisyon**: görünür kenarlık, sert köşe veya tek tip büyük radius, üst üste binen bloklar.
- **Dikkat**: kontrast yüksek ama kolayca "gürültülü" olur — bir sayfada en fazla iki doygun renk.

## Glassmorphism (gerçek derinlikle)

Katmanlı arayüzler, medya-ağırlıklı yüzeyler, overlay ve panel yoğun ekranlar.

- **Tipografi**: nötr, orta ağırlık; cam üstünde ince font okunmaz.
- **Renk**: yarı saydam yüzey + arkada renkli/görsel katman, düşük opaklıkta kenarlık.
- **Kompozisyon**: gerçek z-ekseni: blur + kenarlık + gölge birlikte. Sadece `backdrop-filter` yetmez.
- **Dikkat**: cam üstü metin kontrastını mutlaka ölç; en sık kırılan yer burası. Performans için blur alanını sınırla.

## Dark luxury / light luxury

Premium ürün, finans, marka vitrini.

- **Tipografi**: zarif serif veya geniş tracking'li ince grotesk; nefes alan başlıklar.
- **Renk**: çok dar palet, düşük doygunluk, metalik/sıcak tek accent. Saf siyah değil koyu nötr (oklch ~18%).
- **Kompozisyon**: cömert boşluk, az eleman, yavaş ve az motion.
- **Dikkat**: "az eleman" ile "boş sayfa" arasındaki fark hiyerarşi; ölçek kontrastını yine de kur.

## Bento

Dashboard, özet ekranı, çok metrikli yüzeyler.

- **Tipografi**: kompakt, sayı odaklı; tabular figürler.
- **Renk**: nötr yüzeyler + semantik durum renkleri (iyi/uyarı/kritik).
- **Kompozisyon**: **eşit olmayan** hücreler — 2x1, 1x2, 2x2 karışık. Eşit grid bento değil, sadece grid.
- **Dikkat**: her hücre farklı bir soruyu cevaplamalı; aynı ağırlıkta 12 kutu = hiyerarşisiz.

## Swiss / International

Kurumsal, veri, ciddi ürün; süsten kaçınılan yerler.

- **Tipografi**: tek grotesk aile, ağırlık farkıyla hiyerarşi, sıkı baseline grid.
- **Renk**: siyah/beyaz/gri + tek işlevsel accent.
- **Kompozisyon**: katı kolon grid, sola hizalı, matematiksel spacing ölçeği.
- **Dikkat**: disiplin olmadan "boş ve özensiz"e düşer; grid'e gerçekten uy.

## Scrollytelling

Anlatı, ürün tanıtımı, süreç açıklama.

- **Tipografi**: büyük anlatı başlıkları + kısa gövde blokları.
- **Renk**: bölümler arası kademeli geçiş, ilerlemeyi hissettiren.
- **Kompozisyon**: sticky görsel + akan metin; her bölüm tek bir fikir.
- **Dikkat**: IntersectionObserver kullan, scroll handler'da iş yapma. `prefers-reduced-motion`'da anlatı yine anlaşılır kalmalı.

## Retro-futurism

Yan proje, oyun, topluluk ürünü, nostaljik ton.

- **Tipografi**: geniş tracking'li display, mono aksanlar.
- **Renk**: koyu zemin üstü neon veya soluk 70'ler paleti; grain/scanline dokusu.
- **Kompozisyon**: merkezi simetri, çerçeveler, ufuk çizgisi motifleri.
- **Dikkat**: doku efektleri okunabilirliği hızla bozar; metin katmanını efektten ayır.

---

## Yön seçme yöntemi

1. Ürünün tonunu bir cümlede yaz ("saha mühendisine hızlı karar veren yoğun veri ekranı").
2. Bu cümleye 2-3 yön aday çıkar.
3. Aralarındaki farkı somut karara indir: tipografi pairing'i ve kompozisyon iskeleti.
4. Kullanıcıya onaylat, sonra kodla.

Karanlık tema varsayılan değildir — ürünün istediği şey neyse o.
