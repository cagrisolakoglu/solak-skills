# solak-design-ui — Tasarım Dokümanı

**Tarih:** 2026-07-30
**Durum:** onaylandı, uygulanmayı bekliyor
**Etkilenen skill:** `skills/solak-design-ui` (v0.1.0 draft → v0.2.0 draft)

## Problem

`solak-design-ui` ilk halinde iki kaynağı tekrar ediyor:

1. **Sistemde `frontend-design` skill'i var** ve açıklaması neredeyse birebir aynı ("distinctive, production-grade frontend interfaces… avoids generic AI aesthetics"). İki skill arasındaki seçim belirsiz; model hangisini alacağını bilemez.
2. **Anti-template politikası ve "gerekli nitelikler" listesi global `web/design-quality.md` kuralında zaten yazıyor** ve her oturumda otomatik yükleniyor. Skill'deki kopya, kural dosyası değiştiğinde bayatlar.

Ayrıca `references/style-directions.md` sekiz stil yönü taşıyor (retro-futurism, glassmorphism, neo-brutalism…) — hiçbiri kurumsal veri ekranında kullanılmayacak içerik.

Sonuç: skill genel tasarım öğüdü tekrar ediyor, sahibinin gerçek işine (veri-yoğun kurumsal yüzeyler) dair hiçbir özel bilgi taşımıyor.

## Hedef

Skill'i **veri-yoğun kurumsal UI** uzmanlığına indirgemek: tablo/veri grid'i, filtre-sorgu paneli, veri giriş formu, metrik dashboard. Genel/vitrin tasarım işi `frontend-design`'a devredilir. Global kurallarda ve `dataviz` skill'inde zaten yazan bilgi tekrar edilmez, işaret edilir.

**Kapsam dışı:** tasarım sistemi/token katmanının sıfırdan kurulması (ayrı iş), pazarlama ve marka yüzeyleri (`frontend-design`), grafik tipi ve palet kararları (`dataviz`).

## Kararlar

| Karar | Seçim | Gerekçe |
|-------|-------|---------|
| Konumlanma | Veri-yoğun kurumsal UI'a özelleşme | Çakışmayı bitirir; içerik gerçek işe yarar |
| Kapsanan yüzeyler | Tablo, filtre, form, dashboard (dördü) | Kurumsal ekranların tamamını kapsayan asgari küme |
| Teknoloji | Teknoloji-bağımsız: semantik HTML + CSS custom property | Her projede çalışır, bakımı en kolay; framework repodan tespit edilip kalıp uyarlanır |
| Yapı | İnce `SKILL.md` + yüzey başına referans dosyası | Ortak temel tek yerde; model yalnızca gereken yüzeyi okur; beşinci yüzey eklemek `SKILL.md`'ye dokunmadan mümkün |
| İsim | `solak-design-ui` korunuyor | Dört yüzey de UI; konvansiyon yayınlanmış ismi değiştirmemeyi şart koşuyor |

### Reddedilen alternatifler

- **Tek dosya, derinlemesine (~350 satır):** kılavuzun "150 satırı aşan skill genelde iki skill'dir" kuralını ihlal eder; model her çağrıda dört yüzeyin bilgisini birden yükler.
- **Dört ayrı skill** (`solak-design-table`, `-filter`, `-form`, `-dashboard`): tetiklenmesi kesin ama ortak temel (token disiplini, yoğunluk, doğrulama listesi) dört yerde tekrarlanır ve biri değişince diğerleri bayatlar.
- **`frontend-design`'ı sarmalayan ince orkestrasyon katmanı:** çakışmayı çözer ama sahibinin işine dair özel bilgi taşımaz; sorunun yalnızca yarısını çözer.

## Yapı

```
skills/solak-design-ui/
├── SKILL.md                          ~90 satır: ortak temel ve yönlendirme
└── references/
    ├── density-and-direction.md      yoğunluk ölçeği + 3 stil yönü
    ├── tables.md                     tablo / veri grid'i
    ├── filters.md                    filtre / arama / sorgu paneli
    ├── forms.md                      veri giriş formu
    └── dashboards.md                 metrik özeti / KPI
```

`style-directions.md` **silinir**; içeriğinin kurumsal veri ekranına uygun kısmı `density-and-direction.md`'ye taşınır (8 yön → 3 yön).

## SKILL.md

### Frontmatter

`name: solak-design-ui`, `version: 0.2.0`, `status: draft`, `tags: [design, frontend, ui, data-dense, enterprise]`.

