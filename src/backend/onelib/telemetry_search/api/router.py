from copy import deepcopy
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException

from onelib.api.v1.schemas import resp_200

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

_DASHBOARDS: dict[str, dict] = {}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _new_dashboard(payload: dict) -> dict:
    now = _now()
    dashboard_id = uuid4().hex[:12]
    return {
        "id": dashboard_id,
        "title": payload.get("title") or "OneLib Dashboard",
        "description": payload.get("description") or "",
        "status": payload.get("status") or "draft",
        "dashboard_type": payload.get("dashboard_type") or "custom",
        "layout_config": payload.get("layout_config") or {"layouts": []},
        "style_config": payload.get("style_config") or {"theme": "light"},
        "create_time": now,
        "update_time": now,
        "is_default": len(_DASHBOARDS) == 0,
        "user_name": payload.get("user_name") or "oneLib",
        "write": payload.get("write", True),
        "components": payload.get("components") or [],
    }


def _get_dashboard_or_404(dashboard_id: str) -> dict:
    dashboard = _DASHBOARDS.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard


@router.get("/dashboard", status_code=200)
async def list_dashboards():
    return resp_200(data=list(_DASHBOARDS.values()))


@router.post("/dashboard", status_code=200)
async def create_dashboard(payload: dict | None = Body(default=None)):
    dashboard = _new_dashboard(payload or {})
    _DASHBOARDS[dashboard["id"]] = dashboard
    return resp_200(data=dashboard)


@router.get("/dashboard/dataset/list", status_code=200)
async def list_dashboard_datasets():
    return resp_200(data=[])


@router.get("/dashboard/dataset/field/enums", status_code=200)
async def list_dashboard_field_enums():
    return resp_200(data={"data": [], "total": 0})


@router.post("/dashboard/component/query", status_code=200)
async def query_dashboard_component():
    return resp_200(data={"dimensions": [], "value": []})


@router.get("/dashboard/{dashboard_id}", status_code=200)
async def get_dashboard(dashboard_id: str):
    return resp_200(data=_get_dashboard_or_404(dashboard_id))


@router.put("/dashboard/{dashboard_id}", status_code=200)
async def update_dashboard(dashboard_id: str, payload: dict | None = Body(default=None)):
    current = _get_dashboard_or_404(dashboard_id)
    updated = deepcopy(payload or {})
    updated["id"] = dashboard_id
    updated["create_time"] = current.get("create_time") or _now()
    updated["update_time"] = _now()
    updated.setdefault("status", current.get("status", "draft"))
    updated.setdefault("dashboard_type", current.get("dashboard_type", "custom"))
    updated.setdefault("layout_config", current.get("layout_config", {"layouts": []}))
    updated.setdefault("style_config", current.get("style_config", {"theme": "light"}))
    updated.setdefault("is_default", current.get("is_default", False))
    updated.setdefault("user_name", current.get("user_name", "oneLib"))
    updated.setdefault("write", current.get("write", True))
    updated.setdefault("components", current.get("components", []))
    _DASHBOARDS[dashboard_id] = updated
    return resp_200(data=updated)


@router.delete("/dashboard/{dashboard_id}", status_code=200)
async def delete_dashboard(dashboard_id: str):
    _get_dashboard_or_404(dashboard_id)
    was_default = _DASHBOARDS[dashboard_id].get("is_default", False)
    del _DASHBOARDS[dashboard_id]
    if was_default and _DASHBOARDS:
        next_dashboard = next(iter(_DASHBOARDS.values()))
        next_dashboard["is_default"] = True
        next_dashboard["update_time"] = _now()
    return resp_200()


@router.post("/dashboard/{dashboard_id}/title", status_code=200)
async def update_dashboard_title(dashboard_id: str, payload: dict | None = Body(default=None)):
    dashboard = _get_dashboard_or_404(dashboard_id)
    title = (payload or {}).get("title")
    if title:
        dashboard["title"] = title
        dashboard["update_time"] = _now()
    return resp_200(data=dashboard)


@router.post("/dashboard/{dashboard_id}/default", status_code=200)
async def set_default_dashboard(dashboard_id: str):
    dashboard = _get_dashboard_or_404(dashboard_id)
    for item in _DASHBOARDS.values():
        item["is_default"] = item["id"] == dashboard_id
    dashboard["update_time"] = _now()
    return resp_200(data=dashboard)


@router.post("/dashboard/{dashboard_id}/copy", status_code=200)
async def copy_dashboard(dashboard_id: str, payload: dict | None = Body(default=None)):
    source = _get_dashboard_or_404(dashboard_id)
    copied = deepcopy(source)
    now = _now()
    copied["id"] = uuid4().hex[:12]
    copied["title"] = (payload or {}).get("new_title") or f"{source['title']} Copy"
    copied["is_default"] = False
    copied["status"] = "draft"
    copied["create_time"] = now
    copied["update_time"] = now
    for component in copied.get("components", []):
        component["dashboard_id"] = copied["id"]
    _DASHBOARDS[copied["id"]] = copied
    return resp_200(data=copied)


@router.post("/dashboard/{dashboard_id}/status", status_code=200)
async def update_dashboard_status(dashboard_id: str, payload: dict | None = Body(default=None)):
    dashboard = _get_dashboard_or_404(dashboard_id)
    dashboard["status"] = (payload or {}).get("status") or dashboard.get("status", "draft")
    dashboard["update_time"] = _now()
    return resp_200(data=dashboard)
