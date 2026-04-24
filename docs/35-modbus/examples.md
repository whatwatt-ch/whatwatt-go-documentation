# Modbus Example Configurations

This page collects ready-to-load Modbus slave templates that let whatwatt Go emulate several common power meters.

All example JSON files live in the local `examples` directory next to this page.

## Available Templates

- [siemens_pac2200.json](examples/siemens_pac2200.json) - Siemens PAC2200-compatible layout. This matches the default firmware layout used when no custom Modbus configuration is stored.
- [carlo_gavazzi_em24_e1.json](examples/carlo_gavazzi_em24_e1.json) - Carlo Gavazzi EM24_E1-compatible layout with `lsw` word order for 32-bit values.
- [sunspec_model_1_203.json](examples/sunspec_model_1_203.json) - SunSpec Common Model 1 plus meter Model 203 using `int16` and `int32` values with scale factors.
- [sunspec_model_1_213.json](examples/sunspec_model_1_213.json) - SunSpec Common Model 1 plus meter Model 213 using `float32` values.

## Compatibility Notes

- `siemens_pac2200.json` matches the EVCC `siemens-pac2200` and MBMD `pac2200` paths.
- `carlo_gavazzi_em24_e1.json` is aimed at EVCC `cg-em24_e1` and MBMD `cgem24_e1`.
- `sunspec_model_1_203.json` and `sunspec_model_1_213.json` are suitable for EVCC templates that consume generic SunSpec meter models, including `sunspec-meter`, `keba-kecontact`, `kostal-ksem`, and device-specific templates that fall back to model `203` or `213`.

## Implementation Notes

- The `carlo_gavazzi_em24_e1.json`, `sunspec_model_1_203.json`, and `sunspec_model_1_213.json` templates require **FW 2.0.2** or newer.
- The EM24_E1 template follows the Carlo Gavazzi word order rule `LSW -> MSW` for 32-bit values.
- Where the internal whatwatt Go report has no direct equivalent for a vendor-specific register, the template keeps that register present and fills it with `0`. This preserves contiguous address ranges expected by polling clients.
- The SunSpec templates expose values already available from the internal report, including voltages, per-phase currents, active/reactive/apparent power, power factor, imported/exported active energy, and reactive quadrant energies.

## SunSpec Notes

The SunSpec templates depend on features added in **FW 2.0.2**:

- area-level `constants`, used to publish static SunSpec metadata and placeholder values,
- `string` register type for the `SunS` identifier and Common Model text fields,
- detailed `GET /api/v1/modbus?address_format=dec|hex` output, useful when verifying the calculated register map,
- support for Modbus function **03** in addition to function **04**, which is required by standard SunSpec clients during model discovery.

The Model 203 template defines a single register area starting at address `0` and contains:

1. The `SunS` identifier.
2. SunSpec **Model 1 (Common Model)**.
3. SunSpec **Model 203 (Wye-Connect Three Phase Meter)**.
4. The SunSpec end marker (`0xFFFF`, followed by length `0`).

Its `constants` object is used for manufacturer strings, model identifiers, scale factors, placeholder values, and the final end marker.

Where a matching whatwatt Go measurement exists, the template maps it directly, for example:

- `31.7.0`, `51.7.0`, `71.7.0` for phase currents,
- `32.7.0`, `52.7.0`, `72.7.0` for phase-to-neutral voltages,
- `power.active`, `power.active.l1`, `power.active.l2`, `power.active.l3` for active power,
- `power.reactive`, `power.reactive.l1`, `power.reactive.l2`, `power.reactive.l3` for reactive power,
- `9.7.0` for apparent power,
- `13.7.0` for power factor,
- `1.8.0`, `2.8.0`, `5.8.0`, `6.8.0`, `7.8.0`, `8.8.0` for selected energy counters.

Fields without a native whatwatt Go equivalent are filled with placeholder constants such as `-32768` for `int16` and `sunssf`, or `0` for `acc32` and event bitfields.

Preview:

```json
--8<-- "35-modbus/examples/sunspec_model_1_203.json"
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

Any SunSpec client that supports Modbus TCP discovery can be used to validate SunSpec templates. [`pySunSpec2`](https://github.com/sunspec/pysunspec2) is one external option.
