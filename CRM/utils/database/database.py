from . import call_method


def get_basic_tariffs_by_current_date():
    return call_method("СоединениеБром", "ПолучитьОсновнойПрайсЛистНаДату")
