import os
import xml.etree.ElementTree as ET
import psycopg2

BATCH_SIZE = 1000  # Adjust batch size based on memory

def parse_abn_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        records = []

        for abr in root.findall("ABR"):
            records.append((
                abr.findtext("ABN"),
                abr.findtext("MainEntity/NonIndividualName/NonIndividualNameText"),
                abr.findtext("EntityType/EntityTypeText"),
                abr.find("ABN").get("status") if abr.find("ABN") is not None else None,
                abr.find("ABN").get("ABNStatusFromDate") if abr.find("ABN") is not None else None,
                None,  # Address not available
                abr.findtext("MainEntity/BusinessAddress/AddressDetails/Postcode"),
                abr.findtext("MainEntity/BusinessAddress/AddressDetails/State")
            ))

        return records

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def parse_all_xml_files(root_folder):
    all_records = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".xml"):
                file_path = os.path.join(dirpath, filename)
                all_records.extend(parse_abn_xml(file_path))
    return all_records

def insert_bulk_to_postgres(records, conn):
    try:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO abn_entities (
                    abn, entity_name, entity_type, entity_status,
                    entity_start_date, entity_address, entity_postcode, entity_state
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (abn) DO NOTHING;
            """, records)
        conn.commit()
    except Exception as e:
        print(f"Bulk insert failed: {e}")
        conn.rollback()

def connect_postgres():
    return psycopg2.connect(
        host="localhost",
        database="assignment_firmable",
        user="postgres",
        password="Hanisha@123",
        port="5432"
    )

def main():
    xml_root_folder = "extracted_abn_zip_files"
    all_data = parse_all_xml_files(xml_root_folder)

    print(f"\nTotal records parsed: {len(all_data)}")
    conn = connect_postgres()

    for i in range(0, len(all_data), BATCH_SIZE):
        batch = all_data[i:i+BATCH_SIZE]
        insert_bulk_to_postgres(batch, conn)
        print(f"Inserted records {i + 1} to {i + len(batch)}")

    conn.close()
    print("\n✅ All records inserted into PostgreSQL successfully.")

if __name__ == "__main__":
    main()
