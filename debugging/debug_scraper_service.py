import asyncio
from app.services.scraper_service import ScraperService


async def main():
    print("Testing Scraper...")
    heroes = await ScraperService.get_all_ids()

    for hero in heroes[:5]:
        print(f"ID: {hero['id']} - Name: {hero['name']}")

    print(f"Total heroes found: {len(heroes)}")


if __name__ == "__main__":
    """
    Test in the terminal using `python -m debugging.debug_scraper_service`
    """
    asyncio.run(main())
