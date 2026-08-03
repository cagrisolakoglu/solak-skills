# Skill Geliştirme Kılavuzu

## Skill nedir, ne değildir

Bir skill, **modelin ne zaman devreye alacağını kendisinin anlayabildiği** paketlenmiş bir iş akışıdır. Uzun bir prompt kopyası değil; girdisi, adımları, çıktısı ve sınırları tanımlı bir yordamdır.

İyi bir skill adayı:
- En az iki kez elle yapılmış bir iş
- Adımları sıralanabilir ve doğrulanabilir
- Sonucu somut (dosya, rapor, PR yorumu, yeşil pipeline)

Kötü bir skill adayı:
- Tek seferlik görev
- "Yardımcı ol" düzeyinde belirsiz kapsam
- Sadece bilgi aktarımı → bunu bir doküman yap, skill değil

## Anatomi

```
skills/solak-<eylem>-<hedef>/
└── SKILL.md          # tek zorunlu dosya
    ├── frontmatter   # name, description, metadata
    └── gövde         # When to Use, Inputs, Workflow, Output, Guardrails, Examples
```

Ek dosyalar (`references/`, `templates/`, `scripts/`, `assets/`) yalnızca gerçekten gerekliyse eklenir. Varsayılan tek dosyadır.

| Klasör | İçerik | Ne zaman |
|--------|--------|----------|
| `references/` | Yürütme sırasında **okunacak** kural ve karar içeriği | SKILL.md'yi şişirecek kadar uzun bilgi varsa |
| `templates/` | Kullanıcının veya ajanın **dolduracağı** iskelet dosya | Skill tekrarlanan bir çıktı üretiyorsa (plan, TODO, rapor) |
| `scripts/` | Çalıştırılabilir yardımcı | Elle tekrarlanan bir komut dizisi varsa |
| `evals/` | Prompt + beklenen + **yasak** davranış; koşum sonuçları | Skill davranışının doğru olduğunu kanıtlamak gerekiyorsa |
| `examples/` | Tamamlanmış örnek çıktı ve `anti-patterns/` | Beklenen çıktı biçimi tarifle anlatılamıyorsa |
| `manifest.yaml` | Dosya listesi ve yönlendirme, makine okunur | Doğrulama betiği varsa (tek doğruluk kaynağı) |

`references/` üç dosyayı geçtiğinde SKILL.md'ye bir **yönlendirme tablosu** ekle: hangi durumda hangi referans okunur. Onsuz model ya hepsini okur ya rastgele seçer. Ve bir kuralın **tek sahibi** olur; diğer dosyalar ona link verir, kuralı kopyalamaz.

Referans dosyaları **koşullu okunur**: SKILL.md hangi durumda hangisinin okunacağını söyler. Hepsini her seferinde okutan bir skill, tek dosyalı bir skill'den daha pahalıdır ve daha az işe yarar.

## Frontmatter

```yaml
---
name: solak-review-pr
description: Reviews a pull request ... Use when the user asks to review a PR, names a branch, or says "/solak-review-pr".
metadata:
  version: 0.1.0
  author: cagrisolakoglu
  tags: [review, git]
  status: draft
---
```

- `name` — klasör adıyla **birebir aynı**. Farklıysa skill yüklenmez.
- `description` — **en kritik alan.** Model skill'i yalnızca buna bakarak seçer. Ne yaptığını *ve* hangi ifadelerin tetiklediğini yaz. Tetikleyici örnekleri tırnak içinde ver. Üçüncü şahıs kullan, "Use when the user ..." ile bitir.
- `version` — semver. Davranış değişiyorsa minor, düzeltme ise patch.
- `status` — `draft` (yeni yazıldı, denenmedi) → `stable` (gerçek işte kullanıldı) → `deprecated`.

### description yazarken

| ❌ | ✅ |
|----|-----|
| "PR incelemesi yapar." | "Reviews a pull request against the team's checklist and posts inline findings. Use when the user names a branch or PR id, says 'review this PR', or invokes /solak-review-pr." |
| "Bu skill .NET yükseltir." | "Upgrades a .NET project to a target framework version, updating csproj, packages and breaking API usages. Use when the user asks to upgrade .NET, migrate a target framework, or mentions net8/net9 migration." |

## Gövde bölümleri

| Bölüm | Amaç | Kaçınılacak |
|-------|------|-------------|
| **When to Use** | Devreye girme ve girmeme koşulları | Sadece olumlu örnek; kapsam dışını da yaz |
| **Inputs** | Argümanlar, zorunluluk, eksik girdide davranış | "duruma göre" |
| **Workflow** | Numaralı, uygulanabilir adımlar; hangi araç kullanılacak | Pasif anlatım, "gerekli analizi yap" |
| **Output** | Kullanıcının eline geçen şey + format örneği | Belirsiz "sonuç raporlanır" |
| **Guardrails** | Yasak eylemler, onay gerektiren adımlar | Genel ahlak dersi; somut ol |
| **Examples** | Gerçek çağrı örnekleri | Uydurma çıktı |

