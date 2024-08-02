<p align="center">
  <img src="/logo.png" alt="Kaizen Logo" width="200"/>
</p>

<h1 align="center">Kaizen: AI-Powered Code Quality Assistant</h1>

<p align="center">
  <strong>Find bugs before your customers do!</strong>
</p>

<p align="center">
  <a href="https://github.com/Cloud-Code-AI/"><img src="https://img.shields.io/github/stars/Cloud-Code-AI/cloudcode" alt="Github Stars"></a>
  <a href="https://github.com/Cloud-Code-AI/cloudcode/pulse"><img src="https://img.shields.io/github/commit-activity/w/Cloud-Code-AI/cloudcode" alt="Commits-per-week"></a>
  <a href="https://discord.gg/W33Hh5yWpj"><img src="https://img.shields.io/discord/1156434217966764033.svg?style=social&logo=discord" alt="Discord"></a>
  <a href="https://opensource.org/license/mit"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://hub.docker.com/r/cloudcodeai/kaizen-app"><img src="https://img.shields.io/docker/pulls/cloudcodeai/kaizen-app.svg?style=flat-square" alt="Docker Pulls"></a>
</p>

<p align="center">
  <a href="https://www.cloudcode.ai/book-a-demo.html"><img src="https://img.shields.io/badge/Book%20a%20Demo-Book%20Now-brightgreen" alt="Book a Demo"></a>
  <a href="https://cloudcode.ai/#cta"><img src="https://img.shields.io/badge/Get%20Started-Sign%20Up-blue" alt="Sign Up for Free"></a>
  <a href="https://github.com/apps/kaizen-bot"><img src="https://img.shields.io/badge/Get%20Kaizen%20App-Install-8A2BE2" alt="Install Kaizen App"></a>
  <a href="https://cloudcode.ai/kaizen/docs"><img src="https://img.shields.io/badge/docs-view%20Kaizen%20Docs" alt="Kaizen Docs"></a>
</p>

## 🚀 What is Kaizen?

Kaizen is an open-source AI-powered suite that revolutionizes your code quality assurance process. It seamlessly integrates with your existing workflows to enhance software quality and streamline development.

### 🔍 Key Features

- **🤖 AI-Powered Code Reviews**: Automated pull request reviews with insightful summaries and improvement suggestions.
- **🧪 Smart Test Generation**: 
  - End-to-end tests based on your application's code and documentation.
  - Unit test generation for Python (with TypeScript and React support coming soon!).
- **🎨 UI Testing and Review**: Comprehensive reviews for UI components with automatic test generation.
- **🔬 Code Scanning**: Identify potential issues before they become problems.

## 🌟 Why Choose Kaizen?

- **👁️ Catch Bugs Early**: Identify issues before your customers do.
- **⏱️ Save Time**: Automate tedious code review and testing tasks.
- **💡 Continuous Improvement**: Foster a culture of constant code quality enhancement.
- **🔗 Easy Integration**: Seamlessly fits your existing development workflow.

## 🏁 Getting Started

### Quick Start with Cloud Platform

1. Visit [https://beta.cloudcode.ai](https://beta.cloudcode.ai)
2. Sign up for an account
3. Follow the on-screen instructions to connect your repository

### Local Installation
1. Create and activate a virtual environment:

   **Mac/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install poetry and Kaizen:
   ```bash
   pip install poetry kaizen-cloudcode
   ```
   
3. Generate tests:
   
   **Mac/Linux**
   ```bash
   PYTHONPATH=. poetry run python examples/basic/generate.py
   ```

   **Windows**
   ```bash
   set PYTHONPATH=.
   poetry run python examples/basic/generate.py
   ```


5. Execute tests:
   
   **Mac/Linux**
   ```bash
   PYTHONPATH=. poetry run python examples/basic/execute.py
   ```

   **Windows**
   ```bash
   set PYTHONPATH=.
   poetry run python examples/basic/execute.py
   ```
   
   or

   **Mac/Linux/Windows**   
   ```bash
   pytest -v .kaizen/ui-tests/
   ```

## 🔧 GitHub App Setup

For PR review and description updates:

1. Follow our [GitHub App Setup Guide](docs/pages/github_app.md)
2. Deploy the API using Docker:
   ```bash
   docker-compose up
   ```

> 📝 Note: Create a `.env` file from `.env.example` and store the GitHub app PEM file as `GITHUB_APP_KEY.pem`.

## 🎥 See Kaizen in Action

<p align="center">
  <a href="https://www.youtube.com/watch?v=280CfSQs2ss">
    <img src="https://img.youtube.com/vi/280CfSQs2ss/0.jpg" alt="Kaizen Introduction">
  </a>
</p>


## 📄 License

Kaizen is released under the MIT License.

## 📞 Contact

Need help or have questions? Reach out to us at support@cloudcode.ai.

---

<p align="center">
  Made with ❤️ by the Kaizen team
</p>
