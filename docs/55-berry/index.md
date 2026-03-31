# Berry integration in whatwatt Go

The **whatwatt go** device offers a built-in **Berry v1.1** script interpreter. This allows users to create and run their own automation scenarios, respond to meter events, integrate additional devices, and publish data to external systems – all without an external server or firmware recompilation.

## Purpose of This Manual

- comprehensive documentation of the `ww` module, which extends the pure Berry API with whatwatt go-specific functions,
- practical examples of configuration and usage for each interface (timers, reports, Modbus, HTTP, local REST API),
- debugging tips and best practices for performance and security.

The document is intended for integrators, administrators, and advanced users who want to fully leverage the device's capabilities. Minimal knowledge of the Berry language is required.

## Manual Structure

1. **Documentation Conventions** – rules for writing signatures and types.
2. **Module Features** – overview of timers, report events, Modbus/HTTP clients, and local REST.
3. **Management Interfaces** – REST API for remote script control and the graphical editor embedded in the main Web UI.

## Documentation Conventions

This manual uses the following conventions for function signatures:

- Monospace signature — `name(param: type = default) -> return_type | nil`.
- Parameter names and types in English (`int`, `real`, `string`, `map`, `list`, `bool`).
- Optional parameters are marked with `?` or the column "Required = no".
- Enumerated values are enclosed in braces `{val1, val2}`, and ranges are given as `min‑max`.
- Default values are given after `=` both in the signature and in the parameter table.
- Return types and `nil` are described in the **Return Value** section.
- Code examples are provided in `berry` code blocks.

## Features

Below is a list of available functions in the `ww` module with brief descriptions:

The **whatwatt** firmware introduces a system `ww` module alongside the standard **Berry** libraries. This module is loaded with a single command:

```berry
import ww
```

`ww` acts as a **bridge** between the script and the firmware API layer, providing convenient, high-level access to network services and the device's own resources. It can be divided into three main categories:

1. **Event and timer functions** – respond to periodic clock ticks or the arrival of a new energy report (`ontimer`, `onreport`). This makes it easy to implement schedules (e.g., send data every 60 s) or event-based logic (e.g., power exceeded > 3 kW → send notification).
2. **External protocol clients** – a unified interface for **Modbus TCP** and **HTTP(S)** allows you to read or write data on other devices, in the cloud, or via a REST broker, without manually implementing TCP socket handling.
3. **Access to local REST API** – allows you to configure or query the whatwatt device directly from Berry, as if you were making `curl` requests to `/api/v1/...`, but without network overhead.

Thanks to this, the `ww` module extends the capabilities of pure Berry with true **automation** and **IoT integration** features – from simple energy consumption counting to controlling an external PV inverter.

### The table below summarizes the key capabilities of the `ww` module

| Functionality              | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| Timer Event                | Allows cyclic invocation of a function in the script, for tasks requiring periodic execution. |
| Report Event               | Allows you to assign a function that is called whenever a new report is created. |
| Modbus TCP Master (Client) | Modbus client operating as a master, enabling remote reading and writing of registers in a Modbus TCP Slave device. |
| HTTP(S) client             | Client enabling remote execution of HTTP(S) requests and receiving responses. |
| Local REST API             | Allows reading and writing to the local REST API from within Berry. |

> **Important**
>
> All network calls provided by the `ww` module — `ww.modreq` (Modbus TCP), `ww.httpreq` (HTTP/HTTPS), and local REST API operations (`ww.apiget`, `ww.apiset`, `ww.apidel`) — operate **synchronously**. The Berry interpreter **blocks** until a response is received or the `timeout` expires.
>
> - When designing timer-based logic, ensure that the execution time of a single request is shorter than the timer interval, so that subsequent calls do not overlap.
> - Avoid custom blocking loops (`while true …`) — the script should react to **events** delivered by `ontimer` or `onreport`, ensuring predictability and resource efficiency.
> - Check return values to avoid script interruption and/or use exception handling structures `try-except`.

### Timer event

Allows cyclic invocation of a function in the script, for tasks requiring periodic execution.

**Signature:** `ww.ontimer(name: string, interval: int) -> bool | nil`

The first parameter specifies the name of the function to be called in the script; the function must be in the global scope, and the name must be a 1-31 character string. The second parameter specifies the call interval in seconds. The timer operates in repeat mode; to disable it, call the same function with the `interval` parameter set to `0`.

You can register up to **10** independent timers at the same time; attempting to set an eleventh will return `nil`. Calling with `interval` = `0` removes the timer and frees its slot for reuse.

The timer call does not pass any parameters to the called function.

**Return Value:**

- `true` – the timer was successfully set or disabled.
- `false` - when canceling a timer by setting the value to 0, no timer was found.
- `nil` – invalid arguments, values out of the allowed range (e.g., name length not within 1‑31 characters, `interval` < 0) **or the limit of 10 timers was exceeded**.

Example

```python
# timer example

import ww

count = 0

def on_timer()
    print('Tick')
    count += 1
    if count >= 3
        ww.ontimer('on_timer', 0)
        print('Stop')
    end
end

ww.ontimer('on_timer', 2)
```

### Report event

Allows you to assign a function that is called whenever a new report is created.

**Signature:** `ww.onreport(name: string) -> nil`

