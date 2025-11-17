---
title: Real-time Streaming (SSE)
category: api-endpoints
tags:
- sse
- server-sent-events
- real-time
- streaming
- live-data
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/live
protocols:
- HTTP
- SSE
related_concepts:
- real-time monitoring
- server-sent events
- connection limits
use_cases:
- real-time monitoring
- live dashboards
- instant notifications
- continuous data streams
real_device_tested: true
authentication: required when device password is set
---

# Real-time Streaming (SSE)

## Document Context

- **Purpose**: Receive real-time energy measurements via Server-Sent Events (SSE) streaming
- **When to use**: For live dashboards, real-time monitoring, instant notifications, or continuous data feeds
- **Prerequisites**: SSE-compatible client (browsers, curl, EventSource API); understanding of streaming concepts
- **Related to**: REST polling alternative, WebSocket-like functionality, real-time data integration
- **Validates against**: Real device streaming from 192.168.99.114

## Key Facts

- **Endpoint**: `/api/v1/live`
- **Method**: GET with persistent connection
- **Authentication**: Required when device Web UI password is set
- **Response format**: Server-Sent Events (text/event-stream)
- **Event name**: `live` with JSON payload
- **Connection limit**: Single client only (new connection closes previous)
- **Auto-reconnect**: Browser EventSource handles reconnection automatically
- **Data frequency**: Matches meter report interval (~10 seconds typical)

## Endpoint Details

Real-time streaming of meter data using Server-Sent Events (SSE).

| Endpoint              | `api/v1/live`     |
| --------------------- | ----------------- |
| Method                | GET               |
| Response content type | text/event-stream |

The server emits SSE events named `live` with a JSON payload. A new connection automatically closes any previous stream connection.

!!! warning "Connection Limit"
    Only one client can be connected at a time. When a new client connects, the device closes the previous stream.

--8<-- "../_partials/auth-note.md"

## Example request

=== "No auth"
    ```bash
    curl http://whatwatt-ABCDEF.local/api/v1/live
    ```

=== "With password"
    ```bash
    curl --anyauth -u ":PASSWORD" http://whatwatt-ABCDEF.local/api/v1/live
    ```

## Example JavaScript (browser)

```js
const es = new EventSource('http://whatwatt-ABCDEF.local/api/v1/live');
es.addEventListener('live', (ev) => {
  const data = JSON.parse(ev.data);
  console.log('Live data', data);
});
es.onerror = (err) => {
  console.error('SSE error', err);
  // The browser will auto-reconnect; no explicit retry directive is sent by the device
};
```

## Example event stream data

Measurement data is sent in a `live` event:

```txt
event: live
data: {"P_In":0.036,"P_Out":0,"P_P1_In":0,"P_P2_In":0,"P_P3_In":0,"P_P1_Out":0,"P_P2_Out":0,"P_P3_Out":0,"rP_In":0,"rP_Out":0,"rP_P1_In":0,"rP_P2_In":0,"rP_P3_In":0,"rP_P1_Out":0,"rP_P2_Out":0,"rP_P3_Out":0,"PF":0,"I_P1":0,"I_P2":0,"I_P3":0,"V_P1":230.1,"V_P2":229.8,"V_P3":230.4,"E_In":47.251,"E_In_T1":33.388,"E_In_T2":14.668,"E_Out":8.965,"E_Out_T1":7.868,"E_Out_T2":1.097,"rE_In":0,"rE_Out":0,"rEii":0,"rEic":0,"rEei":0,"rEec":0,"T":1,"Vol":[{"Bus":1,"M_ID":"12345678","DT":"2024-08-24T14:34:00","Cum":123.45}],"Date":"2024-08-24","Time":"14:34:00","Uptime":71.05}
```

!!! note
    - Some fields are included only when available (for example `T` — active tariff), otherwise they can be omitted.
    - The device does not send periodic heartbeat comments; if the meter produces no reports, the stream can be idle for a while.

## Field reference

