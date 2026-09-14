# Mahoraga

**Mahoraga** is an AI desktop assistant designed around the idea that an assistant should do more than generate text.
Instead of functioning purely as a chatbot, Mahoraga combines an AI layer with a modular tool system, persistent memory, task management, browser interaction, computer controls, hardware connectivity, and a native desktop interface.
The project is designed to grow into a general-purpose personal AI system capable of understanding an objective, selecting appropriate tools, executing actions, observing results, and adapting when an approach fails.
It has numerous useful tools ingrained into it, which have numerous practical applications while working on projects.

## Download

The latest stable release of Mahoraga is available on the
[GitHub Releases page](https://github.com/JujharSeehra/mahoraga/releases).

## Architecture

The project is organized into modular components:

```text
mahoraga/
│
├── adaptation/
├── brain/
├── config/
├── core/
├── devices/
├── memory/
├── tasks/
├── tools/
│   ├── browser/
│   ├── computer/
│   └── hardware/
│
├── ui/
│   ├── widgets/
│   ├── main_window.py
│   ├── app.py
│   └── mahoraga.qss
│
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Requirements

### Software

* macOS
* Python 3.11 or newer
* Git
* pip
* A Google Gemini API key
* Chromium via Playwright

### Python dependencies

The main dependencies are:

```text
google-genai
PySide6
python-dotenv
playwright
pyserial
```

Exact versions may vary depending on the development environment.


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JujharSeehra/mahoraga.git
cd mahoraga
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install the Playwright browser

Mahoraga uses Chromium through Playwright.

```bash
python -m playwright install chromium
```

### 5. Configure Gemini

Create a `.env` file:

```bash
cp .env.example .env
```

Then open it:

```bash
open -e .env
```

Add your Gemini API configuration:

```text
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_gemini_model_here
```

### 6. Launch Mahoraga

```bash
mahoraga
```

## macOS Launcher

If the included launcher is configured:

```bash
./run_mahoraga.sh
```

This can be used to start Mahoraga without manually activating the virtual environment each time.

### Workspace access

File-related operations are restricted through the workspace system.

External directories should be explicitly configured before Mahoraga accesses them.

### API keys

Your Gemini API key belongs in:
```text
.env
```

The repository includes:
```text
.env.example
```
as a safe configuration template.

### Local configuration

Some configuration files contain machine-specific or user-specific information and should remain local.

These include:

```text
config/workspaces.json
config/devices.json
config/tasks.json
```


## License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.
