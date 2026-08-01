"""Optional Mistral / PEFT inference client for FarmCredit advisory."""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.app.core.config import Settings
from backend.app.llm.prompts import build_advisory_messages

logger = logging.getLogger("farmcredit.llm")


class MistralClient:
    """Loads base Mistral + optional LoRA adapter from HuggingFace Hub."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_id = settings.hf_model_id
        self._tokenizer = None
        self._model = None
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded and self._model is not None

    def load(self) -> None:
        if self._loaded:
            return

        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        token = self.settings.hf_token
        base_id = self.settings.hf_base_model
        adapter_id = self.settings.hf_model_id

        logger.info("Loading tokenizer/base model %s", base_id)
        self._tokenizer = AutoTokenizer.from_pretrained(
            base_id,
            token=token,
            trust_remote_code=True,
        )
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        quant_config = None
        if self.settings.llm_load_in_4bit:
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

        model = AutoModelForCausalLM.from_pretrained(
            base_id,
            token=token,
            quantization_config=quant_config,
            device_map="auto",
            trust_remote_code=True,
        )

        # Prefer adapter repo; if load fails, fall back to base-only generation.
        try:
            model = PeftModel.from_pretrained(model, adapter_id, token=token)
            self.model_id = adapter_id
            logger.info("Loaded PEFT adapter from %s", adapter_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Adapter load failed (%s); using base model only", exc)
            self.model_id = base_id

        model.eval()
        self._model = model
        self._loaded = True

    def generate_advisory(
        self,
        features: dict[str, Any],
        risk_score: float,
        risk_level: str,
        top_factors: list[dict[str, Any]],
        question: str | None = None,
    ) -> tuple[str, int]:
        if not self.is_loaded:
            self.load()

        assert self._tokenizer is not None and self._model is not None
        messages = build_advisory_messages(
            features, risk_score, risk_level, top_factors, question
        )
        prompt = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}

        start = time.perf_counter()
        import torch

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs,
                max_new_tokens=self.settings.llm_max_new_tokens,
                temperature=self.settings.llm_temperature,
                do_sample=self.settings.llm_temperature > 0,
                pad_token_id=self._tokenizer.pad_token_id,
            )
        latency_ms = int((time.perf_counter() - start) * 1000)
        generated = output_ids[0][inputs["input_ids"].shape[-1] :]
        text = self._tokenizer.decode(generated, skip_special_tokens=True).strip()
        return text, latency_ms
