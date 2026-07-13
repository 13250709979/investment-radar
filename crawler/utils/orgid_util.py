import logging
from typing import Dict, Optional

from utils.http_util import post_form

logger = logging.getLogger(__name__)

# 巨潮 A 股股票列表（含沪深，文件名虽为 szse 但实际包含全部 A 股）
STOCK_LIST_URL = "https://www.cninfo.com.cn/new/data/szse_stock.json"
TOP_SEARCH_URL = "https://www.cninfo.com.cn/new/information/topSearch/query"

_org_id_cache: Dict[str, str] = {}
_cache_loaded = False


def _load_stock_lists(session) -> None:
    global _cache_loaded
    if _cache_loaded:
        return

    try:
        response = session.get(STOCK_LIST_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        stock_list = data.get("stockList") or []
        for item in stock_list:
            code = str(item.get("code") or "").strip()
            org_id = str(item.get("orgId") or "").strip()
            if code and org_id:
                _org_id_cache[code] = org_id
        logger.info("加载 A 股股票列表 %s 条", len(stock_list))
    except Exception as exc:
        logger.warning("加载股票列表失败 %s: %s", STOCK_LIST_URL, exc)

    _cache_loaded = True
    logger.info("orgId 缓存共 %s 条", len(_org_id_cache))


def _lookup_by_top_search(session, stock_code: str) -> Optional[str]:
    try:
        result = post_form(session, TOP_SEARCH_URL, {"keyWord": stock_code})
        if isinstance(result, list) and result:
            org_id = str(result[0].get("orgId") or "").strip()
            return org_id or None
    except Exception as exc:
        logger.warning("topSearch 查询 orgId 失败 stock=%s: %s", stock_code, exc)
    return None


def resolve_org_id(session, stock_code: str) -> str:
    """查询股票对应的巨潮 orgId，如 601012 -> 9900022338。"""
    code = stock_code.strip()
    if not code:
        raise ValueError("stock_code 不能为空")

    if code in _org_id_cache:
        return _org_id_cache[code]

    _load_stock_lists(session)

    if code in _org_id_cache:
        org_id = _org_id_cache[code]
        logger.info("股票列表获取 orgId: %s -> %s", code, org_id)
        return org_id

    org_id = _lookup_by_top_search(session, code)
    if org_id:
        _org_id_cache[code] = org_id
        logger.info("topSearch 获取 orgId: %s -> %s", code, org_id)
        return org_id

    raise ValueError(
        f"未找到股票 {code} 的 orgId，请确认股票代码是否正确"
    )


def build_stock_param(session, stock_code: str) -> str:
    """构造巨潮 stock 参数：股票代码,orgId。"""
    code = stock_code.strip()
    org_id = resolve_org_id(session, code)
    return f"{code},{org_id}"
