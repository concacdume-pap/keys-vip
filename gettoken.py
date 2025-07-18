try:
    import mechanize
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mechanize"])
    import mechanize
import mechanize
import requests
import os

class C25:
    @staticmethod
    def CheckCookie(cookie, userid):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi',
            'cookie': cookie,
            'dpr': '1',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.172", "Google Chrome";v="124.0.6367.172", "Not-A.Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'viewport-width': '767',
        }
        access = requests.get(f'https://mbasic.facebook.com/profile.php?id={userid}', headers=headers).text
        return access.split('<title>')[1].split('<')[0]

os.system('clear')
print('')

user = input('\033[1;31m[\033[1;37mPHUOCAN\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mNhập Tài Khoản :  ')
password = input('\033[1;31m[\033[1;37mPHUOCAN\033[1;31m] \033[1;37m=> \033[1m\033[38;5;51mNhập Mật Khẩu :  ')

browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')]

try:
    code = requests.get('https://taokey567.c25tool.net/src/2fa.php?2fa={_2FA}').json()['code']
    browser.open('https://mbasic.facebook.com/login.php')
    browser.select_form(nr=0)
    browser.form['email'] = str(user)
    browser.form['pass'] = str(password)
    browser.submit()

    try:
        browser.open(f'https://mbasic.facebook.com/checkpoint/?__req')
        browser._factory.is_html = True
        browser.select_form(nr=0)
        browser.form['approvals_code'] = str(code)
        browser.submit()
        browser.open('https://mbasic.facebook.com/login/checkpoint/')
        browser._factory.is_html = True
        browser.select_form(nr=0)
        browser.submit()
    except:
        pass

    browser.open('https://mbasic.facebook.com/home.php')
    browser._factory.is_html = True
    cookies = requests.utils.dict_from_cookiejar(browser.cookiejar)
    cookie = '; '.join(f'{key}={value}' for key, value in cookies.items())
    userid = cookie.split('c_user=')[1].split(';')[0]
    ten = C25.CheckCookie(cookie, userid)
    print(f'Get Cookie: {ten} | {userid} | Đã Lưu Vào File Cookies.txt')
    print('-'*45)
    
    with open('cookies.txt', 'a+', encoding='utf-8') as f:
        f.write(f'{cookie}\n')

except Exception as e:
    print(f'Get Cookie Thất Bại: {e}')
    print('-'*45)