The argument specifies the name of the function to be called on the report event; the function must be in the global scope, and the name must be a 1-31 character string. To disable the callback, call `ww.onreport(nil)`.

The report event call passes the report to the called function as a map with the following structure:

| Field                                                       | Type   | Description                                          |
| ----------------------------------------------------------- | ------ | ---------------------------------------------------- |
| `['id']`                                                    | int    | Report identifier, incremented with each new report. |
| `['interval']`                                              | real   | Period in seconds at which reports are received.     |
| `['tariff']`                                                | int    | Tariff. 0 – unknown, 1 – T1, 2 – T2.                 |
| `['date_time']`                                             | string | Date and time of report arrival in ISO 8601 format.  |
| `['timestamp']`                                             | int    | Report arrival time as UTC timestamp.                |
| `['power']`                                                 | map    | Map containing power elements.                       |
| `['power']['active']`                                       | map    | Active power.                                        |
| `['power']['active']['positive']`                           | map    | Positive active power.                               |
| `['power']['active']['positive']['total']`                  | real   | Total positive active power of all phases.           |
| `['power']['active']['positive']['l1']`                     | real   | Positive active power of phase L1.                   |
| `['power']['active']['positive']['l2']`                     | real   | Positive active power of phase L2.                   |
| `['power']['active']['positive']['l3']`                     | real   | Positive active power of phase L3.                   |
| `['power']['active']['negative']`                           | map    | Negative active power.                               |
| `['power']['active']['negative']['total']`                  | real   | Total negative active power of all phases.           |
| `['power']['active']['negative']['l1']`                     | real   | Negative active power of phase L1.                   |
| `['power']['active']['negative']['l2']`                     | real   | Negative active power of phase L2.                   |
| `['power']['active']['negative']['l3']`                     | real   | Negative active power of phase L3.                   |
| `['power']['reactive']`                                     | map    | Reactive power.                                      |
| `['power']['reactive']['positive']`                         | map    | Positive reactive power.                             |
| `['power']['reactive']['positive']['total']`                | real   | Total positive reactive power of all phases.         |
| `['power']['reactive']['positive']['l1']`                   | real   | Positive reactive power of phase L1.                 |
| `['power']['reactive']['positive']['l2']`                   | real   | Positive reactive power of phase L2.                 |
| `['power']['reactive']['positive']['l3']`                   | real   | Positive reactive power of phase L3.                 |
| `['power']['reactive']['negative']`                         | map    | Negative reactive power.                             |
| `['power']['reactive']['negative']['total']`                | real   | Total negative reactive power of all phases.         |
| `['power']['reactive']['negative']['l1']`                   | real   | Negative reactive power of phase L1.                 |
| `['power']['reactive']['negative']['l2']`                   | real   | Negative reactive power of phase L2.                 |
| `['power']['reactive']['negative']['l3']`                   | real   | Negative reactive power of phase L3.                 |
| `['power']['apparent']`                                     | map    | Apparent power.                                      |
| `['power']['apparent']['total']`                            | real   | Total apparent power of all phases.                  |
| `['voltage']`                                               | map    | Phase voltages.                                      |
| `['voltage']['l1']`                                         | real   | Voltage of phase L1.                                 |
| `['voltage']['l2']`                                         | real   | Voltage of phase L2.                                 |
| `['voltage']['l3']`                                         | real   | Voltage of phase L3.                                 |
| `['current']`                                               | map    | Phase currents.                                      |
| `['current']['l1']`                                         | real   | Current of phase L1.                                 |
| `['current']['l2']`                                         | real   | Current of phase L2.                                 |
| `['current']['l3']`                                         | real   | Current of phase L3.                                 |
| `['energy']`                                                | map    | Energy.                                              |
| `['energy']['active']`                                      | map    | Active energy.                                       |
| `['energy']['active']['positive']`                          | map    | Positive active energy.                              |
| `['energy']['active']['positive']['total']`                 | real   | Total positive active energy.                        |
| `['energy']['active']['positive']['t1']`                    | real   | Positive active energy for tariff T1.                |
| `['energy']['active']['positive']['t2']`                    | real   | Positive active energy for tariff T2.                |
| `['energy']['active']['negative']`                          | map    | Negative active energy.                              |
| `['energy']['active']['negative']['total']`                 | real   | Total negative active energy.                        |
| `['energy']['active']['negative']['t1']`                    | real   | Negative active energy for tariff T1.                |
| `['energy']['active']['negative']['t2']`                    | real   | Negative active energy for tariff T2.                |
| `['energy']['reactive']`                                    | map    | Reactive energy.                                     |
| `['energy']['reactive']['imported']`                        | map    | Imported reactive energy.                            |
| `['energy']['reactive']['imported']['inductive']`           | map    | Inductive imported reactive energy.                  |
| `['energy']['reactive']['imported']['inductive']['total']`  | real   | Total inductive imported reactive energy.            |
| `['energy']['reactive']['imported']['inductive']['t1']`     | real   | Inductive imported reactive energy for T1.           |

---

#### Usage Example

```python
# on report example

import ww

def on_report(report)
  print(report)
end

ww.onreport('on_report')
```

Result

