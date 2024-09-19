<p align="center">
  <img src="/assets/logo.png" alt="Kaizen Logo" width="200"/>
</p>

<h1 align="center">Automating the Grunt Work for Software Teams</h1>

<p align="center">
  <strong>Reclaim 40% of your development time with AI-powered automation.</strong>
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

## 🚀 Kaizen: Automating Development Workflows with AI

In today's fast-paced software development world, teams often find themselves bogged down by time-consuming tasks that divert focus from core feature development. Kaizen, an open-source AI-powered suite, is here to revolutionize your development process by automating the grunt work. By seamlessly integrating into your existing workflows, Kaizen empowers your team to reclaim valuable time and focus on what truly matters - building innovative features and delivering value to your customers.

### 🔍 Key Features

- **🤖 AI-Powered Code Reviews**: Automated pull request reviews with insightful summaries and improvement suggestions, accelerating the review process.
- **🧪 Intelligent Test Generation**: 
  - Automatically create end-to-end tests based on your application's code and documentation.
  - Generate unit tests for Python (with TypeScript and React support coming soon!), ensuring comprehensive test coverage with minimal effort.
- **🎨 UI Testing Automation**: Streamline UI component testing with automatic test generation and execution.
- **🔬 Proactive Code Scanning**: Identify potential issues early in the development cycle, allowing you to maintain high-quality code effortlessly.
- **📝 Automated Documentation**: Generate and maintain comprehensive documentation for your codebase, saving hours of manual writing.
- **🕵️ Smart AI Logger**: Monitor your live applications with our AI-powered logger, automatically detecting and reporting anomalies.

## 💡 How Kaizen Boosts Your Team's Productivity

Kaizen takes a holistic approach to automating development tasks, freeing up your team to focus on core feature development:

1. **Streamlined Development Process**: Automate time-consuming tasks like documentation, code reviews, and testing, allowing your team to concentrate on building innovative features.

2. **Quality Assurance**: Leverage AI-powered code scanning and automated testing to maintain high code quality throughout the development lifecycle.

3. **Continuous Improvement**: Foster a culture of efficiency and innovation by constantly optimizing your development workflows.

## 🌟 Why Choose Kaizen?

- **⏰ Reclaim 40% of Development Time**: Automate repetitive tasks and focus on what truly matters - building great software.
- **💪 Empower Your Team**: Provide developers with AI-powered tools to enhance their productivity and job satisfaction.
- **💡 Drive Innovation**: Free up mental bandwidth for creative problem-solving and feature development.
- **🔗 Seamless Integration**: Easily fits into your existing development workflow, minimizing disruptions and maximizing efficiency.

## 🏁 Getting Started

### Quick Start with Cloud Platform

1. Visit [https://kaizen.cloudcode.ai](https://kaizen.cloudcode.ai)
2. Sign up for an account
3. Follow the on-screen instructions to connect your repository

### Using Kaizen SDK

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
   PYTHONPATH=. poetry run python examples/e2e_test/generate.py
   ```

   **Windows**
   ```bash
   set PYTHONPATH=.
   poetry run python examples/e2e_test/generate.py
   ```

4. Execute tests:
   
   **Mac/Linux**
   ```bash
   PYTHONPATH=. poetry run python examples/e2e_test/execute.py
   ```

   **Windows**
   ```bash
   set PYTHONPATH=.
   poetry run python examples/e2e_test/execute.py
   ```
   
   or

   **Mac/Linux/Windows**   
   ```bash
   pytest -v .kaizen/ui-tests/
   ```

### 🔧 GitHub App Setup

You only need to install the GitHub app for code review (PR review and description updates). Other functionalities don't need a GitHub app.

1. For the self-hosting guide, visit the [Kaizen Documentation](https://cloudcode.ai/kaizen/docs) and navigate to the "Self Hosting Guide" section.
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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Cloud-Code-AI/kaizen&type=Date)](https://star-history.com/#Cloud-Code-AI/kaizen&Date)

## 📄 License

Kaizen is released under the MIT License.

## 📞 Contact

Need help or have questions? Reach out to us at support@cloudcode.ai.

---

<p align="center">
  Made with ❤️ by the Kaizen team
</p>
