---
title: CSV Format - SD Card Reports
category: data-formats
tags:
- csv
- sd-card
- logging
- data-export
- obis
- dlms
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /sdcard/
- /sdcard/{filename}
protocols:
- HTTP
related_concepts:
- energy monitoring
- OBIS codes
- DLMS protocol
- data logging
use_cases:
- historical data analysis
- energy auditing
- offline processing
- data backup
real_device_tested: true
---

# CSV format

CSV files are generated when the SD service is enabled. They are named `YYYYMMDD.CSV` and contain report rows collected over the day.

## Document Context

- **Purpose**: Understand the structure and format of CSV files logged to SD cards by whatwatt Go devices
- **When to use**: When you need to process historical energy data, perform offline analysis, or understand the data export format
- **Prerequisites**: Basic understanding of energy monitoring concepts; familiarity with OBIS codes helpful but not required
- **Related to**: REST API data endpoints, DLMS/COSEM protocol, energy measurement standards
- **Validates against**: Real device data from Landis+Gyr LGZ1030784855204 via MBUS interface

## Key Facts

- **File naming**: `YYYYMMDD.CSV` format (e.g., `20251007.CSV` for October 7, 2025)
- **Timezone**: All timestamps in UTC (indicated by "Z" suffix)
- **Frequency**: Records written every 15 minutes by default (configurable via settings)
- **Protocol basis**: DLMS/COSEM standard with OBIS code mapping
- **Access method**: HTTP GET via `/sdcard/` endpoint (no authentication typically required)
- **Data encoding**: CSV with quoted string fields, comma-separated
- **Field availability**: Many fields may be empty depending on meter capabilities

## Sample header and rows

```csv
RID,TIME,MID,MSTAT,TARIFF,PF,EAP_T,EAP_T1,EAP_T2,EAN_T,EAN_T1,EAN_T2,ERP_T,ERP_T1,ERP_T2,ERN_T,ERN_T1,ERN_T2,ERII_T,ERII_T1,ERII_T2,ERIC_T,ERIC_T1,ERIC_T2,EREI_T,EREI_T1,EREI_T2,EREC_T,EREC_T1,EREC_T2,MDAP_T,MDAP_T1,MDAP_T2,MDAN_T,MDAN_T1,MDAN_T2,IPAP_T,IPAP_L1,IPAP_L2,IPAP_L3,IPAN_T,IPAN_L1,IPAN_L2,IPAN_L3,IPRP_T,IPRP_L1,IPRP_L2,IPRP_L3,IPRN_T,IPRN_L1,IPRN_L2,IPRN_L3,IPA_T,V_L1,V_L2,V_L3,I_L1,I_L2,I_L3,MIDENT,MMODEL,MIF,MPROT,RP
3093,"2025-10-07T20:21:11Z","","OK",2,,75.133,,,25.414,,,82.328,,,19.481,,,,,,,,,,,,,,,,,,,,,0,0,0,0,0,0,0,0,,0,0,0,,0,0,0,,234,0,0,0,0,0,"LGZ1030784855204","","MBUS","DLMS",6818
3096,"2025-10-07T20:21:31Z","","OK",2,,75.133,,,25.414,,,82.328,,,19.481,,,,,,,,,,,,,,,,,,,,,0,0,0,0,0,0,0,0,,0,0,0,,0,0,0,,235,0,0,0,0,0,"LGZ1030784855204","","MBUS","DLMS",6786
```

- TIME is ISO‑8601 in UTC timezone (indicated by "Z" suffix)
- Energy counters use units consistent with REST `/api/v1/report`
- Many fields may be empty if not provided by the meter (depends on meter type and configuration)
- Columns may evolve with firmware; treat unknown columns as optional

## Field reference

The table below lists the CSV columns, their OBIS logical names (C.D.E), descriptions, units and value types.

