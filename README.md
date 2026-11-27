# NEXUS ARCHIVE // MY KEF — v2

QR-linked kitchen-exhaust asset intelligence — the registry, passport,
diagnostics, and service history for hood and fan systems, in one place.
Built for the tech in the field and the QA eye back at the desk: every asset
has a record, every record has evidence, and nothing is left to memory or a
paper note.

> **Live status — read this first:** This v2 build is **NOT pushed and NOT
> live**. The repo **does not exist yet** — `AntManThePro/my-nexperimental-kef`
> will be created later, on Anthony's go. **Claim no live URL** for this
> build. The old live site (`my-kef.netlify.app`) still serves the old build.

## What it does

MY KEF tracks kitchen-exhaust assets (KEF, PCU, ESP, water-wash) across
sites: what each asset is, where it lives, what condition it is in, what has
been done to it, and what still needs doing. It is a working archive, not a
live monitoring system — there is no live telemetry feed. Δp readings are
demo data, shown as reading / stage limit (pre-filter 0.42 / 0.50, bag/HEPA
0.81 / 1.00, carbon 0.38 / 0.60 in wc).

## The 8 sections

1. **Command** — the overview: dynamic stats (04 assets / 04 open issues /
   04 service entries / 07 archived sources), the PCU airflow path with Δp
   reading/limit pairs and a near-limit flag, equipment overview with
   component chips, the unresolved issue board, recent activity, a
   diagnostic navigator, and an archive feed. Command 01.7 is the Flow
   Simulator (illustrative grease-load / wash simulation, not telemetry).
2. **Registry** — the master list of assets. Search by id, name, site or
   component; filter by type (All 4 / KEF 1 / PCU 1 / ESP 1 / Water-Wash 1)
   and by status (All 4 / Nominal 1 / Watch 2 / Fault 1). Each card shows
   model, issue count, and last log date, plus a scannable QR mini.
3. **Asset Passport** — one asset, one page: QR label card, dossier (type,
   site, model, serial, status, site code DMO, QR id, install, last
   service), Δp readings (PCU), component stages, open issues (per-asset
   count first), linked manuals & guides, related diagnostics, timeline,
   and the safety constraint. Reached by tapping an asset — there is no
   passport entry in the sidebar.
4. **Diagnostics** — 6 curated sample-knowledge cards: Low airflow / poor
   capture at hood (Airflow), Odor / smoke carryover at discharge (Odor),
   Filter stage pressure drop high (Pressure), ESP fault indicator /
   arcing noise (Electrical, high voltage), Wash cycle not running /
   incomplete (Wash), Fan vibration / noise (Mechanical). Possible causes
   are hypotheses to investigate — never a confirmed diagnosis. All six
   cards are readable by every role, including the high-voltage ESP card
   for Cleaners and public scanners, with its safety wording — viewing it
   is not doing the work. Diagnostics viewing is not role-gated; only the
   service log is (Cleaner cannot enter a diagnosis; Public scanner cannot
   see the log at all). The ESP card also carries a second symptom,
   "ESP light completely off", with its own causes and evidence; the
   Pressure card carries "Filters missing", "Pressure switch set too
   low", "Tubing clogged"; the Airflow card carries "Fan speed too high"
   and "Pre-filters missing or clogged" — all merged from Variant 2 in
   v2.3 and cited to the OEM manuals in the archive, not independently
   verified against the manuals.
5. **Archive** — 7 official-source **links** (not readings, photos, or
   history): CaptiveAire PCU IOM, Gaylord RSPC ESP OW, Gaylord RSPC TPF
   with FM-100, ASHRAE Standard 62.1, UL 705, Halton KVE water-wash
   manual, NFPA 96. Filter by type (OEM Manual / Standard / Guidance)
   and by tag; search by title, publisher, or tag. Footer: "References
   are starting points. Confirm exact model, revision, listing, and
   site requirements before work."
