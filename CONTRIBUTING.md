# Contributing to Kaizen

Thank you for your interest in contributing to Kaizen! We're excited to have you join our community. This document will guide you through the process of contributing to our project.

For more information on how to contribute to Kaizen, please refer to the [Contributing Guide](https://kaizen-docs.cloudcode.ai/contributing/overview).

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Pull Request Process](#pull-request-process)
6. [Style Guide](#style-guide)
7. [Setting Up Language Models](#setting-up-language-models)
8. [Community Guidelines](#community-guidelines)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our [Code of Conduct](https://kaizen-docs.cloudcode.ai/contributing/code_of_conduct).

## Getting Started

1. Fork the repository to your GitHub account.
2. Clone your fork to your local machine:
   ```bash
   git clone https://github.com/your-username/kaizen.git
   cd kaizen
   ```
3. Add the original repository as an upstream remote:
   ```bash
   git remote add upstream https://github.com/Cloud-Code-AI/kaizen.git
   ```

## Development Setup

1. Install dependencies:
   ```bash
   poetry install
   ```
2. Copy the `.env.example` file to create a new `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Fill in the necessary environment variables in the `.env` file.
4. Create and configure the `config.json` file in the root directory. Refer to the [Setting Up Language Models](#setting-up-language-models) section for details.

## How to Contribute

1. Find an issue to work on or create a new one if you have a feature idea.
2. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes, following our [Style Guide](#style-guide).
4. Write or update tests as necessary.
5. Run tests to ensure all pass:
   ```bash
   pytest .
   ```
6. Commit your changes with a clear and concise commit message.
7. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a pull request against the main repository.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
4. Your pull request will be reviewed by maintainers, who may request changes or improvements.
5. Once approved, your PR will be merged into the main branch.

## Style Guide

- Use [Prettier](https://prettier.io/) for code formatting.
- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) for JavaScript code.
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.
- For CSS/SCSS:
  - Use kebab-case for class names (e.g., `.my-class-name`).
  - Avoid using IDs for styling.
  - Use variables for colors, fonts, and other repeated values.

## Setting Up Language Models

To configure Language Models (LLMs) for your project, update the `config.json` file in the root directory. Here's a basic structure:

```json
{
    "language_model": {
        "provider": "litellm",
        "enable_observability_logging": true,
        "redis_enabled": true,
        "models": [
            {
                "model_name": "default",
                "litellm_params": {
                    "model": "gpt-4o-mini",
                    "input_cost_per_token": 0.000000015,
                    "output_cost_per_token": 0.0000006
                }
            }
        ]
    },
    "github_app": {
        "check_signature": false,
        "auto_pr_review": true,
        "edit_pr_desc": true,
        "process_on_push": true,
        "auto_unit_test_generation": false
    }
}
```

Refer to the [Setting Various LLMs](https://kaizen-docs.cloudcode.ai/contributing/setting_various_llms) guide for more detailed configuration options.

## Community Guidelines

- Be respectful and inclusive in your interactions with other contributors.
- Participate in discussions and help other contributors.
- If you have questions or need help, don't hesitate to ask in our [Community Chat](https://discord.com/invite/zvYZukgeH2).

Thank you for contributing to Kaizen! Your efforts help make our software better for everyone.