```...
{'id': 625, 'voltage': {'l3': 0, 'l1': 232, 'l2': 0}, 'timestamp': 1750589320, 'tariff': 0, 'power_factor': nil, 'current': {'l3': 0, 'l1': 0.09, 'l2': 0}, 'power': {'apparent': {'total': nil}, 'reactive': {'positive': {'l3': nil, 'total': 0, 'l1': nil, 'l2': nil}, 'negative': {'l3': nil, 'total': 0.018, 'l1': nil, 'l2': nil}}, 'active': {'positive': {'l3': nil, 'total': 0.011, 'l1': nil, 'l2': nil}, 'negative': {'l3': nil, 'total': 0, 'l1': nil, 'l2': nil}}}, 'conv_factor': 1, 'interval': 10.045, 'max_demand': {'active': {'positive': {'total': nil, 't1': nil, 't2': nil}, 'negative': {'total': nil, 't1': nil, 't2': nil}}}, 'energy': {'reactive': {'exported': {'inductive': {'total': nil, 't1': nil, 't2': nil}, 'capacitive': {'total': nil, 't1': nil, 't2': nil}}, 'imported': {'inductive': {'total': nil, 't1': nil, 't2': nil}, 'capacitive': {'total': nil, 't1': nil, 't2': nil}}}, 'active': {'positive': {'total': 1.165, 't1': nil, 't2': nil}, 'negative': {'total': 0, 't1': nil, 't2': nil}}}, 'date_time': '2025-06-22T12:48:40Z'}
```

## Modbus TCP Master – `ww.modreq`

A Modbus client operating as a master, enabling remote reading and writing of registers in a Modbus TCP Slave device.

**Signature:** `ww.modreq(request: map) -> map | nil`

The `ww.modreq` function allows you to send synchronous **Modbus TCP Master** requests from Berry. The call is blocking; if the `timeout` parameter (default 5 s) is exceeded, an error is reported.

From **FW 2.0.2**, `ww.modreq` additionally supports the `word_order` field for multi-register numeric types, and for read functions `3` and `4` the `count` field is interpreted as the number of typed values rather than the number of raw 16-bit registers.

### modreq map fields

| Key       | Type                      | Range                                                   | Required         | Default value   | Description                                                        |
| --------- | ------------------------ | ------------------------------------------------------- | --------------- | -------------- | ------------------------------------------------------------------ |
| `host`    | string                   | 4..63                                                   | yes              | —              | IP address/FQDN of the Modbus TCP server (slave).                          |
| `port`    | int                      | 1..65535                                                | no               | 502            | TCP port of the device.                                            |
| `unit_id` | int                      | 0..255                                                  | no               | 0              | Unit identifier. This is important for concentrators.                                      |
| `func`    | int                      | 1..6,15,16                                              | yes              | —              | Function code.                                  |
| `address` | int                      | 0..65535                                                | no               | 0              | Address of the first coil/register. For multi-register numeric types, this is the address of the first register of the first value.                                |
| `type`    | string                   | hex, short, int, long, float, double | no               | hex            | Data format: `hex`, `short`, `int`, `long`, `float`, `double`.     |
| `word_order` | string                | msw, lsw                                                | no               | msw            | Available from **FW 2.0.2**. Word order for multi-register numeric types (`int`, `long`, `float`, `double`). Byte order inside each 16-bit register remains Modbus Big-Endian. |
| `count`   | int                      | 1..2000 (func 1/2), 1..125 (`hex`/`short`), 1..62 (`int`/`float`), 1..31 (`long`/`double`) | yes: for read    | —             | For func `1`/`2`: number of bits. For func `3`/`4`: number of values of the selected `type`, not raw 16-bit registers. Effective register span equals `count × type register width`.            |
| `value`   | int, real or hex string  |                                                         | yes: for write   | —              | Single numeric value or hex string. The effective number of written registers is derived from the selected `type` for numeric values or from the byte length of the hex string. |
| `timeout` | real                     | 0.1..5                                                  | no               | 5              | Request timeout.                                                   |

### List of Modbus functions supported by `ww.modreq`

| Code | Name                     | Direction | Description                      |
| ---- | ------------------------ | --------- | -------------------------------- |
|  1   | Read Coils               |  R        | Read multiple coils.             |
|  2   | Read Discrete Inputs     |  R        | Read discrete inputs.            |
|  3   | Read Holding Registers   |  R        | Read Holding registers.          |
|  4   | Read Input Registers     |  R        | Read Input registers.            |
|  5   | Write Single Coil        |  W        | Write a single coil.             |
|  6   | Write Single Register    |  W        | Write a single register.         |
|  15  | Write Multiple Coils     |  W        | Write multiple coils.            |
|  16  | Write Multiple Registers |  W        | Write multiple registers.        |

### Data formats (`type`)

Data is always transmitted in Big-Endian byte order inside each 16-bit Modbus register.

From **FW 2.0.2**, for multi-register numeric types (`int`, `long`, `float`, `double`), the request can additionally define `word_order`:

- `msw` - most significant word first; default behavior,
- `lsw` - least significant word first.

From **FW 2.0.2**, for read functions `3` and `4`, the `count` field specifies the number of typed values, not the number of raw 16-bit registers. This also affects the address span covered by the request:

