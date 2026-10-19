# Enterprise Hybrid UI & API Automation Framework

[![Enterprise QA Automation Pipeline][![Enterprise QA Automation Pipeline](https://github.com/XHat3rXDazeX/advanced-pytest-framework/actions/workflows/main.yml/badge.svg)](https://github.com/XHat3rXDazeX/advanced-pytest-framework/actions/workflows/main.yml)
][(https://github.com/XHat3rXDazeX/advanced-pytest-framework/tree/main)]

A production-grade QA Automation framework built from scratch using **Python**, **Pytest**, and **Playwright**. This framework implements advanced design patterns to deliver lightning-fast, stable, and scalable continuous integration testing.

## 🚀 Key Engineering Architectural Features

*   **Page Object Model (POM):** Decoupled website locators from test logic into structural classes, ensuring low maintenance overhead and high code reusability.
*   **Isolated API Mocking:** Implemented browser-level request interception and stubbing to execute backend test cases offline, bypassing network latency and strict firewall policies.
*   **Centralized Configuration Engine:** Securely abstracts target environment parameters, credentials, and endpoints using an environment-override dictionary wrapper.
*   **Automated CI/CD Cloud Pipeline:** Fully integrated with GitHub Actions to dynamically provision Linux nodes, initialize clean browser contexts, and validate build safety on every code push.

## 📁 Repository Directory Structure

```text
advanced-pytest-framework/
├── .github/workflows/  # Cloud CI/CD orchestration scripts
├── config/             # Environment & global setting management
├── pages/              # Page Object Model component layout maps
├── tests/              # UI and Mocked API test case suites
└── pytest.ini          # Pytest engine framework configurations
```

## 🛠️ Local Installation & Setup

1. Clone this repository to your machine.
2. Install dependencies via the pre-compiled binary preference pipeline:
   ```bash
   py -m pip install --user pytest playwright pytest-playwright --prefer-binary
   ```
3. Initialize the dedicated automated browser binaries:
   ```bash
   py -m playwright install
   ```
4. Execute the entire integrated verification suite locally:
   ```bash
   py -m pytest
   ```
