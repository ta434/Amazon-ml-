#!/usr/bin/env python3
import csv
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_DIR = os.path.join(ROOT, 'dataset', 'test')
OUTPUT_DIR = os.path.join(ROOT, 'output')


def load_source1(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)
        for row in reader:
            if not row or not row[0].startswith('S1-'):
                continue
            rows.append(row[0])
    return rows


def write_tsv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['source1_entity_id', 'matched_entity_ids'])
        for s1 in rows:
            writer.writerow([s1, ''])


def write_candidates(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['source1_entity_id', 'candidate_entity_ids'])
        for s1 in rows:
            writer.writerow([s1, ''])


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    s1_ids = load_source1(os.path.join(TEST_DIR, 'test_source1.tsv'))
    write_tsv(os.path.join(OUTPUT_DIR, 'matching_results.tsv'), s1_ids)
    write_candidates(os.path.join(OUTPUT_DIR, 'candidate_pairs.tsv'), s1_ids)
    print(f'Generated {len(s1_ids)} rows for matching_results.tsv and candidate_pairs.tsv in {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
