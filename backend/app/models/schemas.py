"""Pydantic request/response schemas for FarmCredit FastAPI."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

StateCode = Literal["AP", "BR", "GJ", "HR", "KA", "MH", "MP", "PB", "RJ", "TG", "TN", "UP"]
CropType = Literal[
    "Rice",
    "Wheat",
    "Cotton",
    "Sugarcane",
    "Soybean",
    "Maize",
    "Pulses",
    "Groundnut",
    "Mustard",
    "Millet",
]
Season = Literal["Kharif", "Rabi", "Zaid"]
SoilType = Literal["Alluvial", "Black", "Red", "Laterite", "Sandy", "ClayLoam"]
IrrigationType = Literal["Rainfed", "Canal", "Tubewell", "Drip"]
RiskLevel = Literal["Low", "Medium", "High", "Critical"]
FactorDirection = Literal["increases_risk", "decreases_risk"]


class FarmerFeatures(BaseModel):
    """Input features aligned with XGBoost feature_schema.json."""

    model_config = ConfigDict(extra="forbid")

    state: StateCode
    district: str = Field(..., min_length=2, max_length=64)
    crop_type: CropType
    season: Season
    land_size_ha: float = Field(..., ge=0.2, le=10.0)
    soil_type: SoilType
    rainfall_mm: float = Field(..., ge=0, le=4000)
    irrigation_type: IrrigationType
    loan_amount_inr: int = Field(..., ge=25_000, le=800_000)
    prior_loan_count: int = Field(..., ge=0, le=8)
    prior_default_flag: int = Field(..., ge=0, le=1)
    repayment_score: float = Field(..., ge=0, le=100)
    annual_income_inr: int = Field(..., ge=40_000, le=700_000)
    existing_debt_inr: int = Field(..., ge=0, le=400_000)

    @field_validator("district")
    @classmethod
    def district_strip(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("district must not be empty")
        return cleaned


class RiskFactor(BaseModel):
    feature: str
    display_label: str
    feature_value: Any
    shap_value: float
    direction: FactorDirection
    points: int
    plain_hint: str


class PredictRiskRequest(FarmerFeatures):
    include_shap: bool = True


class PredictRiskResponse(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: RiskLevel
    top_factors: list[RiskFactor] = Field(default_factory=list)


class ExplainRiskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: FarmerFeatures | None = None
    farmer_id: str | None = None
    top_k: int = Field(default=5, ge=1, le=14)

    @field_validator("farmer_id")
    @classmethod
    def normalize_farmer_id(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()


class ExplainRiskResponse(BaseModel):
    baseline: float
    prediction: float
    risk_level: RiskLevel
    top_factors: list[RiskFactor]
    protective_factors: list[RiskFactor] = Field(default_factory=list)
    waterfall_image_url: str | None = None


class AdvisoryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: FarmerFeatures | None = None
    farmer_id: str | None = None
    risk_score: float | None = Field(default=None, ge=0.0, le=1.0)
    risk_level: RiskLevel | None = None
    top_factors: list[RiskFactor] = Field(default_factory=list)
    question: str | None = Field(default=None, max_length=1000)
    use_demo_cache: bool = True
    use_live_llm: bool = False


class AdvisoryResponse(BaseModel):
    advisory_text: str
    model_id: str
    latency_ms: int
    cached: bool
    degraded: bool = False


class DemoFarmerSummary(BaseModel):
    id: str
    display_name: str
    state: StateCode
    crop_type: CropType
    risk_level: RiskLevel | None = None
    narrative: str


class DemoFarmerBundle(BaseModel):
    id: str
    display_name: str
    narrative: str
    expected_risk_level: RiskLevel | None = None
    features: FarmerFeatures
    prediction: PredictRiskResponse | None = None
    explanation: ExplainRiskResponse | None = None
    advisory_text: str | None = None
    report: dict[str, Any] | None = None
    cached: bool = True
    generated_at: datetime | str | None = None


class ReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: FarmerFeatures | None = None
    farmer_id: str | None = None
    include_advisory: bool = True
    use_demo_cache: bool = True
    use_live_llm: bool = False


class ReportResponse(BaseModel):
    title: str
    farmer_summary: dict[str, Any]
    risk_score: float
    risk_level: RiskLevel
    top_factors: list[RiskFactor]
    advisory_text: str | None = None
    generated_at: datetime | str
    cached: bool = False


class AssessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: FarmerFeatures | None = None
    farmer_id: str | None = None
    use_live_llm: bool = False
    use_demo_cache: bool | None = None
    include_advisory: bool = True


class AssessResponse(BaseModel):
    features: FarmerFeatures
    risk_score: float
    risk_level: RiskLevel
    top_factors: list[RiskFactor]
    explanation: ExplainRiskResponse
    advisory: AdvisoryResponse | None = None
    report: ReportResponse | None = None
    cached: bool = False
    farmer_id: str | None = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
    app_env: str
    xgb_loaded: bool
    shap_ready: bool
    llm_enabled: bool
    llm_loaded: bool
    model_dir: str
