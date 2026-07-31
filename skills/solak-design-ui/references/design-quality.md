# Tasarım Kalitesi

Bu skill kalite ölçütlerini **kendi taşır**; dış bir kural dosyasına bağlı değildir. Aşağıdaki ölçütler pazarlama yüzeyi için değil, operasyonel kurumsal ekran için yazılmıştır.

## Ölçüt: karar hızı, hoşluk değil

Veri-yoğun bir ekranın kalitesi üç soruyla ölçülür:

1. Kullanıcı aradığı değeri **kaç saniyede** buluyor?
2. **Yanlış okuma** riski var mı? (hizasız sayı, karışık birim, eksik veriyi sıfır sanmak)
3. Ekran kullanıcının **bir sonraki eylemini** söylüyor mu?

"Güzel duruyor" bir cevap değil. Estetik bu üç soruya hizmet ettiği kadar değerlidir — ve genelde hizmet eder: hiyerarşisi net, ritmi tutarlı, hizası disiplinli bir ekran hem daha hızlı okunur hem daha iyi görünür.

## Kaçınılacak kalıplar

Bunlar bu alanda tekrar tekrar üretilen, tanınabilir şekilde "düşünülmemiş" yüzeylerdir:

- **Envanter dashboard'u** — aynı boyutta on iki kutu. Hiyerarşi yok, önem farkı yok; kullanıcı nereden başlayacağını bilmiyor.
- **Düz tablo** — her kolon aynı ağırlıkta. Kimlik, karar ve detay kolonu ayrışmıyor; göz aradığı kolonu her satırda yeniden buluyor.
- **Kütüphane varsayılanı** — Bootstrap/Quasar/shadcn/MUI bileşeni hiç dokunulmadan, ürünün token katmanına bağlanmadan bırakılmış. Ürün gibi değil, demo gibi görünür.
- **Tek tip aralık** — her şeyin arası aynı. Alan arası ile grup arası eşitse form bir liste, dashboard bir yığındır.
- **Tek gri + tek mavi** — nötr yüzey ve tek accent, semantik durum rengi yok. Onaylı, beklemede ve itirazlı kayıt aynı görünüyor.
- **Renk tek gösterge** — durum yalnızca renkle bildirilmiş. Renk körlüğü bir yana, gri tonlamalı çıktıda ve düşük parlaklıklı ekranda bilgi yok olur.
- **Yarım etkileşim** — hover var, `focus-visible` yok; ya da yalnızca hover'da görünen eylem. Klavye ve dokunmatik kullanıcısı dışarıda kalır.
- **Dolgu içerik** — boşluğu kapatmak için eklenmiş tile, tekrar eden özet, "grafik olsun diye" grafik.
- **Şov derinliği** — gradient, büyük gölge, cam efekti; ama yükseklik hiçbir şey bildirmiyor. Derinlik anlam taşımıyorsa gürültüdür.
- **Dikkat çeken hareket** — operasyonel ekranda animasyon bilgi taşımaz, yorar. Hareket yalnızca durum değişimini veya süreklilik ilişkisini gösterir.
- **Dekoratif ikon enflasyonu** — başlıklarda süs ikon, veride anlam taşıyan ikon yok.
- **Küçültülerek "sadeleştirilmiş" ekran** — kalabalığa çözüm olarak font küçültülmüş. Kalabalık okunmazlığa çevrilmiş; azaltılması gereken renk, ayırıcı ve vurgudur (`typography.md`, madde 8).
- **İnce ağırlık** — 300 veya altı gövde. 13px'te griye düşer, koyu temada ışır. Vurgu azaltmak için ağırlık değil mürekkep düşürülür.

## Gerekli nitelikler

Her anlamlı yüzey aşağıdakilerin **en az beşini** göstermeli:

