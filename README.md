# OSreconstruction-comparator

Independent Comparator verification of the three theorems of
[**xiyin137/OSreconstruction**](https://github.com/xiyin137/OSreconstruction) (Lake project
`os-reconstruction/`): the Osterwalder–Schrader correspondence between Euclidean Schwinger
functions and relativistic Wightman distributions, in both directions, for every spatial
dimension `d ≥ 1`.

This repository contains **no mathematics of its own**. It is a thin wrapper, in the sense of
the [Palomar Registry](https://palomar-registry.org) policy: it exposes the package's theorems
to [Comparator](https://github.com/leanprover/comparator) and names the substantive
development, pinned to an exact commit, in `formalization.yaml`.

## The two files that matter

| file | what it is |
|---|---|
| `RegistryChallenge.lean` | the statement a mathematician audits — **imports Mathlib and nothing else** |
| `RegistrySolution.lean` | the same three declarations, proved from the package |

The Challenge may not import the package, or anything else project-specific, anywhere in its
transitive import closure. It is therefore the package's own Mathlib-only audit file,
[`verification/comparator/Definitions.lean`](https://github.com/xiyin137/OSreconstruction/blob/main/os-reconstruction/verification/comparator/Definitions.lean),
reproduced verbatim, followed by the three proof obligations:

| theorem | statement |
|---|---|
| `OSReconstructionAudit.e_to_r` | OS axioms E0–E4 on zero-diagonal tests + linear growth ⟹ Wightman distributions, Wick-paired with the input |
| `OSReconstructionAudit.e_to_r_osii` | OS II's form: with growth E0′ (4.1), Wightman distributions exist, satisfy the output bound R0′ (4.3), and are unique among Wick-paired families |
| `OSReconstructionAudit.r_to_e` | every Wightman family yields, via an explicit constructor, Schwinger functions satisfying E0–E4 and Wick-paired with it — no growth hypothesis |

`RegistrySolution.lean` is self-contained in the same way: the package's `Definitions.lean`, its three
bridge files (`eToR_iff`, `eToROSII_iff`, `rToE_iff`) and its `Solution.lean` concatenated into
one module, importing only Mathlib and the package's production modules. Both files start with
`public import Mathlib`. Two facts about Lean's module system force this layout: an auxiliary
proof of an *imported* definition is not re-exported identically, so the compared definitions
must be elaborated locally on both sides; and instance search inside proof terms depends on the
Mathlib modules loaded, so both sides must load the same ones. Comparator then checks that every
shared constant matches structurally, that the proofs rest on nothing beyond Lean's three core
axioms, and replays the exported proofs through a fresh kernel (and NanoDa).

The module names carry a `Registry` prefix because the package itself ships libraries rooted at
`Challenge` and `Solution`, and Palomar resolves modules by name across the whole Lake workspace.
`scripts/gen_challenge.py` and `scripts/gen_solution.py` regenerate the pair from the package's
`verification/comparator/` directory; run both after re-pinning and commit the result.

## What the theorems do and do not say

The package's
[mathematical specification](https://github.com/xiyin137/OSreconstruction/blob/main/os-reconstruction/docs/COMPARATOR_NOTE.html)
states every definition in mathematical notation. Four conventions are weaker than the textbook
ones and are visible in the Challenge: the forward tube additionally requires `Im z₀` in the
open forward cone (a proper subset of the literal `n`-point tube for `n > 0`); locality is
asserted for adjacent transpositions; reflection positivity is stated through a total coercion
onto zero-diagonal tests; and Euclidean growth is a hypothesis of the forward theorems, not a
conclusion of the reverse one — so the two directions do not compose to a biconditional. This
is Osterwalder–Schrader II's own correction of OS I, reproduced faithfully. "Wightman" means
the Wightman *function* axioms; no Hilbert space or field operators appear.

## Verifying

```bash
lake build                  # builds RegistryChallenge and RegistrySolution — both are default targets
./scripts/verify-comparator.sh
bash scripts/check-pair.sh  # source-level gate: no axioms/escape hatches; Challenge has
                            # exactly the three challenge-hole sorries, Solution none
```

`verify-comparator.sh` fetches and pins Comparator, `lean4export`, NanoDa and Landrun, then
runs the comparison under a real sandbox with the independent NanoDa kernel replay. The
`lean4export` pin tracks `lean-toolchain` (`v4.35.0-rc4`); revisit it, and NanoDa
compatibility, whenever the toolchain moves. Landrun is Linux-only, so the scripted run wants
Linux — CI does it on every push. On macOS the package's own
`verification/check.sh comparator --development` performs the same comparison without a
sandbox.

## The pin, and the canary

`lakefile.toml` requires the package at a fixed commit. That is deliberate: a registry entry
names an exact commit, and re-pinning should be a decision rather than a drift. CI carries a
scheduled canary that builds the pair against the package's `main` instead; a red canary means
the registered statement no longer builds against the package, the signal to re-pin,
regenerate the Challenge, and re-verify.

## Provenance

The package is by Xi Yin, Michael R. Douglas and Anna Mei; its comparator audit surface
(`Definitions.lean`, bridges, specification) was added in
[xiyin137/OSreconstruction#97](https://github.com/xiyin137/OSreconstruction/pull/97).
Apache-2.0, matching the package.
