import os
import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_jobs(keyword="Frontend Developer", location="India", pages=10, output="jobs.csv"):
    user = os.getenv("LINKEDIN_USER")
    password = os.getenv("LINKEDIN_PASS")
    if not user or not password:
        raise RuntimeError("Please set LINKEDIN_USER and LINKEDIN_PASS")

    async with async_playwright() as p:
        # Launch browser with anti-detection measures
        browser = await p.chromium.launch(
            headless=False,  # Use visible browser to avoid detection
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Create context with realistic user agent and viewport
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        page = await context.new_page()
        
        # Add stealth measures
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        # --- Login ---
        await page.goto("https://www.linkedin.com/login")
        await page.wait_for_timeout(2000)  # Wait for page to load
        
        # Human-like typing
        await page.fill("#username", user)
        await page.wait_for_timeout(1000)
        await page.fill("#password", password)
        await page.wait_for_timeout(1000)
        await page.press("#password", "Enter")
        await page.wait_for_timeout(8000)  # Longer wait for login

        # Navigate to jobs search
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        print(f"🔗 Navigating to: {search_url}")
        await page.goto(search_url)
        await page.wait_for_timeout(8000)  # Longer wait
        
        # Debug: Check what's on the page
        print("🔍 Debugging page content...")
        page_title = await page.title()
        print(f"Page title: {page_title}")
        
        # Wait longer for dynamic content to load
        print("⏳ Waiting for dynamic content to load...")
        await page.wait_for_timeout(10000)
        
        # Try scrolling to trigger content loading
        print("📜 Scrolling to trigger content loading...")
        await page.evaluate("window.scrollTo(0, 500)")
        await page.wait_for_timeout(3000)
        await page.evaluate("window.scrollTo(0, 1000)")
        await page.wait_for_timeout(3000)
        
        # Check for different possible selectors (updated for current LinkedIn)
        debug_selectors = [
            ".job-card-container",
            ".jobs-search-results__list-item", 
            ".job-card-list__title",
            "[data-job-id]",
            ".jobs-search-results",
            ".jobs-search-results-list",
            ".jobs-search-results-list__list-item",
            ".job-card-list__title",
            ".job-card-container__company-name",
            ".job-card-container__metadata-item",
            "li[data-job-id]",
            ".job-card",
            ".job-search-card",
            "[data-test-id='job-card']",
            ".jobs-search-results__list-item"
        ]
        
        for selector in debug_selectors:
            elements = await page.query_selector_all(selector)
            print(f"Selector '{selector}': {len(elements)} elements found")
            if len(elements) > 0:
                print(f"  ✅ Found {len(elements)} elements with selector: {selector}")
                break
        
        # Check if we're on a login page or blocked
        if "login" in page_title.lower() or "sign in" in page_title.lower():
            print("❌ Redirected to login page - authentication may have failed")
            return
        
        # Check for any error messages
        error_elements = await page.query_selector_all("[class*='error'], [class*='blocked'], [class*='captcha']")
        if error_elements:
            print(f"⚠️ Found {len(error_elements)} potential error elements")
        
        # Take a screenshot for debugging
        try:
            await page.screenshot(path="debug_screenshot.png")
            print("📸 Screenshot saved as debug_screenshot.png")
        except Exception as e:
            print(f"Could not take screenshot: {e}")

        jobs = []
        all_job_cards = set()  # Use set to avoid duplicates

        for page_no in range(pages):
            print(f"Scraping page {page_no+1} of {pages}...")

            # Enhanced scrolling strategy to load more jobs
            previous_count = 0
            no_change_count = 0
            
            for scroll_attempt in range(10):  # More scroll attempts
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                
                # Check if more jobs loaded
                current_cards = await page.query_selector_all(".job-search-card")
                print(f"  Scroll {scroll_attempt+1}: Found {len(current_cards)} total job cards")
                
                # If no new jobs loaded in last 3 scrolls, break
                if scroll_attempt > 2 and len(current_cards) == previous_count:
                    no_change_count += 1
                    if no_change_count >= 3:
                        print(f"  No new jobs loaded for {no_change_count} consecutive scrolls, stopping")
                        break
                else:
                    no_change_count = 0
                    
                previous_count = len(current_cards)

            # Get all job cards on the page
            job_cards = await page.query_selector_all(".job-search-card")
            print(f'Found {len(job_cards)} job cards total')

            if len(job_cards) == 0:
                print(f"No job cards found. Stopping.")
                break

            # Process all job cards and avoid duplicates
            new_jobs_count = 0
            for card in job_cards:
                # Create a unique identifier for each job card
                card_html = await card.inner_html()
                if card_html not in all_job_cards:
                    all_job_cards.add(card_html)
                    new_jobs_count += 1
                    
                    # Try multiple selectors for each field
                    title = None
                    company = None
                    location = None
                    link = None
                    
                    # Title selectors (updated for .job-search-card)
                    title_selectors = [
                        "h3 a span",
                        "h3 span", 
                        "a span",
                        ".job-search-card__title",
                        ".job-card-list__title",
                        "h3",
                        "h4",
                        "a[data-control-name='job_card_click'] span"
                    ]
                    
                    for sel in title_selectors:
                        elem = await card.query_selector(sel)
                        if elem:
                            title = await elem.inner_text()
                            break
                    
                    # Company selectors (updated for .job-search-card)
                    company_selectors = [
                        ".job-search-card__company-name",
                        ".job-search-card__company",
                        "h4 a",
                        ".job-card-container__company-name",
                        "a[data-control-name='job_card_company']",
                        ".job-card-container__metadata-wrapper a",
                        "a[href*='/company/']"
                    ]
                    
                    for sel in company_selectors:
                        elem = await card.query_selector(sel)
                        if elem:
                            company = await elem.inner_text()
                            break
                    
                    # If no company found with selectors, try to find it in spans
                    if not company:
                        spans = await card.query_selector_all("span")
                        for span in spans:
                            text = await span.inner_text()
                            # Look for spans that might be company names (not too long, not location-like)
                            if text and len(text) < 50 and not any(word in text.lower() for word in ['india', 'remote', 'hybrid', 'on-site', 'promoted', 'developer', 'engineer']):
                                company = text
                                break
                    
                    # Location selectors (updated for .job-search-card)
                    location_selectors = [
                        ".job-search-card__location",
                        ".job-search-card__metadata",
                        ".job-card-container__metadata-item",
                        ".job-card-container__metadata-wrapper span",
                        "span[title]"
                    ]
                    
                    for sel in location_selectors:
                        elem = await card.query_selector(sel)
                        if elem:
                            location = await elem.inner_text()
                            break
                    
                    # Link selectors (updated for .job-search-card)
                    link_selectors = [
                        "h3 a",
                        "h4 a",
                        "a[data-control-name='job_card_click']",
                        "a[data-control-name='job_card_title']",
                        "a[href*='/jobs/view/']",
                        ".job-search-card a"
                    ]
                    
                    for sel in link_selectors:
                        elem = await card.query_selector(sel)
                        if elem:
                            link = await elem.get_attribute("href")
                            break

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "link": link
                    })
            
            print(f"  Processed {new_jobs_count} new jobs (total unique: {len(jobs)})")

            # Add a small delay between pages to be respectful to LinkedIn
            if page_no < pages - 1:
                await page.wait_for_timeout(2000)

        await browser.close()

        # --- Save to CSV ---
        df = pd.DataFrame(jobs)
        df.to_csv(output, index=False, encoding="utf-8")
        print(f"✅ Scraping completed! Saved {len(jobs)} jobs from {page_no+1} pages to {output}")
        
        # Print summary
        if len(jobs) > 0:
            print(f"\n📊 Summary:")
            print(f"   Total jobs scraped: {len(jobs)}")
            print(f"   Pages processed: {page_no+1}")
            print(f"   Average jobs per page: {len(jobs)/(page_no+1):.1f}")
            
            # Show unique companies
            companies = df['company'].dropna().unique()
            print(f"   Unique companies: {len(companies)}")
            if len(companies) > 0:
                print(f"   Sample companies: {', '.join(companies[:5])}")
        else:
            print("❌ No jobs were scraped. Please check your search criteria or LinkedIn login.")


