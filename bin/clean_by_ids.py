import csv

import pandas as pd
import sys
import os

# ── Args ───────────────────────────────────────────────────────────────────
if len(sys.argv) < 3:
    print("Usage: python clean_by_ids.py dropped_ids.txt file1.tsv [file2.tsv ...]")
    sys.exit(1)

DROPPED_IDS_FILE = sys.argv[1]
INPUT_FILES = sys.argv[2:]

# ── Load dropped IDs ────────────────────────────────────────────────────────
dropped_ids = pd.read_csv(DROPPED_IDS_FILE)["tconst"].tolist()
print(f"Loaded {len(dropped_ids):,} dropped IDs from {DROPPED_IDS_FILE}\n")

# ── Process each file ───────────────────────────────────────────────────────
for input_file in INPUT_FILES:

    if not os.path.exists(input_file):
        print(f"[SKIP] File not found: {input_file}")
        continue

    print(f"Processing {input_file} ...")
    try:
        df = pd.read_csv(input_file, sep="\t", dtype=str, low_memory=True, quoting=csv.QUOTE_NONE, encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] Impossible to parse the file: {e}.")

    # Detect which column holds the title ID
    if "tconst" in df.columns:
        id_col = "tconst"
    elif "titleId" in df.columns:  # title.akas.tsv uses titleId
        id_col = "titleId"
    else:
        print(f"  [SKIP] No tconst or titleId column found — skipping.\n")
        continue

    before = len(df)
    df_clean = df[~df[id_col].isin(dropped_ids)]
    after = len(df_clean)

    # Build output filename: title.ratings.tsv -> title.ratings.clean.tsv
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}.clean{ext}"

    df_clean.to_csv(output_file, sep="\t", index=False, na_rep=r"\N")
    print(f"  Rows before : {before:,}")
    print(f"  Rows after  : {after:,}")
    print(f"  Dropped     : {before - after:,}")
    print(f"  Written  -> {output_file}\n")

print("Done.")
