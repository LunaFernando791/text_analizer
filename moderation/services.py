from functools import lru_cache
import sys

from huggingface_hub import snapshot_download

MODEL_REPO = "Deeptanshuu/toxic-comment-multilingual-xlmr"
MODEL_REVISION = "1e37e3ce5f04e73b5d4f920a677e77cfc4ddd137"


@lru_cache(maxsize=1)
def _load_model():
    """Carga una vez el modelo ya descargado en la caché local de Hugging Face."""
    try:
        model_path = snapshot_download(
            repo_id=MODEL_REPO,
            revision=MODEL_REVISION,
            local_files_only=True,
        )
    except Exception as error:
        raise FileNotFoundError(
            "No se encontró el modelo en la caché local. Sigue los pasos de descarga "
            "indicados en el README.md."
        ) from error

    if model_path not in sys.path:
        sys.path.insert(0, model_path)

    from modeling_toxic_xlmr import LABEL_NAMES, LANGUAGE_IDS, load_model
    import torch

    model, tokenizer = load_model(model_path, device="cpu")
    return model, tokenizer, LABEL_NAMES, LANGUAGE_IDS, torch


def analyze_text(text):
    text = text.strip()
    if not text:
        raise ValueError("Escribe un texto para analizar.")

    model, tokenizer, labels, languages, torch = _load_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    with torch.inference_mode():
        output = model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            lang_ids=torch.tensor([languages["es"]]),
        )

    scores = output["probabilities"][0].tolist()
    return [
        {
            "label": label,
            "score": round(score, 4),
            "percentage": round(score * 100, 2),
        }
        for label, score in zip(labels, scores)
    ]
