# Scalers configuration

The table below contains scaling coefficients for measurement values from the electricity meter. The first column contains the value name and its corresponding field in the report object. The OBIS column is a shortened version of the OBIS code referencing the name. The E360/E450/E570 scalers columns contain default scaling coefficients for each meter type.

The scaling coefficient represents the power of 10 (10^scaler) that should be applied to the raw value from the meter to obtain the actual measurement value.

Note that report object fields are only present if they are received from the meter. Some fields may be missing depending on the meter type and configuration.

| Register / JSON field                                                                              | OBIS   | E360 scaler | E450 scaler | E570 scaler |
| -------------------------------------------------------------------------------------------------- | ------ | ----------- | ----------- | ----------- |
| Positive active energy (A+) total<br />.report.energy.active.positive.total                        | 1.8.0  | 0           | 0           | 3           |
| Positive active energy (A+) in tariff T1<br />.report.energy.active.positive.t1                    | 1.8.1  | 0           | 0           | 3           |
| Positive active energy (A+) in tariff T2<br />.report.energy.active.positive.t2                    | 1.8.2  | 0           | 0           | 3           |
| Negative active energy (A-) total<br />.report.energy.active.negative.total                        | 2.8.0  | 0           | 0           | 3           |
| Negative active energy (A-) in tariff T1<br />.report.energy.active.negative.t1                    | 2.8.1  | 0           | 0           | 3           |
| Negative active energy (A-) in tariff T2<br />.report.energy.active.negative.t2                    | 2.8.2  | 0           | 0           | 3           |
| Positive reactive energy (Q+) total<br />.report.energy.reactive.positive.total                    | 3.8.0  | 0           | 0           | 3           |
| Positive reactive energy (Q+) in tariff T1<br />.report.energy.reactive.positive.t1                | 3.8.1  | 0           | 0           | 3           |
| Positive reactive energy (Q+) in tariff T2<br />.report.energy.reactive.positive.t2                | 3.8.2  | 0           | 0           | 3           |
| Negative reactive energy (Q-) total<br />.report.energy.reactive.negative.total                    | 4.8.0  | 0           | 0           | 3           |
| Negative reactive energy (Q-) in tariff T1<br />.report.energy.reactive.negative.t1                | 4.8.1  | 0           | 0           | 3           |
| Negative reactive energy (Q-) in tariff T2<br />.report.energy.reactive.negative.t2                | 4.8.2  | 0           | 0           | 3           |
| Positive active instantaneous power (A+)<br />.report.instantaneous_power.active.positive.total    | 1.7.0  | 0           | 0           | -1          |
| Negative active instantaneous power (A-)<br />.report.instantaneous_power.active.negative.total    | 2.7.0  | 0           | 0           | -1          |
| Instantaneous voltage (U) in phase L1<br />.report.voltage.l1                                      | 32.7.0 | -1          | 0           | 0           |
| Instantaneous voltage (U) in phase L2<br />.report.voltage.l2                                      | 52.7.0 | -1          | 0           | 0           |
| Instantaneous voltage (U) in phase L3<br />.report.voltage.l3                                      | 72.7.0 | -1          | 0           | 0           |
| Instantaneous current (I) in phase L1<br />.report.current.l1                                      | 31.7.0 | -2          | -2          | -1          |
| Instantaneous current (I) in phase L2<br />.report.current.l2                                      | 51.7.0 | -2          | -2          | -1          |
| Instantaneous current (I) in phase L3<br />.report.current.l3                                      | 71.7.0 | -2          | -2          | -1          |
| Positive active instantaneous power (A+) in phase L1<br />.report.instantaneous_power.active.positive.l1   | 21.7.0 | 0           | 0           | -1          |
| Positive active instantaneous power (A+) in phase L2<br />.report.instantaneous_power.active.positive.l2   | 41.7.0 | 0           | 0           | -1          |
| Positive active instantaneous power (A+) in phase L3<br />.report.instantaneous_power.active.positive.l3   | 61.7.0 | 0           | 0           | -1          |
| Negative active instantaneous power (A-) in phase L1<br />.report.instantaneous_power.active.negative.l1   | 22.7.0 | 0           | 0           | -1          |
| Negative active instantaneous power (A-) in phase L2<br />.report.instantaneous_power.active.negative.l2   | 42.7.0 | 0           | 0           | -1          |
| Negative active instantaneous power (A-) in phase L3<br />.report.instantaneous_power.active.negative.l3   | 62.7.0 | 0           | 0           | -1          |
| Positive reactive instantaneous power (Q+) in phase L1<br />.report.instantaneous_power.reactive.positive.l1 | 23.7.0 | 0           | 0           | -1          |
| Positive reactive instantaneous power (Q+) in phase L2<br />.report.instantaneous_power.reactive.positive.l2 | 43.7.0 | 0           | 0           | -1          |
| Positive reactive instantaneous power (Q+) in phase L3<br />.report.instantaneous_power.reactive.positive.l3 | 63.7.0 | 0           | 0           | -1          |
| Negative reactive instantaneous power (Q-) in phase L1<br />.report.instantaneous_power.reactive.negative.l1 | 24.7.0 | 0           | 0           | -1          |
| Negative reactive instantaneous power (Q-) in phase L2<br />.report.instantaneous_power.reactive.negative.l2 | 44.7.0 | 0           | 0           | -1          |
| Negative reactive instantaneous power (Q-) in phase L3<br />.report.instantaneous_power.reactive.negative.l3 | 64.7.0 | 0           | 0           | -1          |

