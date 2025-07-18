import requests
from bs4 import BeautifulSoup
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def get_temp_email():
    url = "https://10minutemail.net/?lang=vi"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        email_input = soup.find("input", {"id": "fe_text"})
        email = email_input["value"] if email_input else "Không lấy được email"
        return email, session.cookies.get_dict()
    else:
        return "Lỗi kết nối", {}

def keep_email_alive(cookies):
    url = "https://10minutemail.net/mailbox.ajax.php?_="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    session = requests.Session()
    session.cookies.update(cookies)

    console.print(Panel("[bold green]📬 Đang kiểm tra hộp thư...[/bold green]", title="MAILBOX", border_style="bright_blue"))
    
    while True:
        with Progress(SpinnerColumn(), TextColumn("[cyan]⏳ Đang tải email mới..."), transient=True) as progress:
            task = progress.add_task("wait", total=None)
            response = session.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            mails = soup.find_all("tr", style="font-weight: bold; cursor: pointer;")
            if mails:
                for mail in mails:
                    sender = mail.find("a", class_="row-link").text.strip()
                    content = mail.find_all("a", class_="row-link")[1].text.strip()

                    table = Table(title="📨 Thư Mới", title_style="bold yellow", box=box.ROUNDED, border_style="bright_magenta")
                    table.add_column("👤 NGƯỜI GỬI", justify="center", style="bold white")
                    table.add_column("📝 NỘI DUNG", style="bold green")
                    table.add_row(sender, content)
                    console.print(table)
            else:
                console.print("[bold yellow]📭 Không có thư mới.[/bold yellow]")
        else:
            console.print("[bold red]❌ Lỗi kết nối tới mailbox[/bold red]")
        time.sleep(10)

if __name__ == "__main__":
    email, cookies = get_temp_email()
    console.print(Panel(f"[bold cyan]{email}[/bold cyan]", title="📧 EMAIL TẠM THỜI", border_style="bright_green"))
    keep_email_alive(cookies)
