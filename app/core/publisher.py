"""
Direct Meta Graph API v19+ Automated Publishing Gateway
Manages Instagram Single Image, Video Reel, and 2-10 Item Carousel Containers.
"""
import logging
from typing import List, Dict, Any
import aiohttp
from app.config import settings

logger = logging.getLogger("spatialstudio.publisher")

class MetaGraphPublisher:
    def __init__(self):
        self.base_url = f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}"
        self.account_id = settings.INSTAGRAM_ACCOUNT_ID
        self.access_token = settings.META_ACCESS_TOKEN

    async def create_item_container(self, session: aiohttp.ClientSession, image_url: str) -> str:
        url = f"{self.base_url}/{self.account_id}/media"
        params = {
            "image_url": image_url,
            "is_carousel_item": "true",
            "access_token": self.access_token
        }
        async with session.post(url, params=params) as resp:
            data = await resp.json()
            if "id" not in data:
                raise RuntimeError(f"Failed to create item container: {data}")
            return data["id"]

    async def create_carousel_container(self, item_ids: List[str], caption: str) -> str:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{self.account_id}/media"
            params = {
                "media_type": "CAROUSEL",
                "children": ",".join(item_ids),
                "caption": caption,
                "access_token": self.access_token
            }
            async with session.post(url, params=params) as resp:
                data = await resp.json()
                if "id" not in data:
                    raise RuntimeError(f"Carousel container creation failed: {data}")
                return data["id"]

    async def publish_container(self, container_id: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{self.account_id}/media_publish"
            params = {
                "creation_id": container_id,
                "access_token": self.access_token
            }
            async with session.post(url, params=params) as resp:
                return await resp.json()
