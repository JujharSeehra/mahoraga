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

Mahoraga is a desktop AI assistant for macOS with conversational AI, persistent memory, file search and reading, application and folder launching, web browsing, tool execution, and extensible device support.
Requirements

macOS on Apple Silicon (M1 or newer)
Google Chrome for browser features
A Gemini API key
Installation
Download Mahoraga-v1.0.0-macOS-arm64.zip from the latest release and extract it. Open Mahoraga.app.
Because this release is not signed with an Apple Developer certificate, macOS may block it on first launch. If that happens, right-click or Control-click Mahoraga.app, choose Open, then choose Open again.
On first launch, Mahoraga will ask for your Gemini API key. The key is stored locally in your macOS Application Support directory and is not included with the application.
This release contains the compiled macOS application rather than only the Python source code.

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