6. **Service Log** — what was done, when, and by whom. 4 seed entries
   (LOG-0004–LOG-0007). New entries are saved in the browser's
   localStorage and survive reloads until browser storage is cleared.
   There is no shared backend yet. The form defaults the date to
   **today in the user's local timezone**. An "Export log (JSON)"
   button in 06.2 downloads all entries as `mykef_log_v1.json`, for
   staff roles only (Public scanner never sees it).
7. **Blueprint** — how the production platform would be built: architecture,
   data model, RBAC, privacy & QR, roadmap, integrations, acceptance.
   A design document — there are **no drawings** in it.
8. **About** — what MY KEF is, what it is not, and the honest limits of the
   data inside it (see "Demo data" below).

## QR labels

Every asset can carry a printed QR label. Scanning it opens that asset's
passport directly. QR codes encode:

```
https://mykef.example/a/<ASSET-ID>
```

`mykef.example` is an **example domain — it resolves nowhere yet**. Clicking
a scan URL inside the app shows an explanatory toast instead of navigating
away. The Print label button opens an on-page printable label (with a print
fallback if the browser blocks pop-ups), so a blocked pop-up never strands
the user. The QR format is fixed so labels printed now stay valid once the
real domain is pointed at the live app; until then, a scanned code will not
open a working page. Replace `mykef.example` with the real domain before
printing labels for live use.

## Honest demo-data note

All assets, sites, readings, and logs in this build are **fictional demo
data**. There is **no live telemetry** — no sensor is connected and no reading
arrives from the field on its own. Service entries live in **localStorage
only** (key `mykef_log_v1`) and survive reloads until browser storage is
cleared. Do not treat any number in this build as a real measurement of a
real fan.

## Role gating

- **Public scanner** (someone who scans a QR label with no login) — sees a
  **minimal passport only**: asset ID, type, safety notice, and a
  report-a-concern form (local only, one report per minute). No serial,
  model, location, site, timeline, issues, sources, QR detail, or passport
  buttons. The service log is hidden entirely.
- **Cleaner** — can log cleaning visits and observations and attach photo
  evidence. **Cannot diagnose**: the Diagnosed field is disabled, any
  pre-typed diagnosis is cleared on switching to Cleaner, and the save
  handler rejects/blanks a diagnosis even if one is somehow submitted.
  The high-voltage ESP diagnostic card is visible to every role, with its
  safety wording — viewing it is not doing the work; there is no lock on it.
- **Technician** — cleaner rights plus diagnoses, readings, actions, and
  verification.
- **Manager / Admin** — in this prototype, sees exactly what Technician
  sees; there is no manager-only view or asset editing. The service-log
  JSON export (06.2) is available to all staff roles — Cleaner,
  Technician, and Manager / Admin alike — because it only downloads
  entries the role can already see. The
  Blueprint RBAC table (07.3) lists what a production manager could do:
  manage assets, sources, users, roles, labels; export reports; audit log.
  (The role switcher in the header is a demo affordance; in production,
  roles come from authenticated accounts.)
- There is **no QA role** in this app.

The log form's role dropdown offers Cleaner / Technician only and is synced
to the header role (Manager / Admin maps to Technician in the form).

## Photo evidence

Photos attached to a log entry are downscaled to max 480 px thumbnails and
stored as data URLs with the entry in localStorage (max 3 per entry). If
storage fails, the entry is still saved without photos and a toast says so.
Thumbnails render inside the saved log entry. Nothing is ever uploaded.

## Icons

Custom set in `icons/` — five-blade rotor in neon green (`#00ff87`) on void
(`#07070a`), cyan (`#60efff`) QR finder marks and archive-bracket corners.
Rebuild them any time with `python3 icons/build_icons.py` (Pillow only).

- `icons/favicon.ico` — multi-size 48 / 32 / 16 (simplified bold rotor)
- `icons/favicon-192.png` — 192×192
- `icons/favicon-512.png` — 512×512
- `icons/apple-touch-icon.png` — 180×180

