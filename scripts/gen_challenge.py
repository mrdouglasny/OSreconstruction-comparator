#!/usr/bin/env python3
"""Generate a single-file Palomar Challenge.lean from the package's Mathlib-only
Definitions.lean plus the three theorem holes. Palomar forbids any project source
in the Challenge's transitive import closure, so Definitions cannot be imported."""
import sys, re
defs_path, out_path = sys.argv[1], sys.argv[2]
src = open(defs_path).read()
# Retarget the two sentences that describe the old three-file layout.
src = src.replace(
    "`Challenge.lean` states the three propositions as named proof obligations.\n"
    "`Solution.lean` proves them using the production library. Both import this",
    "This file is the registry Challenge: it ends with the three propositions as\n"
    "named proof obligations. `Solution.lean` proves them using the production\n"
    "library; it imports the identical definitions from the package's module `Definitions`,\n"
    "and Comparator checks that every shared constant matches structurally. The text above\n"
    "the holes is the package's `Definitions.lean`, reproduced verbatim because this")
holes = '''
/-! ## The three registry obligations -/

namespace OSReconstructionAudit

theorem e_to_r {d : ℕ} [NeZero d] : EToR d := by
  sorry

theorem e_to_r_osii {d : ℕ} [NeZero d] : EToROSII d := by
  sorry

theorem r_to_e {d : ℕ} [NeZero d] : RToE d := by
  sorry

end OSReconstructionAudit
'''
open(out_path, "w").write(src.rstrip("\n") + "\n" + holes)
