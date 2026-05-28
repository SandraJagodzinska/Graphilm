import pandas as pd
import sys
import os

# ── Config ─────────────────────────────────────────────────────────────────
INPUT_FILE = "title.basics.tsv"
OUTPUT_CLEAN = "title.basics.clean.tsv"
OUTPUT_DROPPED = "dropped_ids.txt"
YEAR_CUTOFF = 1960

# ───────────────────────────────────────────────────────────────────────────

# checks if argument passed in terminal
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]

if not os.path.exists(INPUT_FILE):
    print(f"[ERROR] File not found: {INPUT_FILE}")
    print("Usage: python filter_titles.py [path/to/title.basics.tsv]")
    sys.exit(1)

print(f"Reading {INPUT_FILE} ...")
df = pd.read_csv(
    INPUT_FILE,
    sep="\t",
    dtype=str,  # keep everything as string to avoids mixed-type issues
    na_values=[r"\N"],  # IMDB uses \N for nulls
    low_memory=False,
)
print(f"  Total rows loaded : {len(df):,}")

# Convert year columns to numeric (coerce -> NaN where missing or cannot convert instead of crushing)
df["startYear_num"] = pd.to_numeric(df["startYear"], errors="coerce")
df["endYear_num"] = pd.to_numeric(df["endYear"], errors="coerce")

# Drop rule 1 — both dates missing
both_missing = df["startYear_num"].isna() & df["endYear_num"].isna()

# Drop rule 2 — all available dates are before YEAR_CUTOFF
# A row passes if at least one valid date is >= YEAR_CUTOFF
start_ok = df["startYear_num"] >= YEAR_CUTOFF
end_ok = df["endYear_num"] >= YEAR_CUTOFF
# boolean logic ~(...) it flips True into False. if True drop the row
year_too_old = ~(start_ok | end_ok)

# drops if dates are missing or year is too old
drop_mask = both_missing | year_too_old
dropped_df = df[drop_mask] # rows where the drop mask is True
clean_df = df[~drop_mask] # rows where drop mask is False

print(f"  Rows kept         : {len(clean_df):,}")
print(f"  Rows dropped      : {len(dropped_df):,}")
print(f"    -> missing dates : {both_missing.sum():,}")
print(f"    -> before {YEAR_CUTOFF}   : {(~both_missing & year_too_old).sum():,}")

# Write clean file — drop helper columns, restore IMDB's \N convention
clean_df.drop(columns=["startYear_num", "endYear_num"]).to_csv(
    OUTPUT_CLEAN,
    sep="\t",
    index=False,
    na_rep=r"\N",
)
print(f"\nClean file written  -> {OUTPUT_CLEAN}")

# Write dropped IDs
dropped_df[["tconst"]].to_csv(OUTPUT_DROPPED, index=False, header=True)
print(f"Dropped IDs written -> {OUTPUT_DROPPED}  ({len(dropped_df):,} IDs)")