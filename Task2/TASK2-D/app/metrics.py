from prometheus_client import Counter, Histogram, Gauge

REQUESTS = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

ERRORS = Counter(
    "prediction_errors_total",
    "Total prediction errors"
)

LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction latency",
    buckets=(0.01, 0.05, 0.1, 0.3, 0.5, 1, 2)
)

PREDICTIONS = Counter(
    "prediction_class_total",
    "Prediction class distribution",
    ["pred_class"]
)

FEATURES = {
    "sepal_length": Gauge("feature_sepal_length", "Sepal length"),
    "sepal_width": Gauge("feature_sepal_width", "Sepal width"),
    "petal_length": Gauge("feature_petal_length", "Petal length"),
    "petal_width": Gauge("feature_petal_width", "Petal width"),
}