| Field        | Type   | Unit   | Description |
| ------------ | ------ | ------ | ----------- |
| `P_In`       | double | kW     | Positive active instantaneous power (A+) total |
| `P_Out`      | double | kW     | Negative active instantaneous power (A-) total |
| `P_P1_In`    | double | kW     | Positive active instantaneous power (A+) in phase L1 |
| `P_P2_In`    | double | kW     | Positive active instantaneous power (A+) in phase L2 |
| `P_P3_In`    | double | kW     | Positive active instantaneous power (A+) in phase L3 |
| `P_P1_Out`   | double | kW     | Negative active instantaneous power (A-) in phase L1 |
| `P_P2_Out`   | double | kW     | Negative active instantaneous power (A-) in phase L2 |
| `P_P3_Out`   | double | kW     | Negative active instantaneous power (A-) in phase L3 |
| `P_P_In`     | double | kW     | Positive active maximum demand (A+) total |
| `P_P_In_T1`  | double | kW     | Positive active maximum demand (A+) in tariff T1 |
| `P_P_In_T2`  | double | kW     | Positive active maximum demand (A+) in tariff T2 |
| `I_P1`       | double | A      | Instantaneous current in phase L1 |
| `I_P2`       | double | A      | Instantaneous current in phase L2 |
| `I_P3`       | double | A      | Instantaneous current in phase L3 |
| `V_P1`       | double | V      | Instantaneous voltage in phase L1 |
| `V_P2`       | double | V      | Instantaneous voltage in phase L2 |
| `V_P3`       | double | V      | Instantaneous voltage in phase L3 |
| `rP_In`      | double | kvar   | Positive reactive instantaneous power (Q+) total |
| `rP_Out`     | double | kvar   | Negative reactive instantaneous power (Q-) total |
| `rP_P1_In`   | double | kvar   | Positive reactive instantaneous power (Q+) in phase L1 |
| `rP_P2_In`   | double | kvar   | Positive reactive instantaneous power (Q+) in phase L2 |
| `rP_P3_In`   | double | kvar   | Positive reactive instantaneous power (Q+) in phase L3 |
| `rP_P1_Out`  | double | kvar   | Negative reactive instantaneous power (Q-) in phase L1 |
| `rP_P2_Out`  | double | kvar   | Negative reactive instantaneous power (Q-) in phase L2 |
| `rP_P3_Out`  | double | kvar   | Negative reactive instantaneous power (Q-) in phase L3 |
| `PF`         | double |        | Instantaneous power factor |
| `E_In`       | double | kWh    | Positive active energy (A+) total |
| `E_In_T1`    | double | kWh    | Positive active energy (A+) in tariff T1 |
| `E_In_T2`    | double | kWh    | Positive active energy (A+) in tariff T2 |
| `E_Out`      | double | kWh    | Negative active energy (A-) total |
| `E_Out_T1`   | double | kWh    | Negative active energy (A-) in tariff T1 |
| `E_Out_T2`   | double | kWh    | Negative active energy (A-) in tariff T2 |
| `rE_In`      | double | kvarh  | Positive reactive energy (Q+) total |
| `rE_Out`     | double | kvarh  | Negative reactive energy (Q-) total |
| `rEii`       | double | kvarh  | Reactive energy imported inductive (quadrant II) |
| `rEic`       | double | kvarh  | Reactive energy imported capacitive (quadrant I) |
| `rEei`       | double | kvarh  | Reactive energy exported inductive (quadrant III) |
| `rEec`       | double | kvarh  | Reactive energy exported capacitive (quadrant IV) |
| `T`          | int    |        | Active tariff number (1…4); present only if reported |
| `Vol`        | array  |        | Optional volumes array; see below |
| `Date`       | string | Y-m-d  | Local date |
| `Time`       | string | H:M:S  | Local time |
| `Uptime`     | double | hour   | System uptime |

### Vol — volume entries

Each entry describes a bus volume (if applicable to your meter):

