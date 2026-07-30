# İsimlendirme Standardı

## Format

```
solak-<eylem>-<hedef>
```

- **Prefix `solak-`**: zorunlu. Bu koleksiyonun skill'lerini üçüncü parti skill'lerden ayırır ve isim çakışmasını önler.
- **`<eylem>`**: fiil, tekil, emir kipi (İngilizce). `review`, `fix`, `design`, `audit`, `upgrade`, `debug`, `optimize`, `write`, `generate`, `analyze`, `plan`.
- **`<hedef>`**: eylemin uygulandığı nesne. `pr`, `ci`, `api`, `auth0`, `dotnet`, `mongodb`, `query`, `adr`, `tests`, `incident`, `migration`.

Tümü **kebab-case** ve **küçük harf**. Klasör adı ile `SKILL.md` içindeki `name` alanı **birebir aynı** olmalı.

## Örnekler

| Skill | Anlamı |
|-------|--------|
| `solak-review-pr` | Pull request incelemesi yapar |
| `solak-fix-ci` | Kırık CI pipeline'ını onarır |
| `solak-design-api` | API sözleşmesi tasarlar |
| `solak-audit-auth0` | Auth0 yapılandırmasını denetler |
| `solak-upgrade-dotnet` | .NET sürüm yükseltmesi yürütür |
| `solak-debug-mongodb` | MongoDB sorun teşhisi yapar |
| `solak-optimize-query` | Yavaş sorguyu iyileştirir |
| `solak-write-adr` | Architecture Decision Record yazar |
| `solak-generate-tests` | Eksik testleri üretir |
| `solak-analyze-incident` | Olay sonrası analiz çıkarır |
| `solak-plan-migration` | Göç planı hazırlar |
| `solak-review-architecture` | Mimari değerlendirmesi yapar |

## Kurallar

1. **Eylem önce, hedef sonra.** `solak-pr-review` değil → `solak-review-pr`.
2. **Tek eylem, tek hedef.** Üç parçalı hedef gerekiyorsa skill fazla geniş; böl.
3. **Kısaltma yerine yaygın kullanım.** `pr`, `ci`, `api`, `adr` kabul; `authz-cfg` gibi uydurma kısaltma yok.
4. **Çoğul yalnızca doğal çoğulda.** `generate-tests` ✅, `review-prs` ❌ (`review-pr` tek PR'a da PR yığınına da uygulanır).
5. **Ürün/marka adları olduğu gibi ve küçük harf.** `auth0`, `dotnet`, `mongodb`, `azure-devops`.
6. **İsim değişmez.** Bir skill yayınlandıktan sonra yeniden adlandırmak kurulumları bozar; yeni isim gerekiyorsa yeni skill oluştur ve eskisini `deprecated` işaretle.

## Kaçınılacak isimler

| ❌ | Neden | ✅ |
|----|-------|-----|
| `pr-review` | prefix yok | `solak-review-pr` |
| `solak-pr-reviewer` | eylem sonda, `-er` eki | `solak-review-pr` |
| `solakReviewPr` | camelCase | `solak-review-pr` |
| `solak-helper` | eylem/hedef belirsiz | somut bir isim seç |
| `solak-do-everything` | kapsam sınırsız | ayrı skill'lere böl |