`description` (skill seçimini belirleyen alan):

> Designs and implements data-dense enterprise UI — tables and data grids, filter and query panels, data-entry forms, and metric dashboards. Decides row/field density deliberately, aligns numbers and text by type, designs the states real data produces (empty, loading, partial, error, overflow, too-many-results), and keeps everything on the project's token layer. Tech-agnostic: semantic HTML + CSS custom properties, adapted to the detected framework. Use when the user works on a table, grid, filter panel, form, report screen or dashboard — "tabloyu düzelt", "filtre paneli tasarla", "bu ekran kalabalık", "dashboard yap" — or invokes /solak-design-ui. For marketing pages, landing pages and brand surfaces, prefer `frontend-design`.

Son cümle kritik: skill kapsamı dışını **açıkça devrediyor**. İki skill arasındaki seçim belirsizliğini bitiren şey bu.

### Workflow

| # | Adım | Durum |
|---|------|-------|
| 1 | Bağlamı oku — token katmanı, mevcut tablo/form kalıpları, framework tespiti | genişledi |
| 2 | Yüzeyi tespit et → ilgili `references/*.md` dosyasını oku | **yeni** |
| 3 | Yoğunluğu karara bağla — comfortable / compact / dense | **yeni** |
| 4 | Yön seç (3 aday), kullanıcıya onaylat | daraldı (8 → 3 yön) |
| 5 | Token'ları yaz veya mevcut olanı kullan | aynı |
| 6 | Kodla — semantik HTML, gerçek veri durumlarının tamamı | genişledi |
| 7 | Motion (varsa) — yalnızca compositor-dostu property | aynı |
| 8 | Doğrula + mümkünse ekran görüntüsü kanıtı | genişledi |
| — | ~~Anti-template testi~~ | **çıkarıldı** → `web/design-quality.md`'ye işaret |

**Yoğunluk kararı neden yeni bir adım:** veri-yoğun UI'da yön seçiminden daha belirleyici. Aynı tablo `comfortable` (44px satır, az kayıt, okuma) ile `dense` (28px satır, yüzlerce kayıt tarama) arasında farklı bir ürün. Karar üç sorudan çıkar: kaç kayıt, kullanıcı tarıyor mu okuyor mu, hangi ekran.

**Yüzey tespiti neden yeni bir adım:** yönlendirme mekanizması. Model dört referansın hepsini değil, o an gerekeni okur.

### Girdiler

Mevcut girdi tablosu korunur, üstüne: **veri hacmi ve kullanım biçimi** (yoğunluk kararı için, zorunlu — yoksa sorulur).

### Guardrails

Mevcut guardrail'ler korunur; ikisi eklenir:

- Grafik tipi ve palet kararı gerektiğinde `dataviz` skill'ine devret; o bilgiyi burada tekrar etme.
- Pazarlama/marka yüzeyi istendiğinde `frontend-design`'ı öner; kapsam dışına taşma.

## Referans dosyalarının içeriği

Biçim: **karar + gerekçe + tuzak**. Jenerik CSS öğüdü değil, o yüzeyde gerçekten hata yapılan yerler.

### density-and-direction.md

Üç seviyeli yoğunluk ölçeği, her biri somut token değeriyle: `comfortable` (44px satır), `compact` (36px), `dense` (28px + tabular sayı). Seçim üç soruya bağlı (kayıt sayısı / tarama mı okuma mı / ekran).

Temel ilke: **yoğunluk sıkıştırma değildir** — satır yüksekliği düşerken hizalama disiplini ve ayırıcı netliği artmak zorunda, yoksa okunmaz.

Üç yön: Swiss/International (varsayılan, operasyonel ekran), editorial-dense (rapor/anlatı), bento (metrik özeti).

### tables.md

- Tipe göre hizalama: metin sola, sayı sağa + `tabular-nums`, tarih sabit genişlik
- Kolon önceliği ve daralma stratejisi — **kolonu sıkıştırmak yasak**; gizle, katla veya yatay kaydır, ama kararı açıkça beyan et
- Sticky başlık ve gerektiğinde sticky ilk kolon
- Tek ayırıcı sistemi: zebra **veya** çizgi, ikisi birden değil
- Taşan hücre: kısalt + tam değeri erişilebilir kıl
- Sıralama ve seçim göstergeleri; toplam satırı
- Durumlar: ilk kullanım boşluğu ile "sonuç yok" **ayrı tasarlanır**; iskelet yükleme satır yüksekliğiyle aynı olur (yoksa layout shift)

