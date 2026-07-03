---
name: model-evaluation
description: Provides a workflow for running and testing machine learning models, including dependency management, model weight acquisition, and inference execution.
tags:
  - mlops
  - testing
  - evaluation
  - inference
  - transformers
  - vllm
  - pytorch
usage: |
  This skill guides you through the process of testing and running a machine learning model. It covers:
  1. Checking and installing necessary Python dependencies (e.g., transformers, vLLM, PyTorch).
  2. Handling dependency installation issues, such as timeouts, and adapting installation strategies.
  3. Downloading model weights from sources like Hugging Face or ModelScope.
  4. Adapting provided code snippets for inference using different backends (e.g., transformers with PyTorch, vLLM).
pitfalls: |
  - **Dependency Installation Timeouts**: Large packages like vLLM can time out during installation. If this occurs, try installing packages individually or consider alternative backends.
  - **Backend Compatibility**: Ensure the chosen web extraction backend (`web_extract` tool) is compatible with the URL type. If not, try searching for the content or cloning the repository.
  - **Model Weight Download Size**: Be mindful of the size of model weights, as downloading can take time and bandwidth.
  - **Hardware Requirements**: Running large models locally may require significant RAM and GPU resources. Check model documentation for requirements.
examples: |
  # Example: Testing a model from a GitHub repository
  The user provides a GitHub repository URL and expresses a desire to test the model.
  1. Clone the repository using `terminal(command='git clone <repo_url>')`.
  2. Read the README.md file for instructions and model details using `read_file()`.
  3. Check and install dependencies using `terminal(command='pip install ...')`. Handle timeouts by installing individually or using alternative packages.
  4. Download model weights (e.g., from Hugging Face links in the README).
  5. Adapt and run the provided inference code snippet using `transformers` and PyTorch, or a specified inference library like vLLM.
---

# Model Evaluation Workflow

This skill provides a structured approach to evaluating and testing machine learning models. It emphasizes handling common issues like dependency installation and adapting to different inference backends. Follow the steps outlined in the `usage` section and consult the `pitfalls` for potential challenges.