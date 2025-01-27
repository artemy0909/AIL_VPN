import asyncio
import logging
import sys


async def main() -> None:
    from loader import user_dp, service_dp, market_bot, service_bot
    from handler.bot import MARKET_ROUTERS, SERVICE_ROUTERS

    user_dp.include_routers(*MARKET_ROUTERS)
    service_dp.include_routers(*SERVICE_ROUTERS)
    await asyncio.gather(
        user_dp.start_polling(market_bot),
        service_dp.start_polling(service_bot)
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
