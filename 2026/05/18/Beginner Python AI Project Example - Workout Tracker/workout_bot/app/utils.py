from opentelemetry import trace
from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor
from phoenix.otel import BatchSpanProcessor, register
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk

def setup_llm_telemetry(app):
    tracer_provider = trace_sdk.TracerProvider()
    exporter = OTLPSpanExporter(endpoint=app.config["PHOENIX_ENDPOINT"])
    tracer_provider.add_span_processor(OpenInferenceSpanProcessor())
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(tracer_provider)
