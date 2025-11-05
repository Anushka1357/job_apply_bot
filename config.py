import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# CREDENTIALS (Loaded securely from .env file)
# ============================================================================
# DO NOT hardcode credentials here! Use .env file instead.
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


# ============================================================================
# JOB SEARCH PARAMETERS
# ============================================================================

# Locations to search jobs in
# For India: Can specify continent "Asia" or specific cities
# Examples: ["India"], ["Asia"], ["Bangalore", "Mumbai", "Delhi"]
LOCATIONS = [
    "Asia",
    "India", 
    "Bangalore", 
    "Mumbai", 
    "Delhi", 
    "Pune", 
    "Hyderabad"
]

# Keywords for job search - Your skills and target roles
# Add all relevant technologies, roles, and skills
KEYWORDS = [
    "Data Science",
    "AI Engineer",
    "ML Engineer",
    "Machine Learning",
    "vector databases",
    "RAG",
    "python",
    "Data Analyst",
    "Python Developer",
    "Data Engineer",
    "Business Analyst",
    "NLP Engineer"
]

# Experience Levels
# Options: "Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"
EXPERIENCE_LEVELS = [
    "Entry level",
    "Internship"  # Fixed typo from your original config
]

# Date Posted - When the job was posted
# Options: "Any Time", "Past Month", "Past Week", "Past 24 hours"
# Select only ONE
DATE_POSTED = "Past Week"

# Job Types - Full-time, part-time, etc.
# Options: "Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship", "Other"
# Can select multiple
JOB_TYPES = [
    "Full-time",
    "Part-time",
    "Contract"
]

# Remote Work Options
# Options: "On-site", "Remote", "Hybrid"
# Can select multiple or all three
REMOTE_OPTIONS = [
    "On-site",
    "Remote",
    "Hybrid"
]

# Salary Filter
# Leave empty ("") to IGNORE salary filters (as you requested)
# Options: "$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", 
#          "$140,000+", "$160,000+", "$180,000+", "$200,000+"
# Select only ONE or leave empty
SALARY = ""  # Empty = No salary filter

# Sort Results By
# Options: "Recent" or "Relevant"
# Select only ONE
SORT_BY = "Recent"


# ============================================================================
# FILTERING & BLACKLISTS
# ============================================================================

# Companies to SKIP (won't apply to these)
# Example: ["Apple", "Google", "Microsoft"]
BLACKLIST_COMPANIES = []

# Job titles to SKIP (won't apply if title contains these words)
# Example: ["manager", ".Net", "Senior", "Lead", "Director"]
# Useful to avoid jobs requiring more experience
BLACKLIST_TITLES = [
    # Uncomment to skip senior positions:
    # "Senior",
    # "Lead", 
    # "Manager",
    # "Director",
    # "Principal",
    # "Staff",
    # "Head of"
]


# ============================================================================
# APPLICATION BEHAVIOR SETTINGS
# ============================================================================

# Maximum number of applications per run (SAFETY LIMIT)
# Start with 20-25, don't go too high to avoid detection
# Recommended: 20-30 per day maximum
MAX_APPLICATIONS_PER_RUN = 25

# Follow companies after successful application?
# True = Yes, False = No
FOLLOW_COMPANIES = False

# Which resume to use if you have multiple uploaded
# 0 = first resume, 1 = second resume, etc.
PREFERRED_RESUME_INDEX = 0


# ============================================================================
# BOT BEHAVIOR - HUMAN-LIKE ACTIONS
# ============================================================================
# These settings make the bot appear more human to avoid detection

# Delay between actions (in seconds)
MIN_DELAY = 3   # Minimum seconds to wait
MAX_DELAY = 8   # Maximum seconds to wait

# Time spent "reading" job descriptions (in seconds)
# Bot will pause and appear to read the job posting
READING_TIME_MIN = 10  # Minimum reading time
READING_TIME_MAX = 25  # Maximum reading time

# Random skip probability
# Bot will randomly skip some jobs to appear more human
# 0.15 = 15% chance to skip each job
SKIP_PROBABILITY = 0.15

# Randomize the order jobs are processed
# True = Apply to jobs in random order (more human)
# False = Apply in the order LinkedIn shows them
RANDOMIZE_JOB_ORDER = True


# ============================================================================
# BROWSER SETTINGS
# ============================================================================

# Use Undetected Chrome (better detection avoidance but can have version issues)
# If you're having Chrome version issues, set this to False
USE_UNDETECTED_CHROME = True  # True = Harder to detect, False = More compatible

# DRY RUN MODE - Test without actually applying!
# True = Bot will go through motions but NOT submit applications
# False = Bot will actually apply to jobs
# ALWAYS test with True first!
DRY_RUN = True  # CHANGE TO False WHEN READY TO APPLY FOR REAL

# Headless mode - Run browser in background
# True = No browser window shown (runs in background)
# False = Show browser window (recommended for first time)
HEADLESS_MODE = False

# Save screenshots of successful applications
# True = Take screenshot after each successful application
# False = Don't save screenshots
SAVE_SCREENSHOTS = True

# Use saved cookies (stay logged in between runs)
# True = Remember login session (recommended)
# False = Login every time
USE_SAVED_COOKIES = True

# Display warning messages in console
# True = Show all warnings and debug info
# False = Only show important messages
DISPLAY_WARNINGS = False

# Debug mode - shows detailed info about what bot is doing
# Useful for troubleshooting when things don't work
DEBUG_MODE = True  # Set to False once everything works


# ============================================================================
# ADVANCED SETTINGS (Optional)
# ============================================================================

# Output file type for logs
# Options: ".txt" or ".csv"
OUTPUT_FILE_TYPE = ".txt"

# Save jobs before applying (click the SAVE button)
# True = Save job to your LinkedIn saves before applying
# False = Just apply without saving
SAVE_JOBS_BEFORE_APPLY = False


# ============================================================================
# USAGE NOTES & TIPS
# ============================================================================
"""
FIRST TIME SETUP:
1. Set DRY_RUN = True
2. Set MAX_APPLICATIONS_PER_RUN = 5
3. Run the bot and watch what it does
4. Check the console output and logs
5. When comfortable, set DRY_RUN = False
6. Gradually increase MAX_APPLICATIONS_PER_RUN to 20-25

SAFETY TIPS:
- Start with 20-25 applications per day MAX
- Run bot once per day maximum
- Monitor your LinkedIn account for warnings
- If you get warnings, STOP immediately and wait 3-7 days

FOR YOUR USE CASE (India, No Salary Filter):
✅ LOCATIONS already includes India + major cities
✅ SALARY is empty (ignores salary filters as you wanted)
✅ EXPERIENCE_LEVELS focuses on entry level
✅ All job types and remote options included

CUSTOMIZATION:
- Edit KEYWORDS to match your exact skills
- Add to BLACKLIST_TITLES to skip unwanted roles
- Adjust delays if you want slower/faster behavior
- Change MAX_APPLICATIONS_PER_RUN based on comfort level

MONITORING:
- Check console output while running
- Review applications_YYYYMMDD.txt file after each run
- Track success rate and adjust filters accordingly
"""