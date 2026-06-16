"""
Quality Engineering Statistical Analysis Application
Backend: Flask REST API

Created by: ENG-2518885
Email: meharibrhanu233@gmail.com
Profession: Mechanical Engineer

This module implements the Flask backend providing REST API endpoints
for statistical quality control analysis including descriptive statistics,
process capability indices (Cp, Cpk), and SPC control limit calculations.
"""

from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from scipy import stats
import logging
import math

# --- Application Initialization ---
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False  # Preserve JSON key ordering for readability

# Configure structured logging for production diagnostics
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper: Statistical Computation Engine
# ---------------------------------------------------------------------------

def compute_descriptive_statistics(data: np.ndarray) -> dict:
    """
    Compute fundamental descriptive statistics for the input dataset.

    Args:
        data: A 1-D NumPy array of numeric measurement values.

    Returns:
        Dictionary containing mean, median, std_dev, variance,
        data_range, sample_size, min_val, and max_val.
    """
    return {
        "mean":        round(float(np.mean(data)), 6),
        "median":      round(float(np.median(data)), 6),
        "std_dev":     round(float(np.std(data, ddof=1)), 6),   # Sample std dev (ddof=1)
        "variance":    round(float(np.var(data, ddof=1)), 6),
        "data_range":  round(float(np.ptp(data)), 6),
        "sample_size": int(len(data)),
        "min_val":     round(float(np.min(data)), 6),
        "max_val":     round(float(np.max(data)), 6),
        "skewness":    round(float(stats.skew(data)), 6),
        "kurtosis":    round(float(stats.kurtosis(data)), 6),
    }


def compute_capability_indices(
    data: np.ndarray,
    usl: float,
    lsl: float
) -> dict:
    """
    Compute process capability indices Cp and Cpk.

    Cp  = (USL - LSL) / (6 * sigma)     — Potential capability (spread)
    Cpk = min(Cpu, Cpl)                  — Actual capability (centering)
      where:
        Cpu = (USL - mean) / (3 * sigma)
        Cpl = (mean - LSL) / (3 * sigma)

    Args:
        data: 1-D NumPy array of measurements.
        usl:  Upper Specification Limit.
        lsl:  Lower Specification Limit.

    Returns:
        Dictionary with cp, cpk, cpu, cpl, and sigma values.
    """
    sigma = float(np.std(data, ddof=1))
    mean  = float(np.mean(data))

    if sigma == 0:
        return {"error": "Standard deviation is zero — all values are identical."}

    spec_range = usl - lsl
    if spec_range <= 0:
        return {"error": "USL must be strictly greater than LSL."}

    cp  = spec_range / (6.0 * sigma)
    cpu = (usl - mean)  / (3.0 * sigma)
    cpl = (mean - lsl)  / (3.0 * sigma)
    cpk = min(cpu, cpl)

    # Process yield estimate via normal distribution
    z_upper = (usl - mean) / sigma
    z_lower = (lsl - mean) / sigma
    yield_pct = (stats.norm.cdf(z_upper) - stats.norm.cdf(z_lower)) * 100.0

    return {
        "cp":         round(cp, 4),
        "cpk":        round(cpk, 4),
        "cpu":        round(cpu, 4),
        "cpl":        round(cpl, 4),
        "sigma":      round(sigma, 6),
        "yield_pct":  round(yield_pct, 4),
        "ppk_rating": _rate_capability(cpk),
    }


def _rate_capability(cpk: float) -> str:
    """Return a plain-language process capability rating based on Cpk value."""
    if cpk >= 1.67:
        return "Excellent (Six Sigma)"
    elif cpk >= 1.33:
        return "Capable"
    elif cpk >= 1.00:
        return "Marginally Capable"
    else:
        return "Incapable — Immediate Action Required"


def compute_spc_control_limits(data: np.ndarray, subgroup_size: int = 5) -> dict:
    """
    Compute X-bar and R chart control limits using standard SPC constants.

    Statistical constants A2, D3, D4 are derived from the subgroup size.
    These are standard Shewhart control chart constants (AIAG reference).

    Args:
        data:           1-D NumPy array of all individual measurements.
        subgroup_size:  Number of observations per rational subgroup (default=5).

    Returns:
        Dictionary with x_bar chart limits, R chart limits, and subgroup data.
    """
    n = subgroup_size

    # Shewhart constants table for subgroup sizes 2–10
    constants = {
        2:  {"A2": 1.880, "D3": 0.000, "D4": 3.267, "d2": 1.128},
        3:  {"A2": 1.023, "D3": 0.000, "D4": 2.574, "d2": 1.693},
        4:  {"A2": 0.729, "D3": 0.000, "D4": 2.282, "d2": 2.059},
        5:  {"A2": 0.577, "D3": 0.000, "D4": 2.114, "d2": 2.326},
        6:  {"A2": 0.483, "D3": 0.000, "D4": 2.004, "d2": 2.534},
        7:  {"A2": 0.419, "D3": 0.076, "D4": 1.924, "d2": 2.704},
        8:  {"A2": 0.373, "D3": 0.136, "D4": 1.864, "d2": 2.847},
        9:  {"A2": 0.337, "D3": 0.184, "D4": 1.816, "d2": 2.970},
        10: {"A2": 0.308, "D3": 0.223, "D4": 1.777, "d2": 3.078},
    }

    # Clamp subgroup size to valid range
    n = max(2, min(10, n))
    c = constants[n]
    A2, D3, D4 = c["A2"], c["D3"], c["D4"]

    # Partition data into rational subgroups
    total = len(data)
    num_subgroups = total // n
    trimmed = data[:num_subgroups * n]
    subgroups = trimmed.reshape(num_subgroups, n)

    subgroup_means  = np.mean(subgroups, axis=1)
    subgroup_ranges = np.ptp(subgroups, axis=1)

    x_double_bar = float(np.mean(subgroup_means))
    r_bar        = float(np.mean(subgroup_ranges))

    # X-bar chart limits
    ucl_xbar = x_double_bar + A2 * r_bar
    lcl_xbar = x_double_bar - A2 * r_bar

    # R chart limits
    ucl_r = D4 * r_bar
    lcl_r = D3 * r_bar

    return {
        "subgroup_size":   n,
        "num_subgroups":   num_subgroups,
        "x_bar_chart": {
            "center_line": round(x_double_bar, 6),
            "ucl":         round(ucl_xbar, 6),
            "lcl":         round(lcl_xbar, 6),
            "data_points": [round(v, 6) for v in subgroup_means.tolist()],
        },
        "r_chart": {
            "center_line": round(r_bar, 6),
            "ucl":         round(ucl_r, 6),
            "lcl":         round(lcl_r, 6),
            "data_points": [round(v, 6) for v in subgroup_ranges.tolist()],
        },
    }


