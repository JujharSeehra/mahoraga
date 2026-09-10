# Mahoraga

**Mahoraga** is an AI desktop assistant designed around the idea that an assistant should do more than generate text.

Instead of functioning purely as a chatbot, Mahoraga combines an AI reasoning layer with a modular tool system, persistent memory, task management, browser interaction, computer controls, hardware connectivity, and a native desktop interface.

The project is designed to grow into a general-purpose personal AI system capable of understanding an objective, selecting appropriate tools, executing actions, observing results, and adapting when an approach fails.

It has numerous useful tools ingrained into it, which have numerous practical applications while working on projects.

> **Status:** Experimental — v1.0.0
> **Primary platform:** macOS
> **AI:** Google Gemini
> **Interface:** PySide6

## 📦 Download

The latest stable release of Mahoraga is available on the
[GitHub Releases page](https://github.com/JujharSeehra/mahoraga/releases).
**Latest release:** [Mahoraga v1.0.0](https://github.com/JujharSeehra/mahoraga/releases/tag/v1.0.0)

## Features

### AI Reasoning

* Google Gemini-powered reasoning
* Multi-step tool execution
* Context-aware conversations
* Tool selection based on the user's objective
* Designed for task-oriented interaction rather than simple question answering

### Modular Tool System

Mahoraga uses a centralized tool registry so capabilities can be added without rewriting the core agent.

Current tool categories include:

* File search
* File listing
* File reading
* Application launching
* Folder opening
* Browser navigation
* Web-page text extraction
* Link interaction
* Browser back navigation
* Serial-device discovery
* Serial-device connection
* Serial communication
* Device management

### Persistent Memory

Mahoraga can store and recall useful information across sessions.

Memory is organized by categories and stored locally, allowing the assistant to retain information that can improve future interactions.

### Task Management

Mahoraga includes a persistent task system supporting:

* Task creation
* Task status
* Step completion
* Step reversal
* Task lookup
* Task listing
* Task deletion

Tasks are stored locally.

### Computer Interaction

Mahoraga can interact with the local computer through tools including:

* Opening applications
* Opening approved folders
* Searching approved workspaces
* Reading files
* Listing files

A workspace system is used to control which external directories Mahoraga can access.

### Browser Control

Mahoraga includes a Playwright-based browser system capable of:

* Opening URLs
* Reading page text
* Navigating backwards
* And more!

Chromium is managed through Playwright.

### Hardware Integration

Mahoraga includes a foundation for communicating with external hardware through serial connections.

The hardware system supports:

* Detecting serial devices
* Connecting to devices
* Disconnecting devices
* Reading serial data
* Managing connected devices

This allows Mahoraga to interface with projects involving microcontrollers and other serial-enabled hardware.

### Custom Desktop Interface

Mahoraga includes a PySide6 desktop interface featuring:

* Chat
* Dashboard
* Tasks
* Memory
* Computer
* Browser
* Hardware
* Tools
* Settings
* System status
* Animated Mahoraga wheel

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


## 🚀 Installation

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

---

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

This file should **never** be committed to the repository.

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

## Current Status

Mahoraga v1.0.0 is an **experimental developer release**.

The system currently provides the foundation for:

* AI reasoning
* Tool execution
* Persistent memory
* Task management
* Workspace-based file access
* Computer interaction
* Browser interaction
* Serial hardware communication
* Device management
* Permission-aware execution
* Native desktop UI

Some systems are intentionally designed as foundations for future development rather than fully autonomous production systems.

## Future Development

Planned areas include:

* More advanced adaptation and learning
* Improved planning
* Better failure recovery
* Expanded computer automation
* More hardware integrations
* Improved browser automation
* Voice input and output
* Perception and visual understanding
* More sophisticated memory retrieval
* Improved task execution
* More robust permissions and safety controls
* Packaged desktop applications

The goal is to progressively move Mahoraga from a modular AI assistant toward a more capable personal computer agent.

## Release

**Current release:** `v1.0.0`

This release represents the first public version of Mahoraga's modular architecture and desktop interface.
For the latest release and source code, see the GitHub repository, titled "Mahoraga".


## License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.
