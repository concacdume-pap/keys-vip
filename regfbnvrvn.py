import hashlib, random, requests, time, os, sys, json, urllib3
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich import box

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

app = {
    'api_key': '882a8490361da98702bf97a021ddc14d',
    'secret': '62f8ce9f74b12f84c123cc23437a4a32',
}
email_prefix = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']

def delay_progress():
    with Progress(TextColumn("[bold yellow]Đang tạo tài khoản..."),
                  BarColumn(bar_width=None),
                  TimeElapsedColumn(), transient=True) as progress:
        task = progress.add_task("reg", total=100)
        for _ in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)

def random_user_agent():
    devices = [
        "Nexus 7", "Redmi Note 9", "SM-G973F", "Pixel 4", "OPPO A54",
        "Vivo Y20", "Samsung Galaxy S21", "Xiaomi Mi 10", "Realme C21"
    ]
    device = random.choice(devices)
    android_version = f"{random.randint(8, 12)}.{random.randint(0, 5)}"
    fbav = f"{random.randint(100, 400)}.0.0.{random.randint(0, 99)}.{random.randint(0, 999)}"
    return f"[FBAN/FB4A;FBAV/{fbav};FBDM={{density=2.75,width=1080,height=1920}};FBLC/vi_VN;FBCR/Viettel;FBMF/Samsung;FBBD/Samsung;FBDV/{device};FBSV/{android_version};FBOP/1;]"

def create_account():
    delay_progress()
    random_birth_day = datetime.strftime(datetime.fromtimestamp(random.randint(
        int(time.mktime(datetime.strptime('1980-01-01', '%Y-%m-%d').timetuple())),
        int(time.mktime(datetime.strptime('1995-12-30', '%Y-%m-%d').timetuple()))
    )), '%Y-%m-%d')

    names = {
        'first': ['NGUYEN', 'TRAN', 'LE', 'PHAM', 'HOANG', 'DO', 'BUI','THACH'],
        'last': ['ANH', 'DUC', 'KHANH', 'HUY', 'LINH', 'NAM', 'THAO'],
        'mid': ['VAN', 'THI', 'HOANG', 'MINH', 'HUU', 'NHAT', 'KIM','SON']
    }

    random_first_name = random.choice(names['first'])
    random_name = f"{random.choice(names['mid'])} {random.choice(names['last'])}"
    password = f'PhuocAn{random.randint(100000,999999)}@#'
    full_name = f"{random_first_name} {random_name}"
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()
    hash_ = f"{md5_time[0:8]}-{md5_time[8:12]}-{md5_time[12:16]}-{md5_time[16:20]}-{md5_time[20:32]}"
    email_rand = f"{full_name.replace(' ', '').lower()}{random.randint(1000,9999)}@{random.choice(email_prefix)}"
    gender = 'M' if random.randint(0, 1) else 'F'

    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': random_birth_day,
        'client_country_code': 'VN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': random_first_name,
        'format': 'json',
        'gender': gender,
        'lastname': random_name,
        'email': email_rand,
        'locale': 'vi_VN',
        'method': 'user.register',
        'password': password,
        'reg_instance': hash_,
        'return_multiple_errors': True
    }

    sig = ''.join([f'{k}={v}' for k, v in sorted(req.items())])
    ensig = hashlib.md5((sig + app['secret']).encode()).hexdigest()
    req['sig'] = ensig

    headers = {
        'User-Agent': random_user_agent()
    }

    try:
        response = requests.post('https://b-api.facebook.com/method/user.register', data=req, headers=headers, verify=False)
        result = json.loads(response.text)

        uid = result.get('session_info', {}).get('uid')
        access_token = result.get('session_info', {}).get('access_token')
        error_code = result.get('error_code') 
        error_msg = result.get('error_msg')

        if uid and access_token:
            with open("AccFB.txt", "a") as f:
                f.write(f"{random_birth_day}|{full_name}|{email_rand}|{password}|{uid}|{access_token}\n")
            table = Table(title="🎉 REG SUCCESS", title_style="bold yellow", box=box.DOUBLE_EDGE, border_style="bright_magenta")
            table.add_column("🎂 NGÀY SINH", justify="center", style="bold white")
            table.add_column("🧑 HỌ TÊN", style="bold green")
            table.add_column("📧 EMAIL", style="bold cyan")
            table.add_column("🔒 PASSWORD", style="yellow")
            table.add_column("🆔 UID", style="magenta")
            table.add_column("🔑 TOKEN", style="white")

            table.add_row(f"{random_birth_day}",f"{full_name}",f"{email_rand}",f"{password}",f"{uid}",f"{access_token}")
            console.print(table)
        else:
            console.print(f"[red]❌ Tạo thất bại: [{error_code}] {error_msg}[/red]")
            return False
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi không xác định: {str(e)}[/bold red]")
        return False

def countdown(sec):
    for i in range(sec, 0, -1):
        console.print(f"[cyan]⏳ Vui lòng chờ {i} giây để chống spam...[/cyan]", end='\r')
        time.sleep(1)

if __name__ == "__main__":
    try:
        account_count = int(console.input("[bold green]Nhập số lượng tài khoản muốn tạo: [/bold green]"))
    except ValueError:
        console.print("[bold red]❌ Số lượng không hợp lệ![/bold red]")
        sys.exit(1)

    for i in range(account_count):
        console.print(f"\n[bold magenta]🚀 Đang tạo tài khoản thứ {i+1}/{account_count}[/bold magenta]")
        create_account()
        countdown(15)

    console.print("\n[bold green]✅ Hoàn tất! Các tài khoản đã được lưu trong [white]AccFB.txt[/white][/bold green]")
