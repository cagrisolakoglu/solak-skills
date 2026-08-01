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

## Test etme

1. Skill'i kur: `Copy-Item -Recurse skills\<isim> "$env:USERPROFILE\.claude\skills\"`
2. Yeni bir oturumda **skill adını anmadan**, doğal bir istekle tetiklenip tetiklendiğine bak. Tetiklenmiyorsa sorun `description`'da.
3. Gerçek bir işte uçtan uca çalıştır.
4. Guardrail'leri sına: eksik girdi ver, çakışma yarat.
5. Çalıştıysa `status: stable`.

## Sürüm ve geriye uyum

- İsim asla değişmez.
- Girdi sözleşmesi bozulacaksa yeni skill oluştur, eskisini `deprecated` işaretle ve `description`'ına yerine geçeni yaz.
- `registry.json` her değişiklikte güncellenir.
