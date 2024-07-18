import os
import datetime
import logging
import re
import sys

logging.basicConfig(encoding='utf-8', format='%(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S',
        level=logging.INFO)
logger = logging.getLogger(__name__)

if len(sys.argv) != 4:
    print("usage: python(3) subtitle-fixer.py <filename> <start_delay> <end_delay>")
    exit()

start_delay = int(sys.argv[2])
end_delay = int(sys.argv[3])

def str_to_time(ts: str, delay: int = 0) -> str:
    old_ts = datetime.datetime.strptime(ts, '%H:%M:%S,%f')
    new_ts = old_ts + datetime.timedelta(milliseconds=delay)
    new_ts_str = datetime.datetime.strftime(new_ts, '%H:%M:%S,%f')[:-3]
    return new_ts_str

file = sys.argv[1]
file_org = file + ".org"

if not os.path.exists(file_org):
    logger.info(f"{file} => {file_org}")
    os.rename(file, file_org)

with open(file_org, 'r', encoding='utf-8-sig') as input:
    lines = input.readlines()

ts_pattern = '^[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]'
out = []
for line in lines:
    line_fixed = line
    if re.search(ts_pattern, line):
        logger.debug("found the timestamp line")
        ts_start = line.split(' ')[0].rstrip()
        ts_end = line.split(' ')[2].rstrip()
        line_fixed = f"{str_to_time(ts_start, start_delay)} --> {str_to_time(ts_end, start_delay + end_delay)}\n"
    out.append(line_fixed)

logger.debug(out)

with open(file, 'w', encoding='utf-8-sig') as output:
    output.writelines(out)