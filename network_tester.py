import asyncio
import time
import aiohttp

async def test_node_latency(session, proxy_url, target_url="https://httpbin.org/ip", timeout=5):
    """
    Evaluates connection latency, response code, and gateway verification for a target node.
    """
    start_time = time.time()
    try:
        async with session.get(target_url, proxy=proxy_url, timeout=timeout) as response:
            if response.status == 200:
                elapsed = (time.time() - start_time) * 1000
                data = await response.json()
                return {
                    "node": proxy_url,
                    "status": "Active",
                    "latency_ms": round(elapsed, 2),
                    "gateway_ip": data.get("origin")
                }
            else:
                return {"node": proxy_url, "status": f"HTTP {response.status}", "latency_ms": None}
    except Exception as e:
        return {"node": proxy_url, "status": f"Connection Timeout/Error", "latency_ms": None}

async def main():
    # Target nodes array to evaluate (sample placeholders for standard structure)
    nodes = [
        "http://username:password@sample-node-1.com:8000",
        "http://username:password@sample-node-2.com:8000"
    ]
    
    print(f"🚀 Launching async performance evaluation across {len(nodes)} nodes...")
    
    async with aiohttp.ClientSession() as session:
        tasks = [test_node_latency(session, node) for node in nodes]
        results = await asyncio.gather(*tasks)
        
        print("\n📊 Metric Log Summary:")
        print("=" * 65)
        for item in results:
            print(f"Node Path: {item['node']}")
            print(f"Status:    {item['status']}")
            if item['latency_ms']:
                print(f"Response:  {item['latency_ms']} ms")
                print(f"Gateway:   {item['gateway_ip']}")
            print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
