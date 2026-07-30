---
name: solak-create-skill
description: Scaffolds a new skill in the solak-skills repository — creates the skill folder, fills the SKILL.md template with metadata, writes usage examples, validates the structure against the naming convention, and updates registry.json. Use when the user wants to add, create, or scaffold a new solak skill ("yeni skill oluştur", "solak-create-skill review-pr", "add a skill for X", "/solak-create-skill"), or when a repeated workflow should be captured as a reusable skill.
metadata:
  version: 0.1.0
  author: cagrisolakoglu
  tags: [meta, scaffolding, authoring]
  status: stable
---

# solak-create-skill

solak-skills reposunda standarda uygun yeni bir skill iskeleti üretir ve kataloğa kaydeder.

## When to Use

- Kullanıcı yeni bir skill eklemek istiyor (`/solak-create-skill upgrade-dotnet`).
- Tekrar eden bir iş akışı (elle yapılan bir inceleme, bir migrasyon rutini) kalıcı bir skill'e dönüştürülecek.
- Var olan bir skill'in yapısı standarda çekilecek (aynı doğrulama adımları geçerli).

Bu skill'i **kullanma**: skill'in *içeriğini* yazmak asıl iş değilse, yani kullanıcı sadece tek seferlik bir görev istiyorsa. O durumda görevi doğrudan yap.

## Inputs

| Girdi | Zorunlu | Açıklama |
|-------|---------|----------|
| skill adı | ✅ | `<eylem>-<hedef>` veya tam `solak-<eylem>-<hedef>`. Prefix yoksa otomatik eklenir. |
| amaç açıklaması | ❌ | Yoksa kullanıcıya tek soru sorulur: skill ne yapacak, hangi ifadelerle tetiklenecek. |
| `tags` | ❌ | Yoksa hedeften çıkarılır (`dotnet` → `[dotnet, upgrade]`). |

İsim standarda uymuyorsa (eylem sonda, camelCase, prefix'siz hedef) **düzeltilmiş halini öner ve onay al** — sessizce yeniden adlandırma.

## Workflow

1. **İsmi doğrula** — `docs/naming-convention.md` kurallarına göre kontrol et: kebab-case, `solak-` prefix, eylem-önce sırası, tek eylem/tek hedef. Uymuyorsa öneriyle dur.
2. **Çakışma kontrolü** — `skills/<isim>/` zaten varsa ve `registry.json` içinde kayıtlıysa oluşturma; mevcut skill'i güncellemek isteyip istemediğini sor.
3. **Klasörü oluştur** — `skills/<isim>/SKILL.md`, `templates/skill-template/SKILL.md` kopyalanarak.
4. **Frontmatter'ı doldur** — `name` klasör adıyla birebir aynı; `description` üçüncü şahıs, tetikleyici ifadeleri içerir ve "Use when the user ..." ile biter; `version: 0.1.0`; `status: draft`.
5. **Gövdeyi yaz** — When to Use / Inputs / Workflow / Output / Guardrails / Examples bölümlerini gerçek içerikle doldur. Şablon yer tutucusu (`<...>`) bırakma.
6. **registry.json'u güncelle** — `skills` dizisine giriş ekle, alfabetik sırayı koru, JSON'un geçerli kaldığını doğrula.
7. **README tablosunu güncelle** — skill listesine satır ekle.
8. **Doğrula** — aşağıdaki kontrol listesini çalıştır ve sonucu raporla.

### Doğrulama kontrol listesi

- [ ] Klasör adı = frontmatter `name`
- [ ] `description` tetikleyici ifadeleri içeriyor ve tek paragraf
- [ ] Zorunlu bölümlerin hepsi var, yer tutucu kalmamış
- [ ] `registry.json` geçerli JSON ve yeni giriş kayıtlı
- [ ] README tablosunda satır var
- [ ] İsim `docs/naming-convention.md`'ye uygun

## Output

Kullanıcıya kısa bir özet:

```
✅ skills/solak-upgrade-dotnet/SKILL.md oluşturuldu
✅ registry.json güncellendi (7 skill)
✅ README tablosuna eklendi
⚠️  status: draft — içerik gözden geçirilip stable'a çekilmeli

Sonraki adım: skill'i dene → /solak-upgrade-dotnet <proje>
```

## Guardrails

- Var olan bir `SKILL.md`'yi **okumadan üzerine yazma**; çakışmada onay al.
- Yayınlanmış bir skill'i yeniden adlandırma — kurulumları bozar. Gerekiyorsa yeni skill oluştur, eskisini `status: deprecated` yap.
- `registry.json`'u elle bozma riskine karşı yazdıktan sonra parse edip doğrula.
- Commit ve push **isteniyorsa** yapılır; varsayılan olarak yalnızca dosyaları oluştur.
- Skill içeriğini uydurma: gerçek iş akışı bilinmiyorsa kullanıcıya adımları sor.

## Examples

```
/solak-create-skill review-pr
/solak-create-skill solak-audit-auth0
/solak-create-skill optimize-query "yavaş MongoDB sorgularını explain planıyla analiz edip index önerir"
```

İlkinde isim `solak-review-pr`'a normalize edilir, amaç sorulur, iskelet oluşturulur ve registry güncellenir.
