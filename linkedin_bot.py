import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pickle
import os
import random
import time
from datetime import datetime

import config
from utils import (
    print_success, print_error, print_warning, print_info, print_colored,
    human_delay, reading_delay, random_mouse_movement, calculate_pages,
    should_skip_randomly, log_application, build_search_url,
    extract_job_id_from_url, ApplicationStats, Colors
)

class LinkedInBot:
    def __init__(self):
        print_info("🤖 LinkedIn Auto Apply Bot Starting...")
        print_info(f"Target: {len(config.KEYWORDS)} keywords × {len(config.LOCATIONS)} locations")
        
        self.driver = None
        self.wait = None
        self.stats = ApplicationStats()
        self.cookies_file = "linkedin_cookies.pkl"
        
        self.setup_driver()
        self.login()
    
    def setup_driver(self):
        """Setup Chrome driver (undetected or regular based on config)"""
        print_info("Setting up browser...")
        
        if config.USE_UNDETECTED_CHROME:
            self._setup_undetected_chrome()
        else:
            self._setup_regular_chrome()
    
    def _setup_undetected_chrome(self):
        """Setup undetected Chrome driver"""
        print_info("Using Undetected Chrome (better detection avoidance)...")
        print_info("Your Chrome version: 141")
        
        options = uc.ChromeOptions()
        
        if config.HEADLESS_MODE:
            options.add_argument('--headless')
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')
        
        try:
            print_info("Starting Chrome browser (downloading correct driver if needed)...")
            self.driver = uc.Chrome(options=options, version_main=141, use_subprocess=True)
            self.wait = WebDriverWait(self.driver, 10)
            print_success("Browser ready!")
        except Exception as e:
            print_error(f"Failed to setup undetected Chrome: {str(e)}")
            print_warning("\n🔧 QUICK FIX:")
            print_warning("In config.py, change: USE_UNDETECTED_CHROME = False")
            print_warning("Then run the bot again (uses regular Chrome instead)")
            raise
    
    def _setup_regular_chrome(self):
        """Setup regular Chrome driver using webdriver-manager"""
        print_info("Using Regular Chrome (more compatible, slightly more detectable)...")
        
        options = webdriver.ChromeOptions()
        
        if config.HEADLESS_MODE:
            options.add_argument('--headless')
        
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        try:
            print_info("Downloading/updating ChromeDriver automatically...")
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            print_success("Browser ready!")
        except Exception as e:
            print_error(f"Failed to setup regular Chrome: {str(e)}")
            raise
    
    def load_cookies(self):
        """Load saved cookies"""
        if config.USE_SAVED_COOKIES and os.path.exists(self.cookies_file):
            try:
                self.driver.get("https://www.linkedin.com")
                human_delay(2, 3)
                
                cookies = pickle.load(open(self.cookies_file, "rb"))
                for cookie in cookies:
                    if 'sameSite' in cookie and cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                        cookie['sameSite'] = 'None'
                    self.driver.add_cookie(cookie)
                
                print_success("Loaded saved cookies")
                return True
            except Exception as e:
                print_warning(f"Could not load cookies: {str(e)}")
                return False
        return False
    
    def save_cookies(self):
        """Save cookies for next session"""
        try:
            pickle.dump(self.driver.get_cookies(), open(self.cookies_file, "wb"))
            print_success("Cookies saved for next session")
        except Exception as e:
            print_warning(f"Could not save cookies: {str(e)}")
    
    def is_logged_in(self):
        """Check if already logged in"""
        try:
            self.driver.get("https://www.linkedin.com/feed")
            human_delay(3, 4)
            
            # Check for navigation bar (only visible when logged in)
            self.driver.find_element(By.CSS_SELECTOR, "nav.global-nav")
            print_success("Already logged in!")
            return True
        except:
            return False
    
    def login(self):
        """Login to LinkedIn"""
        print_info("Logging into LinkedIn...")
        
        # Try loading cookies first
        if self.load_cookies() and self.is_logged_in():
            return
        
        # Manual login
        try:
            self.driver.get("https://www.linkedin.com/login")
            human_delay(3, 5)
            
            # Enter credentials
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.send_keys(config.LINKEDIN_EMAIL)
            human_delay(1, 2)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(config.LINKEDIN_PASSWORD)
            human_delay(1, 2)
            
            # Click login button
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()
            
            print_warning("⏳ Waiting for login... (handle CAPTCHA if needed)")
            human_delay(15, 20)
            
            # Verify login
            if self.is_logged_in():
                self.save_cookies()
                print_success("Login successful!")
            else:
                print_error("Login may have failed. Please check manually.")
                human_delay(10, 15)
                
        except Exception as e:
            print_error(f"Login error: {str(e)}")
            print_warning("Please login manually in the browser window")
            human_delay(30, 35)
    
    def get_job_details(self):
        """Extract job details from current page"""
        job_data = {
            'title': 'Unknown',
            'company': 'Unknown',
            'location': 'Unknown',
            'url': self.driver.current_url
        }
        
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.job-title").text
            job_data['title'] = title.strip()
        except:
            try:
                title = self.driver.find_element(By.CSS_SELECTOR, "h1.jobs-unified-top-card__job-title").text
                job_data['title'] = title.strip()
            except:
                pass
        
        try:
            company = self.driver.find_element(By.CSS_SELECTOR, "a.job-card-container__company-name").text
            job_data['company'] = company.strip()
        except:
            try:
                company = self.driver.find_element(By.CSS_SELECTOR, "span.jobs-unified-top-card__company-name").text
                job_data['company'] = company.strip()
            except:
                pass
        
        try:
            location = self.driver.find_element(By.CSS_SELECTOR, "span.jobs-unified-top-card__bullet").text
            job_data['location'] = location.strip()
        except:
            pass
        
        return job_data
    
    def is_blacklisted(self, job_data):
        """Check if job should be skipped"""
        title_lower = job_data['title'].lower()
        company_lower = job_data['company'].lower()
        
        for blacklist_word in config.BLACKLIST_TITLES:
            if blacklist_word.lower() in title_lower:
                return True, f"Title contains '{blacklist_word}'"
        
        for blacklist_company in config.BLACKLIST_COMPANIES:
            if blacklist_company.lower() in company_lower:
                return True, f"Company is '{blacklist_company}'"
        
        return False, ""
    
    def select_resume(self):
        """Select resume if required"""
        try:
            resumes = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='ui-attachment']")
            
            if resumes and len(resumes) > config.PREFERRED_RESUME_INDEX:
                target_resume = resumes[config.PREFERRED_RESUME_INDEX]
                if "select this resume" in target_resume.get_attribute("aria-label").lower():
                    target_resume.click()
                    human_delay(1, 2)
                    print_info(f"Selected resume #{config.PREFERRED_RESUME_INDEX + 1}")
        except:
            pass  # No resume selection needed
    
    def click_easy_apply(self):
        """Click the Easy Apply button - tries multiple selectors"""
        try:
            # Wait a bit for page to load
            human_delay(2, 3)
            
            if config.DEBUG_MODE:
                print_info("Looking for Easy Apply button...")
            
            # Try multiple selectors based on actual LinkedIn HTML
            selectors = [
                # EXACT match from your screenshot
                ("CSS", "button#jobs-apply-button"),
                ("CSS", "button.jobs-apply-button"),
                
                # Class combinations from your HTML
                ("CSS", "button.jobs-apply-button.artdeco-button"),
                ("CSS", "button.artdeco-button.jobs-apply-button"),
                ("CSS", "button[id='jobs-apply-button']"),
                
                # Generic artdeco button patterns
                ("CSS", "button.artdeco-button[aria-label*='Easy Apply']"),
                ("CSS", "button.artdeco-button[aria-label*='easy apply']"),
                
                # Broader searches
                ("CSS", "button[class*='jobs-apply-button']"),
                ("CSS", "div.jobs-apply-button--top-card button"),
                ("CSS", ".jobs-apply-button--top-card button"),
                
                # XPath alternatives
                ("XPATH", "//button[@id='jobs-apply-button']"),
                ("XPATH", "//button[contains(@class, 'jobs-apply-button')]"),
                ("XPATH", "//button[contains(@class, 'artdeco-button') and contains(@class, 'jobs-apply-button')]"),
                ("XPATH", "//button[contains(text(), 'Easy Apply')]"),
                ("XPATH", "//button[contains(@aria-label, 'Easy Apply')]"),
            ]
            
            for selector_type, selector in selectors:
                try:
                    if config.DEBUG_MODE:
                        print_info(f"Trying: {selector_type} = {selector}")
                    
                    # Find elements
                    if selector_type == "XPATH":
                        buttons = self.driver.find_elements(By.XPATH, selector)
                    else:
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if config.DEBUG_MODE and len(buttons) > 0:
                        print_success(f"Found {len(buttons)} button(s) with this selector!")
                    
                    for button in buttons:
                        try:
                            # Check if button is visible
                            if not button.is_displayed():
                                if config.DEBUG_MODE:
                                    print_warning("Button found but not visible, skipping...")
                                continue
                            
                            button_text = button.text.strip().lower()
                            aria_label = (button.get_attribute("aria-label") or "").lower()
                            button_class = (button.get_attribute("class") or "").lower()
                            button_id = (button.get_attribute("id") or "").lower()
                            
                            if config.DEBUG_MODE:
                                print_info(f"Button details:")
                                print_info(f"  - Text: '{button_text}'")
                                print_info(f"  - Aria-label: '{aria_label}'")
                                print_info(f"  - Class: '{button_class}'")
                                print_info(f"  - ID: '{button_id}'")
                            
                            # Check if already applied
                            if ("applied" in button_text or 
                                "applied" in aria_label or
                                "applied" in button_class):
                                print_info("Already applied to this job")
                                return False, "Already applied"
                            
                            # Check if it's Easy Apply button
                            # Match based on ID, class, text, or aria-label
                            is_easy_apply = (
                                button_id == "jobs-apply-button" or
                                "jobs-apply-button" in button_class or
                                "easy apply" in button_text or
                                "easy apply" in aria_label
                            )
                            
                            if is_easy_apply:
                                if config.DEBUG_MODE:
                                    print_success("This is the Easy Apply button!")
                                
                                # Scroll to button to ensure it's in view
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                                human_delay(0.5, 1)
                                
                                # Try to click
                                try:
                                    if config.DEBUG_MODE:
                                        print_info("Attempting to click...")
                                    button.click()
                                    if config.DEBUG_MODE:
                                        print_success("Regular click successful!")
                                except Exception as click_error:
                                    if config.DEBUG_MODE:
                                        print_warning(f"Regular click failed: {click_error}")
                                        print_info("Trying JavaScript click...")
                                    # If regular click fails, try JavaScript click
                                    self.driver.execute_script("arguments[0].click();", button)
                                    if config.DEBUG_MODE:
                                        print_success("JavaScript click successful!")
                                
                                human_delay(2, 3)
                                print_success("✅ Clicked Easy Apply button!")
                                return True, "Clicked Easy Apply"
                            else:
                                if config.DEBUG_MODE:
                                    print_warning("Button found but not Easy Apply, continuing search...")
                                    
                        except Exception as button_error:
                            if config.DEBUG_MODE:
                                print_warning(f"Error processing this button: {str(button_error)}")
                            continue
                            
                except Exception as selector_error:
                    if config.DEBUG_MODE:
                        print_warning(f"Error with selector '{selector}': {str(selector_error)}")
                    continue
            
            # If we get here, no Easy Apply button found
            print_warning("❌ No Easy Apply button found after trying all selectors")
            if config.DEBUG_MODE:
                print_info("This job might not have Easy Apply enabled")
                print_info("Or LinkedIn may have changed their HTML structure")
            
            return False, "No Easy Apply button found"
            
        except Exception as e:
            print_error(f"Error in click_easy_apply: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def fill_application(self):
        """Fill and submit the application"""
        try:
            max_attempts = 10
            current_step = 0
            
            while current_step < max_attempts:
                human_delay(2, 3)
                
                # Select resume if needed
                self.select_resume()
                
                # Look for submit button
                try:
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Submit application']")
                    
                    # Unfollow company if configured
                    if not config.FOLLOW_COMPANIES:
                        try:
                            follow_checkbox = self.driver.find_element(By.CSS_SELECTOR, "label[for*='follow-company']")
                            follow_checkbox.click()
                            human_delay(0.5, 1)
                        except:
                            pass
                    
                    if config.DRY_RUN:
                        print_warning("DRY RUN: Would have submitted application")
                        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Dismiss']").click()
                        return True, "Dry run - not submitted"
                    
                    # Submit
                    submit_btn.click()
                    human_delay(2, 3)
                    print_success("Application submitted!")
                    return True, "Success"
                    
                except NoSuchElementException:
                    pass
                
                # Look for Next/Continue button
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Continue'], button[aria-label*='next']")
                    next_btn.click()
                    current_step += 1
                    human_delay(2, 3)
                    
                except NoSuchElementException:
                    # Look for Review button
                    try:
                        review_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Review']")
                        review_btn.click()
                        human_delay(2, 3)
                    except:
                        # Can't proceed - probably requires manual input
                        print_warning("Application requires manual input")
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Dismiss']").click()
                        except:
                            pass
                        return False, "Requires manual input"
            
            return False, "Too many steps - likely requires manual input"
            
        except Exception as e:
            print_error(f"Error in application: {str(e)}")
            try:
                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Dismiss']").click()
            except:
                pass
            return False, f"Error: {str(e)}"
    
    def apply_to_job(self, job_url):
        """Apply to a single job"""
        try:
            self.driver.get(job_url)
            human_delay(3, 5)
            
            # Get job details
            job_data = self.get_job_details()
            self.stats.total_viewed += 1
            
            print_info(f"\n{'='*60}")
            print_info(f"Job #{self.stats.total_viewed}: {job_data['title']}")
            print_info(f"Company: {job_data['company']}")
            print_info(f"Location: {job_data['location']}")
            print_info(f"URL: {job_url}")
            print_info(f"{'='*60}")
            
            # Debug screenshot
            if config.DEBUG_MODE:
                try:
                    os.makedirs('debug_screenshots', exist_ok=True)
                    screenshot_path = f"debug_screenshots/job_{self.stats.total_viewed}.png"
                    self.driver.save_screenshot(screenshot_path)
                    print_info(f"Debug screenshot saved: {screenshot_path}")
                except:
                    pass
            
            # Check blacklist
            is_blacklisted, reason = self.is_blacklisted(job_data)
            if is_blacklisted:
                print_warning(f"⛔ Skipped - Blacklisted: {reason}")
                self.stats.blacklisted += 1
                log_application(job_data, f"BLACKLISTED: {reason}")
                return
            
            # Random skip (to appear more human)
            if should_skip_randomly(config.SKIP_PROBABILITY):
                print_warning("⏭️  Randomly skipped (human behavior)")
                self.stats.skipped += 1
                log_application(job_data, "SKIPPED: Random")
                return
            
            # Simulate reading
            reading_delay(config.READING_TIME_MIN, config.READING_TIME_MAX)
            random_mouse_movement()
            
            # Click Easy Apply
            clicked, message = self.click_easy_apply()
            
            if not clicked:
                if "already applied" in message.lower():
                    print_colored("✓ Already applied to this job", Colors.BLUE)
                    self.stats.already_applied += 1
                    log_application(job_data, "ALREADY APPLIED")
                else:
                    print_warning(f"Skipped: {message}")
                    self.stats.skipped += 1
                    log_application(job_data, f"SKIPPED: {message}")
                    
                    # Take screenshot for debugging
                    if config.DEBUG_MODE:
                        try:
                            screenshot_path = f"debug_screenshots/no_easy_apply_{self.stats.total_viewed}.png"
                            self.driver.save_screenshot(screenshot_path)
                            print_info(f"Debug screenshot saved: {screenshot_path}")
                        except:
                            pass
                return
            
            # Fill and submit application
            success, result = self.fill_application()
            
            if success:
                print_success(f"✅ Successfully applied!")
                self.stats.applied += 1
                log_application(job_data, "APPLIED - SUCCESS")
                
                if config.SAVE_SCREENSHOTS:
                    try:
                        screenshot_name = f"screenshots/applied_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        os.makedirs('screenshots', exist_ok=True)
                        self.driver.save_screenshot(screenshot_name)
                    except:
                        pass
            else:
                print_warning(f"⚠️  Application incomplete: {result}")
                self.stats.failed += 1
                log_application(job_data, f"FAILED: {result}")
            
        except Exception as e:
            print_error(f"Error applying to job: {str(e)}")
            self.stats.failed += 1
    
    def search_and_apply(self):
        """Main search and apply loop"""
        print_info("\n🚀 Starting job application process...\n")
        
        # Generate search URLs
        search_urls = []
        for location in config.LOCATIONS:
            for keyword in config.KEYWORDS:
                url = build_search_url(keyword, location, config)
                search_urls.append((keyword, location, url))
        
        # Randomize if configured
        if config.RANDOMIZE_JOB_ORDER:
            random.shuffle(search_urls)
        
        print_info(f"Generated {len(search_urls)} search combinations")
        
        for keyword, location, search_url in search_urls:
            print_info(f"\n{'#'*60}")
            print_info(f"Searching: {keyword} in {location}")
            print_info(f"{'#'*60}\n")
            
            try:
                self.driver.get(search_url)
                human_delay(5, 7)
                
                # Get total jobs
                try:
                    total_text = self.driver.find_element(By.CSS_SELECTOR, "small.jobs-search-results-list__text").text
                    print_info(f"Found: {total_text}")
                except:
                    print_warning("Could not determine total jobs")
                
                # Scroll and collect job links
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "li[data-occludable-job-id]")
                
                job_urls = []
                for card in job_cards[:config.MAX_APPLICATIONS_PER_RUN]:
                    try:
                        job_id = card.get_attribute("data-occludable-job-id").split(":")[-1]
                        job_urls.append(f"https://www.linkedin.com/jobs/view/{job_id}")
                    except:
                        continue
                
                print_info(f"Processing {len(job_urls)} jobs from this search")
                
                # Apply to each job
                for job_url in job_urls:
                    if self.stats.applied >= config.MAX_APPLICATIONS_PER_RUN:
                        print_warning(f"\n⚠️  Reached maximum applications limit ({config.MAX_APPLICATIONS_PER_RUN})")
                        print_warning("Stopping to avoid detection. Run again later!")
                        self.stats.print_summary()
                        return
                    
                    self.apply_to_job(job_url)
                    
                    # Human-like delay between applications
                    if self.stats.applied < config.MAX_APPLICATIONS_PER_RUN:
                        delay = random.uniform(config.MIN_DELAY, config.MAX_DELAY)
                        print_info(f"⏱️  Waiting {delay:.1f}s before next job...")
                        time.sleep(delay)
                
            except Exception as e:
                print_error(f"Error in search: {str(e)}")
                continue
        
        print_success("\n✅ Completed all searches!")
        self.stats.print_summary()
    
    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                print_success("Browser closed")
        except:
            pass

