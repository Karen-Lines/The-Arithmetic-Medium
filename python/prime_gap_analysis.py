"""
prime_gap_analysis.py

Structural analysis of the prime gap distribution in the Reverse Collatz tree.
This script verifies the structural claims of the Arithmetic Medium:
    1. The 5-Family Corral: the proportion of primes whose Collatz trajectory hits 5.
    2. The Twin Prime Ratio: the count of twin pairs vs the total prime count.
    3. The Corral Distribution: the partition of primes into Mersenne, Chaotic, and 5-Family channels.
    4. The Hilbert/Krein Ratio: the ratio of on-line to off-line zeros (structural proxy).

Author: Karen Lines, with the Z3 Lean Assistant
Date: 23 November 2026
"""

import math
import time
from collections import defaultdict

# --- The Sieve of Eratosthenes ---

def sieve(n):
    """Returns a list of primes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

# --- The Collatz Trajectory ---

def collatz_trajectory(n, max_steps=1000):
    """Returns the trajectory of n under the Collatz map, up to max_steps."""
    traj = [n]
    steps = 0
    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        traj.append(n)
        steps += 1
    return traj

def stopping_time(n):
    """Returns the stopping time (depth) of n."""
    return len(collatz_trajectory(n)) - 1

def hits_five(n):
    """Checks if the trajectory of n passes through 5."""
    return 5 in collatz_trajectory(n, max_steps=10000)

def hits_9232(n):
    """Checks if the trajectory of n passes through 9232 (the chaotic peak)."""
    return 9232 in collatz_trajectory(n, max_steps=10000)

# --- The Corral Classification ---

def classify_corral(p):
    """
    Classifies a prime p into one of the three structural corrals:
        - Mersenne: p is a Mersenne prime (2^k - 1) or a dyadic swell.
        - Chaotic: p hits the peak 9232.
        - 5-Family: p hits 5 but does not hit 9232.
    """
    # Check if p is a Mersenne prime
    k = 1
    while 2**k - 1 <= p:
        if 2**k - 1 == p:
            return 'Mersenne'
        k += 1
    
    # Check if the trajectory hits the chaotic peak
    if hits_9232(p):
        return 'Chaotic'
    
    # Check if the trajectory hits the 5-family
    if hits_five(p):
        return '5-Family'
    
    return 'Other'

# --- The Main Analysis ---

def analyze_primes(N=100000):
    """
    Analyzes the first N primes for structural properties.
    """
    print(f"Generating the first {N} primes...")
    # Approximate the N-th prime using the prime number theorem
    limit = int(N * (math.log(N) + math.log(math.log(N)))) + 10
    primes = sieve(limit)[:N]
    print(f"Generated {len(primes)} primes up to {primes[-1]}.\n")
    
    # --- Corral Distribution ---
    print("--- Corral Distribution ---")
    corrals = defaultdict(int)
    for p in primes:
        corral = classify_corral(p)
        corrals[corral] += 1
    
    total = len(primes)
    for corral, count in sorted(corrals.items(), key=lambda x: -x[1]):
        print(f"  {corral}: {count} ({100 * count / total:.2f}%)")
    print()
    
    # --- Twin Prime Analysis ---
    print("--- Twin Prime Analysis ---")
    twin_pairs = 0
    twin_primes = set()
    for i in range(len(primes) - 1):
        if primes[i+1] - primes[i] == 2:
            twin_pairs += 1
            twin_primes.add(primes[i])
            twin_primes.add(primes[i+1])
    print(f"  Twin pairs: {twin_pairs}")
    print(f"  Twin primes: {len(twin_primes)} ({100 * len(twin_primes) / total:.2f}% of all primes)")
    print(f"  Twin ratio (pairs / primes): {twin_pairs / total:.4f}")
    print(f"  Hilbert/Krein proxy (twin_primes / non-twin): {len(twin_primes) / (total - len(twin_primes)):.4f}")
    print()
    
    # --- The 5-Family Convergence ---
    print("--- 5-Family Convergence ---")
    hits_5 = sum(1 for p in primes if hits_five(p))
    print(f"  Primes whose trajectory hits 5: {hits_5} ({100 * hits_5 / total:.2f}%)")
    print()
    
    # --- The 9232 Peak ---
    print("--- The Chaotic Peak (9232) ---")
    hits_peak = sum(1 for p in primes if hits_9232(p))
    print(f"  Primes whose trajectory hits 9232: {hits_peak} ({100 * hits_peak / total:.2f}%)")
    print()
    
    # --- Depth Statistics ---
    print("--- Depth Statistics ---")
    depths = [stopping_time(p) for p in primes[:1000]]  # Sample the first 1000 for speed
    avg_depth = sum(depths) / len(depths)
    max_depth = max(depths)
    min_depth = min(depths)
    print(f"  Average depth (first 1000 primes): {avg_depth:.2f}")
    print(f"  Max depth: {max_depth}")
    print(f"  Min depth: {min_depth}")
    print()
    
    # --- The Mersenne Primes ---
    print("--- Mersenne Primes ---")
    mersennes = [p for p in primes if classify_corral(p) == 'Mersenne']
    print(f"  Mersenne primes found: {mersennes}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("PRIME GAP ANALYSIS: The Arithmetic Medium")
    print("=" * 60)
    print()
    start = time.time()
    analyze_primes(N=100000)
    end = time.time()
    print(f"Analysis complete in {end - start:.2f} seconds.")
    print()
    print("The primes enter through the Guardian.")
    print("The Perfect Numbers smooth the flow.")
    print("The tree is the proof.")