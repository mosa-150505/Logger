# LOGGER

Just a simple facebook auto-logger to launch some reels

## Requirements

- Python 3.10+
- Selenium
- make

## Quick start

```bash
make install   # install dependencies
make run       # start logger
make help      # available make options
```

## Configuration

`config.json` : your ID storage

```json
{
  "email": "you@example.com",
  "password": "your-password"
}
```

## Mechanism

1. Opens Facebook with the dedicated profile `~/selenium_profile`
2. Accepts cookies, logs in if needed
3. On first login, approve it on your phone; the script clicks "Trust this device"
4. Opens Reels and saves `screenshots/reels.png`
5. Keeps the browser open until you press Enter

## Archi

```
.
├── Makefile
├── main.py              entry point
├── config.example.json  config template
├── pyproject.toml       ruff settings
├── requirements.txt
└── src/
    ├── constants.py     paths, URLs, selectors
    ├── config.py        config.json loading
    ├── logger.py        colored output
    ├── human.py         human-like pauses, typing, clicks
    ├── browser.py       Firefox driver
    ├── auth.py          cookies, login, 2FA
    └── reels.py         Reels navigation
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `Failed to set preferences` | Init the profile: `firefox --no-remote --profile ~/selenium_profile`, log in, close it |
| `Fichier introuvable : config.json` | Run `make` from the project root |
| Reels not opening | Check the URLs in the terminal and `screenshots/reels.png` (`login`/`checkpoint` = blocked) |
| Trust button not clicked | Update `TRUST_XPATH` in `src/constants.py` |
| `missing separator` (make) | Makefile commands must start with a tab, not spaces |

## Disclaimer

Automating Facebook violates its Terms of Service and may get your account restricted. Use on your own account only xD.      

## Author
*  Mosa
*  [mosa-150505](https://github.com/mosa-150505)
*  mosa.raharimanou@gmail.com
