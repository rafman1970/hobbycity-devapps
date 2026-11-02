# rf_testpo — test Bringans purchase order

Creates a purchase order in Cin7 for one item from Bringans (Trevor Bringans
Ltd, Cin7 member 5226). It looks up the item's cost in Supabase
(`product_summary.cost_nzd`) and puts the PO through the Cin7 API.

## Running it

Dry run (the default): shows the PO it *would* create, and creates nothing.

```
python C:\HobbyCity-DevApps\rf_testpo\rf_testpo.py
```

Live: creates a **real** PO in Cin7 and prints its number.

```
python C:\HobbyCity-DevApps\rf_testpo\rf_testpo.py --live
```

Options:

| Option   | Default    | Meaning                     |
|----------|------------|-----------------------------|
| `--code` | `TAM87062` | Cin7 product code           |
| `--qty`  | `1`        | Quantity, in units          |
| `--live` | off        | Actually create the PO      |

Example: `rf_testpo.py --code TAM87062 --qty 2 --live`

`RunTestPO.bat` runs the same script and passes options through, so
`RunTestPO.bat --live` works too.

## Finding and cleaning up the test PO

- In Cin7, Supplier Invoice Reference is `TEST - rf_testpo`, and Internal
  Comments say `TEST PO from rf_testpo <date time> - void me`.
- **Every live run creates another real PO. Void each one in Cin7 when
  you're done with it.** Until it's voided, it counts as stock on order, so
  the reorder tools will order less of that item.

## Errors

- `Missing in .env: ...` — `.env` isn't in `C:\HobbyCity-DevApps\`, or the
  value named is missing from it.
- `<code> not found in product_summary` — no product with that Cin7 code.
- `Cin7 PO failed: ...` — Cin7 refused the PO. The message says why.
