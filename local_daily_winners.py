#!/usr/bin/env python3

# Usage: download your leaderboard from
#  https://adventofcode.com/2020/leaderboard/private/view/########
# (click on API, then JSON), then ./local_daily_winners.py ########.json

import datetime
import json
import sys


YEAR = 2020

MAX_TIME = 2 ** 63


def _completion_time(member, day, part):
    return int(member['completion_day_level']
               .get(str(day), {})
               .get(str(part), {})
               .get('get_star_ts', MAX_TIME))


def _format_winner(member, day, part):
    start_time = datetime.datetime(YEAR, 12, day, 5)  # midnight EST
    end_time_t = _completion_time(member, day, part)
    if end_time_t == MAX_TIME:
        time = 'n/a'
    else:
        secs = int((datetime.datetime.utcfromtimestamp(end_time_t)
                    - start_time).total_seconds())
        time = f'{secs // 3600:02d}:{(secs // 60) % 60:02d}:{secs % 60:02d}'

    return f'{member["name"]} ({time})'


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
