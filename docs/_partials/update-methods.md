!!! note "Partial vs. Full Update"

    - Partial update: Use `PUT` with only the fields you want to change. Unspecified fields remain unchanged.
    - Full replace: Use `POST` with the complete object when the API defines a "replace" operation; missing fields may reset to defaults.
    - Validation: Invalid payloads return `400 Bad Request`.