Example report object 1:

```json
{
  "report": {
    "id": 13056,
    "interval": 10.01,
    "tariff": 1,
    "date_time": "2025-11-18T11:17:40Z",
    "date_time_local": "2025-11-18T11:17:40+01:00",
    "date_time_utc": "2025-11-18T10:17:40Z",
    "instantaneous_power": {
      "active": {
        "positive": {
          "total": 7.8497,
          "l1": 2.9433,
          "l2": 2.1458,
          "l3": 2.7606
        },
        "negative": {
          "total": 0,
          "l1": 0,
          "l2": 0,
          "l3": 0
        }
      },
      "reactive": {
        "positive": {
          "l1": 0.634,
          "l2": 0.7086,
          "l3": 0.2861
        },
        "negative": {
          "l1": 0,
          "l2": 0,
          "l3": 0
        }
      }
    },
    "voltage": {
      "l1": 231,
      "l2": 230,
      "l3": 232
    },
    "current": {
      "l1": 13.1,
      "l2": 9.9,
      "l3": 12
    },
    "energy": {
      "active": {
        "positive": {
          "total": 8306146
        },
        "negative": {
          "total": 42615
        }
      },
      "reactive": {
        "positive": {
          "total": 2236203
        },
        "negative": {
          "total": 49110
        }
      }
    },
    "conv_factor": 1
  },
  "meter": {
    "status": "OK",
    "interface": "MBUS",
    "protocol": "DLMS",
    "logical_name": "LGZ1030781449532",
    "vendor": "Landis+Gyr",
    "prefix": "LGZ"
  },
  "system": {
    "id": "ECC9FF5C6DFC",
    "date_time": "2025-11-18T11:17:58Z",
    "date_time_local": "2025-11-18T11:17:58+01:00",
    "date_time_utc": "2025-11-18T10:17:58Z",
    "boot_id": "CFB7A412",
    "time_since_boot": 230860
  }
}
```

**Note:** The `instantaneous_power` fields in the report object are in kilowatts (kW), while the `energy` fields are in kilowatt-hours (kWh). The `time_since_boot` field is in seconds.

Example report object 2:

