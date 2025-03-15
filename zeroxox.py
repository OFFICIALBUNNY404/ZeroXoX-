import os
import socket
import requests
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from dns import resolver, reversename, exception

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    console.print(Panel.fit("""
[red]ZeroXoX[/red]  
[blue]Advanced Security Testing Framework[/blue]
[yellow]Creator [green]:[/green] MR.Bunny404[/yellow]
[purple]Version[/purple] [green]:[/green] [red]1.1[/red]
[green]Status  : Premium[/green]
""", title="ZeroXoX", subtitle="Security Framework", border_style="magenta"))

def menu():
    table = Table(title="Available Tools", box=box.DOUBLE_EDGE, border_style="blue")
    table.add_column("No", justify="center", style="bold yellow")
    table.add_column("Tool", justify="left", style="bold green")
    tools = [
        "Website Information",
        "SQLi Scanner",
        "Admin Panel Finder",
        "Port Scanner",
        "Directory Scanner",
        "Subdomain Scanner",
        "WordPress Scanner",
        "XSS Scanner",
        "Email Scraper",
        "DNS Tools",
        "Reverse IP Lookup",
        "About Framework",
    ]
    for i, tool in enumerate(tools, 1):
        table.add_row(str(i), tool)
    table.add_row("99", "[red]Exit Framework[/red]")
    console.print(table)

def website_information():
    console.print("[bold green]Launching Website Information Tool...[/bold green]")
    url = console.input("[yellow]Enter website URL (e.g., https://example.com): [/yellow]").strip()
    if not url.startswith("http"):
        console.print("[red]Error: URL must start with http or https.[/red]")
        return
    try:
        response = requests.get(url, timeout=10)
        console.print(f"[cyan]Website: {url}[/cyan]")
        console.print(f"[cyan]Status Code: {response.status_code}[/cyan]")
        console.print(f"[cyan]Headers: {response.headers}[/cyan]")
    except requests.RequestException as e:
        console.print(f"[red]Error: Unable to fetch information for {url}. Details: {e}[/red]")

def sqli_scanner():
    console.print("[bold green]Launching SQLi Scanner Tool...[/bold green]")
    url = console.input("[yellow]Enter URL to test SQLi (e.g., https://example.com?id=1): [/yellow]").strip()
    payloads = ["' OR 1=1--", "' AND 1=2--", "' UNION SELECT NULL--"]
    try:
        for payload in payloads:
            test_url = f"{url}{payload}"
            response = requests.get(test_url, timeout=10)
            if "SQL" in response.text or response.status_code == 500:
                console.print(f"[red]Possible SQLi vulnerability found: {test_url}[/red]")
                return
        console.print("[green]No SQLi vulnerabilities detected.[/green]")
    except requests.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")

def admin_panel_finder():
    """Search for admin panels on a website."""
    console.print("[bold green]Launching Admin Panel Finder Tool...[/bold green]")
    url = console.input("[yellow]Enter website URL (e.g., https://example.com): [/yellow]").strip()
    common_paths = [
        "admin", "administrator", "admin1", "admin2", "admin3", "admin4", "admin5",
        "admin6", "admin7", "admin8", "admin9", "admin10", "admin11", "admin12",
        "admin13", "admin14", "admin15", "login", "admin-login", "administrator-login",
        "backend", "controlpanel", "dashboard", "cms", "member", "panel",
        "user", "account", "accounts", "manage", "manage-admin"
    ]

    # Load additional paths from a file if available
    try:
        with open("admin_paths.txt", "r") as file:
            additional_paths = file.read().splitlines()
            common_paths.extend(additional_paths)
    except FileNotFoundError:
        console.print("[yellow]No external file found for additional paths.[/yellow]")

    console.print("[cyan]Searching for admin panels...[/cyan]")
    for path in common_paths:
        test_url = f"{url.rstrip('/')}/{path}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                console.print(f"[green]Found admin panel: {test_url}[/green]")
            elif response.status_code in [403, 401]:
                console.print(f"[yellow]Restricted access detected: {test_url} (status: {response.status_code})[/yellow]")
            else:
                console.print(f"[cyan]Checked: {test_url} (status: {response.status_code})[/cyan]")
        except requests.RequestException as e:
            console.print(f"[red]Error connecting to {test_url}: {e}[/red]")

    console.print("[bold green]Finished searching for admin panels.[/bold green]")

