from prometheus_client import Gauge, Counter, generate_latest
from fastapi import FastAPI, Request, Response
import psutil

request_counter = Counter(
    name="requests_received",
    documentation="Number of requests received by server",
    labelnames=["app_name", "method", "endpoint", "http_status"],
)

system_metrics = Gauge(
    name="system_metrics",
    documentation="Various system metrics",
    labelnames=["resource_type"],
)


def update_system_metrics() -> None:
    """Update system metrics when called."""
    available_mem_per = round(
        psutil.virtual_memory().available / psutil.virtual_memory().total * 100,
        3,
    )
    system_metrics.labels("cpu_count").set(psutil.cpu_count(logical=True))
    system_metrics.labels("cpu_load_percent").set(
        round(psutil.cpu_percent(), 3)
    )
    system_metrics.labels("available_memory_percentage").set(available_mem_per)
    system_metrics.labels("available_disk_space").set(
        100 - psutil.disk_usage("/").percent
    )
    system_metrics.labels("cpu_avg_load_15min").set(psutil.getloadavg()[2])
    system_metrics.labels("cpu_avg_load_5min").set(psutil.getloadavg()[1])


def expose_endpoint(app: FastAPI) -> None:
    """Expose endpoint metric for sharing."""

    @app.get("/metrics", tags=["observability"])
    def metrics() -> Response:
        return Response(generate_latest())


def setup_middleware(app: FastAPI) -> None:
    """Setup middleware to support metrics calculation.

    @param app[FastAPI]: FastApi app
    """
    expose_endpoint(app=app)

    @app.middleware("http")
    async def dispatch_middleware(request: Request, call_next) -> Response:
        response = await call_next(request)
        request_counter.labels(
            app.title,
            request.method,
            request.url,
            response.status_code,
        ).inc()

        update_system_metrics()
        return response
