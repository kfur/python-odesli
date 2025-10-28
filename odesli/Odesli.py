import aiohttp
import json

from .entity.song.SongResult import SongResult
from .entity.album.AlbumResult import AlbumResult
from .entity.EntityResult import EntityResult

BASE_URL = 'https://api.song.link'
API_VERSION = 'v1-alpha.1'
ROOT = f'{BASE_URL}/{API_VERSION}'
LINKS_ENDPOINT = 'links'

class Odesli():
    def __init__(self, key=None):
        self.key = key


    async def __get(self, params, session=None) -> EntityResult:
        if not self.key == None:
            params['key'] = self.key
        if session:
            async with session.get(f'{ROOT}/{LINKS_ENDPOINT}', params=params) as resp:
                resp.raise_for_status()                 
                result = await resp.json()    
        else:
            async with aiohttp.ClientSession() as _session:
                async with _session.get(f'{ROOT}/{LINKS_ENDPOINT}', params=params) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        resultType = next(iter(result['entitiesByUniqueId'].values()))['type']
        if resultType == 'song':
            return SongResult.parse(result)
        elif resultType == 'album':
            return AlbumResult.parse(result)
        else:
            raise NotImplementedError(f'Entities with type {resultType} are not supported yet.')


    async def getByUrl(self, url, session=None) -> EntityResult:
        return await self.__get({ 'url': url }, session)

    async def getById(self, id, platform, type, session=None) -> EntityResult:
        return await self.__get({
            'id': id,
            'platform': platform,
            'type': type
        }, session)

