# Python Directory and File Brute-Forcing Tool

This tool is designed for ethical penetration testing of web servers to brute-force directories and files. It uses various techniques to evade detection, such as rotating proxies, human-like delays, and random user-agents. The script attempts to discover hidden directories and files on the target server, including those with critical extensions like `.bak`, `.config`, `.passwd`, and more.

## Features
- **Rotating Proxies**: Automatically rotates through a list of proxies to avoid IP blocking.
- **Random User-Agent**: Uses random user-agent headers to simulate requests from different browsers/devices.
- **Human-like Delay**: Adds random delays between requests to mimic human behavior.
- **Critical Extensions**: Bruteforces important extensions such as `.bak`, `.backup`, `.old`, `.sql`, and `.passwd`.

## Ethical Usage
This tool is intended for ethical use. Always ensure you have explicit permission to test a system. Unauthorized use of brute-forcing tools may violate legal and ethical standards.

## Requirements
- Python 3.x
- `requests` library for making HTTP requests.
- `fake_useragent` library for randomizing user agents.

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/bohmiiidd/NSForce.git
    cd NSForce
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

```bash
python NSForce.py
