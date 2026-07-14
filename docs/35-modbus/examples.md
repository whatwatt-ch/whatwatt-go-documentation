# Modbus Example Configurations

This page collects ready-to-load Modbus slave templates that let whatwatt Go
emulate several common power meters.

All example JSON files live in the local `examples` directory next to this page.

## Available Templates

- [siemens_pac2200.json](examples/siemens_pac2200.json) - Siemens PAC2200 layout.
  This matches the default firmware layout used when no custom Modbus
  configuration is stored.
- [carlo_gavazzi_em24_e1.json](examples/carlo_gavazzi_em24_e1.json) - Carlo
  Gavazzi EM24_E1 layout with `lsw` word order for 32-bit values.
- [huawei_dtsu666_h.json](examples/huawei_dtsu666_h.json) - Huawei three-phase
  DTSU666-H smart meter block at address `37100`.
- [huawei_ddsu666_h.json](examples/huawei_ddsu666_h.json) - Huawei single-phase
  DDSU666-H smart meter block at address `37100`, with unused phase B/C registers
  kept present and zero-filled.
- [huawei_smartlogger_external_meter.json](examples/huawei_smartlogger_external_meter.json)
  - Huawei SmartLogger external meter view using the `32260` and `32299` register
  spaces.
- [huawei_emma_external_meter.json](examples/huawei_emma_external_meter.json) -
  Huawei EMMA external meter view at address `30500`.
- [fronius_smart_meter_63a.json](examples/fronius_smart_meter_63a.json) - Fronius
  Smart Meter 63A emulation using a Fronius-specific SunSpec-like layout at
  address `40000` plus additional probe registers.
- [herholdt_m3pro.json](examples/herholdt_m3pro.json) - Herholdt M3PRO register
  map beginning at address `4100`, collapsed into one contiguous area for
  compatibility with the current parser.
- [sunspec_model_1_203.json](examples/sunspec_model_1_203.json) - SunSpec Common
  Model 1 plus meter Model 203 using `int16` and `int32` values with scale
  factors.
- [sunspec_model_1_213.json](examples/sunspec_model_1_213.json) - SunSpec Common
  Model 1 plus meter Model 213 using `float32` values.
- [janitza_604.json](examples/janitza_604.json) - Janitza B604 series register
  map at addresses `753`, `911`, `10176`, and `19000`. Uses `net.ip` for the IP
  address register and named energy identifiers. Requires **FW 2.7.0** or newer.
- [janitza_604_old.json](examples/janitza_604_old.json) - Janitza B604 series
  register map for firmware versions **before FW 2.7.0**. Uses a hardcoded
  `C_IP_ADDR` constant instead of `net.ip`, and unnamed padding registers instead
  of `11.7.0`, `energy.active`, `energy.reactive`, `energy.reactive.inductive`,
  and `energy.reactive.capactive`.

## Compatibility Notes

- `siemens_pac2200.json` matches the EVCC `siemens-pac2200` and MBMD `pac2200`
  paths.
- `carlo_gavazzi_em24_e1.json` is aimed at EVCC `cg-em24_e1` and MBMD
  `cgem24_e1`.
- `huawei_dtsu666_h.json` and `huawei_ddsu666_h.json` follow Huawei's shared
  inverter-facing smart meter block at `37100`. The single-phase template differs
  mainly by the meter type flag and zero-filled phase B/C registers.
- `huawei_smartlogger_external_meter.json` and `huawei_emma_external_meter.json`
  model the higher-level register spaces exported by Huawei SmartLogger and EMMA
  integrations, not the raw RS485 meter wire image.
- `fronius_smart_meter_63a.json` follows the Fronius Smart Meter IP emulator style
  used by Fronius inverter probing. It starts with a Fronius-specific SunSpec-like
  block at `40000` and exposes several extra zero-valued probe registers.
- `herholdt_m3pro.json` follows the Herholdt M1PRO/M3PRO protocol table. Register
  addresses are used exactly as printed in the vendor document; some third-party
  Modbus tools may display or require entering `N+1` for the same wire address.
- `sunspec_model_1_203.json` and `sunspec_model_1_213.json` are suitable for EVCC
  templates that consume generic SunSpec meter models, including `sunspec-meter`,
  `keba-kecontact`, `kostal-ksem`, and device-specific templates that fall back to
  model `203` or `213`.
- `janitza_604.json` targets the Janitza B604 series (e.g. UMG 604) register map
  and uses identifiers introduced in **FW 2.7.0** (`net.ip`, `11.7.0`,
  `energy.active`, `energy.reactive`, `energy.reactive.inductive`,
  `energy.reactive.capactive`).
