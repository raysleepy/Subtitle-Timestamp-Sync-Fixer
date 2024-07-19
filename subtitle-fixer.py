import datetime as dt
import logging
import os
import re
import sys

logging.basicConfig(encoding='utf-8', format='%(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)

TIMESTAMP_PATTERN = '^[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]'

def str_to_datetime(timestamp: str) -> dt.datetime:
    return dt.datetime.strptime(timestamp, '%H:%M:%S,%f')

def datetime_to_str(datetime: dt.datetime) -> str:
    return dt.datetime.strftime(datetime, '%H:%M:%S,%f')[:-3]

# Reads the SRT file into a list. Saves the original SRT file
def read_file(filepath: str) -> list[str]:
    file_org = filepath + ".org"
    if not os.path.exists(file_org):
        logger.info(f"{filepath} => {file_org}")
        os.rename(filepath, file_org)

    with open(file_org, 'r', encoding='utf-8-sig') as input:
        return input.readlines()
    
# Scans a list of lines, picks out the lines with timestamps
# Returns a list of (lines, list of start and end datetimes, list of datetime index to line index)
def get_lines_info(lines: list[str]) -> tuple[list[str], list[tuple[dt.datetime, dt.datetime]], list[int]]:
    times = []
    lines_mapping = []
    for i in range(len(lines)):
        line = lines[i]
        if re.search(TIMESTAMP_PATTERN, line):
            logger.debug("found the timestamp line")
            ts_start = str_to_datetime(line.split(' ')[0].rstrip())
            ts_end = str_to_datetime(line.split(' ')[2].rstrip())
            times.append((ts_start, ts_end))
            lines_mapping.append(i)

    logger.debug(times)
    logger.debug(lines_mapping)

    return (lines, times, lines_mapping)

# Process the list of lines with desired "starting delay" and an "extra delay"
# Returns a list of lines
def update_times(lines_with_info: tuple[list[str], list[tuple[dt.datetime, dt.datetime]], list[int]], 
                 start_delay: int, extra_delay: int, allow_overlap: bool) -> list[str]:
    lines, times, lines_mapping = lines_with_info
    out = lines.copy()
    for i in range(len(times)):
        start, end = times[i]

        start += dt.timedelta(milliseconds=start_delay)
        end += dt.timedelta(milliseconds=start_delay + extra_delay)

        if not allow_overlap and i + 1 < len(times):
            next_start = times[i + 1][0] + dt.timedelta(milliseconds=start_delay)

            # Check for preexisting condition (overlapping) in SRT file
            was_already_overlapping = next_start < end - dt.timedelta(milliseconds=extra_delay)
            is_overlapping = next_start < end
            if not was_already_overlapping and is_overlapping:
                end = next_start
        
        out[lines_mapping[i]] = f"{datetime_to_str(start)} --> {datetime_to_str(end)}\n"

    logger.debug(out)

    return out

def main():
    if len(sys.argv) != 5:
        sys.exit("Usage:  python(3) subtitle-fixer.py  <filename.srt>  <start_delay(ms)>  <end_delay(ms)>  <allow_overlap(y/n)>")
    file = sys.argv[1]
    start_delay = int(sys.argv[2])
    extra_delay = int(sys.argv[3])
    allow_overlap = sys.argv[4].lower() in ['y', 'yes']

    lines = read_file(file)
    lines_with_info = get_lines_info(lines)
    out = update_times(lines_with_info, start_delay, extra_delay, allow_overlap)

    with open(file, 'w', encoding='utf-8-sig') as output:
        output.writelines(out)

if __name__ == "__main__":
    main()