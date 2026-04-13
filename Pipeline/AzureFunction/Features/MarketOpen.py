from datetime import datetime, timezone

def get_market_session():
    hour = datetime.now(timezone.utc).hour
    if 12 <= hour < 16:  return "overlap"
    elif 7 <= hour < 16: return "european"
    elif 12 <= hour < 21:return "american"
    elif 0 <= hour < 9:  return "asian"
    else:                return "off_peak"

if __name__ == "__main__":
    session = get_market_session()
    print(f"Current Market Session: {session}")