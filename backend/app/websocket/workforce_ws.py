from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.websocket.manager import manager


router = APIRouter()


@router.websocket(
    "/ws/workforce"
)
async def workforce_monitoring(
    websocket: WebSocket,
):
    await manager.connect(websocket)

    try:
        await websocket.send_json(
            {
                "event": "connection_established",
                "message": (
                    "Connected to real-time "
                    "workforce monitoring"
                ),
            }
        )

        while True:
            data = await websocket.receive_json()

            event_type = data.get(
                "event",
                "workforce_update",
            )

            await manager.broadcast(
                {
                    "event": event_type,
                    "data": data,
                }
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        manager.disconnect(websocket)