- `janitza_604_old.json` is the legacy variant of the Janitza B604 template for
  firmware versions **before FW 2.7.0**. It uses a hardcoded `C_IP_ADDR` constant
  instead of `net.ip` and unnamed padding registers instead of the named energy
  identifiers added in FW 2.7.0.

## Implementation Notes

- The `carlo_gavazzi_em24_e1.json`, Huawei, Fronius, Herholdt, and SunSpec
  templates require **FW 2.0.2** or newer.
- The `janitza_604.json` template requires **FW 2.7.0** or newer, because it uses
  the `net.ip`, `11.7.0`, `energy.active`, `energy.reactive`,
  `energy.reactive.inductive`, and `energy.reactive.capactive` identifiers
  introduced in that version.
- The `janitza_604_old.json` template is compatible with firmware versions
  **before FW 2.7.0**. It uses a hardcoded `C_IP_ADDR` constant instead of `net.ip`
  and unnamed padding registers instead of the named energy identifiers.
- The EM24_E1 template follows the Carlo Gavazzi word order rule `LSW -> MSW` for
  32-bit values.
- The Huawei direct meter templates fix frequency at `50.00 Hz` and leave
  line-to-line voltages at `0`, because the internal report provides
  phase-to-neutral voltages but no dedicated line-voltage or frequency source for
  the Modbus slave.
- The Huawei SmartLogger and EMMA templates reuse the available import/export and
  per-phase power counters. Where Huawei publishes totals with no exact whatwatt
  Go equivalent, the template mirrors the closest available aggregate or keeps the
  field zero-filled.
- The Fronius template intentionally zero-fills most of the trailing Model `213`
  block, following the reference emulator behavior where the inverter primarily
  consumes live total and per-phase power values.
- The Herholdt template fixes register `4117` to floating-point mode. Herholdt's
  custom packed integer `N8` layout is not represented; each `N8` value is exposed
  as a `float32` value in the first two registers with the trailing two registers
  zero-filled. Named Herholdt measurements use `"scaler": 0`, because the internal
  report already stores values in the units used by the Herholdt table.
- Herholdt values are exposed in `kWh`, `kW`, `kvar`, `kVA`, `V`, `A`, and power
  factor ratio, matching the float-mode units in the vendor table.
- The Herholdt template fills the frequency register with a fixed `50.0 Hz`,
  because the current internal report has no live frequency source for the Modbus
  slave.
- Where the internal whatwatt Go report has no direct equivalent for a
  vendor-specific register, the template keeps that register present and fills it
  with `0`. This preserves contiguous address ranges expected by polling clients.
- The SunSpec templates expose values already available from the internal report,
  including voltages, per-phase currents, active/reactive/apparent power, power
  factor, imported/exported active energy, and reactive quadrant energies.

## Huawei Notes

Use one of the direct meter templates when the client expects the common Huawei
smart meter block at `37100`:

- `huawei_dtsu666_h.json` for three-phase DTSU666-H-style polling,
- `huawei_ddsu666_h.json` for single-phase DDSU666-H-style polling.

Use the SmartLogger or EMMA templates when the integration polls the higher-level
Huawei gateway register maps instead:

- `huawei_smartlogger_external_meter.json` exposes the external meter areas at
  `32260` and `32299`,
- `huawei_emma_external_meter.json` exposes the EMMA external meter area at
  `30500`.

Preview:

```json
--8<-- "35-modbus/examples/huawei_dtsu666_h.json"
```

## Fronius Notes

The Fronius template is designed for clients that probe a Fronius Smart Meter
63A-compatible endpoint. It uses a Fronius-specific SunSpec-like register layout
and includes static identification fields, live power values, and zero-filled
compatibility placeholders.

Preview:

```json
--8<-- "35-modbus/examples/fronius_smart_meter_63a.json"
```

## Herholdt M3PRO Notes

The Herholdt template follows the M1PRO/M3PRO register table with literal 0-based
Modbus addresses beginning at `4100`. The template is stored as one contiguous
register area so it remains compatible with the current parser, while preserving
the Herholdt register order.

Important register conventions:

- `4117` is fixed to `0`, selecting floating-point numeric encoding.
- `N4` fields from the Herholdt table are represented as 32-bit floats.
- `N8` fields are represented as 32-bit floats in the first two registers,
  followed by two zero-filled registers.
- Herholdt integer-mode scaling by `10000` does not apply to this template because
  the template selects float mode.

Preview:

```json
--8<-- "35-modbus/examples/herholdt_m3pro.json"
```

## SunSpec Notes

The SunSpec templates depend on features added in **FW 2.0.2**:

