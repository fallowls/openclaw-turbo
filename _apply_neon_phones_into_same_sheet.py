import csv

IN_PATH = r"C:\Users\Administrator\.openclaw\workspace\prospects_enriched_with_neon_phones.csv"
OUT_PATH = r"C:\Users\Administrator\.openclaw\workspace\prospects_enriched_direct_and_mobile_only.csv"


def empty(v):
    return v is None or str(v).strip() == "" or str(v).strip().lower() in {"na", "n/a", "null", "none", "unavailable"}


def main():
    with open(IN_PATH, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        fns = r.fieldnames or []

    # Ensure the original sheet has these columns
    for col in ["Work Direct Phone", "Mobile Phone"]:
        if col not in fns:
            fns.append(col)

    # Fill only these two fields from Neon (do not overwrite non-empty)
    for row in rows:
        if empty(row.get("Mobile Phone")) and not empty(row.get("neon_phone_mobile")):
            row["Mobile Phone"] = row.get("neon_phone_mobile")
        if empty(row.get("Work Direct Phone")):
            if not empty(row.get("neon_phone_work")):
                row["Work Direct Phone"] = row.get("neon_phone_work")
            elif not empty(row.get("neon_phone_other")):
                # fallback: some sources store direct lines in other bucket
                row["Work Direct Phone"] = row.get("neon_phone_other")

    # Keep file clean: drop other neon columns except match_type + the two phone fields (optional)
    keep_extra = {"neon_match_type", "neon_phone_mobile", "neon_phone_work", "neon_phone_other"}
    out_fns = [c for c in fns if not c.startswith("neon_") or c in keep_extra]

    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fns)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in out_fns})

    filled_mobile = sum(1 for row in rows if not empty(row.get("Mobile Phone")))
    filled_work = sum(1 for row in rows if not empty(row.get("Work Direct Phone")))
    print(f"rows={len(rows)} filled_mobile={filled_mobile} filled_work_direct={filled_work}")
    print(f"out={OUT_PATH}")


if __name__ == "__main__":
    main()
