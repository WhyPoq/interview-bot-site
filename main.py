import asyncio
import generate_questions
import generate_website

async def main():
    await generate_questions.generate()
    generate_website.generate()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
