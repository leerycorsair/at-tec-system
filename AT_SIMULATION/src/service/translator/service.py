import os
from typing import List, Tuple
import subprocess
import tempfile


from src.repository.minio.models.models import MinioFile
from src.service.translator.dependencies import IFileRepository, IModelService
from src.service.translator.main import trnsl_model
from src.service.translator.models.models import StagesEnum, TranslateInfo


class TranslatorService:
    def __init__(
        self,
        model_service: IModelService,
        file_repository: IFileRepository,
    ) -> None:
        self._model_service = model_service
        self._file_repository = file_repository

    def translate_model(
        self, model_id: int, user_id: int, file_name: str
    ) -> TranslateInfo:
        self._model_service.check_model_rights(model_id, user_id)
        model = self._model_service.get_model(model_id, user_id)
        rendered_model = trnsl_model(model)

        translate_logs = ""
        temporary_files = []
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".go",
                mode="w+",
                delete=False,
            ) as go_file:
                go_file.write(rendered_model)
                go_file.flush()
                go_file.close()
                temporary_files.append(go_file.name)

                # Stage 1: Formatting
                fmt_result, logs = self._run_formatting(go_file.name)
                translate_logs += logs
                if fmt_result != 0:
                    self._cleanup_files(temporary_files)
                    return TranslateInfo(
                        file_name="",
                        file_content=rendered_model,
                        translate_logs=translate_logs,
                        stage=StagesEnum.FORMATTING,
                    )

                # Stage 2: Building
                file_path = os.path.join(tempfile.gettempdir(), "compiled_program")
                build_result, logs = self._run_building(go_file.name, file_path)
                translate_logs += logs
                temporary_files.append(file_path)
                if build_result != 0:
                    self._cleanup_files(temporary_files)
                    return TranslateInfo(
                        file_name="",
                        file_content=rendered_model,
                        translate_logs=translate_logs,
                        stage=StagesEnum.BUILDING,
                    )

                # Stage 3: Linting
                lint_result, logs = self._run_linting(go_file.name)
                translate_logs += logs
                if lint_result != 0:
                    self._cleanup_files(temporary_files)
                    return TranslateInfo(
                        file_name="",
                        file_content=rendered_model,
                        translate_logs=translate_logs,
                        stage=StagesEnum.LINTING,
                    )

                # Stage 4: Upload
                storage_file_name = self._file_repository.load_file(
                    user_id, file_path, file_name, model.meta.id
                )
                translate_logs += "\nTranslation completed successfully."
                self._cleanup_files(temporary_files)

                return TranslateInfo(
                    file_name=storage_file_name,
                    file_content=rendered_model,
                    translate_logs=translate_logs,
                    stage=StagesEnum.COMPLETED,
                )

        except Exception as e:
            raise ValueError(e)

    def _run_formatting(self, file_path: str) -> Tuple[int, str]:
        try:
            result = subprocess.run(
                ["go", "fmt", file_path],
                capture_output=True,
                text=True,
                check=False,
            )
            logs = result.stdout + result.stderr
            return result.returncode, logs
        except Exception as e:
            return 1, f"Error during formatting: {str(e)}\n"

    def _run_building(self, file_path: str, output_path: str) -> Tuple[int, str]:
        try:
            result = subprocess.run(
                ["go", "build", "-o", output_path, file_path],
                capture_output=True,
                text=True,
                check=False,
            )
            logs = result.stdout + result.stderr
            return result.returncode, logs
        except Exception as e:
            return 1, f"Error during building: {str(e)}\n"

    def _run_linting(self, file_path: str) -> Tuple[int, str]:
        try:
            result = subprocess.run(
                ["golangci-lint", "run", file_path],
                capture_output=True,
                text=True,
                check=False,
            )
            logs = result.stdout + result.stderr
            return result.returncode, logs
        except Exception as e:
            return 1, f"Error during linting: {str(e)}\n"

    def _cleanup_files(self, files: list):
        for file in files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                pass

    def get_translated_files(self, user_id: int) -> List[MinioFile]:
        return self._file_repository.get_files(user_id)