| Field | OBIS (C.D.E) | Description | Unit | Type |
|---|---|---|---|---|
| RID |  | The report number that the device processed. This counter increments from the time the device boots. |  | integer |
| TIME |  | Date and time sent by the meter in the report, in local timezone |  | string (ISO-8601) |
| MID | 96.1.0 | Meter identifier |  | string |
| MSTAT |  | Meter status |  | string enum (NO INIT, NO DATA, RECOGNITION, OK, ENCRYPTION KEY, KEY REQUIRED, NOT RECOGNIZED) |
| TARIFF |  | Current tariff |  | integer (1..2) |
| PF | 13.7.0 | Instantaneous power factor |  | float |
| EAP_T | 1.8.0 | Positive active energy (A+) total | kWh | float |
| EAP_T1 | 1.8.1 | Positive active energy (A+) in tariff T1 | kWh | float |
| EAP_T2 | 1.8.2 | Positive active energy (A+) in tariff T2 | kWh | float |
| EAN_T | 2.8.0 | Negative active energy (A−) total | kWh | float |
| EAN_T1 | 2.8.1 | Negative active energy (A−) in tariff T1 | kWh | float |
| EAN_T2 | 2.8.2 | Negative active energy (A−) in tariff T2 | kWh | float |
| ERP_T | 3.8.0 | Positive reactive energy (Q+) total | kvarh | float |
| ERP_T1 | 3.8.1 | Positive reactive energy (Q+) in tariff T1 | kvarh | float |
| ERP_T2 | 3.8.2 | Positive reactive energy (Q+) in tariff T2 | kvarh | float |
| ERN_T | 4.8.0 | Negative reactive energy (Q−) total | kvarh | float |
| ERN_T1 | 4.8.1 | Negative reactive energy (Q−) in tariff T1 | kvarh | float |
| ERN_T2 | 4.8.2 | Negative reactive energy (Q−) in tariff T2 | kvarh | float |
| ERII_T | 5.8.0 | Imported inductive reactive energy in 1st quadrant (Q1) total | kvarh | float |
| ERII_T1 | 5.8.1 | Imported inductive reactive energy in 1st quadrant (Q1) in tariff T1 | kvarh | float |
| ERII_T2 | 5.8.2 | Imported inductive reactive energy in 1st quadrant (Q1) in tariff T2 | kvarh | float |
| ERIC_T | 6.8.0 | Imported capacitive reactive energy in 2nd quadrant (Q2) total | kvarh | float |
| ERIC_T1 | 6.8.1 | Imported capacitive reactive energy in 2nd quadrant (Q2) in tariff T1 | kvarh | float |
| ERIC_T2 | 6.8.2 | Imported capacitive reactive energy in 2nd quadrant (Q2) in tariff T2 | kvarh | float |
| EREI_T | 7.8.0 | Exported inductive reactive energy in 3rd quadrant (Q3) total | kvarh | float |
| EREI_T1 | 7.8.1 | Exported inductive reactive energy in 3rd quadrant (Q3) in tariff T1 | kvarh | float |
| EREI_T2 | 7.8.2 | Exported inductive reactive energy in 3rd quadrant (Q3) in tariff T2 | kvarh | float |
| EREC_T | 8.8.0 | Exported capacitive reactive energy in 4th quadrant (Q4) total | kvarh | float |
| EREC_T1 | 8.8.1 | Exported capacitive reactive energy in 4th quadrant (Q4) in tariff T1 | kvarh | float |
| EREC_T2 | 8.8.2 | Exported capacitive reactive energy in 4th quadrant (Q4) in tariff T2 | kvarh | float |
| MDAP_T | 1.6.0 | Positive active maximum demand (A+) total | kWh | float |
| MDAP_T1 | 1.6.1 | Positive active maximum demand (A+) in tariff T1 | kWh | float |
| MDAP_T2 | 1.6.2 | Positive active maximum demand (A+) in tariff T2 | kWh | float |
| MDAN_T | 2.6.0 | Negative active maximum demand (A−) total | kWh | float |
| MDAN_T1 | 2.6.1 | Negative active maximum demand (A−) in tariff T1 | kWh | float |
| MDAN_T2 | 2.6.2 | Negative active maximum demand (A−) in tariff T2 | kWh | float |
| IPAP_T | 1.7.0 | Positive active instantaneous power (A+) | kW | float |
| IPAP_L1 | 21.7.0 | Positive active instantaneous power (A+) in phase L1 | kW | float |
| IPAP_L2 | 41.7.0 | Positive active instantaneous power (A+) in phase L2 | kW | float |
| IPAP_L3 | 61.7.0 | Positive active instantaneous power (A+) in phase L3 | kW | float |
| IPAN_T | 2.7.0 | Negative active instantaneous power (A−) | kW | float |
| IPAN_L1 | 22.7.0 | Negative active instantaneous power (A−) in phase L1 | kW | float |
| IPAN_L2 | 42.7.0 | Negative active instantaneous power (A−) in phase L2 | kW | float |
| IPAN_L3 | 62.7.0 | Negative active instantaneous power (A−) in phase L3 | kW | float |
| IPRP_T | 3.7.0 | Positive reactive instantaneous power (Q+) | kvar | float |
| IPRP_L1 | 23.7.0 | Positive reactive instantaneous power (Q+) in phase L1 | kvar | float |
| IPRP_L2 | 43.7.0 | Positive reactive instantaneous power (Q+) in phase L2 | kvar | float |
| IPRP_L3 | 63.7.0 | Positive reactive instantaneous power (Q+) in phase L3 | kvar | float |
| IPRN_T | 4.7.0 | Negative reactive instantaneous power (Q−) | kvar | float |
| IPRN_L1 | 24.7.0 | Negative reactive instantaneous power (Q−) in phase L1 | kvar | float |
| IPRN_L2 | 44.7.0 | Negative reactive instantaneous power (Q−) in phase L2 | kvar | float |
| IPRN_L3 | 64.7.0 | Negative reactive instantaneous power (Q−) in phase L3 | kvar | float |
| IPA_T | 9.7.0 | Apparent instantaneous power (S+) | kVA | float |
| V_L1 | 32.7.0 | Instantaneous voltage (U) in phase L1 | V | float |
| V_L2 | 52.7.0 | Instantaneous voltage (U) in phase L2 | V | float |
| V_L3 | 72.7.0 | Instantaneous voltage (U) in phase L3 | V | float |
| I_L1 | 31.7.0 | Instantaneous current (I) in phase L1 | A | float |
| I_L2 | 51.7.0 | Instantaneous current (I) in phase L2 | A | float |
| I_L3 | 71.7.0 | Instantaneous current (I) in phase L3 | A | float |
| MIDENT | 42.0.0 | Meter identifier |  | string |
| MMODEL | 96.1.1 | Meter model |  | string |
| MIF |  | Meter interface |  | string enum (P1, MBUS, TTL, MEP) |
| MPROT |  | Meter protocol |  | string enum (DSMR, DLMS, KMP, MEP) |
| RP |  | Report period. How often does the meter send a report |  | float |

