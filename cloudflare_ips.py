from datetime import datetime
from zoneinfo import ZoneInfo

import requests

cloudflareIpURLv4 = "https://www.cloudflare.com/ips-v4"
cloudflareIpURLv6 = "https://www.cloudflare.com/ips-v6"
tz = ZoneInfo("Europe/Warsaw")
today = datetime.now(tz).strftime("%c")


def generate_rsc(url: str, outputFile: str) -> None:
    r = requests.get(url, timeout=10); r.raise_for_status()

    with open(outputFile, "w") as writer:
        _ = writer.write("# Generated on " + today)

        if "v6" in url.lower():
            _ = writer.write("\n/ipv6 firewall address-list")
        else:
            _ = writer.write("\n/ip firewall address-list")

        for line in r.text.splitlines():
            ip = line
            print("Adding IP: " + ip)
            if "v6" in url.lower():
                _ = writer.write("\nadd list=cloudflare-ips-v6 address=" + ip)
            else:
                _ = writer.write("\nadd list=cloudflare-ips address=" + ip)


def main() -> None:
    print(today)
    generate_rsc(cloudflareIpURLv4, "cloudflare-ips-v4.rsc")
    generate_rsc(cloudflareIpURLv6, "cloudflare-ips-v6.rsc")


if __name__ == "__main__":
    main()
