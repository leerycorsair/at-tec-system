from fastapi import APIRouter, Depends
from src.delivery.core.models.conversions import InternalServiceError, SuccessResponse
from src.delivery.core.models.models import CommonResponse
from src.delivery.model.dependencies import get_current_user
from src.delivery.processor.dependencies import IProcessorService, get_processor_service
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


@router.post("/{process_id}/run", response_model=CommonResponse[ProcessResponse | None])
def run_process(
    body: RunProcessRequest,
    process_id: int,
    user_id: int = Depends(get_current_user),
    processor_service: IProcessorService = Depends(get_processor_service),
) -> CommonResponse[ProcessResponse]:
    try:
        return SuccessResponse(
            to_ProcessResponse(
                processor_service.run_process(
                    user_id,
                    process_id,
                    body.ticks,
                    body.delay,
                )
            )
        )
    except Exception as e:
        return InternalServiceError(e)


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
