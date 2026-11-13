# Connector Routing Rules

Apply these rules when placing nodes and connectors in any diagram view of `architecture-diagram.html`. Plan coordinates for each view first, then draw.

## Engine helpers (from the template)

- `box(svg,x,y,w,h,lines,cls)` – node; `lines` is an array, prefix `*` = bold. `cls`: `accent`, `warn`, `store`.
- `grp(svg,x,y,w,h,cls)` – dotted group frame; `cls`: `wall` (solid boundary wall), `bound` (pulsing boundary).
- `arrow(svg,pts,opts)` – polyline connector. Options:
  - `dash:1` – control / replication / optional flow (marching dashes);
  - `both:1` – arrowhead at both ends;
  - `nohead:1` – no arrowhead (stubs, trunks into a bus);
  - `noflow:1` – no travelling light pulse (use on stubs and buses);
  - `halo:1` – draws a background-coloured halo under the line, so any line drawn **before** it shows a gap where they cross;
  - `label:[x,y,'text']` – label on a background pill.
- Group titles (`txt(...,'grpt')`) have a background stroke, but still place them where no line enters.

## Rules

1. **No fan-in.** When 3 or more nodes connect to one target, use short stubs into a spine or bus, then one trunk into the target.
2. **Orthogonal lanes.** Use horizontal and vertical segments only. Give each flow type its own lane (y or x coordinate) in the gap between groups.
3. **Fixed ports.** Lines start and end at box edges (top / bottom / left / right centre or a defined offset), never inside a box.
4. **Leave gaps ≥ 20 px** between parallel lanes and between a lane and a box edge or a label pill.
5. **Labels on pills, never on the line.** Place the pill beside the segment, in free space. Only use labels that exist in the source.
6. **Group titles away from entries.** If lines enter a group from the top, move its title to the bottom of the group.
7. **Unavoidable crossings.** Some layouts are not planar (e.g. two shared services each connected to the same two data domains). Draw the line that should appear "on top" last with `halo:1` so the other line shows a gap. Mention the crossing in the report.
8. **Arrowheads only where the flow ends.** Stubs and bus segments get `nohead:1`.
9. **Flow pulses only on real data flows.** Use `noflow:1` on stubs and buses so the motion doesn't look busy.
10. **Respect source structure.** Do not merge or split branches, loops or flows for neatness. Two loop-backs in the source stay two loop-backs, each in its own lane.

## Good and bad examples (illustrative)

| View | Bad | Good |
|---|---|---|
| Context | 11 straight lines from every actor / external system box to the centre circle | Stubs → vertical spine per group → one trunk into the circle; enterprise services on one horizontal bus below |
| Data & integration | Two shared components each drawn with diagonal lines to every data domain; 3 crossings | One request bus at y=188 with drops to each domain; a second flow in its own dashed lane at y=212; the one unavoidable crossing drawn with `halo:1` |
| Deployment | Diagonal lines from Component 1 and Component 2 to both environments, crossing status lines; labels on lines; replication arc crossing a storage line | Release bus at y=185 with drops; status data in its own dashed lane at y=212; right-angled storage links; replication as a short horizontal arrow between sites; group titles moved to the bottom |
| Key flow | Merging two loop-backs into one for neatness | Keep both loop-backs, nested in separate lanes (y=272 and y=236), labels between them |
| Labels | Adding generic labels such as "Box A to Box B" on trunks | No label unless the source names the flow |

## Geometry self-check

For each view, before reporting:
- list every connector with its points;
- check that no horizontal segment crosses a vertical segment except where intended (and then `halo:1` is set);
- check that no segment passes through a box rectangle or a text / title bounding box;
- check pill rectangles (`width ≈ chars × 6.6 + 18`, height 20) don't overlap lines or boxes.