`manifest.json` at the project root wires the 192 / 512 icons (plus the
180 Apple touch icon) into the PWA install prompt. Manifest name
"NEXUS ARCHIVE // MY KEF", short name "MY KEF", theme `#07070a`.

## Files

```
mykef-rebuild-v2/
├── index.html        # single file, zero external dependencies (QR generator inline)
├── README.md
├── manifest.json
└── icons/
    ├── build_icons.py
    ├── favicon.ico
    ├── favicon-192.png
    ├── favicon-512.png
    └── apple-touch-icon.png
```

## Easter egg

*Typing `GREASE` anywhere — or triple-clicking the rotor emblem — spins the
fan and shows a grease-cup joke.*

## v2.4 changes (2026-11-27 — Time + grease-type view in the Flow Simulator)

- **Time since last cleaning + grease type (Command 01.7).** The Flow
  Simulator gains a "TIME SINCE LAST CLEANING" preset row (2 WEEKS /
  1 MONTH / 2 MONTHS / 3 MONTHS) and a "GREASE TYPE" selector
  (Charbroil / animal fat · Fryer oil · Wok / high-heat oil · General
  moderate · Light / low-volume). Picking a type and a time sets the
  simulator's load and redraws everything — grease bar, flow-line
  colour, pressure and capture readouts. The result line also reports
  whether the load is past the pink near-limit line (load 40), the
  weeks until that type hits the pink zone, and the matching NFPA 96
  inspection interval for the cooking type. RUN FLOW / LOAD FILTERS /
  WASH keep working after a preset (manual override, which clears the
  preset highlight); picking a preset again re-applies its computed
  load. The simulator and the new controls are visible to every role
  (viewing, not doing work), same as the diagnostic cards. No new
  subsection — 01.7 stays collapsible and closed by default.
- **Illustrative load rates (defaults, NOT measured data).** Weekly
  load points: Charbroil / animal fat 20, Wok / high-heat oil 17,
  Fryer oil 15, General moderate 8, Light / low-volume 4. Load =
  rate × weeks (1 month = 4 weeks), capped at 100. Resulting loads:
  charbroil 40 / 80 / 100 / 100, wok 34 / 68 / 100 / 100, fryer
  30 / 60 / 100 / 100, moderate 16 / 32 / 64 / 96, light 8 / 16 /
  32 / 48 (2 weeks / 1 month / 2 months / 3 months). Weeks to the
  pink zone (40 ÷ rate): charbroil ~2.0, wok ~2.4, fryer ~2.7,
  moderate ~5.0, light ~10.0. The existing formulas are unchanged:
  pressure = 0.40 + load × 0.01 in wc; capture = max(62, 95 − load
  × 0.22)%. The UI and this entry both state the rates are
  illustrative defaults, not measured data — tune them from field
  experience. NFPA 96 inspection intervals shown in the app:
  Charbroil / solid fuel Monthly; Fryer oil and Wok / high-heat oil
  (high-volume) Quarterly; General moderate Semi-annually; Light /
  low-volume Annually.

## v2.3 changes (2026-11-27 — Flow Simulator merge from Variant 2)

- **Flow Simulator (new Command 01.7, "Flow Simulator // Grease Load &
  Wash").** Ported from Anthony's earlier Variant 2 file and rebuilt in
  this app's style: inline `<canvas>` (900×320), no CDN, same palette.
  RUN FLOW / LOAD FILTERS (+12/tap, max 100) / WASH (−35/tap, min 0),
  grease bar, flow lines turn pink above load 40, live pressure and
  capture readouts. Simulator formulas (illustrative only): pressure =
  0.40 + load × 0.01 in wc; capture = max(62, 95 − load × 0.22)%.
  Labelled throughout as a simulation — "SIMULATION · ILLUSTRATIVE —
  NOT LIVE TELEMETRY · NOT A MEASUREMENT" — and kept separate from the
  verified 01.1 Δp readings, which are untouched. The five zones carry
  the target's airflow-path stage names (HOOD · PRE-FILTER · BAG / HEPA
  · CARBON · FAN + DISCHARGE, with FAN and DISCHARGE combined into the
  final zone). Fixed Variant 2's internal inconsistency: the initial
  capture display is computed from the formula (95 at load 0), not
  hard-coded 94. Collapsible like every other subsection, closed by
  default (storage key `mykef_collapsed_v2`); 27 subsections total now.
