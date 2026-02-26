from crewai import Task
from agents import financial_analyst, verifier, risk_assessor
from tools import read_data_tool


# 1️⃣ Verification Task
verification_task = Task(
    description="""
    Carefully read the uploaded document using the provided tool.

    Determine:
    - Whether the document is a financial report.
    - What type of financial document it is (e.g., quarterly report, annual report).
    - Extract key financial sections found in the document.

    File path: {file_path}
    """,
    expected_output="""
    - Confirmation whether it is a financial document
    - Brief summary of its contents
    - Mention key sections identified
    """,
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)


# 2️⃣ Financial Analysis Task
analyze_financial_document = Task(
    description="""
    Analyze the uploaded financial document to answer the user's query.

    User Query: {query}
    File path: {file_path}

    Carefully extract real financial data such as:
    - Revenue
    - Net income
    - Expenses
    - Assets and liabilities
    - Cash flow

    Base your analysis strictly on the document's content.
    Do not fabricate data.
    Do not include fake URLs.
    """,
    expected_output="""
    Provide a structured financial analysis including:
    - Executive Summary
    - Key Financial Metrics
    - Financial Strengths
    - Financial Weaknesses
    - Investment Insight based only on document data
    """,
    agent=financial_analyst,
    tools=[read_data_tool],
    async_execution=False,
)


# 3️⃣ Risk Assessment Task
risk_assessment_task = Task(
    description="""
    Based strictly on the uploaded financial document, identify realistic financial risks.

    User Query: {query}
    File path: {file_path}

    Evaluate:
    - Debt levels
    - Liquidity risks
    - Profit stability
    - Market exposure
    - Operational risks

    Only use information from the document.
    Do not invent risks.
    """,
    expected_output="""
    Provide a clear risk assessment including:
    - Identified financial risks
    - Severity level (Low/Medium/High)
    - Explanation based on financial data
    - Risk mitigation suggestions
    """,
    agent=risk_assessor,
    tools=[read_data_tool],
    async_execution=False,
)