Bu altısı **zorunlu**. Aşağıdaki ikisi **koşullu** — skill'in yanlış çalışması ne kadar pahalıysa gerekir, merdiven "Aşamalı yürütme" bölümünde:

| Bölüm | Ne zaman | Kaçınılacak |
|-------|----------|-------------|
| **Kapsam sınıflandırması** | İstek küçük de büyük de gelebiliyorsa | Tek iş yapan skill'e dayatmak |
| **Doğrulama kapıları** | Geri alınması pahalı iş yapıyorsa | Bloke edici / raporlanan ayrımı yapmamak |

Gerekmeyen koşullu bölüm **silinir**. Boş başlık ya da yer tutucu bırakmak, olmamasından kötüdür.

## Yazım prensipleri

1. **Doğrulama adımı zorunlu.** Her workflow bir "nasıl kanıtlanır" adımıyla bitmeli — komut, test, kontrol listesi. Doğrulanamayan skill güvenilmez.
2. **Belirsizlikte sor, tahmin etme.** Ama sormaya bağlı olmayan işi önce bitir.
3. **Yıkıcı eylemler onay ister.** Dosya silme, force push, canlı ortama dokunma.
4. **Ölçüt uzunluk değil, içeriğin doğru dosyada olması.** SKILL.md ne kadar gerekiyorsa o kadar uzun olur — satır sayısı için sabit bir tavan yok.

   SKILL.md'de kalması gerekenler: akışı yöneten her şey. Aşama başlıkları, kapılar, girdi sözleşmesi, guardrail'ler, çıktı formatı. Bunlar kısaltılırsa skill akışını kaybeder.

   `references/` altına taşınması gerekenler: yürütme sırasında **koşullu** okunacak bilgi. Tablolar, checklist gövdeleri, karar matrisleri, tuzak anlatımları, şablonlar. Bunlar SKILL.md'de dururken her çağrıda okunur ve çoğu zaman gereksizdir.

   Uzunluk yalnızca bir **soru işareti**dir, kural değil: SKILL.md beklenenden uzunsa iki şeyi kontrol et — (a) içinde koşullu okunacak bilgi kalmış olabilir, referansa taşı; (b) gerçekten iki ayrı iş anlatıyor olabilir, o zaman skill ikiye bölünür. İkisi de değilse uzunluk sorun değildir.

   Örnek: `solak-design-ui` on aşamalı UX akışına geçtiğinde SKILL.md büyüdü. Aşamaları kısaltmak akışı bozardı; doğru hamle tabloları ve şablonları `ux-workflow.md` ile `layout-and-information-architecture.md`'ye almaktı. (Bu maddenin eski hali 150 satırlık sabit bir tavandı ve tam da yanlış tarafı sıkıştırmaya zorluyordu.)
5. **Yer tutucu bırakma.** `<...>` kalmış bir skill draft bile sayılmaz.
6. **Bölüm başlıklarını değiştirme.** `## When to Use` gibi başlıklar araçlar tarafından ayrıştırılabilir; çevirmek veya yeniden adlandırmak eşleşmeyi bozar.

## Aşamalı yürütme

`solak-design-ui` bu repoda en çok test edilmiş skill ve öğrettiği şey kural sayısı değil, **işin nasıl yürütüldüğü**. Aynı disiplin diğer skill'lere de geçer, ama **birebir kopyalanarak değil**: on aşamalı bir akışı üç adımlık bir işe dayatmak, o skill'in düzeltmek için yazıldığı hatanın kendisidir.

Ölçü şu: **skill pahalıya patlayabilir mi?** Yanlış çıktının maliyeti yükseldikçe merdivende yukarı çıkılır.

| Skill ne yapıyor | Gereken |
|---|---|
| Tek, tersine çevrilebilir eylem (`kill-port`, bir dosya biçimlendirme) | Doğrulama adımı. Başka bir şey değil. |
| Birkaç adım, hepsi geri alınabilir | Numaralı akış + her adımda ne kanıtlandığı |
| Dosya yazan/değiştiren iş | Yukarıdakiler + **uygulama öncesi TODO** + iş kalemi başına kabul ölçütü |
| Geri alınması pahalı iş (migrasyon, refactor, canlı ortam, para) | Yukarıdakiler + **kapsam sınıflandırması** + bloke edici kapılar + dürüst rapor |

Merdivenin üst basamaklarındaki beş öğe:

**1 · Kapsam sınıflandırması.** İşe başlamadan önce isteğin *büyüklüğünü* belirle, çünkü **yanlış süreç gerçek bir hatadır**: küçük bir kusura koca bir akış işletmek kullanıcının zamanını yakar, büyük bir işi tek hamlede yapmak da onu güvenli kılan kontrolleri atlar. Kapsam **isteğin sözlerine değil, gereken işe** göre belirlenir; ikisi çelişiyorsa bunu söyleyip devam et.