| Field    | Type   | Description |
| -------- | ------ | ----------- |
| `Bus`    | int    | Bus number (1-based) |
| `M_ID`   | string | Meter identifier for the volume source (if available) |
| `DT`     | string | Timestamp ISO-8601 (local time) |
| `Cum`    | double | Cumulative counter value |

See also: REST conventions, scalers pages if applicable, and the OBIS appendix for mapping.

## Common Issues & Solutions

### Issue: SSE connection drops or won't establish

- **Symptoms**: EventSource shows `readyState: 2` (closed), frequent reconnection attempts
- **Root cause**: Network instability, device overload, or authentication issues
- **Diagnosis**: Check browser network tab for HTTP status codes and errors
- **Solution**:
  - Verify device is reachable: `ping whatwatt-XXXXXX.local`
  - Check authentication if device has password protection
  - Ensure only one SSE client is connected (device closes previous connections)
- **Code pattern**:

```javascript
const es = new EventSource('http://device/api/v1/live');
es.addEventListener('error', (e) => {
    if (es.readyState === EventSource.CLOSED) {
        console.log('Connection closed, will auto-retry');
    }
});
```

- **Related**: [Network Troubleshooting](../10-general/discovery.md)

### Issue: No events received (connection open but silent)

- **Symptoms**: SSE connection established but no `live` events arrive
- **Root cause**: Meter not sending reports, device configuration issue
- **Diagnosis**:
  - Check if REST `/api/v1/report` endpoint returns fresh data
  - Verify `meter.status` in REST response
- **Solution**:
  - If REST endpoint also shows stale data: meter communication problem
  - If REST works but SSE silent: restart SSE connection
- **Code pattern**: Implement timeout detection for missing events

```javascript
let lastEventTime = Date.now();
setInterval(() => {
    if (Date.now() - lastEventTime > 60000) {  // 60 seconds
        console.warn('No events for 60s, checking connection');
    }
}, 10000);
```

- **Related**: [Meter Communication](../50-settings/meter-comm.md)

### Issue: Only one client can connect

- **Symptoms**: Second client connecting causes first client's stream to close
- **Root cause**: Device limitation - single SSE client only
- **Diagnosis**: Multiple browser tabs or applications trying to connect simultaneously
- **Solution**:
  - Coordinate client connections in your application
  - Use server-side proxy to multiplex single device stream to multiple clients
  - Consider WebSocket implementation for multi-client scenarios
- **Code pattern**: Implement connection management

```python
# Server-side proxy example
class SSEMultiplexer:
    def __init__(self, device_url):
        self.device_stream = requests.get(device_url, stream=True)
        self.clients = []

    def add_client(self, client_connection):
        self.clients.append(client_connection)

    def broadcast_event(self, event_data):
        for client in self.clients:
            client.send(event_data)
```

### Issue: Authentication failures with password-protected devices

- **Symptoms**: HTTP 401 errors, connection rejected
- **Root cause**: Device requires HTTP Digest authentication
- **Diagnosis**: Check if device has `system.protection: true` in settings
- **Solution**: Use proper authentication in SSE client
- **Code pattern**:

```bash
# curl with digest auth for SSE
curl --anyauth -u ":PASSWORD" http://device/api/v1/live
```

```javascript
// Browser - use credentials for authenticated requests
const es = new EventSource('http://device/api/v1/live', {
    withCredentials: true  // Include cookies for authentication
});
```

- **Related**: [HTTP Digest Guide](../90-appendix/digest-cheatsheet.md)

### Issue: Missing fields in event data

- **Symptoms**: Expected fields like `P_P2_In` or `V_P2` not present in JSON
- **Root cause**: Single-phase meter or meter doesn't provide those measurements
- **Diagnosis**: Check `Vol` array and phase-specific patterns in multiple events
- **Solution**: Use defensive parsing, assume missing = not available
- **Code pattern**:

```javascript
es.addEventListener('live', (ev) => {
    const data = JSON.parse(ev.data);

    // Safe field access
    const totalPower = data.P_In || 0;
    const phaseVoltages = [
        data.V_P1 || 0,
        data.V_P2 || 0,  // May be 0 for single-phase
        data.V_P3 || 0
    ].filter(v => v > 0);  // Remove unused phases
});
```