Notes:

- Where both `MID` (96.1.0) and `MIDENT` (42.0.0) appear, they may reflect different meter identifier objects depending on protocol/firmware.
- OBIS notations follow C.D.E fields, common in DLMS/COSEM.
- Enumerations are shown in the Type column where applicable.
- Many fields may be empty or contain only null/zero values depending on what the specific meter model provides.
- The `TIME` field uses UTC timezone (Z suffix) rather than local time in current firmware versions.
- `RP` (Report Period) shows the interval in milliseconds between meter reports.

## Common Issues & Solutions

### Issue: Empty CSV file or missing daily files

- **Symptoms**: Expected `YYYYMMDD.CSV` file doesn't exist or is empty
- **Root cause**: SD card service disabled, storage full, or file system corruption
- **Diagnosis**:
  - Check device settings: `services.sd.enable` should be `true`
  - Verify SD card is inserted and detected
  - Check available space on SD card
- **Solution**:
  - Enable SD logging via `/api/v1/settings`: `{"services": {"sd": {"enable": true}}}`
  - Reformat SD card if corruption suspected
  - Adjust `frequency` setting to reduce storage usage
- **Code pattern**:

```python
# Check if SD logging is enabled
settings = requests.get(f"http://{device}/api/v1/settings").json()
if not settings.get("services", {}).get("sd", {}).get("enable", False):
    print("SD card logging is disabled")
```

- **Related**: [SD Card Configuration](./configuration.md)