# Run it
async def main():
    print("🚀 Starting comprehensive LinkedIn job scraping for 1000+ jobs...")
    
    # Test with a smaller subset first
    search_terms = [
        "Software Engineer", "Python Developer", "React Developer", 
        "Java Developer", "Data Scientist", "DevOps Engineer",
        "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "Machine Learning Engineer"
    ]
    
    # Test with fewer locations first
    locations = [
        "India", "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune"
    ]
    
    all_jobs = []
    total_searches = 0
    
    print(f"📋 Planning to search {len(search_terms)} terms across {len(locations)} locations")
    print(f"🎯 Target: 1000+ unique jobs")
    
    for i, term in enumerate(search_terms):
        print(f"\n🔍 [{i+1}/{len(search_terms)}] Searching for: {term}")
        term_jobs = []
        
        # Search in multiple locations for each term
        for j, location in enumerate(locations[:4]):  # Limit to top 4 locations for testing
            print(f"  📍 [{j+1}/4] Location: {location}")
            temp_file = f"temp_{term.replace(' ', '_').lower()}_{location.lower()}.csv"
            
            try:
                # Scrape 2 pages per location for more jobs
                await scrape_jobs(term, location, pages=2, output=temp_file)
                
                # Read and process results
                df = pd.read_csv(temp_file)
                if len(df) > 0:
                    term_jobs.append(df)
                    print(f"    ✅ Found {len(df)} jobs for '{term}' in {location}")
                else:
                    print(f"    ⚠️ No jobs found for '{term}' in {location}")
                
                # Clean up temp file
                os.remove(temp_file)
                
                # Delay between location searches
                await asyncio.sleep(3)
                total_searches += 1
                
            except Exception as e:
                print(f"    ❌ Error searching '{term}' in {location}: {e}")
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        # Combine results for this term
        if term_jobs:
            combined_term_df = pd.concat(term_jobs, ignore_index=True)
            combined_term_df = combined_term_df.drop_duplicates(subset=['link'], keep='first')
            all_jobs.append(combined_term_df)
            print(f"  ✅ Total unique jobs for '{term}': {len(combined_term_df)}")
        else:
            print(f"  ❌ No jobs found for '{term}'")
        
        # Delay between search terms
        await asyncio.sleep(5)
        
        # Show progress
        current_total = sum(len(df) for df in all_jobs)
        print(f"  📊 Running total: {current_total} unique jobs")
    
    # Combine all results
    if all_jobs:
        print(f"\n🔄 Combining results from {len(all_jobs)} search terms...")
        combined_df = pd.concat(all_jobs, ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['link'], keep='first')
        
        # Save final results
        combined_df.to_csv("linkedin_jobs.csv", index=False)
        
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"✅ Total unique jobs collected: {len(combined_df)}")
        print(f"🔍 Total searches performed: {total_searches}")
        print(f"📁 Results saved to: linkedin_jobs.csv")
        
        # Detailed summary
        print(f"\n📊 DETAILED SUMMARY:")
        companies = combined_df['company'].dropna().unique()
        print(f"   🏢 Unique companies: {len(companies)}")
        
        locations_found = combined_df['location'].dropna().unique()
        print(f"   📍 Unique locations: {len(locations_found)}")
        
        # Top companies
        top_companies = combined_df['company'].value_counts().head(10)
        print(f"\n🏆 TOP 10 COMPANIES:")
        for company, count in top_companies.items():
            print(f"   {company}: {count} jobs")
        
        # Top locations
        top_locations = combined_df['location'].value_counts().head(10)
        print(f"\n🌍 TOP 10 LOCATIONS:")
        for location, count in top_locations.items():
            print(f"   {location}: {count} jobs")
            
        if len(combined_df) >= 1000:
            print(f"\n🎯 TARGET ACHIEVED! Collected {len(combined_df)} jobs (target: 1000+)")
        else:
            print(f"\n⚠️ Target not reached. Collected {len(combined_df)} jobs (target: 1000+)")
            print("💡 Consider running again or adding more search terms")
    else:
        print("\n❌ No jobs found across all searches")

asyncio.run(main())