**2 · Kapılı aşamalar.** Her aşamanın geçilmesi gereken bir kapısı olur ve kapı somut olur: "layout onaylandı" değil, "tel kerpeten var ve stil çalışmasından önce yazıldı". Kapı geçilmediyse durulur, sonraki aşamaya kaçılmaz.

**3 · Uygulama öncesi TODO.** Kod yazmadan önce bağımlılık sırasına dizilmiş, dosya düzeyinde, her kalemi tek doğrulanabilir sonuç üreten bir liste çıkar. **Artefakt eşiği tut:** beş kalem ve üstü ayrı bir dosyaya, altı yanıt içinde satır içi listeye. Disiplin ikisinde de aynı, değişen sadece nereye yazıldığı.

**4 · Kalem kalem yürütme.** Her kalem için: dosyaları oku → kabul ölçütünü yeniden söyle → **en küçük** kapsamlı değişikliği yap → kontrolleri çalıştır → doğrula → tamamlandı işaretle. Toplu değişiklik yapıp sonunda hepsini doğrulamaya çalışmak, hangi değişikliğin neyi bozduğunu bilmemek demektir.

**5 · Kapsamlanmış kapılar ve dürüst rapor.** Kapıları **bloke edici** ve **raporlanan** diye ayır. Küçük bir düzeltme yalnızca kendi değişiminin dokunduğu kapıları yanıtlar, hepsini değil. Ve en önemlisi:

> **Kontrol edilmemiş bir kapıyı iddia etmek, kontrol edilmedi demekten kötüdür.**

Neyi doğrulamadığını söyle. "Gerçek kullanıcıyla denenmedi", "koyu tema gözle bakılmadı" satırları raporun en değerli kısmıdır, çünkü okuyanın nereye güvenmeyeceğini bilmesini sağlar.

### Kural eklemenin ölçütü

Bir kural skill'e **bir şey kırıldığı için** girer, kulağa doğru geldiği için değil. `solak-design-ui`'nin kurallarının çoğu bir ekran görüntüsünden çıktı: geçerli kod, temiz konsol, gözle görünen hata. Doküman hacmi kanıt değildir.

Bunun tersi de geçerli: **doğru davranışın ihlal ettiği kural, kötü kuraldır.** Bir değerlendirme koşumu kuralı çiğniyorsa ve koşum haklıysa, kuralı düzelt — koşumu suçlama.

## Test etme

1. Skill'i kur: `Copy-Item -Recurse skills\<isim> "$env:USERPROFILE\.claude\skills\"`
2. Yeni bir oturumda **skill adını anmadan**, doğal bir istekle tetiklenip tetiklendiğine bak. Tetiklenmiyorsa sorun `description`'da.
3. Gerçek bir işte uçtan uca çalıştır.
4. Guardrail'leri sına: eksik girdi ver, çakışma yarat.

### Temiz oturumda koşmak

Bir skill'i yazdığın oturumda denemek **hatırlamayı** ölçer, davranışı değil. Sen hangi referansın hangi kuralı içerdiğini biliyorsun; soğuk bir okuyucu bilmiyor. Gerçek test:

- Ayrı bir oturum (ya da alt-ajan) aç, ona **yalnızca** skill'in yolunu, kullanıcı prompt'unu ve varsa gerçekçi bir hedef dosya ver.
- Beklenen/yasak davranış listesini **gösterme** — gösterirsen teste çalışmış olur.
- Bittiğinde raporunu olduğu gibi kabul etme; çıktıyı **kendin yeniden ölç**.

Yazıldığı oturumda koşulan bir testin sonucu `PASS` değil, **koşulmadı** olarak kaydedilir. Kanıt sayılmayan bir şeyi kanıt gibi yazmak, hiç test etmemekten kötüdür.

### Beklenen/yasak listesi

Değerlendirme yazarken **yasak davranış listesi, beklenen listesinden değerlidir.** Beklenen davranışlar model özen gösterirken zaten çıkar; yasak olanlar otomatik pilotta çıkar — ve skill tam olarak onları engellemek için yazılmıştır.

### Statü kararı

`status` doküman hacmiyle değil kanıtla yükselir:

| Statü | Ne zaman |
|---|---|
| `draft` | Yazıldı, henüz koşulmadı |
| `beta` | Temiz oturumlarda koşuldu, bloke edici hata yok — ama gerçek işte kullanılmadı |
| `stable` | Gerçek işlerde kullanıldı ve dayandı |

Büyük olduğu için `stable` işaretlemek en kolay hata. `solak-design-ui` altı değerlendirmenin altısını temiz bağlamda geçtiği hâlde `beta` kaldı; tek eksik gerçek proje kullanımıydı.

## Sürüm ve geriye uyum

- İsim asla değişmez.
- Girdi sözleşmesi bozulacaksa yeni skill oluştur, eskisini `deprecated` işaretle ve `description`'ına yerine geçeni yaz.
- `registry.json` her değişiklikte güncellenir.
