#!/usr/bin/env python3
"""
Quick Start Setup Script for LinkedIn Auto Apply Bot
Run this first to set up your environment
"""

import os
import sys

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Ensure Python 3.7+"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"   Your version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return
    
    print("📝 Creating .env file...")
    
    email = input("Enter your LinkedIn email: ").strip()
    password = input("Enter your LinkedIn password: ").strip()
    
    if not email or not password:
        print("❌ Email and password cannot be empty!")
        sys.exit(1)
    
    with open('.env', 'w') as f:
        f.write(f"LINKEDIN_EMAIL={email}\n")
        f.write(f"LINKEDIN_PASSWORD={password}\n")
    
    print("✅ .env file created successfully!")
    print("⚠️  IMPORTANT: Never commit this file to Git!")

def create_directories():
    """Create necessary directories"""
    dirs = ['data', 'screenshots']
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created data directories")

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = [
        'selenium',
        'undetected_chromedriver',
        'dotenv',
        'pyautogui'
    ]
    
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_').replace('python_', ''))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages detected!")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def create_gitignore():
    """Create .gitignore if it doesn't exist"""
    if os.path.exists('.gitignore'):
        print("✅ .gitignore already exists")
        return
    
    gitignore_content = """.env
*.pkl
linkedin_cookies.pkl
applications_*.txt
screenshots/
data/
__pycache__/
*.pyc
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore")

def show_config_tips():
    """Show configuration tips"""
    print_header("⚙️  CONFIGURATION TIPS")
    
    print("Edit config.py to customize:")
    print("  • LOCATIONS - Where to search (e.g., India, Bangalore)")
    print("  • KEYWORDS - Job titles/skills (e.g., Data Science, Python)")
    print("  • EXPERIENCE_LEVELS - Entry level, Internship, etc.")
    print("  • MAX_APPLICATIONS_PER_RUN - Start with 20-25")
    print("  • DRY_RUN - Set True for testing (no actual applications)")
    print()

def show_safety_warning():
    """Show important safety warnings"""
    print_header("⚠️  SAFETY WARNINGS")
    
    print("IMPORTANT:")
    print("  1. This violates LinkedIn's Terms of Service")
    print("  2. Your account could be restricted or banned")
    print("  3. Start with DRY_RUN=True to test safely")
    print("  4. Apply to max 20-30 jobs per day")
    print("  5. Don't run multiple times per day")
    print()
    print("FIRST TIME USERS:")
    print("  • Set DRY_RUN=True in config.py")
    print("  • Set MAX_APPLICATIONS_PER_RUN=5")
    print("  • Run and verify it works without applying")
    print("  • Then disable dry run and increase limit")
    print()

def show_next_steps():
    """Show next steps"""
    print_header("🚀 NEXT STEPS")
    
    print("1. Edit config.py:")
    print("   • Set your job search preferences")
    print("   • Set DRY_RUN=True for first test")
    print()
    print("2. Test run:")
    print("   python linkedin_bot.py")
    print()
    print("3. Review logs:")
    print("   • Check console output")
    print("   • Review applications_YYYYMMDD.txt")
    print()
    print("4. Go live:")
    print("   • Set DRY_RUN=False in config.py")
    print("   • Run again: python linkedin_bot.py")
    print()

def main():
    """Main setup function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     🤖 LINKEDIN AUTO APPLY BOT - QUICK START 🤖          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print_header("1️⃣  Checking System")
    check_python_version()
    
    print_header("2️⃣  Setting Up Environment")
    create_env_file()
    create_gitignore()
    create_directories()
    
    print_header("3️⃣  Checking Dependencies")
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n⚠️  Please install dependencies first:")
        print("    pip install -r requirements.txt")
        print("\nThen run this script again.")
        sys.exit(1)
    
    show_config_tips()
    show_safety_warning()
    show_next_steps()
    
    print_header("✅ SETUP COMPLETE!")
    print("You're ready to use the LinkedIn Auto Apply Bot!")
    print("\nRead README.md for detailed documentation.")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()