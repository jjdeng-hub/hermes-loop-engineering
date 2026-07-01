# X (Twitter) API MCP Server Setup

Integrating the X API as an MCP server in Hermes Agent, enabling tools for
searching posts, looking up users, managing bookmarks, and fetching trends.

## Prerequisites

- **xurl CLI** (npm or binary): `npm install -g @xdevplatform/xurl`
- **X Developer App** with OAuth 2.0 enabled at https://developer.x.com
- **Credentials needed**: `CLIENT_ID`, `CLIENT_SECRET`

## X Developer App Setup

1. Go to https://console.x.com → Create new application
2. App type: **Web App, Automated App or Bot** (Confidential client)
3. Callback URI: `http://localhost:8080/callback`
4. Save the **Client ID** and **Client Secret**

## xurl CLI Setup

```bash
# Register app
xurl auth apps add my-app --client-id "YOUR_CLIENT_ID" --client-secret "YOUR_CLIENT_SECRET"

# Set as default
xurl auth default my-app
```

## OAuth 2.0: PKCE Flow (Headless Server)

On a headless/remote server without a browser, use the two-step PKCE flow:

### Step 1: Generate auth URL (Python)

```python
import secrets, hashlib, base64, urllib.parse, json

CLIENT_ID = "YOUR_CLIENT_ID"
REDIRECT_URI = "http://localhost:8080/callback"

code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode()
state = secrets.token_urlsafe(32)

# SAVE this - needed for step 2
with open("/tmp/xurl_oauth_state.json", "w") as f:
    json.dump({"verifier": code_verifier, "state": state}, f)

params = {
    "response_type": "code", "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "tweet.read users.read bookmark.read follows.read list.read block.read mute.read like.read users.email dm.read tweet.write tweet.moderate.write follows.write bookmark.write block.write mute.write like.write list.write media.write dm.write offline.access space.read",
    "state": state, "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}
print("https://x.com/i/oauth2/authorize?" + urllib.parse.urlencode(params))
```

### Step 2: Exchange code for token

```python
import urllib.parse, urllib.request, base64, json, sys, os

CLIENT_ID, CLIENT_SECRET = "YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080/callback"
cb = sys.argv[1]  # callback URL from user
params = urllib.parse.parse_qs(urllib.parse.urlparse(cb).query)
code = params["code"][0]

with open("/tmp/xurl_oauth_state.json") as f:
    saved = json.load(f)

auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
data = {"grant_type": "authorization_code", "code": code,
        "redirect_uri": REDIRECT_URI, "code_verifier": saved["verifier"]}

req = urllib.request.Request("https://api.x.com/2/oauth2/token",
    urllib.parse.urlencode(data).encode(),
    headers={"Authorization": f"Basic {auth}",
             "Content-Type": "application/x-www-form-urlencoded"})

with urllib.request.urlopen(req, timeout=15) as resp:
    tokens = json.loads(resp.read())

# Save to ~/.xurl
with open(os.path.expanduser("~/.xurl"), "w") as f:
    f.write(f"apps:\n  x-api:\n    client_id: \"{CLIENT_ID}\"\n    client_secret: \"{CLIENT_SECRET}\"\n    oauth2:\n      access_token: \"{tokens['access_token']}\"\n      refresh_token: \"{tokens.get('refresh_token', '')}\"\ndefault: x-api\n")
```

### Common pitfalls

- **State mismatch**: Each `xurl auth oauth2` call generates a new PKCE challenge.
  The user's code must come from the SAME URL that was generated. Always use a
  two-step approach: generate URL → user authorizes → exchange with saved verifier.
- **OAuth 1.0a vs 2.0**: The X Developer Console's "Generate" button produces
  OAuth 1.0a tokens, which may not work with all endpoints (returns 401).
  Use the PKCE flow for OAuth 2.0 tokens.
- **Token expiry**: OAuth 2.0 tokens expire after 2 hours (7200s). The
  `refresh_token` handles automatic renewal.

## Hermes MCP Configuration

### Via `hermes config set` (preferred)

```bash
# For HTTP transport (app-only bearer token, read-only)
hermes config set mcp_servers.x-api.url "https://api.x.com/mcp"
hermes config set mcp_servers.x-api.headers.Authorization "Bearer YOUR_TOKEN"
```

Note: `hermes config set` stores string values correctly. For nested objects
(url + headers), set each key individually.

### Config format in config.yaml

✅ Correct:
```yaml
mcp_servers:
  x-api:
    url: https://api.x.com/mcp
    headers:
      Authorization: "Bearer YOUR_TOKEN"
```

❌ Wrong (stored as string, not parsed):
```yaml
mcp_servers:
  x-api: '{"url":"https://api.x.com/mcp","headers":{...}}'
```

### Loading the MCP server

After configuring, send `/reload-mcp` in the chat to hot-reload without
restarting the gateway. The tools should appear with the `mcp_x_api_*` prefix.

## Auth Type Limitations

| Auth type | Endpoints | Limitations |
|-----------|-----------|-------------|
| **OAuth 2.0 User Context** | `get_users_me`, `get_users_by_username`, timeline, mentions, bookmarks, follows | Can't use `search_posts_all` (needs app-only) |
| **App-only Bearer** | `search_posts_all`, trends | Read-only, no user context |
| **OAuth 1.0a** | Legacy endpoints | May return 401 for newer v2 endpoints |

## Credits / Billing

X API requires credits (minimum $5 deposit at https://developer.x.com → Billing).
Without credits, most endpoints return:

```json
{"detail":"credits depleted","status":402,"title":"Payment Required"}
```

The `get_users_me` endpoint works without credits (free tier).
