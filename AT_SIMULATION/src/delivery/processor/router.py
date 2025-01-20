from fastapi import APIRouter, Depends
from src.delivery.core.models.conversions import InternalServiceError, SuccessResponse
from src.delivery.core.models.models import CommonResponse
from src.delivery.model.dependencies import get_current_user
from src.delivery.processor.dependencies import IProcessorService, get_processor_service
from fastapi import WebSocket
from src.delivery.processor.models.conversions import (
    to_ProcessResponse,
    to_ProcessesResponse,
)
from src.delivery.processor.models.models import (
    CreateProcessRequest,
    ProcessResponse,
    ProcessesResponse,
    RunProcessRequest,
)
from src.delivery.websocket_manager import WebsocketManager


router = APIRouter(
    prefix="/processor",
    tags=["processor"],
)


@router.post("", response_model=CommonResponse[ProcessResponse | None])
def create_process(
    body: CreateProcessRequest,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> CommonResponse[ProcessResponse]:
    try:
        return SuccessResponse(
            to_ProcessResponse(
                processor_service.create_process(
                    user_id,
                    body.file_id,
                    body.process_name,
                )
            )
        )
    except Exception as e:
        return InternalServiceError(e)


@router.post("/{process_id}/run", response_model=CommonResponse[None])
async def run_process(
    process_id: str,
    body: RunProcessRequest,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> CommonResponse[None]:
    try:
        await processor_service.run_process(user_id, process_id, body.ticks, body.delay)
        return SuccessResponse(None)
    except Exception as e:
        return InternalServiceError(e)


@router.post(
    "/{process_id}/pause", response_model=CommonResponse[ProcessResponse | None]
)
def pause_process(
    process_id: str,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> CommonResponse[ProcessResponse]:
    try:
        return SuccessResponse(
            to_ProcessResponse(processor_service.pause_process(user_id, process_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.post(
    "/{process_id}/kill", response_model=CommonResponse[ProcessResponse | None]
)
def kill_process(
    process_id: str,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> CommonResponse[ProcessResponse]:
    try:
        return SuccessResponse(
            to_ProcessResponse(processor_service.kill_process(user_id, process_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("", response_model=CommonResponse[ProcessesResponse | None])
def get_processes(
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> CommonResponse[ProcessesResponse]:
    try:
        return SuccessResponse(
            to_ProcessesResponse(processor_service.get_processes(user_id))
        )
    except Exception as e:
        return InternalServiceError(e)


@router.get("/ws", summary="WebSocket Init")
def websocket_documentation():
    """
    ## WebSocket Documentation for `api/processor/ws`

    - **WebSocket Endpoint**: `api/processor/ws`
    - **Description**: Streams real-time updates for a process.

    ### Header:
    HTTPBearer  (http, Bearer): JWT token.

    ### Parameters:
    - `web_socket: WebSocket`: The WebSocket.
    - `process_id: int`:

    ### Example Messages:
    - **Server Message**:
    ```json
    {
    "current_tick": 1,
    "resources": [
        {
        "resource_name": "vlados_ruble",
        "currency": 55,
        "<attr_name>": "<attr_value>",
        ...,
        },
        null,
        {
        "resource_name": "car_1",
        "pos_x": -20,
        "pos_y": 25,
        "<attr_name>": "<attr_value>",
        ...,
        },
        {
        "resource_name": "car_2",
        "pos_x": -20,
        "pos_y": 50,
        "<attr_name>": "<attr_value>",
        ...,
        }
    ],
    "usages": [
        {
        "has_triggered": true,
        "usage_name": "irregular_event_1",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered": false,
        "usage_name": "irregular_event_2",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered": false,
        "usage_name": "irregular_event_3",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered": false,
        "usage_name": "irregular_event_4",
        "usage_type": "IRREGULAR_EVENT"
        },
        {
        "has_triggered_after": false,
        "has_triggered_before": false,
        "usage_name": "operation_1",
        "usage_type": "OPERATION"
        },
        {
        "has_triggered_after": false,
        "has_triggered_before": false,
        "usage_name": "operation_2",
        "usage_type": "OPERATION"
        },
        {
        "has_triggered": true,
        "usage_name": "rule_1",
        "usage_type": "RULE"
        },
        {
        "has_triggered": false,
        "usage_name": "rule_2",
        "usage_type": "RULE"
        }
    ]
    }
    ```

    This endpoint does not return data directly as it is intended for documentation purposes.
    """
    return {}


@router.websocket("/ws")
async def websocket_init(
    websocket: WebSocket,
    process_id: int,
    user_id: int = Depends(get_current_user),
    websocket_manager: WebsocketManager = Depends(WebsocketManager),
) -> None:
    await websocket_manager.connect(websocket, user_id, process_id)

    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        websocket_manager.disconnect(websocket, user_id, process_id)
