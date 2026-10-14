# AI-Powered Text Moderation

A web application built with Django and Python that analyzes Spanish text and displays scores across six harmful-language categories. It integrates a pretrained multilingual classifier from Hugging Face and runs it locally on the CPU with PyTorch and Transformers.

> **AI scope:** This project integrates and serves an existing pretrained model; it does not train its own model weights. The scores are indicative signals produced by the model, not the percentage of offensive words in a text or an automated moderation decision.

## Features

- Web interface for entering or pasting text; the submitted text remains in the form after analysis.
- Analysis across six categories: toxicity, severe toxicity, obscene language, threats, insults, and identity-based hate.
- Local CPU inference. The model is loaded on demand and reused for as long as the server process is running.
- Error handling that displays a helpful message without exposing the traceback to the user.

## Tech stack

Python, Django, Django REST Framework, PyTorch, Hugging Face Transformers, Hugging Face Hub, and XLM-RoBERTa.

## Requirements

- Python 3.13 recommended, matching the development environment used for this project.
- PowerShell on Windows (the instructions below use PowerShell).
- Approximately 2.2 GB of disk space for the model weights, in addition to space for dependencies and temporary files. CPU inference requires additional RAM.
- An internet connection to install dependencies and download the model the first time.

## Local setup

From the project directory:

```powershell
python -m venv .venv-ai
.\.venv-ai\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Download the pinned model revision. Its weights are about 2.2 GB and are not stored in this repository:

```powershell
python -c "from huggingface_hub import snapshot_download; print(snapshot_download(repo_id='Deeptanshuu/toxic-comment-multilingual-xlmr', revision='1e37e3ce5f04e73b5d4f920a677e77cfc4ddd137', max_workers=1))"
```

Set up the local database and start the development server:

```powershell
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. The model is loaded into memory when the first analysis request is made, so that request may take longer. Subsequent requests reuse the loaded model. Stopping the server releases that memory.

### Environment variables

A local development fallback is provided for the Django secret key. Before deploying the project, configure `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, and configure `DJANGO_ALLOWED_HOSTS` on the hosting platform. `.env.example` documents the expected variable names; it is not loaded automatically.

## Model, attribution, and limitations

This project uses [`Deeptanshuu/toxic-comment-multilingual-xlmr`](https://huggingface.co/Deeptanshuu/toxic-comment-multilingual-xlmr), pinned to revision `1e37e3ce5f04e73b5d4f920a677e77cfc4ddd137`. Review the model card, license, and documentation before reusing it.

The model author notes that the scores are not calibrated as literal probabilities and documents false positives in Spanish, particularly around certain identity-related terms. This application is therefore intended as an educational project and a tool to support human review. It should not automatically delete comments, block accounts, or penalize users.

## Potential improvements

- Add a REST API endpoint for text analysis alongside the web interface.
- Add tests for empty input, service responses, and model-loading errors.
- Improve accessibility and results visualization, including explanations of each category.
- Evaluate the model on Spanish examples and document false positives and false negatives.
- Consider a task queue for deployments with concurrent requests, since CPU inference can take time and consume memory.

## Project status

A personal learning and portfolio project. Before public deployment, configure secrets and allowed hosts, evaluate the model for the intended use, and define input and concurrency limits.