1. **Ölçek kontrastıyla hiyerarşi** — en önemli sayı en büyük; başlık/gövde/mikro üç kademe net
2. **Kasıtlı ritim** — grup arası boşluk alan arasının en az iki katı; tek tip padding yok
3. **Hizalama disiplini** — alanlar ve kolonlar ortak grid çizgilerinden başlıyor (`grid.md`)
4. **Anlam taşıyan derinlik** — sticky yüzey, çökmüş alan, kart sınırı; her biri bir şey bildiriyor
5. **Sayı tipografisi** — tabular figür, tipe göre hizalama, kolon boyunca sabit hassasiyet (`formatting.md`)
6. **Semantik renk** — durum renkleri işlevsel accent'ten ayrı; her biri ikon veya metinle eşli
7. **Tasarlanmış etkileşim** — hover, `focus-visible`, active, disabled/readonly, seçili; hepsi kasıtlı
8. **Kompozisyon hiyerarşisi** — span ve tile boyutu önemi bildiriyor; eşit kutu dizisi değil
9. **Durumlar** — boş, ilk kullanım, yükleniyor, kısmi, hata, taşma. Bu alanda kalite **durumlarda** görünür
10. **Kasıtlı yoğunluk** — `comfortable`/`compact`/`dense` seçimi gerekçeli (`density-and-direction.md`)

Bu alanda 9. madde ayrıcalıklıdır: mutlu yolu iyi görünen ama boş durumu "Kayıt yok" yazan bir ekran tasarlanmamıştır.

## Yön ve tema

Yön seçimi (Swiss / editorial-dense / bento) `density-and-direction.md`'de; kullanıcıya onaylatılır.

- **"Clean minimal", "modern", "şık" yön değildir.** Somut bir yöne çevir: tipografi ailesi, palet stratejisi, kompozisyon kararı.
- **Karanlık tema varsayılan değildir.** Ürünün istediği neyse o. İki tema destekleniyorsa ikisi de kasıtlı durmalı — koyu tema açık temanın tersi değil (`tokens.md`).
- Bir ekranda **tek yön**. Tablo Swiss, üstündeki özet bento ise bu iki yön değil, tek yön içinde iki bileşendir: ortak token, ortak tipografi, yalnızca kompozisyon farkı.

## Grafik gerekiyorsa

Bu skill grafiği kendi kurallarıyla kurar; dış bir skill'e ihtiyaç duymaz:

- **Grafik tipi soruyu izler** — zaman içinde değişim → çizgi; kategori karşılaştırma → çubuk; parça-bütün → yığılmış çubuk (pasta değil, 2-3 dilimden fazlasında okunmaz); dağılım → histogram
- **Kategorik palet en fazla 5-6 seri**; daha fazlası ayırt edilemez. Fazla seriyi "diğer"de topla
- **Seri ayrımı renk + biçim** — çizgi tipi, işaretçi şekli veya doğrudan etiket; renk tek gösterge olamaz
- **Y ekseni sıfırdan başlamıyorsa belirt** — küçük dalgalanma dramatik görünür
- **Eksen etiketinde birim bir kez**, veri noktasında tekrar etmez
- **Tooltip veriyi tekrarlar, yenisini üretmez**; klavyeyle de erişilebilir olmalı
- Renk paletinin kontrast ve tema uyumu `tokens.md`'deki semantik renklerden türetilir

Daha derin görselleştirme işi (karmaşık çok serili analiz, özel palet üretimi) için `dataviz` skill'i varsa **isteğe bağlı** olarak kullanılabilir; bu skill onsuz da tam çalışır.

## Kontrol listesi

- [ ] Yüzey kütüphane varsayılanı gibi değil, ürüne ait görünüyor
- [ ] Hiyerarşi ölçekle kurulmuş; her şey aynı vurguda değil
- [ ] Grup/alan ritmi ayrışıyor; tek tip aralık yok
- [ ] Derinlik ve sınırlar bilgi taşıyor, süs değil
- [ ] Durum renkleri semantik ve ikon/metinle eşli
- [ ] Etkileşim state'lerinin hepsi tasarlanmış (`focus-visible` dahil)
- [ ] Durumların hepsi tasarlanmış — mutlu yol tek başına yeterli değil
- [ ] Dolgu içerik yok; her bileşen bir soruyu cevaplıyor
- [ ] Gerçek bir ürün ekran görüntüsü olarak inandırıcı
