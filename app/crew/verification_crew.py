"""
Agentic Document Verification Workflow
Multi-agent system using CrewAI + LangChain for automated document processing.
Based on production implementation at State of Florida DL & MV services.
"""

import logging
from typing import Optional
from crewai import Crew, Process
from app.agents.classifier import DocumentClassifierAgent
from app.agents.extractor import DataExtractorAgent
from app.agents.validator import ComplianceValidatorAgent
from app.agents.reporter import ReportGeneratorAgent
from app.tasks.verification_tasks import (
    classify_task,
    extract_task,
    validate_task,
    report_task,
)
from app.tools.mcp_tool import GovernmentDataTool
from app.tools.document_tools import PDFReaderTool, OCRTool
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class DocumentVerificationCrew:
    """
    Multi-agent document verification system.

    Agents:
    1. Classifier   — determines document type and routing
    2. Extractor    — extracts structured data fields
    3. Validator    — checks compliance rules and data integrity
    4. Reporter     — generates structured verification report

    Each agent operates independently and communicates via CrewAI's
    shared memory and task output chaining.
    """

    def __init__(self):
        self._init_tools()
        self._init_agents()

    def _init_tools(self):
        self.gov_data_tool = GovernmentDataTool(
            endpoint=settings.GOV_DATA_API_URL,
            api_key=settings.GOV_DATA_API_KEY,
        )
        self.pdf_tool = PDFReaderTool()
        self.ocr_tool = OCRTool()

    def _init_agents(self):
        self.classifier = DocumentClassifierAgent(
            tools=[self.pdf_tool, self.ocr_tool],
            verbose=settings.AGENT_VERBOSE,
        )
        self.extractor = DataExtractorAgent(
            tools=[self.pdf_tool, self.ocr_tool, self.gov_data_tool],
            verbose=settings.AGENT_VERBOSE,
        )
        self.validator = ComplianceValidatorAgent(
            tools=[self.gov_data_tool],
            verbose=settings.AGENT_VERBOSE,
        )
        self.reporter = ReportGeneratorAgent(
            tools=[],
            verbose=settings.AGENT_VERBOSE,
        )

    def run(self, document_path: str, applicant_id: Optional[str] = None) -> dict:
        """
        Execute full document verification workflow.

        Args:
            document_path: Path or S3 URI to the document
            applicant_id: Optional applicant ID for cross-referencing gov data

        Returns:
            Structured verification report dict
        """
        logger.info(f"Starting verification workflow for document: {document_path}")

        tasks = [
            classify_task(self.classifier, document_path),
            extract_task(self.extractor, document_path, applicant_id),
            validate_task(self.validator),
            report_task(self.reporter, applicant_id),
        ]

        crew = Crew(
            agents=[
                self.classifier.agent,
                self.extractor.agent,
                self.validator.agent,
                self.reporter.agent,
            ],
            tasks=tasks,
            process=Process.sequential,  # each task feeds into the next
            verbose=settings.AGENT_VERBOSE,
            memory=True,  # enable shared crew memory
            embedder={
                "provider": "openai",
                "config": {"model": "text-embedding-3-small"},
            },
        )

        result = crew.kickoff()
        logger.info(f"Verification workflow completed for: {document_path}")
        return result
