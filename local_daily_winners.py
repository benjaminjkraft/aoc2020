#!/usr/bin/env python3

# Usage: download your leaderboard from
#  https://adventofcode.com/2020/leaderboard/private/view/########
# (click on API, then JSON), then ./local_daily_winners.py ########.json

import datetime
import json
import sys


YEAR = 2020


def _completion_time(member, day, part):
    return int(member['completion_day_level']
               .get(str(day), {})
               .get(str(part), {})
               .get('get_star_ts', 2 ** 31 - 1))


def _format_timedelta(td):
    secs = int(td.total_seconds())
    return f'{secs // 3600:02d}:{(secs // 60) % 60:02d}:{secs % 60:02d}'


def _format_winner(member, day, part):
    start_time = datetime.datetime(YEAR, 12, day, 5)  # midnight EST
    time = datetime.datetime.utcfromtimestamp(
        _completion_time(member, day, part)) - start_time

    return f'{member["name"]} ({_format_timedelta(time)})'


def main():
    with open(sys.argv[1]) as f:
        leaderboard = json.load(f)

    last_day = max(max(map(int, m['completion_day_level'].keys()))
                   for m in leaderboard['members'].values())

    for day in range(1, last_day+1):
        for part in [1, 2]:
            winners = sorted(leaderboard['members'].values(),
                             key=lambda m: _completion_time(m, day, part))

            print(f'Day {day} Part {part}: ' + ', '.join(
                _format_winner(m, day, part) for m in winners[:2]))


if __name__ == '__main__':
    main()