- **Diagnostics fold-in (no 7th card).** Genuinely new Variant 2
  causes/actions only, re-expressed in the app's causes/evidence
  structure and cited to the OEM manuals already in the archive — they
  were **not independently verified against the manuals**: ESP card
  gains "Bent collector plates", "Loose ionizer wires", "Debris between
  plates" plus evidence "Straighten plates, reseat wires and dry
  completely — qualified personnel only" (Gaylord RSPC ESP OW), and a
  second symptom in the same card, "ESP light completely off", with
  causes "Door interlock not made", "Wash cycle active", "Cells hard
  shorted" and evidence "Confirm door fully closed; wait for wash or
  cancel; check breaker and power pack"; Pressure card gains "Filters
  missing", "Pressure switch set too low", "Tubing clogged" plus
  evidence "verify all filters installed; verify switch setpoint"
  (CaptiveAire PCU IOM); Airflow card gains "Fan speed too high" and
  the nuance "Pre-filters missing or clogged". Variant 2's "Verify all
  doors and seals" was **not** ported — the Odor card's "confirm all
  stages seated" already covers it.
- **Export log (JSON).** New "Export log (JSON)" button in Service Log
  06.2, inside the staff-only log area (Public scanner never sees it).
  Downloads the full service log — the 4 seed entries plus any user
  entries, in the app's own schema — as `mykef_log_v1.json`. Available
  to all staff roles (Cleaner, Technician, Manager / Admin alike); it
  is **not** manager-only, and Manager still equals Technician
  everywhere else in this prototype. The README and Blueprint 07.3
  wording that said the prototype has "no export" is corrected.
- **Archive footer.** "References are starting points. Confirm exact
  model, revision, listing, and site requirements before work." now
  sits below the source list in Archive (05).
- Nothing else from Variant 2 was ported: no 5th asset (counts stay
  04/04/04/07, computed from data), no hero/stat/CTA changes, no Tech
  name field, no Action/Status dropdown schema changes, no CDN links,
  no "MyKEF:…" QR payload, no safety-gate text (already subsumed).

## v2.2 changes (2026-11-27 — Anthony's phone check)

- **All subsections start collapsed.** Every numbered subsection now
  loads closed — tap a header to open it. The choice is remembered:
  expanded state persists in localStorage (key `mykef_collapsed_v2`)
  across role switches, passport re-renders, and reloads. The key was
  bumped from v2.1's `mykef_collapsed_v1` (which recorded collapsed
  sections under an expanded default) so no old stored state can leak
  the old behavior into this version; the old key's data is not
  migrated. Collapsed = chevron points right, expanded = chevron points
  down. Nothing else changed.

## v2.1 changes (2026-11-27 — Anthony's phone check)

- **Collapsible subsections.** All 26 numbered subsections are now
  disclosure headers: Command 01.1–01.6, Passport 03.1–03.7 plus 03.P
  (Report a Concern, public only), Service Log 06.1–06.2, Blueprint
  07.1–07.7, About 08.1–08.3. Each header is a real `<button>` with a
  small neon rotor mark before the number, the title unchanged, and a
  down-arrow chevron at the right end. Tapping anywhere on the header —
  or Enter / Space on the keyboard — toggles just that subsection's body;
  the chevron rotates to point right when collapsed. Everything was
  expanded by default in v2.1 (superseded in v2.2 — all subsections now
  start collapsed; storage key `mykef_collapsed_v2`). Registry (02), Diagnostics (04), and Archive (05) have no
  numbered subsections, so nothing collapses there. Page-level safety
  blocks are never part of a collapsible body.