### Issue: Event data format changes

- **Symptoms**: Parsing errors, unexpected field types or missing expected fields
- **Root cause**: Firmware updates may modify SSE payload structure
- **Diagnosis**: Compare event JSON structure across firmware versions
- **Solution**: Implement robust parsing with version compatibility
- **Code pattern**: Version-aware parsing

```javascript
function parseEvent(data) {
    const parsed = JSON.parse(data);

    // Handle different firmware versions
    if (parsed.version) {
        return parseVersionedEvent(parsed);
    } else {
        return parseLegacyEvent(parsed);
    }
}
```

- **Related**: Firmware update documentation

## Usage Patterns

### Pattern: Real-time energy dashboard with SSE

**Use case**: Live energy monitoring dashboard with instant updates
**Method**: Server-Sent Events with JavaScript EventSource
**Code**:

```javascript
class EnergyDashboard {
    constructor(deviceUrl, password = null) {
        this.deviceUrl = deviceUrl;
        this.password = password;
        this.eventSource = null;
        this.lastUpdate = null;
        this.connectionAttempts = 0;
    }

    start() {
        this.connect();

        // Monitor connection health
        setInterval(() => {
            if (this.lastUpdate && Date.now() - this.lastUpdate > 60000) {
                console.warn('No data for 60 seconds, reconnecting...');
                this.reconnect();
            }
        }, 10000);
    }

    connect() {
        // Close existing connection
        if (this.eventSource) {
            this.eventSource.close();
        }

        const url = `${this.deviceUrl}/api/v1/live`;
        this.eventSource = new EventSource(url, {
            withCredentials: this.password ? true : false
        });

        this.eventSource.addEventListener('live', (event) => {
            this.handleLiveData(JSON.parse(event.data));
            this.lastUpdate = Date.now();
            this.connectionAttempts = 0;
        });

        this.eventSource.addEventListener('error', (event) => {
            console.error('SSE connection error:', event);
            this.connectionAttempts++;

            if (this.connectionAttempts > 5) {
                console.error('Too many connection failures, stopping');
                this.eventSource.close();
            }
        });

        this.eventSource.addEventListener('open', () => {
            console.log('SSE connection established');
        });
    }

    handleLiveData(data) {
        // Update dashboard elements
        this.updatePowerDisplay(data.P_In, data.P_Out);
        this.updateVoltageDisplay(data.V_P1, data.V_P2, data.V_P3);
        this.updateEnergyCounters(data.E_In, data.E_Out);

        // Solar-specific updates
        if (data.P_Out > 0) {
            this.updateSolarProduction(data.P_Out);
        }

        // Store data for trending
        this.addDataPoint(data);
    }

    updatePowerDisplay(importPower, exportPower) {
        document.getElementById('import-power').textContent = `${importPower.toFixed(3)} kW`;
        document.getElementById('export-power').textContent = `${exportPower.toFixed(3)} kW`;

        // Visual indicators
        const netPower = importPower - exportPower;
        const indicator = document.getElementById('net-flow');
        indicator.className = netPower > 0 ? 'importing' : 'exporting';
        indicator.textContent = `${Math.abs(netPower).toFixed(3)} kW ${netPower > 0 ? '→' : '←'}`;
    }

    reconnect() {
        console.log('Reconnecting SSE...');
        this.connect();
    }
}

// Usage
const dashboard = new EnergyDashboard('http://whatwatt-ABCDEF.local', 'device_password');
dashboard.start();
```

### Pattern: Real-time data logging to database

**Use case**: Continuous data collection for historical analysis
**Method**: SSE with server-side database storage
**Code**:

