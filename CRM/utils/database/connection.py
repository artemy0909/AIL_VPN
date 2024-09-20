import logging
import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from zeep.exceptions import Fault

from .brom import *
from ..config import Config


class DatabaseError(BaseException):
    pass


class DatabaseErrorReport(BaseModel):
    module: str
    method: str
    args: list = None
    status: int = None
    message: str = None


class MethodReturn:

    def __init__(self, structure_1c: Структура):
        if not isinstance(structure_1c, Структура):
            raise DatabaseError("Server sent an incorrect response")

        self.result: any = structure_1c.result
        self.status: int = int(structure_1c.status)


@dataclass
class BromClientWrapper:
    brom_client = БромКлиент(Config.BROM_API_URL, Config.BROM_LOGIN, Config.BROM_PASSWORD)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def connection_is_working(self) -> bool:
        return self._call_method("ТестСоединения") is True

    def _call_method(self, method: str, *args) -> any:

        module = "СоединениеБром"

        method_return = None
        try:

            method_return = MethodReturn(self.brom_client.ВызватьМетод(module, method, *args))

            if method_return.status == 200:
                return method_return.result
            else:
                raise DatabaseError()

        except Fault or DatabaseError as e:

            if isinstance(e, Fault):
                status = 500
            elif isinstance(e, DatabaseError):
                if method_return is not None:
                    status = method_return.status
                else:
                    status = 501
            else:
                status = 500

            report = DatabaseErrorReport(
                module=module, method=method, args=args, status=status, message=e.message)

            file_name = f"{Config.ERROR_REPORTS_PATH}{uuid.uuid4()}.json"
            with open(file_name, "w") as f:
                f.write(report.model_dump_json())

            logging.error(f"Error (status {status}) on the server when executing the method '{method}'"
                          f", details in the file {file_name}")
