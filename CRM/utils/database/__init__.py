import logging

from pydantic import BaseModel
from zeep.exceptions import Fault

from .brom import *
from ..config import Config

brom_client = БромКлиент(Config.BROM_API_URL, Config.BROM_LOGIN, Config.BROM_PASSWORD)
brom_client.ЗагрузитьМетаданные("*")


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


def call_method(module: str, method: str, *args) -> any:
    method_return = None
    try:

        method_return = MethodReturn(brom_client.ВызватьМетод(module, method, *args))

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

        file_name = f"{Config.ERROR_REPORTS_PATH}{datetime.now()}.json"
        with open(file_name, "w") as f:
            f.write(report.model_dump_json())

        logging.error(f"Error (status {status}) on the server when executing the method '{method}'"
                      f", details in the file {file_name}")

    # todo уведомление админа об ошибке
