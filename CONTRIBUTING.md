# Katkı Rehberi

Bu repo kişisel bir skill kütüphanesi; yine de tutarlılık için aşağıdaki akış geçerlidir.

## Yeni skill eklemek

En kısa yol reponun kendi yardımcı skill'i:

```
/solak-create-skill <eylem>-<hedef>
```

Elle eklemek istersen:

1. İsmi [docs/naming-convention.md](docs/naming-convention.md)'ye göre belirle.
2. Şablonu kopyala:
   ```powershell
   Copy-Item -Recurse templates\skill-template skills\solak-<eylem>-<hedef>
   ```
3. `SKILL.md` frontmatter'ını doldur — `name` klasör adıyla birebir aynı olmalı.
4. Gövdeyi [docs/skill-development-guide.md](docs/skill-development-guide.md)'ye göre yaz; yer tutucu (`<...>`) bırakma.
5. `registry.json`'a girişi ekle (alfabetik).
6. README'deki skill tablosuna satır ekle.
7. Skill'i kur ve gerçek bir işte dene. Çalışıyorsa `status: stable`.

## Kabul kriterleri

- [ ] Klasör adı = frontmatter `name`
- [ ] `description` tek paragraf, üçüncü şahıs, tetikleyici ifadeleri içeriyor
- [ ] When to Use / Inputs / Workflow / Output / Guardrails / Examples bölümleri dolu
- [ ] Workflow bir doğrulama adımıyla bitiyor
- [ ] Yıkıcı eylemler için guardrail tanımlı
- [ ] `registry.json` geçerli JSON
- [ ] README güncel

## Commit formatı

```
<type>: <açıklama>
```

`feat`, `fix`, `docs`, `refactor`, `chore`. Skill eklerken:

```
feat: add solak-upgrade-dotnet skill
```

## Değişiklik yapmak

- Davranış değişikliği → `version` minor artır.
- Yazım/düzeltme → patch.
- Girdi sözleşmesi bozuluyorsa → yeni skill, eskisi `status: deprecated`.
- **Yayınlanmış skill'i yeniden adlandırma.** Kurulumları bozar.
