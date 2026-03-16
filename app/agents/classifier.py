"""
Agent Definitions — Document Classifier Agent
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from app.core.config import settings
from typing import List


class DocumentClassifierAgent:
    """
    Agent 1: Document Classifier
    Determines document type, language, quality, and routing path.
    """

    def __init__(self, tools: List, verbose: bool = False):
        self.agent = Agent(
            role="Document Classification Specialist",
            goal=(
                "Accurately classify incoming documents by type, quality, "
                "and determine the appropriate verification pathway. "
                "Extract key metadata including document category, issuing authority, "
                "and completeness score."
            ),
            backstory=(
                "You are an expert document analyst with deep knowledge of "
                "government-issued identity documents, licenses, and official records. "
                "You can identify document types, detect quality issues (blurriness, "
                "tampering, incompleteness), and route documents to the correct "
                "processing pipeline."
            ),
            tools=tools,
            llm=ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.0,  # deterministic for classification
                api_key=settings.OPENAI_API_KEY,
            ),
            verbose=verbose,
            allow_delegation=False,
            max_iter=3,
        )


class DataExtractorAgent:
    """
    Agent 2: Data Extractor
    Extracts structured fields from classified documents and cross-references
    against government data sources via MCP tool.
    """

    def __init__(self, tools: List, verbose: bool = False):
        self.agent = Agent(
            role="Document Data Extraction Specialist",
            goal=(
                "Extract all required data fields from the document with high accuracy. "
                "Cross-reference extracted data against authoritative government databases "
                "to verify authenticity. Flag discrepancies immediately."
            ),
            backstory=(
                "You are a data extraction expert specializing in structured information "
                "retrieval from government documents. You have access to real-time "
                "government database APIs and can verify extracted data against "
                "authoritative sources. You follow strict data handling protocols."
            ),
            tools=tools,
            llm=ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.0,
                api_key=settings.OPENAI_API_KEY,
            ),
            verbose=verbose,
            allow_delegation=False,
            max_iter=5,
        )


class ComplianceValidatorAgent:
    """
    Agent 3: Compliance Validator
    Applies business rules and regulatory requirements to extracted data.
    """

    def __init__(self, tools: List, verbose: bool = False):
        self.agent = Agent(
            role="Compliance and Regulatory Validation Specialist",
            goal=(
                "Validate extracted document data against all applicable regulatory "
                "requirements, business rules, and compliance standards. "
                "Produce a clear pass/fail determination with detailed reasoning "
                "for every validation check performed."
            ),
            backstory=(
                "You are a compliance expert with comprehensive knowledge of "
                "government regulations for identity verification, driver licensing, "
                "and motor vehicle documentation. You apply rules precisely and "
                "document every decision for audit trail purposes."
            ),
            tools=tools,
            llm=ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.0,
                api_key=settings.OPENAI_API_KEY,
            ),
            verbose=verbose,
            allow_delegation=False,
            max_iter=3,
        )


class ReportGeneratorAgent:
    """
    Agent 4: Report Generator
    Synthesizes all prior agent outputs into a structured verification report.
    """

    def __init__(self, tools: List, verbose: bool = False):
        self.agent = Agent(
            role="Verification Report Specialist",
            goal=(
                "Synthesize all findings from classification, extraction, and validation "
                "agents into a clear, structured verification report. "
                "The report must be audit-ready, contain full traceability, "
                "and provide actionable recommendations."
            ),
            backstory=(
                "You are a technical writer and reporting specialist for government "
                "verification systems. You transform complex multi-step verification "
                "findings into clear, structured reports that meet regulatory audit "
                "requirements and are understandable to both technical and non-technical "
                "stakeholders."
            ),
            tools=tools,
            llm=ChatOpenAI(
                model=settings.LLM_MODEL,
                temperature=0.1,
                api_key=settings.OPENAI_API_KEY,
            ),
            verbose=verbose,
            allow_delegation=False,
            max_iter=2,
        )
