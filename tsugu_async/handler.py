import base64
from typing import List, Union, Dict

from .utils import *
from . import remote
from loguru import logger


async def handler(message: str, user_id: str, platform: str, channel_id: str) -> List[Union[bytes, str]]:
    '''
    Tsugu Handler
    处理用户输入的自然语言，返回处理后的结果

    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :param channel_id: 频道ID / 群号
    :return: List[Union[bytes, str]]
    '''
    data = await handler_raw(message, user_id, platform, channel_id)
    response = []
    if not data:
        return response
    for item in data:
        response.append(item['string']) if item['type'] == 'string' else None
        response.append(base64.b64decode(item['string'].encode('utf-8')) if item['type'] == 'base64' else None)
    return response


async def handler_raw(message: str, user_id: str, platform: str, channel_id: str) -> List[Dict[str, str]]:
    '''
    handler_raw 除了返回的数据类型不同外，其他与 handler 函数一致
    返回格式为 Tsugu 标准数据格式
    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :param channel_id: 频道ID / 群号
    :return: List[Dict[str, str]]
    '''
    try:
        # 使用远程服务器
        res = await remote.handler(message, user_id, platform, channel_id)
        if not res:
            return []
        return res
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e



