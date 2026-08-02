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

Claude Code skill'leri `~/.claude/skills/<skill-adı>/` altında arar (proje bazlı kullanım için `<proje>/.claude/skills/`). Klasör adı `SKILL.md` frontmatter'ındaki `name` ile **birebir aynı** olmalı; farklıysa skill yüklenmez.

İki yol var, seçim önemli:

| Yol | Ne zaman | Sonuç |
|-----|----------|-------|
| **Bağlantı** (junction / symlink) | Skill geliştirilecek veya güncel tutulacak | Repo tek kaynak; `git pull` anında kurulu skill'e yansır |
| **Kopya** | Salt kullanım, repo makinede kalmayacak | Bağımsız kopya; repo değişince elle güncellenir |

Kopya iki yerde **ayrışır**: bir tarafta düzeltilen kural öbür tarafta olmaz. Geliştirme yapılacaksa bağlantı kur.

### Bağlantı — Windows

Sembolik link yönetici yetkisi (veya Geliştirici Modu) ister; **dizin junction'ı istemez.** Bu yüzden sıra: junction → symlink → kopya.

```powershell
$repo  = "$env:USERPROFILE\solak-skills"
$skill = "solak-design-ui"
$dest  = "$env:USERPROFILE\.claude\skills\$skill"

# Hedefte eski bir KOPYA varsa, once icerigin repoda oldugunu dogrula
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest -Confirm:$false }

New-Item -ItemType Junction -Path $dest -Target "$repo\skills\$skill" | Out-Null
Get-Item $dest | Select-Object Name, LinkType, Target
```

Tüm skill'ler için:

```powershell
$repo = "$env:USERPROFILE\solak-skills"
Get-ChildItem "$repo\skills" -Directory | ForEach-Object {
  $dest = "$env:USERPROFILE\.claude\skills\$($_.Name)"
  if (-not (Test-Path $dest)) { New-Item -ItemType Junction -Path $dest -Target $_.FullName | Out-Null }
}
```

### Bağlantı — macOS / Linux

```bash
ln -s ~/solak-skills/skills/solak-design-ui ~/.claude/skills/solak-design-ui
```

### Kopya

```powershell
Copy-Item -Recurse skills\solak-design-ui "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse skills\* "$env:USERPROFILE\.claude\skills\"
```

```bash
cp -R skills/solak-design-ui ~/.claude/skills/
```

### Doğrulama

1. `~/.claude/skills/<skill>/SKILL.md` okunabiliyor mu?
2. Yeni bir oturumda skill listesinde **açıklamasıyla** görünüyor mu?
3. Ad görünüp açıklama görünmüyorsa frontmatter ayrıştırılamamış: satır sonlarını (LF olmalı — [`.gitattributes`](.gitattributes) bunu zorlar) ve YAML geçerliliğini kontrol et.
4. Hiç görünmüyorsa klasör adı ile `name` aynı mı?

### Ajanla kurulum

Bu repoyu bir ajan kuruyorsa: **junction dene → hata alırsan symlink dene → o da olmazsa kopyala** ve kullanıcıya "kopya kuruldu, repo güncellenince tekrar kopyalanmalı" bilgisini ver. Hedefteki mevcut bir klasörü silmeden önce içeriğinin repoda bulunduğunu doğrula — kurulu kopya repodan ileride olabilir.

## Skill listesi

| Skill | Amaç | Durum |
|-------|------|-------|
| [solak-create-skill](skills/solak-create-skill/SKILL.md) | Bu repoda standarda uygun yeni skill üretir | ✅ stable |
| [solak-design-ui](skills/solak-design-ui/SKILL.md) | UX-first veri-yoğun ürün UI'ı: görev analizi → layout → TODO → adım adım uygulama. Tablo, filtre, form, dashboard. Kendi kendine yeten, İngilizce. Doğrulama betiği + 6 eval | 🧪 beta |

Güncel ve makine-okunur liste: [`registry.json`](registry.json)

### Doğrulama

`solak-design-ui` yapısal olarak doğrulanabilir — kırık referans, eksik dosya, geçersiz semver, boş dosya ve emekli dosya adları hata verir. Yalnızca standart kütüphane; kurulum adımı yok.

```bash
python skills/solak-design-ui/scripts/validate_skill.py
```

Aynı komut skill'e dokunan her PR ve push'ta [CI'da](.github/workflows/validate-solak-design-ui.yml) koşar. Dosya listesinin kaynağı [`manifest.yaml`](skills/solak-design-ui/manifest.yaml); değerlendirmeler [`evals/`](skills/solak-design-ui/evals/), örnekler [`examples/`](skills/solak-design-ui/examples/) altında.

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
