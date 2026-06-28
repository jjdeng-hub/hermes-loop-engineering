# Twitter/X API Setup

## Accounts
- Username: TomDengnc1c
- User ID: 2071058933972897792
- App type: OAuth 2.0 (configured via developer.twitter.com)
- Bearer Token: regeneration URL from Developer Portal (token included in encrypted session metadata)

## Status
- Bearer Token authenticates successfully (no 401)
- v2 API returns **402 CreditsDepleted** — the account has not activated the free API tier
- v1.1 API returns **403** — limited to media/oauth endpoints only
- Bearer Token must be passed URL-encoded (with `%2B` for `+` and `%3D` for `=`) — decoding causes 401

## To Fix 402 CreditsDepleted
Go to: Developer Portal → Project → Products tab → **Free** tier → "Set up" / "Subscribe"

## Access Alternatives (when API fails)
1. Browser preview: tweet title + snippet visible, full X Articles blocked without login
2. `fxtwitter.com` API: curl `https://api.fxtwitter.com/{user}/status/{id}` — but blocked from this server IP
3. Nitter/etc: all blocked from Alibaba Cloud IPs
4. Web search: `site:x.com {query}` via DuckDuckGo/Brave — can find tweets but not full articles

## Limitation
Server IP (47.86.180.83, Alibaba Cloud) is blocked by:
- Twitter/X from browser login
- Reddit entirely (even JSON API)
- Google Search (CAPTCHA)
- Brave Search (CAPTCHA)
- Nitter/fxtwitter alternates
