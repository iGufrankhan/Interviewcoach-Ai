import asyncio
from mongoengine import Document
from typing import TypeVar, List, Optional

T = TypeVar('T', bound='AsyncDocument')


class AsyncDocument(Document):
    meta = {'abstract': True}
    
    @classmethod
    async def async_find_one(cls: type[T], **query) -> Optional[T]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: cls.objects(**query).first())
    
    @classmethod
    async def async_find(cls: type[T], skip: int = 0, limit: int = 10, **query) -> List[T]:
        loop = asyncio.get_event_loop()
        def _query():
            return list(cls.objects(**query).skip(skip).limit(limit))
        return await loop.run_in_executor(None, _query)
    
    @classmethod
    async def async_find_all(cls: type[T], **query) -> List[T]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: cls.objects(**query).all())
    
    @classmethod
    async def async_count(cls, **query) -> int:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: cls.objects(**query).count())
    
    @classmethod
    async def async_delete(cls, **query) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: cls.objects(**query).delete())
    
    @classmethod
    async def async_update(cls, query_dict: dict, **update_dict) -> int:
        loop = asyncio.get_event_loop()
        def _update():
            return cls.objects(**query_dict).update(**update_dict)
        return await loop.run_in_executor(None, _update)
    
    async def async_save(self: T) -> T:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.save)
    
    async def async_reload(self: T) -> T:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.reload)
    
    async def async_delete_instance(self: T) -> int:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.delete)
