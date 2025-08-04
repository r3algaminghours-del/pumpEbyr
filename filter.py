def is_promising(token: dict):
    try:
        mc = token.get("marketCap", 0)
        volume = token.get("volume5m", 0)
        inflow = token.get("netflow5m", 0)
        dev_hold = token.get("devTokenPercentage", 100)
        holders = token.get("holders", 0)
        links = token.get("links", {})

        return (
            18000 <= mc <= 35000 and
            volume >= 4000 and
            inflow >= 1500 and
            dev_hold <= 3 and
            holders >= 40 and
            ("x" in links or "web" in links)
        )
    except:
        return False