- `type: 'short'`, `count: 4` reads 4 registers, so for `address: 0` the request covers registers `0..3`,
- `type: 'float'`, `count: 4` reads 4 float values = 8 registers, so for `address: 0` the request covers registers `0..7`,
- `type: 'double'`, `count: 4` reads 4 double values = 16 registers, so for `address: 0` the request covers registers `0..15`.

| Type     | Registers |
| -------- | --------- |
| `hex`    | 1         |
| `short`  | 1         |
| `int`    | 2         |
| `long`   | 4         |
| `float`  | 2         |
| `double` | 4         |

### Response structure

| Key        | Returned Type                                                | Description                         |
| ---------- | ----------------------------------------------------------- | ----------------------------------- |
| `code`     | int                                                         | Numeric status of the request       |
| `code_str` | string                                                      | Text status of the request          |
| `data`     | list of int, real or byte array or nil for write operations | Data returned by the read operation |

> **Important**
>
> As you may have noticed, the write value can be passed as a `string` type in `hex` notation, but the response may be passed as a special `bytes array` data type.

### Return value

- **Read:** `{'code': 1, 'data': [list], 'code_str': 'OK'}`
- **Write:** `{'code': 1, 'data': nil, 'code_str': 'OK'}`

If `code < 0`, the operation failed—details are in the `code_str` field.

### Error code mapping (`code < 0`)

| Code  | Description                             |
| ---- | --------------------------------------- |
|  ‑1  | INVALID ARG                             |
|  ‑2  | READ BUFFER OVERFLOW                    |
|  ‑3  | READ TIMEOUT                            |
|  ‑4  | READ ERROR                              |
|  ‑5  | INVALID READ PDU LEN                    |
|  ‑6  | CANNOT CREATE REQUEST FRAME             |
|  ‑7  | WRITE ERROR                             |
|  ‑8  | INVALID HEADER                          |
|  ‑9  | TRANSACTION MISMATCH                    |
| ‑10  | FUNCTION MISMATCH                       |
| ‑11  | INVALID EXCEPTION FRAME                 |
| ‑12  | UNIT ID MISMATCH                        |
| ‑13  | RESPONSE FRAME TOO SHORT                |
| ‑14  | BODY MISMATCH                           |
| ‑15  | CANNOT PROCESS RESPONSE                 |
| ‑16  | CANNOT RESOLVE HOST                     |
| ‑17  | CANNOT CONNECT                          |
| ‑18  | TLS HANDSHAKE ERROR                     |
| ‑19  | CANNOT CREATE CONNECTION                |
| ‑20  | INVALID CONTENT LENGTH                  |
| ‑21  | FUNCTION NOT SUPPORTED                  |
| ‑100 | EXCEPTION BASE                          |
| ‑101 | ILLEGAL FUNCTION                        |
| ‑102 | ILLEGAL DATA ADDRESS                    |
| ‑103 | ILLEGAL DATA VALUE                      |
| ‑104 | SLAVE DEVICE FAILURE                    |
| ‑105 | ACKNOWLEDGE                             |
| ‑106 | SLAVE DEVICE BUSY                       |
| ‑107 | NEGATIVE ACKNOWLEDGE                    |
| ‑108 | MEMORY PARITY ERROR                     |
| ‑109 | UNKNOWN                                 |
| ‑110 | GATEWAY PATH UNAVAILABLE                |
| ‑111 | GATEWAY TARGET DEVICE FAILED TO RESPOND |

### Usage examples

#### Read Coils or Read Discrete Inputs

```python
# modbus read coils - func 1

import ww

MB_SRV_HOST = '192.168.99.100'
MB_SRV_PORT = 1502

read_req = {
  'host': MB_SRV_HOST,
  'port': MB_SRV_PORT,
  'unit_id': 0,
  'func': 1, # for read discrete inputs use 2
  'address': 0, # start from coil 0
  'type': 'hex',
  'timeout': 2,
  'count': 16 # read 16 coils/bits
}

resp = ww.modreq(read_req)
print(resp)
```

Result

```...
{'code': 1, 'data': bytes('0C05'), 'code_str': 'OK'}
```

##### Read Multiple Holding Registers or Read Input Registers

```python
# modbus read multiple holding registers

import ww

MB_SRV_HOST = '192.168.99.100'
MB_SRV_PORT = 1502

read_req = {
  'host': MB_SRV_HOST,
  'port': MB_SRV_PORT,
  'unit_id': 0,
  'func': 3, # in case of read input registers use 4
  'address': 0, # first register of the first value
  'type': 'short', # natural form
  'timeout': 2,
  'count': 4 # read 4 values of type 'short', covering registers 0..3
}

resp = ww.modreq(read_req)
print(resp)
```

Result

```...
{'code': 1, 'data': [1000, 200, 30, 4], 'code_str': 'OK'}
```

From **FW 2.0.2**, if the same request used `type: 'float'` and `count: 4`, it would read 4 float values spanning registers `0..7`. For `type: 'double'`, `count: 4` would span registers `0..15`.

##### Write Single Coil

