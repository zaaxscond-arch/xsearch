#!/usr/bin/env python3
"""
XSEARCH v2.0 - Admin Panel Finder
By @zaax | EXEL Framework
"""

import sys
import requests
import threading
import urllib3
import time
import argparse
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── KONFIGURASI ───
BANNER = f"""
{Fore.MAGENTA}
 ██╗  ██╗███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
 ╚██╗██╔╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
  ╚███╔╝ ███████╗█████╗  ███████║██████╔╝██║     ███████║
  ██╔██╗ ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
 ██╔╝ ██╗███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
 ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{Fore.CYAN}              [ Admin Panel Finder v2.0 ]
{Fore.YELLOW}                    [ EXEL By @zaax ]
{Style.RESET_ALL}
"""

# Path admin panel yang umum (real, bukan fake)
ADMIN_PATHS = [
    # ─── CMS POPULER ───
    "admin/", "administrator/", "admin1/", "admin2/", "admin3/",
    "admin.php", "admin.html", "admin.asp", "admin.aspx",
    "admin/login.php", "admin/login.html", "admin/login.asp",
    "admin/index.php", "admin/index.html",
    "adminpanel/", "admin-panel/", "admin_area/",
    "adminarea/", "admincontrol/", "admincp/",
    "admin/login", "admin/signin", "admin/auth",
    
    # ─── WORDPRESS ───
    "wp-admin/", "wp-login.php", "wp-admin/login.php",
    "wp-admin/admin.php", "wp-admin/index.php",
    "wordpress/wp-admin/", "blog/wp-admin/",
    
    # ─── JOOMLA ───
    "administrator/index.php", "administrator/login.php",
    "joomla/administrator/", "administrator/",
    
    # ─── DRUPAL ───
    "user/login", "admin/config", "admin/people",
    "node/add", "admin/content",
    
    # ─── MAGENTO ───
    "admin/", "admin/admin/", "backend/",
    "index.php/admin/", "admin/dashboard/",
    
    # ─── OPENCART ───
    "admin/index.php", "admin/", "admin/login",
    
    # ─── LARAVEL ───
    "login", "admin/login", "dashboard",
    "admin/dashboard", "admin/home",
    
    # ─── DJANGO ───
    "admin/", "admin/login/", "admin/auth/",
    "django-admin/", "administrator/",
    
    # ─── RUBY ON RAILS ───
    "admin/", "admin/login", "admin/sign_in",
    "admins/", "admin/dashboard",
    
    # ─── GENERIC PANELS ───
    "login.php", "login.html", "login.asp", "login.aspx",
    "signin.php", "signin.html", "signin",
    "auth.php", "auth.html", "auth/login",
    "panel/", "cpanel/", "control-panel/",
    "controlpanel/", "cp/", "webadmin/",
    "webmaster/", "manager/", "management/",
    "moderator/", "moderator/login",
    "cms/", "cms/login", "cms/admin",
    "portal/", "portal/admin", "portal/login",
    "member/", "member/login", "member/admin",
    "user/", "user/login", "users/login",
    "account/", "account/login", "accounts/login",
    
    # ─── CUSTOM PANELS ───
    "admin/login.jsp", "admin/login.do",
    "sysadmin/", "sysadmin/login",
    "superadmin/", "superadmin/login",
    "root/", "root/login", "root/admin",
    "master/", "master/login", "master/admin",
    "owner/", "owner/login", "owner/admin",
    "operator/", "operator/login",
    "support/", "support/login",
    "helpdesk/", "helpdesk/login",
    "staff/", "staff/login", "staff/admin",
    
    # ─── API ENDPOINTS ───
    "api/admin", "api/v1/admin", "api/v2/admin",
    "api/login", "api/auth", "api/authenticate",
    "rest/admin", "graphql/admin",
    
    # ─── DEV/STAGING ───
    "dev/", "dev/admin", "dev/login",
    "test/", "test/admin", "test/login",
    "staging/", "staging/admin", "staging/login",
    "beta/", "beta/admin", "beta/login",
    "demo/", "demo/admin", "demo/login",
    
    # ─── BACKUP/OLD ───
    "old/", "old/admin", "old/login",
    "backup/", "backup/admin", "backup/login",
    "bak/", "bak/admin", "bak/login",
    "temp/", "temp/admin", "temp/login",
    "tmp/", "tmp/admin", "tmp/login",
    
    # ─── LANGUAGE SPECIFIC ───
    "administrador/", "administrateur/",
    "administrador/login", "administrateur/login",
    "yonetim/", "yonetim/login",
    "yonetici/", "yonetici/login",
    "guanli/", "guanli/login",
    "guanliyuan/", "guanliyuan/login",
    
    # ─── OTHERS ───
    "phpmyadmin/", "phpMyAdmin/", "pma/",
    "mysql/", "mysql/admin", "dbadmin/",
    "database/", "database/admin",
    "server/", "server/admin", "server/login",
    "config/", "config/admin", "config/login",
    "setup/", "setup/admin", "setup/login",
    "install/", "install/admin", "install/login",
]

