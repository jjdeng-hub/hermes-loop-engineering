# Twitter API v2 Bearer Token Access

## Overview

Twitter/X offers a free API v2 tier via Bearer Token authentication. This allows reading public tweets, searching, and accessing full tweet content (including X Articles) without needing a logged-in browser session.

## Obtaining a Bearer Token

1. Go to https://developer.twitter.com and sign in with a Twitter account
2. Create a Project → Create a standalone App
3. Navigate to Keys and Tokens → Bearer Token
4. Copy the token (starts with `AAAA...`)

## Usage

```python
import urllib.request, json

token = "YOUR_BEARER_TOKEN"
tweet_id = "2070789303978840351"

url = f"https://api.twitter.com/2/tweets/{tweet_id}"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {token}")

try:
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    print(json.dumps(data, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.reason}")
    body = e.read().decode()
    print(body[:500])
```

## Pitfalls

### Bearer Token URL Encoding

The Bearer Token from the developer portal may contain URL-encoded characters (`%2B` = `+`, `%3D` = `=`). Use `urllib.parse.unquote()` to decode before use:

```python
import urllib.parse
raw_token = "AAAA...%2BQE...%3D..."
token = urllib.parse.unquote(raw_token)
```

### 401 Unauthorized

Common causes:
1. Token has URL-encoded characters that weren't decoded
2. App was just created — wait a few minutes for propagation
3. Token is from wrong tier (free tier supports v2 but may need project setup)
4. App needs to be activated / made public in developer portal
5. Check that the app has the correct permissions set (Read is sufficient for public tweets)

### Rate Limits

Free tier: 500k tweets/month (approx 690 tweets/hour sustained).
Use sparingly — prefer caching results locally.

## X Articles

X Articles (long-form content posted as X Articles) are accessible via the API with `tweet.fields=note_tweet`:

```python
url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=note_tweet,text"
```

The article content appears in the `note_tweet.text` field when present.
