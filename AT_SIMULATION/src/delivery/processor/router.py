from fastapi import APIRouter, Depends, WebSocketDisconnect
from src.delivery.core.models.conversions import InternalServiceError, SuccessResponse
from src.delivery.core.models.models import CommonResponse
from src.delivery.model.dependencies import get_current_user
from src.delivery.processor.dependencies import IProcessorService, get_processor_service
from fastapi import WebSocket
from src.delivery.processor.models.models import (
    CreateProcessRequest,
    ProcessResponse,
    ProcessesResponse,
    RunProcessRequest,
)


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


@router.websocket("/{process_id}/run")
async def run_process_websocket(
    web_socket: WebSocket,
    process_id: int,
    ticks: int,
    delay: int,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
):
    await web_socket.accept()
    try:
        await processor_service.run_process(
            user_id=user_id,
            process_id=process_id,
            ticks=ticks,
            delay=delay,
            web_socket=web_socket,
        )
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for process {process_id}")
    except Exception as e:
        await web_socket.send_text(f"Error: {str(e)}")
        await web_socket.close()


@router.get("/{process_id}/run", response_model=dict, summary="WebSocket Documentation")
def websocket_documentation(process_id: int):
    """
    ## WebSocket Documentation for `api/processor/{process_id}/run`

    - **WebSocket Endpoint**: `api/processor/{process_id}/run`
    - **Description**: Streams real-time updates for a process.

    ### Parameters:
    - `web_socket: WebSocket`: The WebSocket. 
    - `auth_token: str`: Auth user JWT token. 
    - `process_id: int`: The ID of the process to run.
    - `ticks: int`: The number of ticks to process.
    - `delay: int`: The delay between ticks, in milliseconds.

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
    return {
        "websocket_endpoint": f"/processor/{process_id}/run",
        "description": "See docstring for WebSocket details.",
    }


@router.post(
    "/{process_id}/pause", response_model=CommonResponse[ProcessResponse | None]
)
def pause_process(
    process_id: int,
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
    process_id: int,
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
            to_ProcessResponse(processor_service.get_processes(user_id))
        )
    except Exception as e:
        return InternalServiceError(e)
