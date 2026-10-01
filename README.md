# starknet-ecosystem-data

Ecosystem Data snapshots of the Starknet Ecosystem.

## Snapshots

| File | Taken | Profiles |
| --- | --- | --- |
| [`starknetdata-sep-2026.json`](starknetdata-sep-2026.json) | September 2026 | 298 |
| [`starknetdata-jan-2026.json`](starknetdata-jan-2026.json) | January 2026 | 219 |
| [`starknet.json`](starknet.json) | June 2025 | 173 |

Each snapshot holds every profile carrying the Starknet tag in The Grid, with its
products, assets, socials, and URLs. The newest file is the current one. The older
files stay in place so you can compare the ecosystem over time.

The field set grew between snapshots, so older files carry fewer fields.

## Regenerating

`scripts/fetch_snapshot.py` reads The Grid's public GraphQL API and writes a new
snapshot. It needs no credentials:

```
python3 scripts/fetch_snapshot.py starknetdata-<month>-<year>.json
```

# The Grid

For more on Ecosystem Data in Web3, see https://thegrid.id/

You can also access live and updated data via The Grid's API.

## Dual License

This json file is dual licensed and available under:

Apache 2.0; and

Open Database License