### Issue: Many CSV fields contain empty values or zeros

- **Symptoms**: Most columns show empty strings or zero values
- **Root cause**: Meter doesn't provide all OBIS objects, or communication issues
- **Diagnosis**: Check `MSTAT` column - should be "OK" for valid data
- **Solution**:
  - Filter rows where `MSTAT != "OK"`
  - Focus on populated fields for your specific meter model
  - Different meter types provide different data sets
- **Code pattern**:

```python
import pandas as pd

df = pd.read_csv('20251007.CSV')
# Filter valid meter status
valid_data = df[df['MSTAT'] == 'OK']

# Find non-empty columns for this meter
populated_cols = []
for col in df.columns:
    if df[col].notna().sum() > 0 and (df[col] != 0).sum() > 0:
        populated_cols.append(col)
```

- **Related**: Meter model specifications, OBIS code availability

### Issue: Timestamp parsing errors

- **Symptoms**: TIME field format not recognized by date parsers
- **Root cause**: ISO-8601 UTC format may not be handled by all parsers
- **Diagnosis**: Check TIME field format: should be `"2025-10-07T20:21:11Z"`
- **Solution**: Use ISO-8601 compatible parsers, handle Z suffix correctly
- **Code pattern**:

```python
from datetime import datetime
import pandas as pd

# Proper timestamp parsing
df['timestamp'] = pd.to_datetime(df['TIME'], format='%Y-%m-%dT%H:%M:%SZ', utc=True)

# Convert to local timezone if needed
df['timestamp_local'] = df['timestamp'].dt.tz_convert('Europe/Zurich')
```

### Issue: Inconsistent data frequency

- **Symptoms**: CSV rows don't appear at expected intervals
- **Root cause**: Meter report frequency varies, or device missed some reports
- **Diagnosis**: Check `RP` (Report Period) field for actual meter intervals
- **Solution**: Handle variable intervals in data processing
- **Code pattern**:

```python
# Calculate actual intervals between readings
df['time_diff'] = df['timestamp'].diff().dt.total_seconds()
median_interval = df['time_diff'].median()
print(f"Median report interval: {median_interval} seconds")

# Detect gaps in data
gaps = df[df['time_diff'] > median_interval * 2]
print(f"Found {len(gaps)} data gaps")
```

### Issue: Energy counter resets or discontinuities

- **Symptoms**: Cumulative energy values (EAP_T, EAN_T) decrease unexpectedly
- **Root cause**: Meter reset, device restart, or data corruption
- **Diagnosis**: Look for sudden drops in cumulative counters
- **Solution**: Implement continuity checks and handle resets gracefully
- **Code pattern**:

```python
# Detect energy counter resets
def detect_resets(series):
    resets = []
    for i in range(1, len(series)):
        if pd.notna(series.iloc[i]) and pd.notna(series.iloc[i-1]):
            if series.iloc[i] < series.iloc[i-1] * 0.9:  # 10% tolerance
                resets.append(i)
    return resets

eap_resets = detect_resets(df['EAP_T'])
if eap_resets:
    print(f"Detected energy counter resets at rows: {eap_resets}")
```

### Issue: Phase data inconsistency on single-phase meters

- **Symptoms**: L2 and L3 columns always zero, only L1 has values
- **Root cause**: Single-phase meter installation - L2/L3 don't exist
- **Diagnosis**: Check if voltage and current L2/L3 fields are consistently zero
- **Solution**: Use total values or L1 values for single-phase analysis
- **Code pattern**:

```python
# Detect meter phase configuration
def detect_phases(df):
    phases = []
    if (df['V_L1'] > 0).any():
        phases.append('L1')
    if (df['V_L2'] > 0).any():
        phases.append('L2')
    if (df['V_L3'] > 0).any():
        phases.append('L3')
    return phases

active_phases = detect_phases(df)
print(f"Active phases: {active_phases}")
```

## Semantic Field Map

Understanding the logical grouping and meaning of CSV fields for RAG and data processing:

### Energy Counters Group (Cumulative Values)

