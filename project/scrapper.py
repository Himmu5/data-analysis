import os
import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_jobs(keyword="Frontend Developer", location="India", pages=1, output="jobs.csv"):
    user = os.getenv("LINKEDIN_USER")
    password = os.getenv("LINKEDIN_PASS")
    if not user or not password:
        raise RuntimeError("Please set LINKEDIN_USER and LINKEDIN_PASS")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # set True for headless
        context = await browser.new_context()
        page = await context.new_page()

        # --- Login ---
        await page.goto("https://www.linkedin.com/login")
        await page.fill("#username", user)
        await page.fill("#password", password)
        await page.press("#password", "Enter")
        await page.wait_for_timeout(5000)

        # --- Navigate to jobs search ---
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        await page.goto(search_url)
        await page.wait_for_timeout(5000)

        jobs = []

        for page_no in range(pages):
            print(f"Scraping page {page_no+1}...")

            # Grab all job cards
            job_cards = await page.query_selector_all(".jobs-search-results__list-item")
            print('job_cards: ', job_cards)

            for card in job_cards:
                title = await card.query_selector_eval("a.job-card-list__title", "el => el.innerText") if await card.query_selector("a.job-card-list__title") else None
                company = await card.query_selector_eval(".job-card-container__company-name", "el => el.innerText") if await card.query_selector(".job-card-container__company-name") else None
                loc = await card.query_selector_eval(".job-card-container__metadata-item", "el => el.innerText") if await card.query_selector(".job-card-container__metadata-item") else None
                link = await card.query_selector_eval("a.job-card-list__title", "el => el.href") if await card.query_selector("a.job-card-list__title") else None

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "link": link
                })

            # --- Next page if available ---
            next_btn = await page.query_selector("button[aria-label='Next']")
            if next_btn:
                await next_btn.click()
                await page.wait_for_timeout(5000)
            else:
                break

        await browser.close()

        # --- Save to CSV ---
        df = pd.DataFrame(jobs)
        df.to_csv(output, index=False, encoding="utf-8")
        print(f"✅ Saved {len(jobs)} jobs to {output}")


# Run it
async def main():
    await scrape_jobs("Frontend Developer", "India", pages=2, output="linkedin_jobs.csv")

asyncio.run(main())
