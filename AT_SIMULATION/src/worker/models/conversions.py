import json
from typing import List, Union

from src.repository.minio.models.models import MinioFile
from src.repository.model.models.models import ModelMetaDB
from src.service.processor.models.models import Process
from src.worker.models.models import (
    ProcessDict,
    ProcessStatusEnum,
    ResourceDict,
    TickDict,
    TranslatedFileDict,
    UsageIrregularEventDict,
    UsageOperationDict,
    UsageRuleDict,
)


def to_TranslatedFileDicts(
    files: List[MinioFile],
    models: List[ModelMetaDB],
) -> List[TranslatedFileDict]:
    models_map = {model.id: model.name for model in models}

    enriched_files: List[TranslatedFileDict] = [
        {
            "id": file.minio_name,
            "name": file.file_meta.file_name,
            "model_id": file.file_meta.model_id,
            "created_at": file.file_meta.created_at,
            "size": file.size,
            "model_name": models_map.get(file.file_meta.model_id, "Unknown"),
        }
        for file in files
    ]

    return enriched_files


def to_ProcessDict(process: Process) -> ProcessDict:
    return {
        "id": process.process_id,
        "name": process.process_name,
        "file_id": process.file_uuid,
        "status": ProcessStatusEnum(process.status),
        "current_tick": process.current_tick,
    }


def to_ProcessDicts(processes: List[Process]) -> List[ProcessDict]:
    return [to_ProcessDict(process) for process in processes]


def to_TickDict(raw_data: dict) -> TickDict:
    try:
        tick_data = TickDict(
            current_tick=raw_data.get("current_tick", 0),
            current_state=ProcessStatusEnum(raw_data.get("current_state")),
            resources=[
                ResourceDict(resource_name=resource["resource_name"])
                for resource in raw_data.get("resources", [])
            ],
            usages=[_parse_usage_dict(usage) for usage in raw_data.get("usages", [])],
        )
        return tick_data
    except json.JSONDecodeError as e:
        raise ValueError("Failed to decode JSON.") from e


def _parse_usage_dict(
    usage: dict,
) -> Union[UsageIrregularEventDict, UsageOperationDict, UsageRuleDict]:
    if "has_triggered_after" in usage or "has_triggered_before" in usage:
        return UsageOperationDict(
            has_triggered_after=usage.get("has_triggered_after", False),
            has_triggered_before=usage.get("has_triggered_before", False),
            usage_name=usage["usage_name"],
            usage_type=usage["usage_type"],
        )
    elif "has_triggered" in usage:
        return UsageRuleDict(
            has_triggered=usage["has_triggered"],
            usage_name=usage["usage_name"],
            usage_type=usage["usage_type"],
        )
    else:
        return UsageIrregularEventDict(
            has_triggered=usage["has_triggered"],
            usage_name=usage["usage_name"],
            usage_type=usage["usage_type"],
        )
