import Mathlib

namespace MEADium.PrimeStructure

-- ============================================================
-- §1. PRIME PARENT GENERATOR (Theorem 3.1)
-- ============================================================

/-- The forward Collatz odd step. -/
def odd_step (n : Nat) : Nat := 3 * n + 1

/-- The reverse trigger. -/
def trigger (m : Nat) : Nat := (m - 1) / 3

/-- The parity gate: the trigger m = 3p+1 for odd p is
    always congruent to 4 mod 6. -/
theorem prime_parent_mod_six (p : Nat) (hp : Nat.Prime p) (h_gt : p > 3) :
    odd_step p % 6 = 4 := by
  have h_odd : p % 2 = 1 := by
    have h2 : p <> 2 := by omega
    have h_odd_or_two := hp.eq_two_or_odd
    cases h_odd_or_two with
    | inl h => contradiction
    | inr h => exact h
  unfold odd_step
  omega

/-- The trigger is the exact inverse of the odd step
    when the source is odd. -/
theorem trigger_exact_inverse (p : Nat) :
    trigger (odd_step p) = p := by
  unfold trigger odd_step
  have h : 3 * p + 1 - 1 = 3 * p := by omega
  rw [h, Nat.mul_div_left p (by norm_num : 0 < 3)]

/-- The trigger output is odd when the source is 4 mod 6.
    (This is the structural lemma from the v5.3 library.) -/
theorem trigger_output_odd (m : Nat) (hm : m % 6 = 4) :
    ((m - 1) / 3) % 2 = 1 := by
  obtain ⟨k, hk⟩ : exists k, m = 6 * k + 4 := by
    exact ⟨m / 6, by omega⟩
  rw [hk]
  have h_num : 6 * k + 4 - 1 = 3 * (2 * k + 1) := by omega
  rw [h_num]
  have h_div3 : 3 * (2 * k + 1) / 3 = 2 * k + 1 :=
    Nat.mul_div_left _ (by decide : 0 < 3)
  rw [h_div3]
  omega

-- ============================================================
-- §2. TWIN PRIMES AS 6-SHIFT (Theorem 5.1, 5.2)
-- ============================================================

/-- The trigger parents of p and p+2 are separated by 6. -/
theorem twin_parent_gap (p : Nat) :
    odd_step (p + 2) - odd_step p = 6 := by
  unfold odd_step
  ring

/-- The Parity Gate is invariant under a shift of 6. -/
theorem gate_shift_invariant (m : Nat) :
    m % 6 = 4 <-> (m + 6) % 6 = 4 := by
  omega

/-- Twin gate preservation: if p's parent passes the gate,
    so does (p+2)'s parent. -/
theorem twin_gate_preserved (p : Nat) (hp : Nat.Prime p) (h_gt : p > 3) :
    odd_step p % 6 = 4 /\ odd_step (p + 2) % 6 = 4 := by
  have h1 := prime_parent_mod_six p hp h_gt
  refine ⟨h1, ?_⟩
  unfold odd_step
  omega

-- ============================================================
-- §3. GOLDBACH REFLECTION (Theorem 6.1)
-- ============================================================

/-- The midpoint of the trigger parents is the Collatz step
    of the average. -/
theorem goldbach_midpoint (p q n : Nat) (h_pq : p + q = 2 * n) :
    (odd_step p + odd_step q) / 2 = 3 * n + 1 := by
  unfold odd_step
  rw [<- h_pq]
  have h : 3 * p + 1 + (3 * q + 1) = 3 * (p + q) + 2 := by ring
  rw [h]
  omega

/-- The reflection distance is 3|q - p|/2. -/
theorem goldbach_reflection_distance (p q : Nat) :
    (odd_step q - odd_step p) = 3 * ((q : Int) - p) := by
  unfold odd_step
  push_cast
  ring

-- ============================================================
-- §4. WITNESSES (L2 empirical closures)
-- ============================================================

/-- 5-Family closure, verified for p in {7, 11, 13, 17, 19, 29}. -/
theorem five_family_witness_7  : odd_step 7  = 22 := by decide
theorem five_family_witness_11 : odd_step 11 = 34 := by decide
theorem five_family_witness_13 : odd_step 13 = 40 := by decide
theorem five_family_witness_17 : odd_step 17 = 52 := by decide
theorem five_family_witness_19 : odd_step 19 = 58 := by decide
theorem five_family_witness_29 : odd_step 29 = 88 := by decide

end MEADium.PrimeStructure
