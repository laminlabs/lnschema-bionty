# Changelog

<!-- prettier-ignore -->
Name | PR | Developer | Date | Version
--- | --- | --- | --- | ---
⬆️ Upgrade and rename `lndb_setup` to `lndb` (v0.32.0) | [49](https://github.com/laminlabs/lnschema-bionty/pull/49) | [bpenteado](https://github.com/bpenteado) | 2023-02-14 | 0.6.9
🐛 Fixed taxon_id type | [48](https://github.com/laminlabs/lnschema-bionty/pull/48) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-17 | 0.6.8
⬆️ Upgrade dependencies | [47](https://github.com/laminlabs/lnschema-bionty/pull/47) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-17 | 0.6.7
⏪ Revert the last PR | [46](https://github.com/laminlabs/lnschema-bionty/pull/46) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-17 |
🐛 Fixed typo for postgres | [45](https://github.com/laminlabs/lnschema-bionty/pull/45) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-16 | 0.6.6
🎨 Change `Species.taxon_id` type to int | [43](https://github.com/laminlabs/lnschema-bionty/pull/43) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-13 |
👷 Extend CI to py3.8-3.10 | [42](https://github.com/laminlabs/lnschema-bionty/pull/42) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-12 |
🚚 Rename `Species.common_name` to `Species.name` | [41](https://github.com/laminlabs/lnschema-bionty/pull/41) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
🐛 Fix migration for sqlite | [40](https://github.com/laminlabs/lnschema-bionty/pull/40) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 | 0.6.5
♻️ Treat link tables as in all other schema modules | [39](https://github.com/laminlabs/lnschema-bionty/pull/39) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 | 0.6.4
🚚 Move knowledge version tables into module | [38](https://github.com/laminlabs/lnschema-bionty/pull/38) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 | 0.6.3
🧪 Added test for ontology autopopulate | [37](https://github.com/laminlabs/lnschema-bionty/pull/37) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-09 |
✅ Add migrations test | [36](https://github.com/laminlabs/lnschema-bionty/pull/36) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 |
✨ Added bionty_version table | [35](https://github.com/laminlabs/lnschema-bionty/pull/35) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-07 | 0.6.2
🎨 Updated bionty_versions | [34](https://github.com/laminlabs/lnschema-bionty/pull/34) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-05 |
✨ Added `bionty_versions` table | [33](https://github.com/laminlabs/lnschema-bionty/pull/33) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-18 | 0.6.1
🏗️ Introduce relationships, move Features table to core | [32](https://github.com/laminlabs/lnschema-bionty/pull/32) | [falexwolf](https://github.com/falexwolf) | 2022-11-17 | 0.6.0
⚡ Implemented knowledge as a decorator | [31](https://github.com/laminlabs/lnschema-bionty/pull/31) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-11 | 0.5.4
✨ Added populator for ontologies | [30](https://github.com/laminlabs/lnschema-bionty/pull/30) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-11 |
♻️ Refactor knowledge population | [29](https://github.com/laminlabs/lnschema-bionty/pull/29) | [falexwolf](https://github.com/falexwolf) | 2022-11-06 |
🐛 Fixed postgres migration script | [28](https://github.com/laminlabs/lnschema-bionty/pull/28) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-06 | 0.5.3
✨ Use bionty to populate species | [27](https://github.com/laminlabs/lnschema-bionty/pull/27) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-06 | 0.5.2
🐛 Fix prefix | [26](https://github.com/laminlabs/lnschema-bionty/pull/26) | [falexwolf](https://github.com/falexwolf) | 2022-11-03 | 0.5.1
🎨 Modularize and capitalize | [24](https://github.com/laminlabs/lnschema-bionty/pull/24) | [falexwolf](https://github.com/falexwolf) | 2022-11-03 | 0.5.0
🎨 Updated cell marker id gen | [23](https://github.com/laminlabs/lnschema-bionty/pull/23) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-25 | 0.4.5
✏️ Updated species id to be 3 chars | [22](https://github.com/laminlabs/lnschema-bionty/pull/22) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-24 | 0.4.4
🧑‍💻 Added naming convention | [20](https://github.com/laminlabs/lnschema-bionty/pull/20) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-20 |
🩹 Fix type annotations of primary keys | [19](https://github.com/laminlabs/lnschema-bionty/pull/19) | [falexwolf](https://github.com/falexwolf) | 2022-09-29 | 0.4.3
✏️ Changed ids to str | [18](https://github.com/laminlabs/lnschema-bionty/pull/18) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-29 | 0.4.2
🍱 Added `description` and `version` columns to the gene table | [17](https://github.com/laminlabs/lnschema-bionty/pull/17) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-27 | 0.4.1
🚚 Update primary keys to universal ids | [16](https://github.com/laminlabs/lnschema-bionty/pull/16) | [falexwolf](https://github.com/falexwolf) | 2022-09-22 | 0.4.0
🚚 Rename column in version table, add testdb, and migration script | [15](https://github.com/laminlabs/lnschema-bionty/pull/15) | [falexwolf](https://github.com/falexwolf) | 2022-09-22 | 0.3.1
✨ Add migrations infra | [14](https://github.com/laminlabs/lnschema-bionty/pull/14) | [falexwolf](https://github.com/falexwolf) | 2022-09-22 | 0.3.0
🩹 Added unique constraints | [13](https://github.com/laminlabs/lnschema-bionty/pull/13) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-22 |
🐛 Fixed API ref | [12](https://github.com/laminlabs/lnschema-bionty/pull/12) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-06 | 0.2.4
🎨 Import additional modules, species -> species_id | [11](https://github.com/laminlabs/lnschema-bionty/pull/11) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 | 0.2.3
🚚 Rename gene_symbol to symbol, protein_name to name | [10](https://github.com/laminlabs/lnschema-bionty/pull/10) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 | 0.2.2
⬆️ Update schema to match bionty 0.2.0 | [9](https://github.com/laminlabs/lnschema-bionty/pull/9) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 | 0.2.1
🚚 Rename `lndb-schema-bionty` to `lnschema-bionty` | [8](https://github.com/laminlabs/lnschema-bionty/pull/8) | [falexwolf](https://github.com/falexwolf) | 2022-08-19 | 0.2.0
🔧 Add schema module id | [7](https://github.com/laminlabs/lnschema-bionty/pull/7) | [falexwolf](https://github.com/falexwolf) | 2022-08-18 |
🍱 Updated the gene table to match new ensembl table | [6](https://github.com/laminlabs/lnschema-bionty/pull/6) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-18 | 0.1.4
🎨 Changed type of `species` and `entrez_gene_id` in `gene` table to `int` | [5](https://github.com/laminlabs/lnschema-bionty/pull/5) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-15 | 0.1.3
🚚 Move `biolab` to `lnschema-wetlab` | [4](https://github.com/laminlabs/lnschema-bionty/pull/4) | [falexwolf](https://github.com/falexwolf) | 2022-07-31 |
✨ Introduced featureset to replace geneset and proteinset | [2](https://github.com/laminlabs/lnschema-biology/pull/2) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-31 | 0.1.2
🎨 Changed `resolution` to `platform` in `readout_type` | [commit](https://github.com/laminlabs/lnschema-biology/commit/14552dd71cea463157f29201126ca9a2e259aded) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-23 | 0.1.1
🚚 Move code from `lamindb-schema` | [1](https://github.com/laminlabs/lnschema-biology/pull/1) | [falexwolf](https://github.com/falexwolf) | 2022-07-23 | 0.1.0
