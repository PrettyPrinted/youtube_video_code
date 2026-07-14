from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic import BaseModel, Field
from datetime import date
from pydantic_ai.capabilities import Instrumentation

from opentelemetry import trace
from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor
from phoenix.otel import BatchSpanProcessor, register
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk

tracer_provider = trace_sdk.TracerProvider()
exporter = OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
tracer_provider.add_span_processor(OpenInferenceSpanProcessor())
tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(tracer_provider)

class Transaction(BaseModel):
    description: str = Field(description="Description of the transaction")
    amount: float = Field(description="Amount of the transaction")
    transaction_date: date = Field(description="Date of the transaction")


class Transactions(BaseModel):
    is_bank_statement: bool = Field(description="Indicates if the document is a bank statement or not")
    transactions: list[Transaction] = Field(description="All the transactions in the statement")
    statement_date: date = Field(description="The statement date")
    beginning_balance: float = Field(description="Statement balance at the beginning of the statement period")
    current_balance: float = Field(description="Current balance at the end of the statement period")

agent = Agent(
    instructions="Read the provided bank statement",
    output_type=Transactions,
    capabilities=[Instrumentation()],
)

with open("bank-statement.pdf", "rb") as file:
    model = OpenAIResponsesModel("gpt-5.4-mini-2026-03-17")
    result = agent.run_sync(
        [BinaryContent(file.read(), media_type="application/pdf")],
        model=model
    )

    if not result.output.is_bank_statement:
        print("Not a bank statement")
        raise ValueError

    if result.output.beginning_balance is not None:
        transactions_total = round(sum(t.amount for t in result.output.transactions), 2)
    if round(result.output.beginning_balance + transactions_total, 2) != round(result.output.current_balance, 2):
        print("Balance doesn't match", round(result.output.beginning_balance + transactions_total, 2), round(result.output.current_balance, 2))
        raise ValueError

    print(result.output)

    # for transaction in result.output.transactions:
    #     print(transaction.transaction_date, transaction.amount)