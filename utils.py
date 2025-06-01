import yfinance as yf

#TODO Skal gjøre navn im til symbol Frontline -> FRO (Ikke ferdig)
def search_symbol(query: str):
    results = yf.Ticker(query).info
    print(results)
    return results.get("symbol", None)

if __name__ == "__main__":
    symbol = search_symbol("Frontline")

    print("symbol:", symbol)