```json
{
  "report": {
    "id": 13093,
    "interval": 10.045,
    "tariff": 1,
    "date_time": "2025-11-18T11:23:50Z",
    "date_time_local": "2025-11-18T11:23:50+01:00",
    "date_time_utc": "2025-11-18T10:23:50Z",
    "instantaneous_power": {
      "active": {
        "positive": {
          "total": 6.4644,
          "l1": 2.3708,
          "l2": 2.2449,
          "l3": 1.8486
        },
        "negative": {
          "total": 0,
          "l1": 0,
          "l2": 0,
          "l3": 0
        }
      },
      "reactive": {
        "positive": {
          "l1": 0.4561,
          "l2": 1.23,
          "l3": 0.4827
        },
        "negative": {
          "l1": 0,
          "l2": 0,
          "l3": 0
        }
      }
    },
    "voltage": {
      "l1": 231,
      "l2": 230,
      "l3": 232
    },
    "current": {
      "l1": 10.6,
      "l2": 10.9,
      "l3": 8.3
    },
    "energy": {
      "active": {
        "positive": {
          "total": 8306870
        },
        "negative": {
          "total": 42615
        }
      },
      "reactive": {
        "positive": {
          "total": 2236409
        },
        "negative": {
          "total": 49110
        }
      }
    },
    "conv_factor": 1
  },
  "meter": {
    "status": "OK",
    "interface": "MBUS",
    "protocol": "DLMS",
    "logical_name": "LGZ1030781449532",
    "vendor": "Landis+Gyr",
    "prefix": "LGZ"
  },
  "system": {
    "id": "ECC9FF5C6DFC",
    "date_time": "2025-11-18T11:24:13Z",
    "date_time_local": "2025-11-18T11:24:13+01:00",
    "date_time_utc": "2025-11-18T10:24:13Z",
    "boot_id": "CFB7A412",
    "time_since_boot": 231236
  }
}
```

Example scalers configuration array:

```json
[
{"obis":"1.8.0","scaler":3},
{"obis":"1.8.1","scaler":3},
{"obis":"1.8.2","scaler":3},

{"obis":"2.8.0","scaler":3},
{"obis":"2.8.1","scaler":3},
{"obis":"2.8.2","scaler":3},

{"obis":"3.8.0","scaler":3},
{"obis":"3.8.1","scaler":3},
{"obis":"3.8.2","scaler":3},

{"obis":"4.8.0","scaler":3},
{"obis":"4.8.1","scaler":3},
{"obis":"4.8.2","scaler":3},

{"obis":"1.7.0","scaler":0},
{"obis":"2.7.0","scaler":0},

{"obis":"32.7.0","scaler":0},
{"obis":"52.7.0","scaler":0},
{"obis":"72.7.0","scaler":0},

{"obis":"31.7.0","scaler":-1},
{"obis":"51.7.0","scaler":-1},
{"obis":"71.7.0","scaler":-1},

{"obis":"21.7.0","scaler":-1},
{"obis":"41.7.0","scaler":-1},
{"obis":"61.7.0","scaler":-1},

{"obis":"22.7.0","scaler":-1},
{"obis":"42.7.0","scaler":-1},
{"obis":"62.7.0","scaler":-1},

{"obis":"23.7.0","scaler":-1},
{"obis":"43.7.0","scaler":-1},
{"obis":"63.7.0","scaler":-1},

{"obis":"24.7.0","scaler":-1},
{"obis":"44.7.0","scaler":-1},
{"obis":"64.7.0","scaler":-1}
]
```

## Calculating Positive Active Power from Energy

To calculate positive active power from energy readings:

1. Obtain two reports from the same device at different times
2. Calculate the time difference (dt) based on the `.system.time_since_boot` field in the report object (the newer object has a higher value)
3. Calculate the difference between `.energy.active.positive.total` fields from both reports
4. Multiply the energy difference by `3600/dt` to get the power in kW

Similar calculations can be performed for:

- **Negative active power**: Use `.energy.active.negative.total` field
- **Positive reactive power**: Use `.energy.reactive.positive.total` field
- **Negative reactive power**: Use `.energy.reactive.negative.total` field

## Default Scalers Configuration for Each Meter Type

### E360 Meter Default Scalers