```python
# modbus write single coil

import ww

MB_SRV_HOST = '192.168.99.100'
MB_SRV_PORT = 1502

write_req = {
  'host': MB_SRV_HOST,
  'port': MB_SRV_PORT,
  'unit_id': 0,
  'func': 5,
  'address': 0,
  'type': 'hex',
  'timeout': 2,
  'value': 'FF00' # turn on coil, to off use 0000
}
resp = ww.modreq(write_req)
print(resp)
```

##### Write Single Holding Register

```python
# modbus write single holding register

import ww

MB_SRV_HOST = '192.168.99.100'
MB_SRV_PORT = 1502

write_req = {
  'host': MB_SRV_HOST,
  'port': MB_SRV_PORT,
  'unit_id': 0,
  'func': 6,
  'address': 0,
  'type': 'short',
  'timeout': 2,
  'value': 12345
}
resp = ww.modreq(write_req)
print(resp)
```

Result

```...
{'code': 1, 'data': nil, 'code_str': 'OK'}
```

##### Write Multiple Coils

```python
# modbus write multiple coils

import ww

MB_SRV_HOST = '192.168.99.100'
MB_SRV_PORT = 1502

write_req = {
  'host': MB_SRV_HOST,
  'port': MB_SRV_PORT,
  'unit_id': 0,
  'func': 15,
  'address': 0,
  'type': 'hex',
  'timeout': 2,
  'value': '5555' # set even coils to 1, odd to 0
}
resp = ww.modreq(write_req)
print(resp)
```

##### Write Multiple Holding Registers

```python
# modbus write multiple holding registers

import ww

MB_SRV_HOST = '192.168.99.100'
MB_SRV_PORT = 1502

write_req = {
  'host': MB_SRV_HOST,
  'port': MB_SRV_PORT,
  'unit_id': 0,
  'func': 16, # write multiple holding registers
  'address': 0,
  'type': 'hex',
  'timeout': 2,
  'value': '0001000200030004' # registers to values 1, 2, 3, 4
}
resp = ww.modreq(write_req)
print(resp)
```

From **FW 2.0.2**, for multi-register numeric writes, `word_order` can also be provided, for example with `type: 'float'` or `type: 'double'`, to match the target device's expected register word order.

Example: when writing a single `float` value with `func: 16`, `type: 'float'`, `address: 100`, and `word_order: 'lsw'`, the request still starts at register `100`, but the two 16-bit words of that float are sent in LSW-first order.

---

## HTTP(S) client – `ww.httpreq`

A client enabling remote execution of HTTP(S) requests and receiving responses.

**Signature:** `ww.httpreq(request: map) -> map | nil`

The `ww.httpreq` function allows you to perform synchronous **HTTP/HTTPS** requests from Berry. The call is blocking; if the `timeout` parameter (default 5 s) is exceeded, the function returns code `0` or `nil`.

### httpreq map fields

| Key       | Type                 | Range                                     | Required | Default value | Description                                                        |
| --------- | ------------------- | ------------------------------------------ | -------- | ------------- | ------------------------------------------------------------------ |
| `url`     | string              | 8..255                                     | yes      | —             | Full URL (protocols `http://` or `https://`). May contain port, username and password.                      |
| `method`  | string              | `GET`, `POST`, `PUT`, `DELETE` | no       | `GET`         | HTTP method. Case insensitive.                                     |
| `payload` | string              | *                                          | no       | —             | Request body for methods that accept data (`POST`, `PUT`).         |
| `timeout` | real                | 0.1..5                                     | no       | 5             | Request timeout.                                                   |
| `headers` | map<string,string>  |                                            | no       | —             | Additional headers sent with the request. Header names are case-insensitive. |

> **Important**
>
> - If the `request` field contains invalid syntax or an unsupported parameter, the function returns `nil`.
> - The `payload` parameter is passed as-is; conversion (e.g., `json.dump`) should be done in the script.
> - The `Content-Type` header for the request must be provided in `headers` if required by the server.
> - The `Authorization` header e.g., `Bearer` ... must be provided manually.
> - The client supports Basic and Digest authentication via URL credentials; use `http(s)://user:password@host/...`
> - If the server requires Basic authentication, add the header and omit `user:password` from the URL.

**Return value:**

The function returns a **map** with the following structure or `nil`:

| Field           | Type    | Description                                                        |
| --------------  | ------  | ------------------------------------------------------------------ |
| `code`          | int     | `0` – timeout exceeded, TLS/connection transport error; otherwise, standard HTTP code (200, 404, ...). |
| `content_type`  | string  | Value of the response `Content-Type` header or empty string if absent. |
| `content`       | string  | Response body; empty string if absent.   |

#### Simple report reading from myStrom wifi switch

```python
# http client example fetch mystrom switch report

import ww
import json
import string

MY_SWITCH_API = "http://192.168.99.188/"

do
  req = {
        'url': MY_SWITCH_API .. "/report"
  }
  resp = ww.httpreq(req)
    body = json.load(resp['content'])
    for k: body.keys()
      print(k .. ": " .. body[k])
  end
end
```

Result

```...
time_since_boot: 5710154
energy_since_boot: 2.36496e+08
relay: true
boot_id: BE8BFEAD
time: 2025-07-01T18:49:19Z
temperature: 26.56
power: 4.26
Ws: 4.6
```

#### Usage example - reading/changing Shelly output state

