# Motion and Hover Catalogue

All of this is already implemented in `templates/architecture-diagram.html`. Keep it unless the user asks for changes. The motion level is subtle and premium, never busy.

## Page level

| Effect | Implementation |
|---|---|
| Moving gradient + floating orb behind the header | `.sky` + `.orb`, keyframes `drift` (18 s) and `float` (9 s) |
| Sliding highlight bar under the active tab | `.ink`, positioned by `moveInk()` |
| View fade / slide-in on tab switch | `section.view.on` → `viewIn` |
| "Animate flows" on / off switch | `#flowtg` toggles `body.noflow` |

## On entering a tab

| Effect | Implementation |
|---|---|
| Staggered reveal of boxes, bands, rows, cards | class `rv` with `--i` index; `.view.in .rv` → `rise`, delay `--i × 40 ms` |
| Solid lines draw themselves | `.ln.draw` with `pathLength=1` → `draw` |
| Arrowheads and label pills fade in after the line | `.hd`, `.pill`, `.lbl` → `fade` |
| Light pulses travel along solid data flows | `.flow` overlay path, `flow` keyframes |
| Dashed control / replication lines march slowly | `.ln.dash` → `march` |
| The reveal replays every time a tab opens | `show()` removes and re-adds `in` |

## View-specific interactions

| View | Interaction |
|---|---|
| Logical | Driver chips pulse matching blocks (`.blk.hl` → `pulse`); detail panel slides in over a blurred scrim |
| Key flow | Play / Step / Reset; progress bar fills; current step glows; event-log markers light up |
| Critical scenario | Scenario chips animate the path step by step (`N` map + scenario arrays); rest dims (`svg.trace`) |
| Data & integration | Solid domain walls; "Show broker access" lights the broker path |
| Deployment | Pulsing boundary on the primary environment (`.grp.bound`) |
| Context | Soft ring pulse around the central system |

## Hover (premium motion)

| Element | Hover effect |
|---|---|
| Headings, lead text, notes, open questions (`.dr`) | **Drift**: text moves down 10 px over 0.8 s and floats back on leave. An invisible 14 px strip above (`::after`) keeps hover active, so there is no jitter |
| Logical blocks | Spring lift 6 px, sheen sweep, name rises and turns blue, description drifts down, epic tag rises; also on keyboard focus |
| Layer bands | Layer number grows and glows; layer name drifts; border lights up |
| Diagram boxes | Text drifts down 5 px; box glows; connected lines turn blue, everything else dims (`linkHover`, uses box bounds `_b` and connector points `_p`) |
| Connectors | Label pill rises and lights up |
| Traceability rows | Row slides right; blue bar on the left edge; text brightens |
| Decision cards | Spring lift; blue line draws across the top; ID slides right; title turns blue; text drifts |
| Buttons, chips, tabs | Lift 2 px with soft glow |

Timing: spring `cubic-bezier(.34,1.56,.64,1)` ≈ 0.35–0.45 s for lifts; `0.8 s ease` for drift.

## Rules

- Only the hovered element and its own children move. Never shift layout.
- Any element that moves away from the cursor needs a hit-area extension (`::after`) to avoid jitter.
- Node-to-line linking requires `_b` (bounds) on every node group: `box()` and `dia()` set it automatically; set it manually for custom shapes (circles, step groups).
- Reduced motion (`prefers-reduced-motion: reduce`): all animations and transitions off, flow pulses and rings hidden, no hover transforms.