```python
import asyncio
import aiohttp
import asyncpg
from datetime import datetime
import json

class SSEDataLogger:
    def __init__(self, device_url, db_connection_string, password=None):
        self.device_url = device_url
        self.db_connection = db_connection_string
        self.password = password
        self.session = None
        self.db_pool = None

    async def setup(self):
        # Setup HTTP session with authentication
        auth = aiohttp.BasicAuth("", self.password) if self.password else None
        self.session = aiohttp.ClientSession(auth=auth)

        # Setup database connection pool
        self.db_pool = await asyncpg.create_pool(self.db_connection)

        # Create table if not exists
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS energy_data (
                    timestamp TIMESTAMPTZ PRIMARY KEY,
                    import_power FLOAT,
                    export_power FLOAT,
                    voltage_l1 FLOAT,
                    voltage_l2 FLOAT,
                    voltage_l3 FLOAT,
                    current_l1 FLOAT,
                    current_l2 FLOAT,
                    current_l3 FLOAT,
                    energy_imported FLOAT,
                    energy_exported FLOAT,
                    active_tariff INTEGER,
                    device_uptime FLOAT,
                    raw_data JSONB
                )
            """)

    async def start_logging(self):
        await self.setup()

        while True:
            try:
                await self.connect_and_log()
            except Exception as e:
                print(f"Connection error: {e}, retrying in 30 seconds...")
                await asyncio.sleep(30)

    async def connect_and_log(self):
        url = f"{self.device_url}/api/v1/live"

        async with self.session.get(url) as response:
            if response.status != 200:
                raise aiohttp.ClientError(f"HTTP {response.status}")

            async for line in response.content:
                line = line.decode('utf-8').strip()

                if line.startswith('data: '):
                    json_data = line[6:]  # Remove 'data: ' prefix
                    await self.process_event(json_data)

    async def process_event(self, json_data):
        try:
            data = json.loads(json_data)
            timestamp = datetime.now()

            # Extract key metrics
            metrics = {
                'timestamp': timestamp,
                'import_power': data.get('P_In', 0),
                'export_power': data.get('P_Out', 0),
                'voltage_l1': data.get('V_P1', 0),
                'voltage_l2': data.get('V_P2', 0),
                'voltage_l3': data.get('V_P3', 0),
                'current_l1': data.get('I_P1', 0),
                'current_l2': data.get('I_P2', 0),
                'current_l3': data.get('I_P3', 0),
                'energy_imported': data.get('E_In', 0),
                'energy_exported': data.get('E_Out', 0),
                'active_tariff': data.get('T'),
                'device_uptime': data.get('Uptime', 0),
                'raw_data': json.dumps(data)
            }

            # Store in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO energy_data VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
                    ) ON CONFLICT (timestamp) DO NOTHING
                """, *metrics.values())

            print(f"Logged: {metrics['import_power']:.3f} kW import, {metrics['export_power']:.3f} kW export")

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
        except Exception as e:
            print(f"Database error: {e}")

# Usage
async def main():
    logger = SSEDataLogger(
        device_url="http://whatwatt-ABCDEF.local",
        db_connection_string="postgresql://user:pass@localhost/energy_db",
        password="device_password"
    )
    await logger.start_logging()

# Run with: asyncio.run(main())
```

### Pattern: Real-time alerting system

**Use case**: Instant notifications for power events
**Method**: SSE with threshold monitoring and alerts
**Code**:

