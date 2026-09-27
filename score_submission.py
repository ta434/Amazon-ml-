#!/usr/bin/env python3
import argparse
import csv

DELIM = "\t"


def read_truth(path):
    truth = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            s1 = row[0].strip()
            matched = row[1].strip() if len(row) > 1 else ""
            truth[s1] = set(m.strip() for m in matched.split(',') if m.strip())
    return truth


def read_predictions(path):
    pred = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            s1 = row[0].strip()
            matched = row[1].strip() if len(row) > 1 else ""
            pred[s1] = set(m.strip() for m in matched.split(',') if m.strip())
    return pred


def f_beta_score(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision == 0.0 and recall == 0.0:
        return 1.0
    return (1.25 * precision * recall) / (0.25 * precision + recall)


def eval_entity(true_set, pred_set):
    tp = len(true_set & pred_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    if not true_set and not pred_set:
        return 1.0
    return f_beta_score(tp, fp, fn)


def evaluate(pred_path, truth_path):
    truth = read_truth(truth_path)
    pred = read_predictions(pred_path)
    common = sorted(set(truth) & set(pred))
    all_s1 = sorted(set(truth) | set(pred))
    print(f"Ground-truth entities: {len(truth)}")
    print(f"Prediction entities: {len(pred)}")
    print(f"Common S1 keys: {len(common)}")

    if not common:
        print("No overlapping S1 IDs between the provided predictions and the training ground truth.")
        print("This file cannot be scored against the training labels because it contains test-set IDs.")
        return 1

    scores = []
    for s1 in sorted(truth):
        expected = truth[s1]
        predicted = pred.get(s1, set())
        scores.append(eval_entity(expected, predicted))

    macro = sum(scores) / len(scores) if scores else 0.0
    print(f"Macro F_0.5 on training ground truth: {macro:.6f}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='Evaluate a matching TSV against the training ground truth using F_0.5.')
    parser.add_argument('--pred', default='output/matching_results.tsv', help='Path to predictions TSV (matching_results.tsv)')
    parser.add_argument('--truth', default='dataset/train/train_ground_truth.tsv', help='Path to training ground truth TSV')
    args = parser.parse_args()
    raise SystemExit(evaluate(args.pred, args.truth))


if __name__ == '__main__':
    main()