# ─── USER AGENTS ROTATION ───
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

class XSearch:
    def __init__(self, target, threads=50, timeout=8, output=None, verbose=False):
        self.target = target.rstrip('/')
        self.threads = threads
        self.timeout = timeout
        self.output = output or f"results/admin_panels_{int(time.time())}.txt"
        self.verbose = verbose
        self.found = []
        self.checked = 0
        self.total = len(ADMIN_PATHS)
        self.lock = threading.Lock()
        self.session = requests.Session()
        
        # Headers default
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        # Warna status
        self.status_colors = {
            200: Fore.GREEN,
            301: Fore.YELLOW,
            302: Fore.YELLOW,
            401: Fore.RED,
            403: Fore.RED,
            404: Fore.CYAN,
        }

    def log(self, msg, color=Fore.WHITE):
        with self.lock:
            print(f"{color}{msg}{Style.RESET_ALL}")

    def check_path(self, path):
        """Cek satu path admin panel"""
        url = urljoin(self.target + '/', path)
        headers = self.headers.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        
        try:
            resp = self.session.get(
                url, 
                headers=headers, 
                timeout=self.timeout,
                verify=False,
                allow_redirects=True
            )
            
            with self.lock:
                self.checked += 1
                progress = f"[{self.checked}/{self.total}]"
                
            status_color = self.status_colors.get(resp.status_code, Fore.WHITE)
            
            # ─── VALIDASI REAL PANEL ───
            is_valid = self.validate_panel(resp, url)
            
            if is_valid:
                result = f"{progress} {Fore.GREEN}[FOUND]{Style.RESET_ALL} {url} ({resp.status_code})"
                self.log(result)
                with self.lock:
                    self.found.append({
                        "url": url,
                        "status": resp.status_code,
                        "title": self.get_title(resp),
                        "server": resp.headers.get('Server', 'Unknown'),
                        "length": len(resp.content)
                    })
                return True
            elif self.verbose:
                result = f"{progress} {status_color}[{resp.status_code}]{Style.RESET_ALL} {url}"
                self.log(result)
                
        except requests.exceptions.Timeout:
            if self.verbose:
                self.log(f"[TIMEOUT] {url}", Fore.MAGENTA)
        except requests.exceptions.ConnectionError:
            if self.verbose:
                self.log(f"[CONN ERR] {url}", Fore.MAGENTA)
        except Exception as e:
            if self.verbose:
                self.log(f"[ERROR] {url} - {str(e)[:50]}", Fore.MAGENTA)
        
        return False

    def validate_panel(self, resp, url):
        """Validasi apakah ini real admin panel"""
        content = resp.text.lower()
        headers = {k.lower(): v.lower() for k, v in resp.headers.items()}
        
        # Status code yang menandakan panel ada
        valid_status = [200, 301, 302, 401, 403]
        if resp.status_code not in valid_status:
            return False
            
        # Content length terlalu kecil = probably 404 page
        if len(resp.content) < 100:
            return False
            
        # ─── KEYWORDS PANEL LOGIN ───
        panel_keywords = [
            'login', 'sign in', 'signin', 'admin', 'password',
            'username', 'email', 'authentication', 'auth',
            'dashboard', 'control panel', 'admin panel',
            'cpanel', 'phpmyadmin', 'wordpress', 'joomla',
            'magento', 'drupal', 'opencart', 'laravel',
            'django', 'administrator', 'management',
            'cms', 'portal', 'backend', 'console',
            'wp-submit', 'log in', 'user login',
            'admin login', 'panel login', 'system login',
            'remember me', 'forgot password', 'reset password',
        ]
        
        # ─── FORM LOGIN DETECTION ───
        form_indicators = [
            '<input type="password"',
            '<input type="text" name="',
            '<form method="post"',
            'name="password"',
            'name="username"',
            'name="email"',
            'name="login"',
            'name="passwd"',
        ]
        
        # ─── TITLE CHECK ───
        title = self.get_title(resp).lower()
        title_keywords = ['login', 'admin', 'sign in', 'signin', 'panel', 
                         'dashboard', 'control', 'backend', 'auth',
                         'wordpress', 'joomla', 'magento', 'drupal']
        
        # Scoring system
        score = 0
        
        # Status code bonus
        if resp.status_code == 200:
            score += 2
        elif resp.status_code in [401, 403]:
            score += 3  # Protected panel = very likely real
        
        # Content keywords
        for kw in panel_keywords:
            if kw in content:
                score += 1
                if score >= 5:
                    break
                    
        # Form detection (strong indicator)
        for fi in form_indicators:
            if fi in content:
                score += 2
                
        # Title check
        for tk in title_keywords:
            if tk in title:
                score += 2
                
        # Server header hints
        server = headers.get('server', '')
        if any(x in server for x in ['apache', 'nginx', 'iis', 'litespeed']):
            score += 1
            
        # Cookie hints
        if 'set-cookie' in headers:
            score += 1
            
        # Redirect to login = likely panel
        if resp.status_code in [301, 302]:
            location = resp.headers.get('Location', '').lower()
            if any(x in location for x in ['login', 'admin', 'auth', 'signin']):
                score += 3
        
        # Minimum score to consider as real panel
        return score >= 4

    def get_title(self, resp):
        """Extract title dari HTML"""
        try:
            content = resp.text
            start = content.lower().find('<title>')
            end = content.lower().find('</title>')
            if start != -1 and end != -1:
                return content[start+7:end].strip()
        except:
            pass
        return "No Title"

    def run(self):
        """Jalankan scan"""
        print(BANNER)
        self.log(f"🎯 Target    : {self.target}", Fore.CYAN)
        self.log(f"🔧 Threads   : {self.threads}", Fore.CYAN)
        self.log(f"⏱️  Timeout   : {self.timeout}s", Fore.CYAN)
        self.log(f"📁 Output    : {self.output}", Fore.CYAN)
        self.log(f"📊 Total Path: {self.total}", Fore.CYAN)
        self.log("─" * 60, Fore.MAGENTA)
        print()
        
        start_time = time.time()
        
        # Multi-threaded scan
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_path, path): path for path in ADMIN_PATHS}
            
            for future in as_completed(futures):
                pass  # Results handled in check_path
        
        elapsed = time.time() - start_time
        
        # ─── SUMMARY ───
        print()
        self.log("─" * 60, Fore.MAGENTA)
        self.log(f"✅ Scan Complete!", Fore.GREEN)
        self.log(f"⏱️  Time      : {elapsed:.2f}s", Fore.CYAN)
        self.log(f"🔍 Checked   : {self.checked}/{self.total}", Fore.CYAN)
        self.log(f"🎯 Found     : {len(self.found)} panels", Fore.GREEN if self.found else Fore.RED)
        print()
        
        # ─── SAVE RESULTS ───
        if self.found:
            import os
            os.makedirs(os.path.dirname(self.output) or '.', exist_ok=True)
            
            with open(self.output, 'w') as f:
                f.write(f"{'='*60}\n")
                f.write(f"XSEARCH RESULTS\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Found: {len(self.found)} panels\n")
                f.write(f"{'='*60}\n\n")
                
                for i, panel in enumerate(self.found, 1):
                    f.write(f"[{i}] {panel['url']}\n")
                    f.write(f"    Status : {panel['status']}\n")
                    f.write(f"    Title  : {panel['title']}\n")
                    f.write(f"    Server : {panel['server']}\n")
                    f.write(f"    Size   : {panel['length']} bytes\n")
                    f.write(f"{'─'*40}\n")
                    
            self.log(f"💾 Saved to: {self.output}", Fore.GREEN)
            
            # Print found panels
            print()
            self.log("🎯 ADMIN PANELS FOUND:", Fore.GREEN)
            for i, panel in enumerate(self.found, 1):
                status_color = Fore.GREEN if panel['status'] == 200 else Fore.YELLOW
                self.log(f"  [{i}] {panel['url']} {status_color}({panel['status']}){Style.RESET_ALL} - {panel['title'][:50]}", Fore.WHITE)
        else:
            self.log("❌ No admin panels found.", Fore.RED)
            
        print()
        self.log("[ EXEL By @zaax ] - Done.", Fore.MAGENTA)

def main():
    parser = argparse.ArgumentParser(
        description="XSEARCH - Admin Panel Finder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xsearch.py -u https://target.com
  python xsearch.py -u https://target.com -t 100 -o results.txt
  python xsearch.py -u https://target.com --verbose
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g., https://example.com)')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('--timeout', type=int, default=8, help='Request timeout in seconds (default: 8)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all requests (slower)')
    
    args = parser.parse_args()
    
    # Validate URL
    parsed = urlparse(args.url)
    if not parsed.scheme:
        args.url = 'https://' + args.url
    if not parsed.netloc and not args.url.startswith('http'):
        print(f"{Fore.RED}❌ Invalid URL format{Style.RESET_ALL}")
        sys.exit(1)
    
    scanner = XSearch(
        target=args.url,
        threads=args.threads,
        timeout=args.timeout,
        output=args.output,
        verbose=args.verbose
    )
    scanner.run()

if __name__ == "__main__":
    main()