def port_scanner():
    console.print("[bold green]Launching Port Scanner Tool...[/bold green]")
    target = console.input("[yellow]Enter target IP or hostname: [/yellow]").strip()
    try:
        for port in range(20, 1025):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((target, port))
                if result == 0:
                    console.print(f"[green]Port {port} is open.[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def directory_scanner():
    console.print("[bold green]Launching Directory Scanner Tool...[/bold green]")
    url = console.input("[yellow]Enter website URL (e.g., https://example.com): [/yellow]")
    common_dirs = ["admin", "images", "css", "js", "uploads"]
    console.print("[cyan]Scanning for common directories...[/cyan]")
    for directory in common_dirs:
        test_url = f"{url.rstrip('/')}/{directory}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                console.print(f"[green]Found directory: {test_url}[/green]")
            else:
                console.print(f"[yellow]Not found: {test_url} (status: {response.status_code})[/yellow]")
        except requests.RequestException:
            console.print(f"[red]Error connecting to {test_url}[/red]")

def subdomain_scanner():
    console.print("[bold green]Launching Subdomain Scanner Tool...[/bold green]")
    domain = console.input("[yellow]Enter domain (e.g., example.com): [/yellow]")
    subdomains = ["www", "mail", "ftp", "test", "dev"]
    console.print("[cyan]Scanning for subdomains...[/cyan]")
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            response = requests.get(f"http://{subdomain}", timeout=5)
            if response.status_code == 200:
                console.print(f"[green]Found subdomain: {subdomain}[/green]")
        except requests.RequestException:
            pass
    console.print("[green]Finished scanning subdomains.[/green]")

def wordpress_scanner():
    console.print("[bold green]Launching WordPress Scanner Tool...[/bold green]")
    url = console.input("[yellow]Enter WordPress URL (e.g., https://example.com): [/yellow]")
    paths = ["wp-login.php", "wp-admin", "xmlrpc.php"]
    console.print("[cyan]Scanning WordPress-specific paths...[/cyan]")
    for path in paths:
        test_url = f"{url.rstrip('/')}/{path}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                console.print(f"[green]Found: {test_url}[/green]")
        except requests.RequestException:
            console.print(f"[red]Error connecting to {test_url}[/red]")

def xss_scanner():
    console.print("[bold green]Launching XSS Scanner Tool...[/bold green]")
    url = console.input("[yellow]Enter URL to test XSS (e.g., https://example.com/search?q=): [/yellow]").strip()
    payload = "<script>alert('XSS')</script>"
    try:
        test_url = f"{url}{payload}"
        response = requests.get(test_url, timeout=10)
        if payload in response.text:
            console.print(f"[red]Possible XSS vulnerability found: {test_url}[/red]")
        else:
            console.print("[green]No XSS vulnerabilities detected.[/green]")
    except requests.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")

def email_scraper():
    console.print("[bold green]Launching Email Scraper Tool...[/bold green]")
    url = console.input("[yellow]Enter website URL (e.g., https://example.com): [/yellow]")
    try:
        response = requests.get(url, timeout=10)
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response.text)
        if emails:
            console.print(f"[green]Found emails: {', '.join(emails)}[/green]")
        else:
            console.print("[yellow]No emails found on the website.[/yellow]")
    except requests.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")

def dns_tools():
    console.print("[bold green]Launching DNS Tools...[/bold green]")
    domain = console.input("[yellow]Enter domain (e.g., example.com): [/yellow]")
    try:
        answers = resolver.resolve(domain, "A")
        for rdata in answers:
            console.print(f"[green]A record: {rdata}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def reverse_ip_lookup():
    console.print("[bold green]Launching Reverse IP Lookup Tool...[/bold green]")
    ip = console.input("[yellow]Enter IP address: [/yellow]").strip()
    api_url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            domains = response.text.strip().split('\n')
            if domains:
                console.print("[green]Domains hosted on this IP:[/green]")
                for domain in domains:
                    console.print(f"[cyan]{domain}[/cyan]")
            else:
                console.print("[yellow]No domains found for this IP.[/yellow]")
        else:
            console.print(f"[red]Error: Unable to perform reverse IP lookup (status code: {response.status_code}).[/red]")
    except requests.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")

def about_framework():
    console.print(Panel("""
[green]ZeroXoX Security Framework[/green]
[cyan]Version: 1.1 BIG[/cyan]
[magenta]Status: Premium[/magenta]
[bold yellow]Creator: Mr.Bunny404[/bold yellow]
[white]This framework is designed for advanced security testing.[/white]
""", title="About ZeroXoX Framework", border_style="blue"))

def exit_framework():
    console.print("[red]Exiting ZeroXoX Framework. Goodbye![/red]")
    exit()

def main():
    banner()
    while True:
        menu()
        choice = console.input("[yellow]Enter your choice: [/yellow]")
        tools = {
            "1": website_information,
            "2": sqli_scanner,
            "3": admin_panel_finder,
            "4": port_scanner,
            "5": directory_scanner,
            "6": subdomain_scanner,
            "7": wordpress_scanner,
            "8": xss_scanner,
            "9": email_scraper,
            "10": dns_tools,
            "11": reverse_ip_lookup,
            "12": about_framework,
            "99": exit_framework,
        }
        tool_function = tools.get(choice)
        if tool_function:
            tool_function()
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

if __name__ == "__main__":
    main()
