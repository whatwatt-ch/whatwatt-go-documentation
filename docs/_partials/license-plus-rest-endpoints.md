The REST endpoints below are available only with an active Plus or higher license.
On devices reporting `FREE`, these routes return `404 License required`.

| Endpoint | Methods | Purpose |
|----------|---------|---------|
| `/api/v1/report` | `GET` | Latest parsed energy and meter report |
| `/api/v1/report/objects` | `GET` | Raw DLMS/COSEM object list |
| `/api/v1/variables` | `GET` | MQTT/template variables exposed over REST |
| `/api/v1/actions` | `GET`, `POST`, `DELETE` | Actions definition management |
| `/api/v1/actions/call` | `POST` | Action execution |
| `/api/v1/actions/status` | `GET` | Action execution status |
