# Solak Skills

A growing collection of practical AI agent skills for software engineering, architecture and team workflows.

Bu repo, tek tek dağınık prompt'lar yerine **standart yapıda, versiyonlanabilir ve yeniden kullanılabilir** AI agent skill'lerini tek yerde toplar. İleride bir registry, CLI veya web kataloğuna dönüşebilecek şekilde tasarlandı.

## Yapı

```
solak-skills/
├── skills/                     # Skill'ler (her biri kendi klasöründe)
│   └── solak-create-skill/
│       └── SKILL.md
├── templates/
│   └── skill-template/         # Yeni skill için başlangıç şablonu
│       └── SKILL.md
├── docs/
│   ├── naming-convention.md
│   └── skill-development-guide.md
└── registry.json               # Makine-okunur skill kataloğu
```

## Kurulum

Claude Code'un skill'leri görmesi için `skills/` altındaki klasörü kopyala veya sembolik link ver:

```powershell
# Tek skill (user scope)
Copy-Item -Recurse skills\solak-create-skill "$env:USERPROFILE\.claude\skills\"

# Tüm skill'ler
Copy-Item -Recurse skills\* "$env:USERPROFILE\.claude\skills\"
```

Proje bazlı kullanım için hedefi `<proje>\.claude\skills\` yap.

## Skill listesi

| Skill | Amaç | Durum |
|-------|------|-------|
| [solak-create-skill](skills/solak-create-skill/SKILL.md) | Bu repoda standarda uygun yeni skill üretir | ✅ hazır |

Güncel ve makine-okunur liste: [`registry.json`](registry.json)

## İsimlendirme

Tüm skill'ler `solak-` prefix'i ve `solak-<eylem>-<hedef>` formatını kullanır (örn. `solak-review-pr`).
Detay: [docs/naming-convention.md](docs/naming-convention.md)

## Yeni skill eklemek

En kısa yol, reponun kendi yardımcı skill'ini kullanmak:

```
/solak-create-skill review-pr
```

Elle eklemek istersen: [CONTRIBUTING.md](CONTRIBUTING.md)

## Yol haritası

- [ ] Çekirdek skill seti (`review-pr`, `fix-ci`, `design-api`, `audit-auth0`, `upgrade-dotnet`)
- [ ] `registry.json` şeması + CI doğrulaması
- [ ] Kurulum CLI'ı (`solak install <skill>`)
- [ ] Web kataloğu

## Lisans

[MIT](LICENSE)
