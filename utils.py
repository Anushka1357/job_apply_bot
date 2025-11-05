import time
import random
import math
import pyautogui
from datetime import datetime
from typing import List, Tuple

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_colored(text: str, color: str):
    """Print colored text to console"""
    print(f"{color}{text}{Colors.END}")

def print_success(text: str):
    print_colored(f"✅ {text}", Colors.GREEN)

def print_error(text: str):
    print_colored(f"❌ {text}", Colors.RED)

def print_warning(text: str):
    print_colored(f"⚠️  {text}", Colors.YELLOW)

def print_info(text: str):
    print_colored(f"ℹ️  {text}", Colors.CYAN)

def human_delay(min_seconds: float = 2, max_seconds: float = 5):
    """Simulate human-like delay with random timing"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def reading_delay(min_seconds: float = 10, max_seconds: float = 25):
    """Simulate time spent reading job description"""
    delay = random.uniform(min_seconds, max_seconds)
    print_info(f"Reading job description for {delay:.1f} seconds...")
    time.sleep(delay)

def random_mouse_movement():
    """Add random mouse movements to appear more human"""
    try:
        current_x, current_y = pyautogui.position()
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-100, 100)
        duration = random.uniform(0.5, 1.5)
        pyautogui.moveTo(current_x + offset_x, current_y + offset_y, duration=duration)
    except:
        pass  # Fail silently if mouse control isn't available

def calculate_pages(total_jobs: str, jobs_per_page: int = 25) -> int:
    """Calculate number of pages from total jobs string"""
    try:
        if ' ' in total_jobs:
            space_index = total_jobs.index(' ')
            total = total_jobs[0:space_index].replace(',', '')
            total_int = int(total)
            pages = math.ceil(total_int / jobs_per_page)
            return min(pages, 40)  # Max 40 pages for safety
        else:
            return int(total_jobs)
    except:
        return 1

def should_skip_randomly(probability: float = 0.15) -> bool:
    """Randomly decide to skip a job (makes behavior more human)"""
    return random.random() < probability

def log_application(job_data: dict, status: str):
    """Log application results to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"applications_{datetime.now().strftime('%Y%m%d')}.txt"
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            log_entry = (
                f"\n[{timestamp}] {status}\n"
                f"Title: {job_data.get('title', 'N/A')}\n"
                f"Company: {job_data.get('company', 'N/A')}\n"
                f"Location: {job_data.get('location', 'N/A')}\n"
                f"URL: {job_data.get('url', 'N/A')}\n"
                f"{'-'*80}\n"
            )
            f.write(log_entry)
    except Exception as e:
        print_error(f"Failed to log application: {str(e)}")

