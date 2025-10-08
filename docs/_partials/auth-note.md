<!-- normalized admonition for reuse across pages and partial includes -->
!!! note "Authentication"
    When a Web UI password is set, HTTP endpoints require **HTTP authentication**.

    **Firmware 1.10.X and later**: Uses **HTTP Digest authentication**
    - Server challenges with `WWW-Authenticate: Digest …` (realm is the device hostname)
    - Algorithm: `MD5-sess` (device advertises MD5-sess; integrity variant supported)
    - qop: `auth` (and optionally `auth-int` for requests with body integrity)
    - Nonce and opaque are issued by the device; the client must include `cnonce` and increment `nc`
    - Expired nonce: server may return `401` with `WWW-Authenticate: …, stale=true`.
      In that case, retry the same request once using the new server challenge, a new `cnonce`, and reset `nc=00000001`.

    **Firmware before 1.10.X**: Uses **HTTP Basic authentication**
    - Server challenges with `WWW-Authenticate: Basic realm="..."`
    - Credentials are base64-encoded in `Authorization: Basic <encoded-credentials>`

    **Recommended approach**: Use `--anyauth` in curl to automatically detect and use the appropriate method:

    ```bash
    curl --anyauth -u ":<password>" http://whatwatt-ABCDEF.local/api/v1/system
    ```
