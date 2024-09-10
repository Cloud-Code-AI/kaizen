<p align="center">
  <img src="/assets/logo.png" alt="Kaizen Logo" width="200"/>
</p>

<h1 align="center">Accelerating Bug Detection</h1>

<p align="center">
  <strong>Unleash the power of AI to find and squash bugs before they reach your customers.</strong>
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

## 🚀 Kaizen: Accelerating Bug detection with AI

In the ever-evolving world of software development, delivering high-quality code is paramount. Kaizen, an open-source AI-powered suite, is here to revolutionize your code quality assurance process. With its seamless integration into your existing workflows, Kaizen empowers you to enhance software quality and streamline development, ensuring your applications are robust, reliable, and bug-free.

### 🔍 Key Features

- **🤖 AI-Powered Code Reviews**: Automated pull request reviews with insightful summaries and improvement suggestions, catching potential issues before they escalate.

- **🧪 Smart Test Generation**: 
  - End-to-end tests based on your application's code and documentation, ensuring comprehensive coverage.
  - Unit test generation for Python (with TypeScript and React support coming soon!), saving you valuable time and effort.
- **🎨 UI Testing and Review**: Comprehensive reviews for UI components with automatic test generation, ensuring a flawless user experience.
- **🔬 Code Scanning**: Identify potential issues before they become problems, allowing you to take proactive measures and maintain high-quality code.
- **🕵️ Intelligent AI Logger**: Monitor your live applications with our AI-powered logger, catching and reporting bugs as they occur.

## 💡 How Kaizen Helps You Find Bugs

Kaizen takes a two-pronged approach to help you find and squash bugs, both before and after deployment:

1. **Pre-Deployment**: Kaizen provides AI-powered code reviews, automatically generates and runs unit tests, and performs code scanning to identify potential issues early in the development cycle.

2. **Post-Deployment**: Kaizen's AI logger monitors your live applications, catching and reporting bugs as they occur. Additionally, our end-to-end test generation and execution capabilities allow you to thoroughly test your applications after deployment, ensuring a seamless user experience.

## 🌟 Why Choose Kaizen?

- **👁️ Catch Bugs Early**: Identify issues before your customers do, minimizing the impact and cost of fixes.
- **⏱️ Save Time**: Automate tedious code review and testing tasks, freeing up valuable resources for more strategic work.
- **💡 Continuous Improvement**: Foster a culture of constant code quality enhancement, driving innovation and excellence.
- **🔗 Easy Integration**: Seamlessly fits your existing development workflow, minimizing disruptions and maximizing efficiency.

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


5. Execute tests:
   
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