```python
# shelly example

import ww
import json
import string

SHELLY_API = "http://192.168.99.127/rpc/"

def http_resp_to_json(resp)
  if resp != nil && isinstance(resp, map) && resp['code'] == 200 &&
        string.find(resp['content_type'], "application/json") != nil &&
      resp['content'] != nil
        return json.load(resp['content'])
  end
end

def get_switch_status(id)
  req = {
    'url': SHELLY_API .. "Switch.GetStatus?id=" .. id,
    'method': "GET" # by default is get
  }
  return http_resp_to_json(ww.httpreq(req))
end

def set_switch_output(id, on)
  req = {
        'url': SHELLY_API .. "Switch.Set?id=" .. id .. "&on=" .. bool(on),
        'method': "GET"
  }
  return http_resp_to_json(ww.httpreq(req))
end

def test()
  resp = get_switch_status(0)
  if resp != nil
    print("Power: " .. resp['apower'] .. "W, on: " .. resp['output'])
  end
  resp = set_switch_output(0, 0)
  if resp != nil
    print("On: " .. resp['was_on'])
  end
end

test()
```

> **Tip**
>
> - String concatenation in Berry is done using the `..` operator, so you don't need to explicitly convert types like numbers to `string`.
> - It doesn't matter whether you enclose the string in single `'` or double `"` quotes, e.g., the convention adopted here is to use single quotes in map key names, or if you're writing a JSON string.

#### Usage example – changing Shelly output state with POST method

```python
# shelly post request example

import ww
import json
import string

SHELLY_API = "http://192.168.99.127/rpc/"

def http_resp_to_json(resp)
  if resp != nil && isinstance(resp, map) && resp['code'] == 200 &&
    string.find(resp['content_type'], "application/json") != nil &&
    resp['content'] != nil
      return json.load(resp['content'])
  end
end

def set_switch_output(id, on)
  req_json = {
    'id': 1,
    'method': "Switch.Set",
    'params': {
      'id': int(id),
      'on': bool(on)
    }
  }
  req = {
    'url': SHELLY_API,
    'method': "POST",
    'payload': json.dump(req_json)
  }
  return http_resp_to_json(ww.httpreq(req))
end

def set_relay(on)
  resp = set_switch_output(0, on)
  # check if nil etc. here
  print("Realy: " .. resp['result']['was_on'])
end

set_relay(0)
set_relay(1)
set_relay(0)
```

> **Tip**
>
> - Check `code` and `content_type` — this allows you to filter HTML responses where JSON is expected.
> - Set `timeout` as short as possible (1–3 s) for local connections to avoid blocking the Berry thread.
> - Place variables in functions or blocks (`do-end`) to avoid cluttering memory.

---

## Local REST API – `ww.apiget`, `ww.apiset`, `ww.apidel`

The `ww` module provides a simplified interface to the internal REST API of the **whatwatt** device. Operations are performed exclusively at the address `http://localhost/api/v1/...` – in the script, you provide **only the path** without the `api/v1` prefix.

> **General convention** — if any of the function parameters are passed in an incorrect format or range, the function returns `nil`.

### `ww.apiget`

**Signature:** `ww.apiget(path: string) -> map | nil`

- **HTTP method**: `GET`
- **Parameters**: `path` – resource path (without `api/v1`), e.g. `"report"`, `"meter/settings"`.
- **Returns**: map resulting from decoding the server's JSON response.

**Example: reading a report:**

```python
# local api get

import ww

resp = ww.apiget('report')
print(resp)
```

**Result:**

```...
{'system': {'id': '000000000000', 'boot_id': '303A0B39', 'time_since_boot': 1925686, 'date_time': '2025-07-01T17:31:32Z'}, 'meter': {'interface': 'P1', 'status': 'OK', 'model': '6841131BN240101065', 'protocol': 'DLMS', 'logical_name': 'Kamstrup_V0001', 'id': '5706567368531468'}, 'report': {'id': 567, 'conv_factor': 1, 'current': {'l3': 0, 'l1': 0.09, 'l2': 0}, 'date_time': '2025-06-22T12:39:00Z', 'energy': {'reactive': {'positive': {'total': 0}, 'negative': {'total': 1.499}}, 'active': {'positive': {'total': 1.165}, 'negative': {'total': 0}}}, 'voltage': {'l3': 0, 'l1': 232, 'l2': 0}, 'instantaneous_power': {'reactive': {'positive': {'total': 0}, 'negative': {'total': 0.018}}, 'active': {'positive': {'total': 0.011}, 'negative': {'total': 0}}}, 'interval': 10.066}}
```

### `ww.apiset`

**Signature:** `ww.apiset(path: string, payload: map) -> map | nil`

- **HTTP method**: `PUT`
- **Parameters**:
  - `path` – resource path to modify,
  - `payload` – map, which after internal serialization to JSON **must** match the local API specification.
- **Returns**: response map (if the operation succeeds) or `nil` (invalid data format/range).

**Example: changing device name:**

```python
# local api set

import ww

resp = ww.apiset('settings', {'system':{'name': 'My'}})
print(resp)
resp = ww.apiget('settings')
print(resp['system']['name'])
```

**Result:**

```...
true
My
```