def build_search_url(keyword: str, location: str, config) -> str:
    """Build LinkedIn job search URL with filters - Python 3.8 compatible"""
    base_url = "https://www.linkedin.com/jobs/search/"
    
    # Start with Easy Apply filter
    params = ["f_AL=true"]
    
    # Add keywords and location
    params.append(f"keywords={keyword.replace(' ', '%20')}")
    params.append(f"location={location.replace(' ', '%20')}")
    
    # Add location GeoID if continent (using if-elif instead of match)
    location_lower = location.lower()
    if location_lower == "asia":
        params.append("geoId=102393603")
    elif location_lower == "europe":
        params.append("geoId=100506914")
    elif location_lower in ["north america", "northamerica"]:
        params.append("geoId=102221843")
    elif location_lower in ["south america", "southamerica"]:
        params.append("geoId=104514572")
    elif location_lower == "australia":
        params.append("geoId=101452733")
    elif location_lower == "africa":
        params.append("geoId=103537801")
    
    # Add experience levels (using if-elif instead of match)
    if config.EXPERIENCE_LEVELS:
        exp_codes = []
        for level in config.EXPERIENCE_LEVELS:
            if level == "Internship":
                exp_codes.append("1")
            elif level == "Entry level":
                exp_codes.append("2")
            elif level == "Associate":
                exp_codes.append("3")
            elif level == "Mid-Senior level":
                exp_codes.append("4")
            elif level == "Director":
                exp_codes.append("5")
            elif level == "Executive":
                exp_codes.append("6")
        
        if exp_codes:
            params.append(f"f_E={('%2C').join(exp_codes)}")
    
    # Add job types (using if-elif instead of match)
    if config.JOB_TYPES:
        type_codes = []
        for jt in config.JOB_TYPES:
            if jt == "Full-time":
                type_codes.append("F")
            elif jt == "Part-time":
                type_codes.append("P")
            elif jt == "Contract":
                type_codes.append("C")
            elif jt == "Temporary":
                type_codes.append("T")
            elif jt == "Volunteer":
                type_codes.append("V")
            elif jt == "Internship":
                type_codes.append("I")
            elif jt == "Other":
                type_codes.append("O")
        
        if type_codes:
            params.append(f"f_JT={('%2C').join(type_codes)}")
    
    # Add remote options (using if-elif instead of match)
    if config.REMOTE_OPTIONS:
        remote_codes = []
        for opt in config.REMOTE_OPTIONS:
            if opt == "On-site":
                remote_codes.append("1")
            elif opt == "Remote":
                remote_codes.append("2")
            elif opt == "Hybrid":
                remote_codes.append("3")
        
        if remote_codes:
            params.append(f"f_WT={('%2C').join(remote_codes)}")
    
    # Add date posted (using if-elif instead of match)
    if config.DATE_POSTED == "Past 24 hours":
        params.append("f_TPR=r86400")
    elif config.DATE_POSTED == "Past Week":
        params.append("f_TPR=r604800")
    elif config.DATE_POSTED == "Past Month":
        params.append("f_TPR=r2592000")
    # "Any Time" adds nothing
    
    # Add salary if specified (using if-elif instead of match)
    if config.SALARY:
        if config.SALARY == "$40,000+":
            params.append("f_SB2=1")
        elif config.SALARY == "$60,000+":
            params.append("f_SB2=2")
        elif config.SALARY == "$80,000+":
            params.append("f_SB2=3")
        elif config.SALARY == "$100,000+":
            params.append("f_SB2=4")
        elif config.SALARY == "$120,000+":
            params.append("f_SB2=5")
        elif config.SALARY == "$140,000+":
            params.append("f_SB2=6")
        elif config.SALARY == "$160,000+":
            params.append("f_SB2=7")
        elif config.SALARY == "$180,000+":
            params.append("f_SB2=8")
        elif config.SALARY == "$200,000+":
            params.append("f_SB2=9")
    
    # Add sort (using if-elif instead of match)
    if config.SORT_BY == "Recent":
        params.append("sortBy=DD")
    else:
        params.append("sortBy=R")
    
    return base_url + "?" + "&".join(params)

def extract_job_id_from_url(url: str) -> str:
    """Extract job ID from LinkedIn job URL"""
    try:
        if '/view/' in url:
            return url.split('/view/')[-1].split('/')[0].split('?')[0]
        return ""
    except:
        return ""

class ApplicationStats:
    """Track application statistics"""
    def __init__(self):
        self.total_viewed = 0
        self.applied = 0
        self.already_applied = 0
        self.skipped = 0
        self.failed = 0
        self.blacklisted = 0
    
    def print_summary(self):
        print_info("\n" + "="*50)
        print_info("APPLICATION SUMMARY")
        print_info("="*50)
        print_colored(f"Jobs Viewed: {self.total_viewed}", Colors.CYAN)
        print_success(f"Successfully Applied: {self.applied}")
        print_colored(f"Already Applied: {self.already_applied}", Colors.BLUE)
        print_warning(f"Skipped (Random): {self.skipped}")
        print_warning(f"Blacklisted: {self.blacklisted}")
        print_error(f"Failed: {self.failed}")
        print_info("="*50 + "\n")