- area-level `constants`, used to publish static SunSpec metadata and placeholder
  values,
- `string` register type for the `SunS` identifier and Common Model text fields,
- detailed `GET /api/v1/modbus?address_format=dec|hex` output, useful when
  verifying the calculated register map,
- support for Modbus function **03** in addition to function **04**, which is
  required by standard SunSpec clients during model discovery.

The Model 203 template defines a single register area starting at address `0` and
contains:

1. The `SunS` identifier.
2. SunSpec **Model 1 (Common Model)**.
3. SunSpec **Model 203 (Wye-Connect Three Phase Meter)**.
4. The SunSpec end marker (`0xFFFF`, followed by length `0`).

Its `constants` object is used for manufacturer strings, model identifiers, scale
factors, placeholder values, and the final end marker.

Where a matching whatwatt Go measurement exists, the template maps it directly,
for example:

- `31.7.0`, `51.7.0`, `71.7.0` for phase currents,
- `32.7.0`, `52.7.0`, `72.7.0` for phase-to-neutral voltages,
- `power.active`, `power.active.l1`, `power.active.l2`, `power.active.l3` for
  active power,
- `power.reactive`, `power.reactive.l1`, `power.reactive.l2`, `power.reactive.l3`
  for reactive power,
- `9.7.0` for apparent power,
- `13.7.0` for power factor,
- `1.8.0`, `2.8.0`, `5.8.0`, `6.8.0`, `7.8.0`, `8.8.0` for selected energy
  counters.

Fields without a native whatwatt Go equivalent are filled with placeholder
constants such as `-32768` for `int16` and `sunssf`, or `0` for `acc32` and event
bitfields.

Preview:

```json
--8<-- "35-modbus/examples/sunspec_model_1_203.json"
```

## Janitza B604 Notes

The Janitza B604 templates emulate the register map of the Janitza B604 series
(e.g. UMG 604). Both templates define four register areas:

1. **Address 753** – two zero-filled `float` padding registers.
2. **Address 911** – one zero-filled `float` padding register.
3. **Address 10176** – device identification block with serial number, product
   number, Modbus address, and IP address, all as `int` registers.
4. **Address 19000** – main measurement block with voltages, currents, power
   values, and energy counters, all as `float` with `msw` word order.

### Key differences between the two templates

| Feature | `janitza_604.json` (FW 2.7.0+) | `janitza_604_old.json` (before FW 2.7.0) |
|---------|-------------------------------|------------------------------------------|
| IP address register | `net.ip` (live device IP) | `C_IP_ADDR` constant (hardcoded value) |
| Total current | `11.7.0` (unsigned sum) | unnamed padding register |
| Net active energy | `energy.active` | unnamed padding register |
| Net reactive energy | `energy.reactive` | unnamed padding register |
| Reactive energy inductive | `energy.reactive.inductive` | unnamed padding register |
| Reactive energy capacitive | `energy.reactive.capactive` | unnamed padding register |

The `janitza_604.json` template uses the `net.ip` identifier (available from
**FW 2.7.0**) to expose the live device IP address in the identification block at
address `10176`. The legacy `janitza_604_old.json` template instead defines a
`C_IP_ADDR` constant with a hardcoded IP value, because `net.ip` was not
available before FW 2.7.0.

Similarly, the `janitza_604.json` template uses named identifiers `11.7.0`,
`energy.active`, `energy.reactive`, `energy.reactive.inductive`, and
`energy.reactive.capactive` (all available from **FW 2.7.0**) for the
corresponding measurement registers in the main block at address `19000`. The
legacy template uses unnamed padding registers (`{"type": "float"}` without an
`id`) in those positions, because the named identifiers were not available.

Both templates define a `GRID_FREQUENCY_50HZ` constant set to `50` and expose it
as a `float` register, because the internal report has no live frequency source
for the Modbus slave.

Preview (FW 2.7.0+):

```json
--8<-- "35-modbus/examples/janitza_604.json"
```

Preview (before FW 2.7.0):

```json
--8<-- "35-modbus/examples/janitza_604_old.json"
```

## Applying a Template

To load any template into `/api/v1/modbus`, post the chosen JSON file directly:

```bash
curl -i -H 'Content-Type: application/json' \
  --data-binary @template.json \
  http://<whatwattGoIP>/api/v1/modbus
```

To inspect the resulting calculated addresses and register sizes:

```bash
curl -s 'http://<whatwattGoIP>/api/v1/modbus?address_format=dec'
```

Any SunSpec client that supports Modbus TCP discovery can be used to validate
SunSpec templates. [`pySunSpec2`](https://github.com/sunspec/pysunspec2) is one
external option.
