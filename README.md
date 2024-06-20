<p align="center">
  <a href="https://github.com/Cloud-Code-AI/">
    <img src="https://img.shields.io/github/stars/Cloud-Code-AI/cloudcode" alt="Github Stars">
  </a>
  <a href="https://github.com/Cloud-Code-AI/cloudcode/pulse">
    <img src="https://img.shields.io/github/commit-activity/w/Cloud-Code-AI/cloudcode" alt="Commits-per-week">
  </a>
    <a href="https://discord.gg/W33Hh5yWpj">
    <img src="https://img.shields.io/discord/1156434217966764033.svg?style=social&logo=discord" alt="Discord">
    </a>
  <a href="https://opensource.org/license/agpl-v3">
    <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" alt="License: AGPL-3.0">
  </a>
  <a href="https://hub.docker.com/r/cloudcodeai/kaizen-app">
    <img src="https://img.shields.io/docker/pulls/cloudcodeai/kaizen-app.svg?style=flat-square" alt="License: AGPL-3.0">
  </a>

</p>

# Kaizen

Kaizen is an open-source project that helps teams ensure quality in their software delivery by providing an AI-powered suite of tools for code review, test generation, and end-to-end testing. It seamlessly integrates with your existing code repositories and workflows, allowing you to streamline your software development process and catch bugs early.

[![Book a Demo](https://img.shields.io/badge/Book%20a%20Demo-Book%20Now-brightgreen)](https://www.cloudcode.ai/book-a-demo.html) [![Join the Waitlist](https://img.shields.io/badge/Join%20the%20Waitlist-Sign%20Up-blue)](https://cloudcode.ai/#cta) [![Install Kaizen App](https://img.shields.io/badge/Get%20Kaizen%20App-Install-8A2BE2)](https://github.com/apps/kaizen-bot)


## Features

### End-to-End Testing

Kaizen leverages advanced AI techniques to generate comprehensive end-to-end tests based on your application's code and documentation. These tests ensure that your application functions correctly from start to finish, catching regressions and edge cases that may have been overlooked during development.

### UI Testing and Review

Kaizen provides teams with insightful reviews for their UI components and automatically generates necessary tests to ensure that their website works as expected, reducing the risk of visual and functional regressions.

### Code Review

Kaizen automatically reviews pull requests, summarizes code changes, and provides insightful feedback on potential issues or areas of improvement. It leverages advanced natural language processing techniques to understand the context and implications of the code changes, helping developers write better, more maintainable code.

## File Structure

- `github_app`: Contains the API server used by the GitHub app to process and respond to incoming requests.
- `kaizen`: Contains the main logic for interaction with LLMs and data processing.
  - `actors`: Contains classes used to process various actions like Code Review and Test execution.
  - `generators`: Contains the main logic for generative use cases like test case generation, description generation, etc.
  - `llms`: Contains LLM integrations.
- `docs`: Contains Nextra-powered documentation for the project.
- `examples`: Contains sample code for various use cases.

## Getting Started

To get started with Kaizen, follow these steps:

1. Install the Kaizen package:

```
pip install kaizen-cloudcode
```

2. Copy the example code from `examples/basic`.
3. Generate tests for your website:
   First, you need to update the URL in the `examples/basic/generate.py`.

```
PYTHONPATH=. poetry run python examples/basic/generate.py
```

Kaizen will generate all the tests and store them inside `.kaizen/tests/`.

4. Execute tests:
   Once you have generated all the necessary tests, you can run all the tests in two of the following ways:

```
PYTHONPATH=. poetry run python examples/basic/execute.py
```

Or using the default pytest module:

```
pytest -v .kaizen/ui-tests/
```

Kaizen will execute the generated tests and provide detailed reports.

## Running API Server for GitHub App

Kaizen utilizes a GitHub app to perform actions like PR review and description updates. Here's a quick link to set up your own GitHub App: [docs/pages/github_app.md](docs/pages/github_app.md)

You can find the docker image [here](https://hub.docker.com/r/cloudcodeai/kaizen-app)

Deploy the API using Docker Compose:

```
docker-compose up
```

You can also configure features by tweaking the `config.json` file.

**NOTE:** You need to create a `.env` file by copying `.env.example` and also store the PEM file for the GitHub app as `GITHUB_APP_KEY.pem`.

## Contributing

We welcome contributions from the community! If you'd like to contribute to Kaizen, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

Kaizen is released under the AGPL License.

## Contact

If you have any questions or need further assistance, please feel free to contact us at support@cloudcode.ai.
