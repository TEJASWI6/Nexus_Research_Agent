from ddgs import DDGS

with DDGS() as ddgs:
    results = list(ddgs.text("bitcoin current price", max_results=3))
    print(results)