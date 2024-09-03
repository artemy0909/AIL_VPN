import asyncio
import logging
import sys


async def main() -> None:
    from loader import user_dp, service_dp, market_bot, service_bot
    # from handlers import ROUTERS
    
    # from utils.database import get_all_subscriptions
    #
    # for subscription in get_all_subscriptions():
    #     scheduler.add_subscribe_alert(subscription.telegram_id, subscription.article)
    # asyncio.get_event_loop().create_task(scheduler.start())

    # dp.include_routers()
    await asyncio.gather(
        user_dp.start_polling(market_bot),
        service_dp.start_polling(service_bot)
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