> **Important**
>
> - **Validate data** before passing to `ww.apiset`; the device will return `nil` if the JSON after conversion does not match the API schema.
> - Treat responses from `ww.apiget`/`ww.apiset` as the source of truth – the server may correct or supplement data (e.g., default values).

---

## REST API for Berry script management – `/api/v1/berry`

The **HTTP REST** interface allows remote management of the Berry script stored and run on the whatwatt device.

> All the following operations are performed on the device host, e.g. `http://192.168.99.50/api/v1/berry`.

### Endpoint summary

| Method   | Endpoint                | Request body         | Response body                        | Success code | Short description                              |
| -------- | ----------------------- | -------------------- | ------------------------------------- | ------------ | ---------------------------------------------- |
| `GET`    | `/api/v1/berry`         | —                    | `text/plain` (script source)          | `200` / `404`| Download the current script.                   |
| `POST`   | `/api/v1/berry`         | `text/plain` < 8 kB  | `text/plain` (saved script)           | `200`        | Save or overwrite the script (no restart).     |
| `PUT`    | `/api/v1/berry?[run=…]` | —                    | `application/json` `{"run":bool}`   | `200`        | Read status or start/stop the script.          |
| `DELETE` | `/api/v1/berry`         | —                    | —                                     | `204`        | Delete the script (no stop).                   |

### Detailed behavior

#### `GET /api/v1/berry`

- Returns the current script as `text/plain`.
- If the script does not exist, the server returns `404 Not Found`.

#### `POST /api/v1/berry`

- The request body must contain the full Berry script.
- Maximum content size: **8191 B**.
- On success, the server returns `200 OK` and the same script in the body.
- This operation **does not stop** the currently running script or start the new version.

#### `PUT /api/v1/berry?[run=true|false]`

- Without the `run` parameter – responds with JSON `{"run": bool}` indicating whether the Berry interpreter is active.
- With `run=true` – starts the script (if it exists); responds with `{"run": true}`.
- With `run=false` – stops the running script; responds with `{"run": false}`.
- Idempotent: repeated calls with the same state do not cause an error.

#### `DELETE /api/v1/berry`

- Deletes the saved script; does not stop it if it was running.
- Returns `true` on success.

### Virtual console (SSE)

- **Endpoint:** `/api/v1/berry/console`
- Mechanism: **Server-Sent Events** (`Content-Type: text/event-stream`).
- Allows real-time monitoring of the script's `stdout` and `stderr` output.
- **Only one SSE session** can be active at a time; subsequent requests are blocked or rejected.

### Usage examples (curl)

```bash
# Download the script
curl -i http://192.168.99.50/api/v1/berry -o script.berry

# Upload a new script version
curl -i -X POST --data-binary @script.berry http://192.168.99.50/api/v1/berry

# Check if the script is running
curl http://192.168.99.50/api/v1/berry

# Start the script
curl -X PUT "http://192.168.99.50/api/v1/berry?run=true"

# Stop the script
curl -X PUT "http://192.168.99.50/api/v1/berry?run=false"

# Delete the script
curl -X DELETE http://192.168.99.50/api/v1/berry

# Connect to the virtual console (SSE)
curl http://192.168.99.50/api/v1/berry/console
```

> **Important**
>
> - **Script size** – keep the file < 8 kB; split larger scripts into modules or reduce comments.
> - **Security** – do not expose the device outside the local network, use a password for the device panel.
> - **Version control** – before overwriting the script, download a backup copy using `GET`.
> - **Console** – close the SSE connection when not needed to avoid blocking further sessions.

---

## Berry editor in the main Web UI

The Berry editor is embedded in the main whatwatt Web UI and lets you edit the Berry script and view its output in real time. Open the device panel in your browser and click the **Berry** tile to enter the editor. The view consists of two main components:

1. **Script editor** – supports syntax highlighting and line numbering.
2. **Console** – a clear, monochrome panel displaying data from the virtual console (`/api/v1/berry/console`). The console is **read-only**; it does not accept input.

Below the editor is a bar with six buttons for controlling the script and file:

| Control         | Function           | Description                                                                 |
| --------------- | ------------------ | --------------------------------------------------------------------------- |
| ![run](img/icon-run.svg) Run   | **Start / Restart** | Starts the script, or if the interpreter is already running—restarts it with the current editor content. |
| ![stop](img/icon-stop.svg) Stop | **Stop**            | Stops the currently running script (`PUT /api/v1/berry?run=false`).         |
| ![load](img/icon-load.svg) Load | **Save to device**  | Sends the editor content to `POST /api/v1/berry`; does not restart the script. |
| ![save](img/icon-save.svg) Save | **Save to disk**    | Downloads the current script as a `*.be` file using the standard "Save as" dialog. |
| ![open](img/icon-open.svg) Open | **Open from disk**  | Loads a `*.be` file from the local computer into the editor (the content is not sent to the device until you press **Load**). |
| Clear console   | **Clear console**   | Empties the console panel in the interface (does not clear logs on the device side). |

### Typical workflow

1. Open the main device panel in your browser (Chrome, Edge, Firefox) and click the **Berry** tile to enter the editor.
2. Edit, paste, or load a script from disk using ![open](img/icon-open.svg) **Open from disk** in the editor window.
3. Click ![load](img/icon-load.svg) **Save to device** – the script is sent to `/api/v1/berry` and is ready to run.
4. Click ![run](img/icon-run.svg) **Start** – the interpreter executes the script; output appears in the console.
5. To stop execution, use ![stop](img/icon-stop.svg) **Stop**.
6. Repeat steps 2–4 as many times as needed during debugging.