def main():
    """Main entry point"""
    bot = None
    try:
        # Validate config
        if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
            print_error("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
            return
        
        # Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Start bot
        bot = LinkedInBot()
        bot.search_and_apply()
        
    except KeyboardInterrupt:
        print_warning("\n\n⚠️  Bot stopped by user")
        if bot:
            bot.stats.print_summary()
    except Exception as e:
        print_error(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if bot:
            bot.close()

if __name__ == "__main__":
    print_colored("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        🤖 LINKEDIN AUTO APPLY BOT v2.0 🤖                ║
    ║                                                           ║
    ║  Built with: Undetected ChromeDriver                      ║
    ║  Features: Human-like behavior, Smart detection avoidance ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Colors.CYAN)
    
    print_warning("\n⚠️  IMPORTANT DISCLAIMERS:")
    print_warning("1. Use at your own risk - LinkedIn prohibits automation")
    print_warning("2. Start with DRY_RUN=True to test safely")
    print_warning("3. Keep MAX_APPLICATIONS_PER_RUN low (20-30)")
    print_warning("4. Don't run multiple times per day")
    print_warning("5. Your account could be restricted\n")
    
    response = input("Do you understand the risks and want to continue? (yes/no): ")
    if response.lower() == 'yes':
        main()
    else:
        print_info("Bot cancelled. Stay safe!")