```json
[
{"obis":"1.8.0","scaler":0},
{"obis":"1.8.1","scaler":0},
{"obis":"1.8.2","scaler":0},

{"obis":"2.8.0","scaler":0},
{"obis":"2.8.1","scaler":0},
{"obis":"2.8.2","scaler":0},

{"obis":"3.8.0","scaler":0},
{"obis":"3.8.1","scaler":0},
{"obis":"3.8.2","scaler":0},

{"obis":"4.8.0","scaler":0},
{"obis":"4.8.1","scaler":0},
{"obis":"4.8.2","scaler":0},

{"obis":"1.7.0","scaler":0},
{"obis":"2.7.0","scaler":0},

{"obis":"32.7.0","scaler":-1},
{"obis":"52.7.0","scaler":-1},
{"obis":"72.7.0","scaler":-1},

{"obis":"31.7.0","scaler":-2},
{"obis":"51.7.0","scaler":-2},
{"obis":"71.7.0","scaler":-2},

{"obis":"21.7.0","scaler":0},
{"obis":"41.7.0","scaler":0},
{"obis":"61.7.0","scaler":0},

{"obis":"22.7.0","scaler":0},
{"obis":"42.7.0","scaler":0},
{"obis":"62.7.0","scaler":0},

{"obis":"23.7.0","scaler":0},
{"obis":"43.7.0","scaler":0},
{"obis":"63.7.0","scaler":0},

{"obis":"24.7.0","scaler":0},
{"obis":"44.7.0","scaler":0},
{"obis":"64.7.0","scaler":0}
]
```

### E450 Meter Default Scalers

```json
[
{"obis":"1.8.0","scaler":0},
{"obis":"1.8.1","scaler":0},
{"obis":"1.8.2","scaler":0},

{"obis":"2.8.0","scaler":0},
{"obis":"2.8.1","scaler":0},
{"obis":"2.8.2","scaler":0},

{"obis":"3.8.0","scaler":0},
{"obis":"3.8.1","scaler":0},
{"obis":"3.8.2","scaler":0},

{"obis":"4.8.0","scaler":0},
{"obis":"4.8.1","scaler":0},
{"obis":"4.8.2","scaler":0},

{"obis":"1.7.0","scaler":0},
{"obis":"2.7.0","scaler":0},

{"obis":"32.7.0","scaler":0},
{"obis":"52.7.0","scaler":0},
{"obis":"72.7.0","scaler":0},

{"obis":"31.7.0","scaler":-2},
{"obis":"51.7.0","scaler":-2},
{"obis":"71.7.0","scaler":-2},

{"obis":"21.7.0","scaler":0},
{"obis":"41.7.0","scaler":0},
{"obis":"61.7.0","scaler":0},

{"obis":"22.7.0","scaler":0},
{"obis":"42.7.0","scaler":0},
{"obis":"62.7.0","scaler":0},

{"obis":"23.7.0","scaler":0},
{"obis":"43.7.0","scaler":0},
{"obis":"63.7.0","scaler":0},

{"obis":"24.7.0","scaler":0},
{"obis":"44.7.0","scaler":0},
{"obis":"64.7.0","scaler":0}
]
```

### E570 Meter Default Scalers

```json
[
{"obis":"1.8.0","scaler":3},
{"obis":"1.8.1","scaler":3},
{"obis":"1.8.2","scaler":3},

{"obis":"2.8.0","scaler":3},
{"obis":"2.8.1","scaler":3},
{"obis":"2.8.2","scaler":3},

{"obis":"3.8.0","scaler":3},
{"obis":"3.8.1","scaler":3},
{"obis":"3.8.2","scaler":3},

{"obis":"4.8.0","scaler":3},
{"obis":"4.8.1","scaler":3},
{"obis":"4.8.2","scaler":3},

{"obis":"1.7.0","scaler":-1},
{"obis":"2.7.0","scaler":-1},

{"obis":"32.7.0","scaler":0},
{"obis":"52.7.0","scaler":0},
{"obis":"72.7.0","scaler":0},

{"obis":"31.7.0","scaler":-1},
{"obis":"51.7.0","scaler":-1},
{"obis":"71.7.0","scaler":-1},

{"obis":"21.7.0","scaler":-1},
{"obis":"41.7.0","scaler":-1},
{"obis":"61.7.0","scaler":-1},

{"obis":"22.7.0","scaler":-1},
{"obis":"42.7.0","scaler":-1},
{"obis":"62.7.0","scaler":-1},

{"obis":"23.7.0","scaler":-1},
{"obis":"43.7.0","scaler":-1},
{"obis":"63.7.0","scaler":-1},

{"obis":"24.7.0","scaler":-1},
{"obis":"44.7.0","scaler":-1},
{"obis":"64.7.0","scaler":-1}
]
```
