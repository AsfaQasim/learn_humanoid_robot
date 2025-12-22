"""
Test script to verify CORS configuration is working properly.
"""
import asyncio
import httpx

async def test_cors():
    """
    Test CORS headers by making a preflight OPTIONS request to the chat endpoint.
    """
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Test preflight request (OPTIONS) that browsers send before actual request
        try:
            response = await client.options(
                "/chat",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type",
                }
            )

            print(f"Preflight request status: {response.status_code}")
            print(f"CORS headers received:")
            for header, value in response.headers.items():
                if header.lower().startswith('access-control'):
                    print(f"  {header}: {value}")

            # Check if CORS headers are present
            cors_headers = [h for h in response.headers.keys() if h.lower().startswith('access-control')]
            if cors_headers:
                print("\n✅ CORS configuration is working correctly!")
                if 'Access-Control-Allow-Origin' in response.headers:
                    allowed_origin = response.headers['Access-Control-Allow-Origin']
                    print(f"✅ Access-Control-Allow-Origin: {allowed_origin}")
                    if allowed_origin == "http://localhost:3000":
                        print("✅ Correct origin is allowed")
                    else:
                        print("⚠️  Unexpected allowed origin")
                else:
                    print("❌ Missing Access-Control-Allow-Origin header")
            else:
                print("\n❌ CORS headers are missing - configuration may not be working")

        except httpx.ConnectError:
            print("❌ Server is not running. Please start the backend server on port 8000.")
        except Exception as e:
            print(f"❌ Error during CORS test: {e}")

if __name__ == "__main__":
    print("Testing CORS configuration...")
    asyncio.run(test_cors())