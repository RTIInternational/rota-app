import os

from psutil import cpu_count

# Constants from the performance optimization available in onnxruntime
# It needs to be done before importing onnxruntime
os.environ["OMP_NUM_THREADS"] = str(cpu_count(logical=True))
os.environ["OMP_WAIT_POLICY"] = "ACTIVE"
os.environ["TOKENIZERS_PARALLELISM"] = "true"

import json
import os
from pathlib import Path
from typing import Any, Dict, List
import gzip
import shutil

from numpy import ndarray
import requests
import streamlit as st
from onnxruntime import GraphOptimizationLevel, InferenceSession, SessionOptions
from scipy.special import softmax
from transformers import AutoTokenizer
from transformers.file_utils import http_get

from cleaning_utils import cleaner

RELEASE_TAG = "2021.05.17.14"
OUTPUT_PATH = Path("onnx/rota-quantized.onnx")
ONNX_RELEASE = (
    "https://github.com/RTIInternational/"
    "rota/"
    "releases/download/"
    f"{RELEASE_TAG}/"
    "rota-quantized.onnx.gz"
)


@st.cache
def cleaner_cache(text):
    return cleaner(text)


def get_label_config(model_name, config_path: Path = Path("config.json")):
    if config_path.exists():
        config_json = json.loads(config_path.read_text())
        labels = {int(k): v for k, v in config_json["id2label"].items()}
    else:
        config_url = f"https://huggingface.co/{model_name}/raw/main/config.json"
        config_json = requests.get(config_url).json()
        config_path.write_text(json.dumps(config_json))
        labels = {int(k): v for k, v in config_json["id2label"].items()}
    return labels


class ONNXCPUClassificationPipeline:
    def __init__(self, tokenizer, model_path):
        self.tokenizer = tokenizer
        self.model = create_cpu_model(model_path)
        self.labels = get_label_config(
            tokenizer.name_or_path, config_path=Path("onnx/config.json")
        )

    def __call__(self, texts: List[str]) -> List[List[Dict[str, Any]]]:
        # Inputs are provided through numpy array
        model_inputs = self.tokenizer(texts, return_tensors="pt", padding=True)
        inputs_onnx = {k: v.cpu().detach().numpy() for k, v in model_inputs.items()}

        # Run the model (None = get all the outputs)
        output = self.model.run(0, inputs_onnx)
        probs = softmax(output[0], axis=1)
        predictions = self._format_predictions(probs, self.labels)
        return predictions

    def _format_predictions(
        self, softmax_array: ndarray, labels: List[str]
    ) -> List[List[Dict[str, Any]]]:
        """Format predictions from ONNX similar to the
        huggingface transformers classification pipeline

        Args:
            softmax_array (np.ndarray): array of shape (n_preds, n_labels)

        Returns:
            List[List[Dict[str, Any]]]: Output of predictions, where each row is a list of
            Dict with keys "label" and "score"
        """
        predictions = [
            [
                {"label": labels[column], "score": float(softmax_array[row][column])}
                for column in range(softmax_array.shape[1])
            ]
            for row in range(softmax_array.shape[0])
        ]
        return predictions


def create_cpu_model(model_path: str) -> InferenceSession:
    # Few properties that might have an impact on performances (provided by MS)
    options = SessionOptions()
    options.intra_op_num_threads = 1
    options.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL

    # Load the model as a graph and prepare the CPU backend
    session = InferenceSession(model_path, options, providers=["CPUExecutionProvider"])
    session.disable_fallback()

    return session


def download_model():
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(f"{OUTPUT_PATH}.gz", "wb") as f:
        http_get(
            ONNX_RELEASE,
            f,
        )

    with gzip.open(f"{OUTPUT_PATH}.gz", "rb") as f_in:
        with open(f"{OUTPUT_PATH}", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def load_model():
    if not OUTPUT_PATH.exists():
        download_model()
    tokenizer = AutoTokenizer.from_pretrained("rti-international/rota")
    pipeline = ONNXCPUClassificationPipeline(tokenizer, str(OUTPUT_PATH))
    return pipeline


pipeline = load_model()


def predict(text: str, sort=True) -> List[List[Dict[str, Any]]]:
    """Generate a single prediction on an input text

    Args:
        text (str): The input text to generate a prediction for (post-clean)
        sort (bool, optional): Whether to sort the predicted labels by score. Defaults to True.

    Returns:
        List[List[Dict[str, Any]]]: A list with a single element containing predicted label scores.
    """
    clean = cleaner_cache(text)
    preds = pipeline([clean])
    if sort:
        sorted_preds = [
            sorted(p, key=lambda d: d["score"], reverse=True) for p in preds
        ]
        return sorted_preds
    else:
        return preds


def predict_bulk(texts: List[str]) -> List[List[Dict[str, Any]]]:
    """Generate predictions on a list of strings.

    Args:
        texts (List[str]): Input texts to generate predictions (post-cleaning)

    Returns:
        List[List[Dict[str, Any]]]: Predicted label scores for each input text
    """
    cleaned = [cleaner_cache(text) for text in texts]
    preds = pipeline(cleaned)
    del cleaned
    return preds


def _max_pred(prediction_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Utility function to find the maximum predicted label
    for a single prediction

    Args:
        prediction_scores (List[Dict[str, Any]]): A list of predictions with keys
            'label' and 'score'

    Returns:
        Dict[str, Any]: The 'label' and 'score' dict with the highest score value
    """
    return max(prediction_scores, key=lambda d: d["score"])


def max_pred_bulk(preds: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Generates a "column" of label predictions by finding the max
    prediction score per element

    Args:
        preds (List[List[Dict[str, Any]]]): A list of predictions

    Returns:
        List[Dict[str, Any]: A list of  'label' and 'score' dict with the highest score value
    """
    return [_max_pred(pred) for pred in preds]