### Debugging tips

- The console uses SSE – if the output suddenly stops updating, refresh the page or make sure there is not a second concurrent session.
- Syntax errors are displayed in red with the `SyntaxError` prefix – most often related to indentation or missing `end`.
- Long blocking operations (incorrectly configured `timeout`) will freeze the interface until a response is received; monitor the time in the console.

> **Important**
>
> **Security note** – the script file is stored in the device's flash memory; overwriting via ![load](img/icon-load.svg) **Save to device** or `POST /api/v1/berry` replaces the previous version without a backup. Consider manually downloading a copy of the script with ![save](img/icon-save.svg) **Save to disk** before each major change.
>
> Remove console output statements such as `print` from the final version of the script.

---

## Auto-starting Berry Scripts

The whatwatt go device supports automatic Berry script execution on startup through configuration settings available in the general REST API. Scripts run automatically after boot.

### Configuration via Settings API

Configure auto-start through the device settings endpoint at `/api/v1/settings`. Berry configuration is located in the `services.berry` object within the settings structure.

#### Reading current settings

```bash
# Get current device settings
curl http://192.168.99.50/api/v1/settings
```

Example response structure:

```json
{
  "system": {
    "name": "My",
    "host_name": "whatwatt-000000",
    "protection": false,
    "power_save": false,
    "password_len": 4
  },
  "services": {
    "cloud": {
      "what_watt": true,
      "solar_manager": false,
      "mystrom": false,
      "stromkonto": false
    },
    "local": {
      "solar_manager": true
    },
    "broadcast": true,
    "other_energy_provider": false,
    "report_interval": 30,
    "log": false,
    "meter_proxy": false,
    "sd": {
      "frequency": 5,
      "enable": true
    },
    "modbus": {
      "enable": true,
      "port": 5020
    },
    "berry": {
      "auto_run": false,
      "run_delay": 300
    }
  }
}
```

### Berry Auto-start Configuration

The `services.berry` object contains two key parameters for auto-start functionality:

| Parameter   | Type | Range     | Default | Description                                                  |
| ----------- | ---- | --------- | ------- | ------------------------------------------------------------ |
| `auto_run`  | bool |           | false   | Enables or disables automatic script execution on device boot. |
| `run_delay` | int  | 60..86400 | 300     | Delay in seconds before starting the script after device boot. |

#### Enabling auto-start

To enable automatic script execution, set `auto_run` to `true`:

```bash
# Enable auto-start with 300 second delay (default)
curl -i -X PUT -d '{"services": {"berry": {"auto_run": true, "run_delay": 300}}}' http://192.168.99.50/api/v1/settings
```

#### Disabling auto-start

To disable automatic script execution:

```bash
# Disable auto-start
curl -i -X PUT -d '{"services": {"berry": {"auto_run": false}}}' http://192.168.99.50/api/v1/settings
```

#### Configuring startup delay

The `run_delay` parameter allows you to specify how long the device should wait after boot before starting the Berry script. This is useful to ensure all system services are fully initialized before script execution begins.

```bash
# Set auto-start with 60 second delay
curl -i -X PUT -d '{"services": {"berry": {"run_delay": 60}}}' http://192.168.99.50/api/v1/settings
```

### Using Berry API for auto-start configuration

You can also configure auto-start settings directly from within a Berry script using the local REST API functions:

```python
# Enable auto-start from within Berry script
import ww

# Get current settings
current_settings = ww.apiget('settings')

# Enable auto-start with 120 second delay
new_settings = {
    'services': {
        'berry': {
            'auto_run': true,
            'run_delay': 120
        }
    }
}

result = ww.apiset('settings', new_settings)
print("Auto-start configured:", result)
```

### Best Practices

- **Startup delay**: Use an appropriate `run_delay` value (typically 60-300 seconds) to ensure the device is fully operational before script execution.
- **Error handling**: Design your auto-start scripts with proper error handling, as they will run without user supervision.
- **Recovery**: Ensure your script can handle network unavailability or temporary service interruptions during boot.
- **Testing**: Thoroughly test auto-start functionality by rebooting the device and verifying script execution.

### Troubleshooting

If auto-start is not working as expected:

1. **Check settings**: Verify that `auto_run` is set to `true` in the device settings.
2. **Script existence**: Ensure a Berry script is saved on the device (use `GET /api/v1/berry` to verify).
3. **Delay timing**: Consider increasing `run_delay` if the script depends on network services that may not be ready immediately after boot.
4. **Console monitoring**: Use the virtual console (`/api/v1/berry/console`) to monitor script output and identify any startup issues.
5. **Manual testing**: Test your script manually before enabling auto-start to ensure it works correctly.

> **Important**
>
> - The script will start automatically only after the specified `run_delay` period.
> - Auto-start settings persist across device reboots and firmware updates.
> - Ensure your auto-start scripts are production-ready and do not contain debugging output that might fill up logs.
> - If you manually start or stop the script, auto-start will not be triggered.
