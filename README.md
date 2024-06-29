<p align="center">
  <a href="https://github.com/Cloud-Code-AI/"><img src="https://img.shields.io/github/stars/Cloud-Code-AI/cloudcode" alt="Github Stars"></a>
  <a href="https://github.com/Cloud-Code-AI/cloudcode/pulse"><img src="https://img.shields.io/github/commit-activity/w/Cloud-Code-AI/cloudcode" alt="Commits-per-week"></a>
  <a href="https://discord.gg/W33Hh5yWpj"><img src="https://img.shields.io/discord/1156434217966764033.svg?style=social&logo=discord" alt="Discord"></a>
  <a href="https://opensource.org/license/agpl-v3"><img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" alt="License: AGPL-3.0"></a>
  <a href="https://hub.docker.com/r/cloudcodeai/kaizen-app"><img src="https://img.shields.io/docker/pulls/cloudcodeai/kaizen-app.svg?style=flat-square" alt="Docker Pulls"></a>
</p>

# Kaizen

Kaizen is an open-source AI-powered suite for code review, test generation, and end-to-end testing. It integrates seamlessly with your existing code repositories and workflows to enhance software quality and streamline development processes.

[![Book a Demo](https://img.shields.io/badge/Book%20a%20Demo-Book%20Now-brightgreen)](https://www.cloudcode.ai/book-a-demo.html) [![Join the Waitlist](https://img.shields.io/badge/Join%20the%20Waitlist-Sign%20Up-blue)](https://cloudcode.ai/#cta) [![Install Kaizen App](https://img.shields.io/badge/Get%20Kaizen%20App-Install-8A2BE2)](https://github.com/apps/kaizen-bot)

## Features

- **End-to-End Testing**: AI-generated comprehensive tests based on your application's code and documentation.
- **UI Testing and Review**: Insightful reviews for UI components with automatic test generation.
- **Code Review**: Automated pull request reviews with code change summaries and improvement suggestions.

## Cloud Platform

Kaizen offers a cloud platform for seamless integration and enhanced features. Access it at [https://beta.cloudcode.ai](https://beta.cloudcode.ai).

Watch our introduction video to learn more about Kaizen:

<p align="center">
  <a href="https://www.youtube.com/watch?v=280CfSQs2ss">
    <img src="https://img.youtube.com/vi/280CfSQs2ss/0.jpg" alt="Kaizen Introduction">
  </a>
</p>

## Getting Started

1. Install Kaizen:
   ```
   pip install kaizen-cloudcode
   ```

2. Generate tests:
   ```
   PYTHONPATH=. poetry run python examples/basic/generate.py
   ```

3. Execute tests:
   ```
   PYTHONPATH=. poetry run python examples/basic/execute.py
   ```
   or
   ```
   pytest -v .kaizen/ui-tests/
   ```

## GitHub App Setup

For PR review and description updates, set up a GitHub App:
1. Follow the guide in [docs/pages/github_app.md](docs/pages/github_app.md)
2. Deploy the API using Docker:
   ```
   docker-compose up
   ```

Note: Create a `.env` file from `.env.example` and store the GitHub app PEM file as `GITHUB_APP_KEY.pem`.

## Project Structure

- `github_app`: API server for the GitHub app
- `kaizen`: Main logic for LLM interaction and data processing
- `docs`: Project documentation
- `examples`: Sample code for various use cases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

Kaizen is released under the AGPL License.

## Contact

For support or inquiries, contact us at support@cloudcode.ai.