- **Role audit (Anthony asked whether the service log is the only thing
  that changes with role).** No — roles change three things, and the app
  now says so in About 08.2: the service log (public scanner cannot see
  it at all; Cleaner cannot enter a diagnosis), the asset passport
  (public scanner sees a minimal view — asset ID and type only — plus a
  report-a-concern form; staff roles see the full passport), and the
  diagnostics view. The high-voltage ESP card no longer shows a lock
  notice for Cleaner / Public: it is visible to every role with its
  safety wording, matching the live Lovable app and the RBAC table —
  viewing it is not doing the work. **Manager / Admin is confirmed
  identical to Technician everywhere in this prototype** — no
  manager-only view or asset editing (log export added in v2.3 — see
  above); the README and About
  now say so plainly instead of implying manager powers. The log form
  role still offers Cleaner / Technician only and maps Manager / Admin
  to Technician, matching the live app.
- No content, demo data, safety wording, icons, manifest, or Easter egg
  changed.

## v2 changes vs v1 (summary)

- Δp limits corrected: pre-filter 0.42 / **0.50** (was 0.90); bag 0.81 / 1.00
  flagged near-limit (81% of limit); carbon 0.38 / 0.60 — shown everywhere.
- Passport dossiers corrected to live values (e.g. PCU model
  "CaptiveAire-style PCU", serial "DMO-0002", installed 2019-03-02; KEF
  model "CaptiveAire / Greenheck-style", serial "DMO-0001", installed
  2021-06-15) and restructured to the live layout (dossier fields, QR label
  card, components, issues with ISS ids, linked manuals, related
  diagnostics, timeline with roles, safety block on all four passports).
- Sidebar has no Asset Passport (03) nav entry; hash routes mirror the live
  routes (`#/`, `#/assets`, `#/assets/<ID>`, `#/diagnostics`, `#/archive`,
  `#/log`, `#/blueprint`, `#/about`).
- Diagnostics rebuilt to the exact 6 live cards in order, including the
  Pressure card ("Filter stage pressure drop high").
- Archive rebuilt to the exact 7 live sources (ASHRAE 62.1 and UL 705 in;
  ASHRAE Handbook Ch. 33 and UL 8782 updates out) with the exact links.
- Service log seeds replaced with the exact 4 live entries; form uses
  local-today default date, type list without "Filter change", role list
  Cleaner/Technician only; photo evidence now persists with the entry.
- Extended safety-constraint wording everywhere, including the WWU passport.
- Storage copy corrected: entries persist in localStorage (no "resets on
  reload" wording anywhere).
- Command gained the issue board, recent activity, diagnostic navigator,
  archive feed, and component chips; stats are computed from the data.
- Registry gained status filter, summary line, last-log dates, and the real
  WWU site ("Main line hood, 12 ft").
- Blueprint rewritten to the live content (single-file app, no Lovable
  mention; localStorage truth in the Architecture node).
- Mobile: `.grid2` stacks below 480 px, About swatches wrap to 3 columns,
  top bar no longer squeezes search to nothing at 390 px.

## Carried over, unverified against video

- KEF component stage names/descriptions and the WWU dossier values are
  carried from the live-walk inventory in the build brief; no independent
  video frames verified them.
- Archive links are used exactly as supplied in the live-walk inventory
  (the correction overrides the first brief). Independently verified by
  search/fetch: the NFPA 96 page exists at nfpa.org, and an official
  CaptiveAire PCU IOM PDF exists — but at
  `captiveaire.com/manuals/pollution-control/pcu-oim.pdf`, NOT at the
  correction's `captiveaire.com/Manuals/PCU%20Manual.pdf?psrid=1.2-1`
  (unverified, used as supplied). The Gaylord, ASHRAE 62.1, UL 705, and
  Halton KVE URLs are as supplied and were not re-verified live.
