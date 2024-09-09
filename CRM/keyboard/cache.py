

class Delivery:
    tariff_guid: str
    amount: int
    currency: str
    currency_guid: str
    payment_method_guid: str


if __name__ == '__main__':
    pass
    # data_model = Delivery(
    #     tariff_guid="asdsad",
    #     amount=120000,
    #     currency="rub",
    #     currency_guid="asdasdsaujhafehufea",
    #     payment_method_guid="fdsakjsdfajksdfak"
    # )
    #
    # guid = data_model.save_data()
    # guid = "9d6eed93-6edd-476d-ba63-5b356dfc59d4"
    # loaded_data = Delivery().load_data(guid)
    # print(guid)
    # print(loaded_data)