```javascript
class PowerAlert {
    constructor(deviceUrl, thresholds, notificationCallback) {
        this.deviceUrl = deviceUrl;
        this.thresholds = thresholds;
        this.notify = notificationCallback;
        this.lastAlerts = {};
        this.eventSource = null;
    }

    start() {
        const url = `${this.deviceUrl}/api/v1/live`;
        this.eventSource = new EventSource(url);

        this.eventSource.addEventListener('live', (event) => {
            const data = JSON.parse(event.data);
            this.checkThresholds(data);
        });
    }

    checkThresholds(data) {
        const now = Date.now();

        // High power consumption alert
        if (data.P_In > this.thresholds.maxImportPower) {
            this.sendAlert('high_consumption',
                `High power consumption: ${data.P_In.toFixed(2)} kW`, data);
        }

        // Low voltage alert
        const minVoltage = Math.min(data.V_P1 || 999, data.V_P2 || 999, data.V_P3 || 999);
        if (minVoltage < this.thresholds.minVoltage && minVoltage > 0) {
            this.sendAlert('low_voltage',
                `Low voltage detected: ${minVoltage}V`, data);
        }

        // Solar production drop (if applicable)
        if (this.thresholds.expectedSolarPower &&
            data.P_Out < this.thresholds.expectedSolarPower * 0.8) {
            this.sendAlert('solar_drop',
                `Solar production below expected: ${data.P_Out.toFixed(2)} kW`, data);
        }

        // Phase imbalance
        const phases = [data.P_P1_In || 0, data.P_P2_In || 0, data.P_P3_In || 0];
        const activePhases = phases.filter(p => p > 0);
        if (activePhases.length > 1) {
            const maxPhase = Math.max(...activePhases);
            const minPhase = Math.min(...activePhases);
            const imbalance = ((maxPhase - minPhase) / maxPhase) * 100;

            if (imbalance > this.thresholds.maxPhaseImbalance) {
                this.sendAlert('phase_imbalance',
                    `Phase imbalance: ${imbalance.toFixed(1)}%`, data);
            }
        }
    }

    sendAlert(type, message, data) {
        const now = Date.now();
        const lastAlert = this.lastAlerts[type] || 0;

        // Rate limiting: only send alert every 5 minutes for same type
        if (now - lastAlert > 5 * 60 * 1000) {
            this.notify({
                type: type,
                message: message,
                timestamp: new Date().toISOString(),
                data: data
            });
            this.lastAlerts[type] = now;
        }
    }
}

// Usage
const alertSystem = new PowerAlert(
    'http://whatwatt-ABCDEF.local',
    {
        maxImportPower: 5.0,     // 5 kW
        minVoltage: 220,         // 220V
        expectedSolarPower: 3.0,  // 3 kW solar system
        maxPhaseImbalance: 15     // 15% max imbalance
    },
    (alert) => {
        // Send notification (email, SMS, push notification, etc.)
        console.log(`ALERT: ${alert.message}`);

        // Example: Send to webhook
        fetch('/api/alerts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(alert)
        });
    }
);

alertSystem.start();
```

## Semantic Field Map

Understanding the SSE JSON payload structure for RAG and real-time data processing:

### Real-Time Power Group (Instantaneous Values)

- `P_In` → **semantic_name**: "live_import_power_total" → **meaning**: "Current power consumption from grid" → **unit**: "kW" → **type**: "real_time_stream" → **update_frequency**: "every_meter_report"
- `P_Out` → **semantic_name**: "live_export_power_total" → **meaning**: "Current power fed back to grid" → **unit**: "kW" → **type**: "real_time_stream"
- `P_P1_In, P_P2_In, P_P3_In` → **semantic_name**: "live_import_power_per_phase" → **meaning**: "Per-phase power consumption" → **unit**: "kW" → **type**: "real_time_stream"
- `P_P1_Out, P_P2_Out, P_P3_Out` → **semantic_name**: "live_export_power_per_phase" → **meaning**: "Per-phase power export" → **unit": "kW" → **type**: "real_time_stream"

### Electrical Parameters Group (Live Measurements)

- `V_P1, V_P2, V_P3` → **semantic_name**: "live_voltage_per_phase" → **meaning**: "Real-time line voltages" → **unit**: "V" → **type**: "real_time_stream" → **normal_range**: "220V-240V"
- `I_P1, I_P2, I_P3` → **semantic_name**: "live_current_per_phase" → **meaning**: "Real-time line currents" → **unit**: "A" → **type**: "real_time_stream"
- `PF` → **semantic_name**: "live_power_factor" → **meaning**: "Instantaneous power factor (efficiency indicator)" → **unit**: "dimensionless" → **type**: "real_time_stream" → **range**: "0-1"

### Reactive Power Group (Live Values)

