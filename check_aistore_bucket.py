#!/usr/bin/env python3
"""
Helper script to check and create AIStore buckets before running DLIO.
"""
import os
import sys

# Remove AWS credentials to avoid HMAC signing issues
for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"]:
    os.environ.pop(key, None)

from aistore.sdk import Client

def main():
    endpoint = os.environ.get("AIS_ENDPOINT", "http://localhost:51080")
    bucket_name = sys.argv[1] if len(sys.argv) > 1 else "dlio-benchmark-1gb"

    print(f"Connecting to AIStore at: {endpoint}")
    print(f"Checking bucket: {bucket_name}")
    print()

    try:
        client = Client(endpoint)
        print("✅ Connected to AIStore")

        # Try to list buckets
        try:
            buckets = client.cluster().list_buckets()
            print(f"✅ Found {len(buckets)} buckets on the cluster:")
            for bck in buckets:
                print(f"   - {bck.name} (provider: {bck.provider})")
            print()
        except Exception as e:
            print(f"⚠️  Could not list buckets: {e}")
            print()

        # Check if our bucket exists
        bucket = client.bucket(bucket_name)
        try:
            bucket.head()
            print(f"✅ Bucket '{bucket_name}' exists")

            # Try to list objects
            try:
                obj_list = bucket.list_objects()
                entries = obj_list.entries if hasattr(obj_list, 'entries') else []
                print(f"   Contains {len(entries)} objects (showing first 5)")
                for obj in entries[:5]:
                    print(f"   - {obj.name}")
            except Exception as e:
                print(f"   ⚠️  Could not list objects: {e}")
        except Exception as e:
            if "does not exist" in str(e).lower() or "404" in str(e):
                print(f"❌ Bucket '{bucket_name}' does not exist")
                print()
                print("Attempting to create bucket...")
                try:
                    bucket.create()
                    print(f"✅ Bucket '{bucket_name}' created successfully!")
                except Exception as create_err:
                    print(f"❌ Could not create bucket: {create_err}")
                    print()
                    print("Solutions:")
                    print("  1. Ask your AIStore admin to create the bucket")
                    print("  2. Use an existing bucket (change storage_root in config)")
                    print("  3. Check if you have permissions to create buckets")
                    sys.exit(1)
            else:
                print(f"❌ Error checking bucket: {e}")
                sys.exit(1)

        print()
        print("✅ Everything looks good! You can run DLIO now.")

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check if AIStore endpoint is correct")
        print("  2. Check if AIStore is running and accessible")
        print("  3. Check firewall/network settings")
        sys.exit(1)

if __name__ == "__main__":
    main()
