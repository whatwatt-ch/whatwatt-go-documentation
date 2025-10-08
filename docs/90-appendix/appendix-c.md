---
title: Appendix C
category: concepts
tags:
- appendix_c
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# JSON Formatting Script

## Document Context

- **Purpose**: JSON flattening script using jq for converting nested API responses into readable tabular format with type information
- **When to use**: Debugging API responses, analyzing complex JSON structures, data exploration, converting hierarchical data for processing
- **Prerequisites**: jq command-line tool installed, bash shell access, basic JSON and command-line knowledge
- **Related to**: REST API usage (rest-conventions.md), cURL commands (curl-options.md), JSON data analysis
- **Validates against**: Real WhatWatt Go API responses, jq syntax compatibility, cross-platform shell usage

## Key Facts

- **Tool**: jq-based bash script for recursive JSON flattening into dot-notation paths
- **Output format**: Tabular with field path, data type, and value columns
- **Use cases**: API debugging, data analysis, field discovery, type inspection
- **Features**: Handles nested objects and arrays, preserves type information, column-aligned output
- **Integration**: Works with cURL output, pipeable design, grep-friendly format

## Flattening JSON with jq

Below is a script that allows you to flatten a JSON structure using the `jq` command. This powerful tool streamlines the process of manipulating JSON data, enabling you to transform nested structures into a more manageable and readable format. By leveraging `jq`, you can effectively query and reshape your JSON data with ease, making it an invaluable asset for developers and data analysts alike.

## The Script

Create a file named `format_json.sh` with the following content:

```bash title="format_json.sh"
#!/bin/bash

jq -r '
  def walk(path):
    if (type == "object") then
      to_entries[]
      | . as $entry
      | $entry.value
      | walk(path + [ $entry.key ])
    elif (type == "array") then
      to_entries[]
      | . as $entry
      | $entry.value
      | walk(path + [ "[\($entry.key)]" ])
    else
      "\(path | join("."))\t\(type)\t\(.)"
    end;
  walk([])
' | column -t
```

Make the script executable:

```bash
chmod +x format_json.sh
```

## Usage

Thanks to this script, you can format API responses in a readable tabular format. For example, with the `/api/v1/report` endpoint:

```bash
curl -s http://192.168.1.100/api/v1/report | ./format_json.sh
```

## Example Output

The script will transform the complex JSON response into a flattened, easy-to-read format:

```txt
report.id                                         number  6381
report.interval                                   number  6.8
report.tariff                                     number  1
report.date_time                                  string  2025-10-07T11:35:36Z
report.date_time_local                            string  2025-10-07T11:35:36+02:00
report.date_time_utc                              string  2025-10-07T09:35:36Z
report.instantaneous_power.active.positive.total  number  0
report.instantaneous_power.active.positive.l1     number  0
report.instantaneous_power.active.positive.l2     number  0
report.instantaneous_power.active.positive.l3     number  0
report.instantaneous_power.active.negative.total  number  0
report.instantaneous_power.active.negative.l1     number  0
report.instantaneous_power.active.negative.l2     number  0
report.instantaneous_power.active.negative.l3     number  0
report.instantaneous_power.reactive.positive.l1   number  0
report.instantaneous_power.reactive.positive.l2   number  0
report.instantaneous_power.reactive.positive.l3   number  0
report.instantaneous_power.reactive.negative.l1   number  0
report.instantaneous_power.reactive.negative.l2   number  0
report.instantaneous_power.reactive.negative.l3   number  0
report.voltage.l1                                 number  235
report.voltage.l2                                 number  0
report.voltage.l3                                 number  0
report.current.l1                                 number  0
report.current.l2                                 number  0
report.current.l3                                 number  0
report.energy.active.positive.total               number  75.133
report.energy.active.negative.total               number  25.414
report.energy.reactive.positive.total             number  82.328
report.energy.reactive.negative.total             number  19.481
report.conv_factor                                number  1
meter.status                                      string  OK
meter.interface                                   string  MBUS
meter.protocol                                    string  DLMS
meter.logical_name                                string  LGZ1030784855204
meter.vendor                                      string  Landis+Gyr
meter.prefix                                      string  LGZ
system.id                                         string  ECC9FF5C7F14
system.date_time                                  string  2025-10-07T11:35:49Z
system.date_time_local                            string  2025-10-07T11:35:49+02:00
system.date_time_utc                              string  2025-10-07T09:35:49Z
system.boot_id                                    string  7CDC08FD
system.time_since_boot                            number  327919
```

## Benefits

- **Readability**: Complex nested JSON becomes easy to scan and understand
- **Type Information**: Shows the data type of each field (number, string, etc.)
- **Filtering**: Makes it easy to grep for specific fields
- **Analysis**: Perfect for debugging and data exploration

This script turns complex JSON hierarchies into simplified, flat structures that are much easier to work with during development and testing.