def build_histogram_data(data: np.ndarray) -> dict:
    """
    Compute histogram bin frequencies and a fitted normal distribution overlay.

    Uses Sturges' rule for automatic bin count selection.

    Args:
        data: 1-D NumPy array of measurements.

    Returns:
        Dictionary with bin_edges, frequencies, and normal curve (x, y) points.
    """
    # Sturges' rule: k = ceil(1 + log2(n))
    num_bins = max(5, math.ceil(1 + math.log2(len(data))))
    counts, bin_edges = np.histogram(data, bins=num_bins)

    # Fitted normal distribution curve for overlay
    mu    = float(np.mean(data))
    sigma = float(np.std(data, ddof=1))
    x_curve = np.linspace(float(np.min(data)), float(np.max(data)), 200)
    bin_width = float(bin_edges[1] - bin_edges[0])
    # Scale PDF to match histogram area (frequency density × n × bin_width)
    y_curve = stats.norm.pdf(x_curve, mu, sigma) * len(data) * bin_width

    return {
        "bin_edges":   [round(v, 6) for v in bin_edges.tolist()],
        "bin_centers": [round(float((bin_edges[i] + bin_edges[i+1]) / 2), 6)
                        for i in range(len(bin_edges) - 1)],
        "frequencies": counts.tolist(),
        "normal_curve": {
            "x": [round(v, 6) for v in x_curve.tolist()],
            "y": [round(v, 6) for v in y_curve.tolist()],
        },
    }


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the single-page mobile dashboard."""
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    POST /api/analyze

    Accepts JSON body:
    {
        "data":           [float, ...],   // Measurement values (required)
        "usl":            float,          // Upper Specification Limit (optional)
        "lsl":            float,          // Lower Specification Limit (optional)
        "subgroup_size":  int             // SPC subgroup size, default 5 (optional)
    }

    Returns JSON with descriptive_stats, capability (if USL/LSL provided),
    spc_charts (if ≥10 data points), and histogram_data.
    """
    try:
        payload = request.get_json(force=True, silent=True)

        # --- Input Validation ---
        if payload is None:
            return jsonify({"error": "Request body must be valid JSON."}), 400

        raw_data = payload.get("data")
        if raw_data is None or not isinstance(raw_data, list):
            return jsonify({"error": "'data' field is required and must be a list."}), 400

        if len(raw_data) < 2:
            return jsonify({"error": "At least 2 data points are required for analysis."}), 400

        # Convert and validate all values are numeric
        try:
            data = np.array([float(v) for v in raw_data], dtype=np.float64)
        except (TypeError, ValueError) as exc:
            return jsonify({"error": f"All data values must be numeric. Detail: {exc}"}), 400

        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            return jsonify({"error": "Data must not contain NaN or infinite values."}), 400

        # --- Build Response ---
        response = {
            "status":             "success",
            "descriptive_stats":  compute_descriptive_statistics(data),
            "histogram_data":     build_histogram_data(data),
        }

        # Optional capability analysis (requires USL and LSL)
        usl_raw = payload.get("usl")
        lsl_raw = payload.get("lsl")

        if usl_raw is not None and lsl_raw is not None:
            try:
                usl = float(usl_raw)
                lsl = float(lsl_raw)
            except (TypeError, ValueError):
                return jsonify({"error": "USL and LSL must be numeric values."}), 400

            capability = compute_capability_indices(data, usl, lsl)
            if "error" in capability:
                return jsonify({"error": capability["error"]}), 400
            response["capability"] = capability
        else:
            response["capability"] = None

        # Optional SPC charts (requires at least 2 complete subgroups)
        subgroup_size = int(payload.get("subgroup_size", 5))
        if len(data) >= subgroup_size * 2:
            response["spc_charts"] = compute_spc_control_limits(data, subgroup_size)
        else:
            response["spc_charts"] = None
            response["spc_note"] = (
                f"SPC charts require at least {subgroup_size * 2} data points "
                f"for subgroup size {subgroup_size}."
            )

        logger.info("Analysis complete: n=%d, capability=%s", len(data),
                    "yes" if response["capability"] else "no")
        return jsonify(response), 200

    except Exception as exc:
        logger.exception("Unexpected error during analysis")
        return jsonify({"error": f"Internal server error: {str(exc)}"}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint for monitoring and deployment validation."""
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
