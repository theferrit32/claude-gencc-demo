# GenCC Submissions Viewer

A zero-dependency, single-file HTML viewer for [GenCC](https://thegencc.org/) gene-disease classification data. Supports configurable grouping, custom classification tiers, and MONDO hierarchy-based disease clustering with an interactive cluster review UI.

## Usage

1. Download your submissions CSV from [thegencc.org](https://thegencc.org/download.html)
2. Open `gencc-viewer.html` in a browser
3. Drop the CSV file onto the page

### Optional: Disease clustering

To merge related MONDO disease terms, provide the MONDO hierarchy:

```bash
# Download mondo.json from https://mondo.monarchinitiative.org/
# Then generate the compact hierarchy file:
python3 trim_mondo.py mondo.json mondo-hierarchy.json
```

Drop `mondo-hierarchy.json` (or the raw `mondo.json`) onto the hierarchy drop zone in the viewer. This enables hop-based disease clustering and the Cluster Review tab.

## License

MIT
