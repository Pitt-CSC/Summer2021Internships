import os
import json
from log import logger

import requests


def create_md_table(listings):
    col_names = ["Name", "Location", "Notes"]
    col_keys = ["Name", "Location", "Notes"]
    result = "| "
    for name in col_names:
        result += name + " | "
    result += "\n| "
    for name in col_names:
        result += " --- | "
    for listing in listings:
        result += "\n| "
        for key in col_keys:
            result += listing[key] + " | "
    return result


def parse_file(listings: list, path: str, year: int, is_closed: bool, is_off_season: bool):
    logger.info(f"parsing file: {path}")
    with open(path, "r") as f:
        table_line_num = 0
        for line in f.readlines():
            if line[0] == "|":
                data = {}
                if table_line_num == 0:
                    header = [t.strip() for t in line.split('|')[1:-1]]
                elif table_line_num > 1:
                    values = [t.strip() for t in line.split('|')[1:-1]]
                    job_is_closed = False
                    for col, value in zip(header, values):
                        data[col] = value
                        if value.find("Closed") != -1:
                            job_is_closed = True
                    data["is_closed"] = is_closed or job_is_closed
                    data["year"] = year
                    data["is_off_season"] = is_off_season
                    listings.append(data)
                table_line_num += 1


def main():
    logger.info(f"Running main() in main.py")
    result = []
    parse_file(result, "README.md", 2024, False, False)
    parse_file(result, "README-Off-Season.md", 2024, False, True)
    parse_file(result, "README-2023.md", 2023, True, False)
    text_file = open("simplify/listings.json", "w")
    n = text_file.write(json.dumps(result, indent=4))
    text_file.close()
    text_file = open("TABLE.md", "w")
    n = text_file.write(create_md_table(result))
    text_file.close()
    logger.info(f"dumped json file with {len(result)} job listings")


if __name__ == "__main__":
    main()