- `rP_In` → **semantic_name**: "live_reactive_power_positive" → **meaning**: "Real-time inductive reactive power" → **unit**: "kvar" → **type**: "real_time_stream"
- `rP_Out` → **semantic_name**: "live_reactive_power_negative" → **meaning**: "Real-time capacitive reactive power" → **unit**: "kvar" → **type**: "real_time_stream"
- `rP_P1_In, rP_P2_In, rP_P3_In` → **semantic_name**: "live_reactive_power_per_phase_positive" → **meaning**: "Per-phase reactive power (inductive)" → **unit**: "kvar" → **type**: "real_time_stream"

### Energy Counters Group (Live Updates)

- `E_In` → **semantic_name**: "live_total_energy_imported" → **meaning**: "Current cumulative energy consumed" → **unit**: "kWh" → **type**: "cumulative_stream"
- `E_Out` → **semantic_name**: "live_total_energy_exported" → **meaning**: "Current cumulative energy exported" → **unit**: "kWh" → **type**: "cumulative_stream"
- `E_In_T1, E_In_T2` → **semantic_name**: "live_energy_imported_per_tariff" → **meaning**: "Tariff-specific energy consumption" → **unit**: "kWh" → **type**: "cumulative_stream"
- `E_Out_T1, E_Out_T2` → **semantic_name**: "live_energy_exported_per_tariff" → **meaning**: "Tariff-specific energy export" → **unit**: "kWh" → **type**: "cumulative_stream"

### Reactive Energy Group (Quadrant-Based)

- `rE_In` → **semantic_name**: "live_total_reactive_energy_positive" → **meaning**: "Cumulative positive reactive energy" → **unit**: "kvarh" → **type**: "cumulative_stream"
- `rE_Out` → **semantic_name**: "live_total_reactive_energy_negative" → **meaning**: "Cumulative negative reactive energy" → **unit**: "kvarh" → **type**: "cumulative_stream"
- `rEii` → **semantic_name**: "live_reactive_energy_quadrant_ii" → **meaning**: "Reactive energy imported inductive (Q2)" → **unit**: "kvarh" → **type**: "cumulative_stream"
- `rEic` → **semantic_name**: "live_reactive_energy_quadrant_i" → **meaning**: "Reactive energy imported capacitive (Q1)" → **unit**: "kvarh" → **type**: "cumulative_stream"

### Temporal and System Group

- `Date, Time` → **semantic_name**: "live_measurement_local_time" → **meaning**: "Local timestamp of measurement" → **unit**: "date_time_strings" → **type**: "temporal_metadata"
- `Uptime` → **semantic_name**: "device_uptime_hours" → **meaning**: "Hours since device restart" → **unit**: "hours" → **type**: "system_metadata"
- `T` → **semantic_name**: "active_tariff_number" → **meaning**: "Currently active tariff period" → **unit**: "integer" → **type**: "tariff_metadata" → **range**: "1-4"

### Volume Data Group (Optional)

- `Vol[].Bus` → **semantic_name**: "volume_bus_identifier" → **meaning**: "Bus number for volume measurement" → **unit": "integer" → **type**: "volume_metadata"
- `Vol[].M_ID` → **semantic_name**: "volume_meter_identifier" → **meaning**: "Meter ID providing volume data" → **unit**: "string" → **type**: "volume_metadata"
- `Vol[].Cum` → **semantic_name**: "volume_cumulative_value" → **meaning**: "Cumulative volume measurement" → **unit**: "meter_dependent" → **type**: "volume_stream"

**SSE Processing Patterns**:

- **Real-time dashboards**: Use `P_In`, `P_Out`, `V_P1-P3` for live energy flow visualization
- **Power quality monitoring**: Track `PF`, voltage/current ratios for electrical system health
- **Load balancing**: Monitor `P_P1_In`, `P_P2_In`, `P_P3_In` for phase distribution
- **Solar system monitoring**: Focus on `P_Out` and `E_Out` for production tracking
- **Tariff optimization**: Use `T` with `E_In_T1/T2` for cost analysis
- **Connection management**: Handle single-client limitation with proper reconnection logic
- **Data validation**: Missing fields indicate meter doesn't provide that measurement
