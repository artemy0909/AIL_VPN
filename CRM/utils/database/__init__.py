from model.views import PriceList, PriceItem, Invoice, InvoiceStatus, StartSubscriptionInfo
from .xenon import XenonClient
from ..config import Config


class Database(XenonClient):

    def get_basic_price_list(self) -> PriceList:
        response = self.get("pricelist")
        return PriceList.model_validate_json(response.text)

    def get_promo_code_info(self, promo_code: str) -> PriceList | None:
        response = self.get("promocode_info", promo_code=promo_code)
        if response.status_code == 204:
            return None
        else:
            return PriceList.model_validate_json(response.text)

    def create_counterparty(self):
        pass
        # self._call_method("СоздатьСессиюЕслиНовая")

    def create_invoice(self, telegram_id: int, selected_item: PriceItem, payment_method_id: str) -> Invoice:
        response = self.post("invoice",
                             telegram_id=telegram_id, selected_item=selected_item, payment_method_id=payment_method_id)
        if response.status_code == 201 or response.status_code == 200:
            return Invoice.model_validate_json(response.text)
        ...  # TODO: exceptions

    def check_invoice(self, invoice: Invoice) -> InvoiceStatus:
        response = self.get("invoice", invoice=invoice)
        return InvoiceStatus.model_validate_json(response.text)

    def payment_success(self, invoice: Invoice) -> StartSubscriptionInfo:
        response = self.post("payment", invoice=invoice)
        return StartSubscriptionInfo.model_validate_json(response.text)

    def check_user_exist(self, telegram_id: int, full_name: str):
        import re
        full_name = re.sub("[^A-Za-zА-Яа-я0-9\\s\\-.,$@*&?]", "", full_name)
        self.post("user", telegram_id=telegram_id, full_name=full_name)


database = Database(api_url=Config.XENON_API_URL, login=Config.XENON_LOGIN, password=Config.XENON_PASSWORD)
