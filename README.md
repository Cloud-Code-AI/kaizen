<p align="center">
  <a href="https://github.com/Cloud-Code-AI/">
    <img src="https://img.shields.io/github/stars/Cloud-Code-AI/cloudcode" alt="Github Stars">
  </a>
  <a href="https://github.com/Cloud-Code-AI/cloudcode/pulse">
    <img src="https://img.shields.io/github/commit-activity/w/Cloud-Code-AI/cloudcode" alt="Commits-per-week">
  </a>
  <a href="https://opensource.org/license/agpl-v3">
    <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" alt="License: AGPL-3.0">
  </a>
</p>

# Kaizen

Kaizen is an open-source project that helps teams ensure quality in their software delivery by providing a suite of tools for code review, test generation, and end-to-end testing. It integrates with your existing code repositories and workflows, allowing you to streamline your software development process.

## Features

### End-to-End Testing

CloudCode generates comprehensive end-to-end tests based on your application's code and documentation. These tests ensure that your application functions correctly from start to finish, catching regressions and edge cases that may have been overlooked during development.

### Code Review

CloudCode automatically reviews pull requests, summarizing code changes, and providing insightful feedback on potential issues or areas of improvement. It leverages advanced natural language processing techniques to understand the context and implications of the code changes.

### RAGify

CloudCode RAGifies your code repositories, generating relevant context and allowing you to integrate your own Large Language Models (LLMs) or use pre-trained models. This feature enables you to leverage the power of LLMs for various tasks, such as code generation, documentation, and more.

## File Structure

- `github_app`: Contains the API server used by the GitHub app to process incoming requests and respond.
- `kaizen`: Contains the main logic for interaction with LLMs and data processing.
  - `actions`: Contains classes used to process various different actions like Code Review.
  - `llms`: Contains LLM integrations.
- `docs`: Contains Nextra-powered documentation for the project.

## Getting Started

To get started with CloudCode, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Cloud-Code-AI/kaizen.git
   ```

2. Install dependencies:

   ```bash
   cd kaizen
   poetry install
   ```

3. Generate tests for your website:

  First you need to update the url in the `examples/basic/generate.py`.
  ```bash
    PYTHONPATH=. poetry run python examples/basic/generate.py
  ```

  Kaizen will generate all the tests and store them inside `.kaizen/tests/`


### Running API Server for GitHub App

CloudCode utilizes a GitHub app to perform actions like PR review and description updates. Here is a quick link to set up your own GitHub App: [docs/pages/github_app.md](docs/pages/github_app.md)

Deploy the API using Docker Compose:
```
docker-compose up
```

You can also configure features by tweaking the config.json file.

**NOTE:** You need to create a `.env` file by copying `.env.example` and also store the PEM file for the GitHub app as `GITHUB_APP_KEY.pem`.

## Contributing

We welcome contributions from the community! If you'd like to contribute to CloudCode, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

CloudCode is released under the [AGPL License](LICENSE).

## Contact

If you have any questions or need further assistance, please feel free to reach out to us at support@cloudcode.ai.