- `EAP_T` (OBIS: 1.8.0) → **semantic_name**: "total_imported_energy" → **meaning**: "Cumulative energy consumed from grid" → **unit**: "kWh" → **type**: "cumulative_counter"
- `EAN_T` (OBIS: 2.8.0) → **semantic_name**: "total_exported_energy" → **meaning**: "Cumulative energy fed back to grid" → **unit**: "kWh" → **type**: "cumulative_counter"
- `ERP_T` (OBIS: 3.8.0) → **semantic_name**: "total_reactive_positive" → **meaning**: "Cumulative positive reactive energy" → **unit**: "kvarh" → **type**: "cumulative_counter"
- `ERN_T` (OBIS: 4.8.0) → **semantic_name**: "total_reactive_negative" → **meaning**: "Cumulative negative reactive energy" → **unit**: "kvarh" → **type**: "cumulative_counter"

### Power Measurements Group (Instantaneous Values)

- `IPAN_T` (OBIS: 2.7.0) → **semantic_name**: "instantaneous_export_power" → **meaning**: "Current power fed back to grid" → **unit**: "kW" → **type**: "instantaneous_value"
- `IPRP_T` (OBIS: 3.7.0) → **semantic_name**: "instantaneous_reactive_positive" → **meaning**: "Current positive reactive power" → **unit**: "kvar" → **type**: "instantaneous_value"
- `IPA_T` (OBIS: 9.7.0) → **semantic_name**: "instantaneous_apparent_power" → **meaning**: "Current apparent power (total)" → **unit**: "kVA" → **type**: "instantaneous_value"

### Electrical Parameters Group (Per-Phase Values)

- `V_L1, V_L2, V_L3` (OBIS: 32.7.0, 52.7.0, 72.7.0) → **semantic_name**: "voltage_phases" → **meaning**: "Line voltages for three phases" → **unit**: "V" → **type**: "instantaneous_value"
- `I_L1, I_L2, I_L3` (OBIS: 31.7.0, 51.7.0, 71.7.0) → **semantic_name**: "current_phases" → **meaning**: "Line currents for three phases" → **unit**: "A" → **type**: "instantaneous_value"

### Device Metadata Group

- `MIDENT` (OBIS: 42.0.0) → **semantic_name**: "meter_identifier" → **meaning**: "Unique meter serial number" → **unit**: "string" → **type**: "device_metadata"
- `MSTAT` → **semantic_name**: "meter_status" → **meaning**: "Communication status with meter" → **unit**: "enum" → **type**: "status_indicator"
- `MPROT` → **semantic_name**: "meter_protocol" → **meaning**: "Communication protocol used" → **unit**: "enum" → **type**: "device_metadata"
- `MIF` → **semantic_name**: "meter_interface" → **meaning**: "Physical interface type" → **unit**: "enum" → **type**: "device_metadata"

### Temporal Data Group

- `TIME` → **semantic_name**: "measurement_timestamp" → **meaning**: "When measurement was taken" → **unit**: "ISO-8601" → **type**: "timestamp"
- `RID` → **semantic_name**: "report_sequence_id" → **meaning**: "Sequential report number since device boot" → **unit**: "integer" → **type**: "sequence_metadata"
- `RP` → **semantic_name**: "report_period_ms" → **meaning**: "Milliseconds between meter reports" → **unit**: "ms" → **type**: "configuration_metadata"

### Tariff-Specific Data Group

- `EAP_T1, EAP_T2` (OBIS: 1.8.1, 1.8.2) → **semantic_name**: "tariff_imported_energy" → **meaning**: "Energy consumption per tariff period" → **unit**: "kWh" → **type**: "tariff_cumulative"
- `TARIFF` → **semantic_name**: "current_tariff" → **meaning**: "Active tariff number" → **unit**: "integer" → **type**: "tariff_indicator"

**RAG Processing Notes**:

- Group energy calculations: Use `EAP_T` and `EAN_T` for net energy analysis
- Real-time monitoring: Focus on `IPAP_T`, `V_L1-L3`, `I_L1-L3` for live data
- Data quality check: Always validate `MSTAT == "OK"` before processing values
- Missing data handling: Empty fields indicate meter doesn't provide that measurement

- **Related**: Three-phase vs single-phase installation types
