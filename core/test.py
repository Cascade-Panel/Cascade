from incus import IncusClient

async def test():
    async with IncusClient("https://your-incus-api-url", "your-api-key") as Client:
        new_instance = await Client.instances.create("my-instance", {"source": {"type": "image", "fingerprint": "abc123"}})

        cluster_info = await Client.clusters.get()

        new_instance.put_files()