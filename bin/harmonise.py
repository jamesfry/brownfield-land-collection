#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#

import sys
import re
import csv

# TBD: load full schema.json
schema = {
    "fields": [
        {
            "name": "OrganisationURI",
            "title": "Organisation URI",
            "typos": [ "OrganistionURI", "LPA URL", "OPEN DATA WEBSITE" ]
        },
        {
            "name": "SiteReference",
            "title": "Site reference",
            "typos": ["LA SITE REF"]
        },
        {
            "name": "GeoX",
        },
        {
            "name": "GeoY",
        },
        {
            "name": "Hectares",
            "typos": ["AREA (HA)"]
        },
        {
            "name": "FirstAddedDate"
        },
        {
            "name": "LastUpdatedDate"
        }
    ]
}

pattern = re.compile(r'[^a-z0-9]')


def name(name):
    return re.sub(pattern, '', name.lower())


if __name__ == "__main__":
    fieldnames = [field["name"] for field in schema["fields"]]

    # index of typos
    typos = {}
    for field in schema["fields"]:
        typos[name(field["name"])] = field["name"]
        if "title" in field:
            typos[name(field["title"])] = field["name"]
        for typo in field.get("typos", []):
            typos[name(typo)] = field["name"]

    reader = csv.DictReader(open(sys.argv[1], newline=""))

    # build index of read headers
    headers = {}
    for field in reader.fieldnames:
        if name(field) in typos:
            headers[field] = typos[name(field)]

    with open(sys.argv[2], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            o = {}
            for header in headers:
                o[headers[header]] = row[header]

            writer.writerow(o)
