import pandas as pd
import numpy as np
import sys
import time
import os
# =============================================================================
# [ROA SYSTEM CONFIGURATION] - V151.2 Digital Twin
# =============================================================================
TARGET_START = 10000000000000000  # 1 Quadrillion (10^16)
SEARCH_RANGE = 5000000            # Scan Range
MERIT_THRESHOLD = 0.25            # Merit Cutoff for Singularity Detection
# =============================================================================
def hunt_singularities(start_num, search_range):
    print(f"::: [SYSTEM] Sunggil-AI V151.2 Initializing... :::")
    print(f"::: [TARGET] Range: 10^16 (1 Quadrillion) | Mode: Deep Scan :::")
    # [Phase 1] System Setup (Sieve Matrix Construction)
    setup_start = time.time()
    # Memory safety calculation: Sqrt(10^16) = 10^8. Array size approx 100MB (Safe).
    shield_limit = int((start_num + search_range)**0.5) + 5000
    try:
        # Optimized Boolean Sieve for O(1) Access Simulation
        sieve = np.ones(shield_limit + 1, dtype=bool)
        sieve[0:2] = False
        for p in range(2, int(shield_limit**0.5) + 1):
            if sieve[p]:
                sieve[p*p : shield_limit+1 : p] = False
        check_primes = np.nonzero(sieve)[0].astype(np.int32)
        setup_end = time.time()
        print(f"   > [Setup] TQML Lattice Simulation Built in {setup_end - setup_start:.2f}s")
        print(f"   > [Ready] {len(check_primes):,} basis primes loaded.")
    except MemoryError: 
        print("!!! [CRITICAL] Insufficient RAM. Simulation aborted.")
        return None
    # [Phase 2] Singularity Hunting (Core Logic)
    print(f"\n::: [PHASE 2] Starting ROA Navigation... :::")
    found_anomalies = []
    curr = start_num
    if curr % 2 == 0: curr += 1
    # Anchor Prime Search
    prev_prime = -1
    while True:
        is_prime = True
        limit = int(curr**0.5)
        for p in check_primes:
            if p > limit: break
            if curr % int(p) == 0:
                is_prime = False; break
        if is_prime: 
            prev_prime = curr
            break
        curr += 2
    # Main Navigation Loop
    curr = prev_prime + 2
    end_point = start_num + search_range
    while curr <= end_point:
        lookup_start = time.time() # Measure lookup latency
        is_prime = True
        limit = int(curr**0.5)
        for p in check_primes:
            if int(p) > limit: break
            if curr % int(p) == 0: 
                is_prime = False
                break
        if is_prime:
            lookup_end = time.time()
            lookup_duration = lookup_end - lookup_start
            gap = curr - prev_prime
            merit = gap / (np.log(prev_prime)**2)
            if merit >= MERIT_THRESHOLD:
                # Log the discovery
                print(f"   >>> [Singularity Found] Prime: {prev_prime} | Gap: {gap} | Merit: {merit:.4f}")
                found_anomalies.append([prev_prime, gap, merit, lookup_duration])
            prev_prime = curr
        curr += 2
        if (curr - start_num) % 1000000 == 0:
            sys.stdout.write(f"\r   > Navigation Progress... {(curr - start_num):,} / {search_range:,} units")
            sys.stdout.flush()
    # [Phase 3] Result Export
    if found_anomalies:
        df = pd.DataFrame(found_anomalies, columns=['Prime', 'Gap', 'Merit', 'Lookup_Time'])
        df = df.sort_values(by='Merit', ascending=False)
        filename = 'V151_2_Singularity_Report.csv'
        df.to_csv(filename, index=False)
        print(f"\n\n::: [COMPLETE] {len(df)} Singularities exported to {filename}")
        # [Compatible Download Logic]
        # Google Colab인 경우에만 다운로드 창을 띄우고, 아니면 파일로만 저장
        try:
            from google.colab import files
            files.download(filename)
        except ImportError:
            print(f"   > [Note] File saved locally as '{filename}'. Check your folder.")
    else:
        print("\n\n   > [Result] No singularities found in this sector.")
if __name__ == "__main__":
    hunt_singularities(TARGET_START, SEARCH_RANGE)
