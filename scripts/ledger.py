#!/usr/bin/env python3
"""Summarise the latest entries in an append-only findings book."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re

ROLES = ('holmes', 'watson', 'moriarty', 'checker', 'front_office', 'blind_pass')
SEVERITIES = ('CRITICAL', 'HIGH', 'MODERATE', 'LOW', 'INFORMATIONAL', 'UNKNOWN')
ENUMS = {'tier': ('triage', 'focused', 'standard'), 'raised_by': ROLES,
         'event': ('RAISED', 'CHANGED', 'REPAIRED', 'WITHDRAWN'),
         'severity': SEVERITIES, 'status': ('CONFIRMED', 'HYPOTHESIS', 'CONTESTED', 'WITHDRAWN'),
         'disposition': ('REQUIRED_REPAIR', 'INVESTIGATE', 'FOLLOW_UP', 'ACCEPTED')}
FIELDS = set(ENUMS) | {'series', 'case_id', 'round', 'reviewed_head', 'finding_id', 'recorded_at', 'cost'}


def validate(row):
    if not isinstance(row, dict) or set(row) - (FIELDS | {'reviewed_head_reason'}) or FIELDS - set(row):
        raise ValueError('missing or unrecognised fields')
    for key, values in ENUMS.items():
        if row[key] not in values:
            raise ValueError('unrecognised ' + key)
    for key in ('series', 'case_id', 'finding_id'):
        if not isinstance(row[key], str) or not row[key].strip():
            raise ValueError(key + ' must be a nonempty identifier')
    if type(row['round']) is not int or row['round'] < 1:
        raise ValueError('round must be a positive integer')
    head = row['reviewed_head']
    if head == 'N/A':
        if not isinstance(row.get('reviewed_head_reason'), str) or not row['reviewed_head_reason'].strip():
            raise ValueError('N/A head requires reviewed_head_reason')
    elif not isinstance(head, str) or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', head):
        raise ValueError('reviewed_head must be a full commit ID')
    stamp = row['recorded_at']
    if not isinstance(stamp, str):
        raise ValueError('recorded_at must be a timestamp')
    parsed = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('recorded_at requires a timezone')
    cost = row['cost']
    if not isinstance(cost, dict) or set(cost) != {'elapsed_seconds', 'tokens'}:
        raise ValueError('cost requires elapsed_seconds and tokens')
    if any(v != 'UNKNOWN' and (type(v) is not int or v < 0) for v in cost.values()):
        raise ValueError('cost must be nonnegative integers or UNKNOWN')
    return row


def blank():
    return {severity: dict(raised=0, confirmed=0, withdrawn=0, repaired=0)
            for severity in SEVERITIES}


def exact_median(values):
    if not values: return None
    ordered = sorted(values); middle = len(ordered) // 2
    if len(ordered) % 2: return ordered[middle]
    total = ordered[middle - 1] + ordered[middle]
    whole, half = divmod(total, 2)
    if not half: return whole
    return whole + .5 if whole < 2 ** 52 else str(whole) + '.5'


def summarize(path):
    latest = {}; first = {}
    with path.open('rb') as source:
        for number, line in enumerate(source, 1):
            try:
                row = validate(json.loads(line.decode('utf-8')))
            except (ValueError, TypeError, OverflowError, RecursionError) as exc:
                raise ValueError('line ' + str(number) + ': ' + str(exc)) from exc
            key = (row['series'], row['finding_id'])
            if key in first and row['raised_by'] != first[key]['raised_by']:
                raise ValueError('line ' + str(number) + ': raised_by cannot change')
            first.setdefault(key, row)
            latest[key] = row
    roles = {role: blank() for role in ROLES}; rounds = {}; costs = {}; discovery = {}
    for key, row in latest.items():
        round_number = str(row['round']); severity = row['severity']
        found = str(first[key]['round']); discovery[found] = discovery.get(found, 0) + 1
        for counts in (roles[row['raised_by']], rounds.setdefault(round_number, blank())):
            item = counts[severity]; item['raised'] += 1
            if row['event'] == 'WITHDRAWN' or row['status'] == 'WITHDRAWN':
                item['withdrawn'] += 1
            elif row['event'] == 'REPAIRED':
                item['repaired'] += 1
            elif row['status'] == 'CONFIRMED':
                item['confirmed'] += 1
        bucket = costs.setdefault(round_number, {'elapsed_seconds': [], 'tokens': []})
        for metric, value in row['cost'].items():
            if type(value) is int:
                bucket[metric].append(value)
    medians = {r: {metric: exact_median(values)
                   for metric, values in bucket.items()} for r, bucket in costs.items()}
    return dict(total_findings=len(latest), by_role=roles, by_round=rounds,
                discovery_by_round=discovery, median_cost_by_round=medians)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['summarize'])
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--json', action='store_true', help='Use compact JSON')
    args = parser.parse_args()
    try:
        result = summarize(args.ledger)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.exit(2, 'Ledger refused: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True, indent=None if args.json else 2))


if __name__ == '__main__':
    main()
