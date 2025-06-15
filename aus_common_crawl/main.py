from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from tqdm import tqdm

from utils import (
    extract_au_domains,
    process_record,
    get_base_domain,
    connect_postgres,
    insert_commoncrawl_record
)

def main():
    print(" Starting extraction of Australian company websites...")
    company_records = extract_au_domains()
    print(f" Found {len(company_records)} company groups")

    seen_domains = set()
    output = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for record_group in company_records:
            for record in record_group:
                url = record["url"]
                domain = get_base_domain(url)
                if domain in seen_domains:
                    continue
                seen_domains.add(domain)
                futures.append(executor.submit(process_record, record))

        for future in tqdm(as_completed(futures), total=len(futures), desc="🚀 Processing records"):
            try:
                result = future.result()
                if result:
                    output.append(result)
            except Exception as e:
                print(f" Thread error: {e}")

    print(f"\n Extracted {len(output)} valid companies.")

    # --- INSERT INTO POSTGRES ---
    conn = connect_postgres()

    inserted = 0
    for record in output:
        try:
            insert_commoncrawl_record({
                "url": record["Website"],
                "company_name": record["Company Name"],
                "industry": record["Industry"]
            }, conn)
            inserted += 1
        except Exception as e:
            print(f"Insert error for {record['Website']}: {e}")

    conn.close()

    print(f"\n Inserted {inserted} company records into PostgreSQL ✅")


if __name__ == "__main__":
    main()