### filters.md

- Aktif filtre chip'leri tek doğruluk kaynağı — kullanıcı ne uyguladığını her an görür
- Durum URL'de: paylaşılabilir, geri tuşu çalışır
- Filtre ile arama ayrımı; sonuç sayısı geri bildirimi
- Sıfırlama ve kayıtlı görünüm
- "Sonuç yok" durumunda **hangi filtrenin gevşetileceğini öner** — çıkmaz sokak bırakma
- Pahalı filtrede debounce + beklemede olduğunu göster

### forms.md

- Alan gruplama ve ritim; etiket üstte (tarama hızı)
- Çoğunluk zorunluysa **isteğe bağlı olanı işaretle**, tersi değil
- Hata mesajı: alanın altında, ne yapılacağını söyleyen tonda, `blur`'da doğrula — her tuş vuruşunda değil
- Uzun formda özet hata bloğu + ilk hataya odak
- `disabled` ile `read-only` ayrımı ve nedenini gösterme
- Kaydet/iptal hiyerarşisi; yıkıcı eylem ayrı
- Alan genişliği beklenen içerik uzunluğuyla eşleşir

### dashboards.md

- Her tile **tek bir soruyu** cevaplar; cevaplamıyorsa çıkar
- Eşit olmayan bento kompozisyonu
- KPI anatomisi: etiket / değer / değişim / bağlam — bağlamsız sayı bilgi değil
- Eşik renkleri semantik; **renk tek gösterge olamaz** (ikon veya metin eşlik eder)
- Sparkline kuralları
- Grafik tipi ve palet gerektiğinde `dataviz` skill'ine devret

## Doğrulama kapıları

Düz kontrol listesi ikiye ayrılır, çünkü maddeler aynı ağırlıkta değil.

**Bloklayan** — geçilmezse skill "tamamlandı" demez, eksiği açıkça yazar:

- [ ] Metin kontrastı ≥ 4.5:1 (büyük metin ≥ 3:1); durum renkleri dahil
- [ ] Renk tek gösterge değil — ikon veya metin eşlik ediyor
- [ ] Klavye ile gezinilebiliyor, `focus-visible` görünür; grid içi gezinme dahil
- [ ] Boş / yükleniyor / hata durumları var
- [ ] Sayılar `tabular-nums` ve sağa hizalı
- [ ] Komponentte hardcoded palet / spacing / type değeri yok
- [ ] 320px'te taşma yok **veya** daralma stratejisi açıkça beyan edilmiş

**Bildirilen** — eksikse raporlanır, iş durmaz:

- [ ] Kısmi veri / çok fazla sonuç / taşan hücre durumları
- [ ] `prefers-reduced-motion` karşılığı
- [ ] İki tema da kasıtlı duruyor
- [ ] Yoğunluk seçimi gerekçelendirilmiş

Çıktı raporu bu ikiliyi yansıtır. Mümkünse 320/768/1440 ekran görüntüsü kanıt olarak eklenir.

## Etkilenen diğer dosyalar

- `registry.json` — `solak-design-ui` girişinin `version` ve `description` alanları güncellenir; `tags`'e `data-dense`, `enterprise` eklenir
- `README.md` — skill tablosundaki açıklama satırı güncellenir
- `skills/solak-design-ui/references/style-directions.md` — silinir

## Doğrulama planı

1. `registry.json` geçerli JSON, `name` alanı klasör adıyla eşleşiyor, yer tutucu (`<...>`) kalmamış.
2. `SKILL.md` 150 satırın altında.
3. Yeni bir oturumda skill adı anılmadan doğal bir istekle tetiklenip tetiklendiği sınanır ("bu tabloda 400 kayıt var, okunmuyor"). Tetiklenmiyorsa sorun `description`'da.
4. Pazarlama yüzeyi istendiğinde `frontend-design`'a devrettiği sınanır.
5. Gerçek bir ekranda uçtan uca çalıştırılır. Geçerse `status: stable`.

## Açık konular

- **`solak-design-system` gerekecek mi:** token katmanının sıfırdan kurulması bu skill'in kapsamı dışında bırakıldı. Mevcut token'ı olmayan bir projede bu skill token yazmak zorunda kalıyor — ilk gerçek kullanımda bunun yeterli olup olmadığı görülecek.
- **Ekran görüntüsü kanıtı:** Playwright/`/run` her projede hazır olmayabilir; o durumda doğrulama görsel olmayan maddelerle sınırlı kalır.
