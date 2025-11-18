"""
Reference Workflows
Pre-built multi-agent workflows demonstrating platform capabilities
Supports HR, Customer Service, and cross-domain use cases
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def register_reference_workflows(orchestrator):
    """
    Register all reference workflows with the orchestrator

    Args:
        orchestrator: WorkflowOrchestrator instance
    """

    # ========================================================================
    # HR Onboarding Workflow
    # ========================================================================

    hr_onboarding_workflow = {
        "name": "hr_onboarding",
        "description": "Complete employee onboarding process with policy review and analysis",
        "domain": "hr",
        "tasks": [
            {
                "id": "gather_onboarding_info",
                "agent": "hr_policy",
                "input": {
                    "question": "What are the complete onboarding steps for a ${input.employee_type} employee in the ${input.department} department?",
                    "task_type": "onboarding",
                    "employee_type": "${input.employee_type}"
                },
                "description": "Get onboarding requirements and steps"
            },
            {
                "id": "get_benefits_info",
                "agent": "hr_policy",
                "input": {
                    "question": "What benefits are available for ${input.employee_type} employees?",
                    "task_type": "benefits",
                    "employee_type": "${input.employee_type}"
                },
                "description": "Retrieve benefits information"
            },
            {
                "id": "analyze_requirements",
                "agent": "analysis",
                "input": {
                    "data": {
                        "onboarding": "${gather_onboarding_info.answer}",
                        "benefits": "${get_benefits_info.answer}"
                    },
                    "analysis_type": "themes",
                    "focus": "Key deadlines, required documents, and critical action items"
                },
                "description": "Analyze onboarding requirements"
            },
            {
                "id": "synthesize_guide",
                "agent": "synthesis",
                "input": {
                    "sources": [
                        {
                            "type": "onboarding",
                            "content": "${gather_onboarding_info.answer}"
                        },
                        {
                            "type": "benefits",
                            "content": "${get_benefits_info.answer}"
                        },
                        {
                            "type": "analysis",
                            "content": "${analyze_requirements.analysis}"
                        }
                    ],
                    "synthesis_type": "report",
                    "output_format": "markdown",
                    "focus": "Create a comprehensive onboarding guide for ${input.employee_name}"
                },
                "description": "Create personalized onboarding guide"
            },
            {
                "id": "validate_guide",
                "agent": "validation",
                "input": {
                    "content": "${synthesize_guide.output}",
                    "validation_type": "completeness",
                    "requirements": {
                        "must_include": ["onboarding steps", "benefits", "deadlines", "documents"],
                        "employee_type": "${input.employee_type}"
                    }
                },
                "description": "Validate onboarding guide completeness"
            }
        ],
        "output": {
            "onboarding_guide": "${synthesize_guide.output}",
            "validation": "${validate_guide.validation_result}",
            "quality_score": "${validate_guide.quality_score}",
            "key_insights": "${analyze_requirements.insights}",
            "policy_references": "${gather_onboarding_info.policy_references}"
        }
    }

    orchestrator.register_workflow("hr_onboarding", hr_onboarding_workflow)
    logger.info("Registered HR onboarding workflow")


    # ========================================================================
    # Customer Service Ticket Response Workflow
    # ========================================================================

    cs_ticket_workflow = {
        "name": "cs_ticket_response",
        "description": "Intelligent customer service ticket handling with routing and validation",
        "domain": "customer_service",
        "tasks": [
            {
                "id": "analyze_ticket",
                "agent": "analysis",
                "input": {
                    "data": {
                        "ticket": "${input.ticket_content}",
                        "customer_history": "${input.customer_history}"
                    },
                    "analysis_type": "themes",
                    "focus": "Customer sentiment, key issues, urgency indicators"
                },
                "description": "Analyze ticket content and sentiment"
            },
            {
                "id": "route_ticket",
                "agent": "cs_document",
                "input": {
                    "ticket": "${input.ticket_content}",
                    "task_type": "route",
                    "priority": "${input.priority}",
                    "category": "${input.category}"
                },
                "description": "Determine optimal routing"
            },
            {
                "id": "generate_response",
                "agent": "cs_document",
                "input": {
                    "ticket": "${input.ticket_content}",
                    "task_type": "respond",
                    "customer_info": {
                        "type": "${input.customer_type}",
                        "history": "${input.customer_history}"
                    },
                    "category": "${input.category}"
                },
                "description": "Generate customer response"
            },
            {
                "id": "validate_response",
                "agent": "validation",
                "input": {
                    "content": "${generate_response.response}",
                    "validation_type": "comprehensive",
                    "requirements": {
                        "addresses_issue": True,
                        "professional_tone": True,
                        "includes_next_steps": True
                    },
                    "question": "${input.ticket_content}"
                },
                "description": "Validate response quality"
            },
            {
                "id": "check_escalation",
                "agent": "cs_document",
                "input": {
                    "ticket": "${input.ticket_content}",
                    "task_type": "escalate",
                    "priority": "${route_ticket.routing.priority_adjustment}",
                    "customer_info": {
                        "type": "${input.customer_type}",
                        "sentiment": "${analyze_ticket.insights}"
                    }
                },
                "description": "Prepare escalation if needed"
            }
        ],
        "output": {
            "response": "${generate_response.response}",
            "routing": "${route_ticket.routing}",
            "escalation_needed": "${generate_response.escalation_needed}",
            "escalation_summary": "${check_escalation.response}",
            "validation": "${validate_response.validation_result}",
            "quality_score": "${validate_response.quality_score}",
            "sentiment_analysis": "${analyze_ticket.analysis}"
        }
    }

    orchestrator.register_workflow("cs_ticket_response", cs_ticket_workflow)
    logger.info("Registered CS ticket response workflow")


    # ========================================================================
    # Cross-Domain: Legal Compliance for HR Policy
    # ========================================================================

    legal_hr_compliance_workflow = {
        "name": "legal_hr_compliance",
        "description": "Check HR policy compliance with legal requirements (cross-domain workflow)",
        "domain": "cross_domain",
        "tasks": [
            {
                "id": "get_hr_policy",
                "agent": "hr_policy",
                "input": {
                    "question": "What is our policy on ${input.policy_topic}?",
                    "task_type": "policy_search",
                    "context": "${input.context}"
                },
                "description": "Retrieve HR policy"
            },
            {
                "id": "search_legal_requirements",
                "agent": "legal_research",
                "input": {
                    "question": "What are the Hong Kong legal requirements for ${input.policy_topic}?",
                    "search_type": "sections",
                    "top_k": 5
                },
                "description": "Find relevant legal ordinances"
            },
            {
                "id": "compare_policy_and_law",
                "agent": "analysis",
                "input": {
                    "data": {
                        "hr_policy": "${get_hr_policy.answer}",
                        "legal_requirements": "${search_legal_requirements.answer}",
                        "sources": "${search_legal_requirements.sources}"
                    },
                    "analysis_type": "comparison",
                    "focus": "Identify gaps, conflicts, and compliance issues between HR policy and legal requirements"
                },
                "description": "Compare policy against legal requirements"
            },
            {
                "id": "synthesize_compliance_report",
                "agent": "synthesis",
                "input": {
                    "sources": [
                        {
                            "type": "hr_policy",
                            "content": "${get_hr_policy.answer}"
                        },
                        {
                            "type": "legal_requirements",
                            "content": "${search_legal_requirements.answer}"
                        },
                        {
                            "type": "gap_analysis",
                            "content": "${compare_policy_and_law.analysis}"
                        }
                    ],
                    "synthesis_type": "reconcile",
                    "output_format": "structured",
                    "focus": "Create compliance assessment with recommendations"
                },
                "description": "Generate compliance report"
            },
            {
                "id": "validate_analysis",
                "agent": "validation",
                "input": {
                    "content": "${synthesize_compliance_report.output}",
                    "sources": [
                        "${get_hr_policy.answer}",
                        "${search_legal_requirements.answer}"
                    ],
                    "validation_type": "comprehensive",
                    "requirements": {
                        "must_identify_gaps": True,
                        "must_cite_law": True,
                        "must_provide_recommendations": True
                    },
                    "question": "Is our ${input.policy_topic} policy compliant with Hong Kong law?"
                },
                "description": "Validate compliance analysis"
            }
        ],
        "output": {
            "compliance_report": "${synthesize_compliance_report.output}",
            "hr_policy": "${get_hr_policy.answer}",
            "legal_requirements": "${search_legal_requirements.answer}",
            "gap_analysis": "${compare_policy_and_law.analysis}",
            "recommendations": "${synthesize_compliance_report.recommendations}",
            "validation": "${validate_analysis.validation_result}",
            "quality_score": "${validate_analysis.quality_score}",
            "legal_citations": "${search_legal_requirements.sources}"
        }
    }

    orchestrator.register_workflow("legal_hr_compliance", legal_hr_compliance_workflow)
    logger.info("Registered legal HR compliance workflow")


    # ========================================================================
    # Simple: Document Q&A with Validation
    # ========================================================================

    simple_qa_workflow = {
        "name": "simple_qa",
        "description": "Simple question answering with validation (general purpose)",
        "domain": "general",
        "tasks": [
            {
                "id": "answer_question",
                "agent": "${input.domain}_document",  # Dynamic agent selection
                "input": {
                    "question": "${input.question}",
                    "context": "${input.context}",
                    "task_type": "general"
                },
                "description": "Answer question using domain knowledge"
            },
            {
                "id": "validate_answer",
                "agent": "validation",
                "input": {
                    "content": "${answer_question.answer}",
                    "validation_type": "accuracy",
                    "question": "${input.question}",
                    "requirements": {
                        "min_length": 50,
                        "must_answer_question": True
                    }
                },
                "description": "Validate answer quality"
            }
        ],
        "output": {
            "answer": "${answer_question.answer}",
            "validation": "${validate_answer.validation_result}",
            "quality_score": "${validate_answer.quality_score}",
            "confidence": "${answer_question.confidence}"
        }
    }

    orchestrator.register_workflow("simple_qa", simple_qa_workflow)
    logger.info("Registered simple Q&A workflow")


    # ========================================================================
    # Multi-Agent Research: Complex Analysis
    # ========================================================================

    research_workflow = {
        "name": "multi_agent_research",
        "description": "Comprehensive research using multiple agents (demonstrates parallel agent coordination)",
        "domain": "general",
        "tasks": [
            {
                "id": "gather_legal_info",
                "agent": "legal_research",
                "input": {
                    "question": "${input.research_question}",
                    "search_type": "sections",
                    "top_k": 5
                },
                "description": "Gather legal perspective"
            },
            {
                "id": "gather_hr_info",
                "agent": "hr_policy",
                "input": {
                    "question": "${input.research_question}",
                    "task_type": "general",
                    "context": "${input.context}"
                },
                "description": "Gather HR perspective"
            },
            {
                "id": "analyze_legal",
                "agent": "analysis",
                "input": {
                    "data": "${gather_legal_info.answer}",
                    "analysis_type": "themes",
                    "focus": "Legal implications and requirements"
                },
                "description": "Analyze legal information"
            },
            {
                "id": "analyze_hr",
                "agent": "analysis",
                "input": {
                    "data": "${gather_hr_info.answer}",
                    "analysis_type": "themes",
                    "focus": "HR policy implications and requirements"
                },
                "description": "Analyze HR information"
            },
            {
                "id": "synthesize_findings",
                "agent": "synthesis",
                "input": {
                    "sources": [
                        {
                            "type": "legal",
                            "content": "${gather_legal_info.answer}",
                            "analysis": "${analyze_legal.analysis}"
                        },
                        {
                            "type": "hr",
                            "content": "${gather_hr_info.answer}",
                            "analysis": "${analyze_hr.analysis}"
                        }
                    ],
                    "synthesis_type": "merge",
                    "output_format": "report",
                    "focus": "Comprehensive multi-perspective analysis of: ${input.research_question}"
                },
                "description": "Synthesize all perspectives"
            },
            {
                "id": "final_validation",
                "agent": "validation",
                "input": {
                    "content": "${synthesize_findings.output}",
                    "sources": [
                        "${gather_legal_info.answer}",
                        "${gather_hr_info.answer}"
                    ],
                    "validation_type": "comprehensive",
                    "question": "${input.research_question}",
                    "requirements": {
                        "must_include_legal": True,
                        "must_include_hr": True,
                        "must_be_synthesized": True
                    }
                },
                "description": "Validate comprehensive analysis"
            }
        ],
        "output": {
            "research_report": "${synthesize_findings.output}",
            "legal_perspective": {
                "content": "${gather_legal_info.answer}",
                "analysis": "${analyze_legal.analysis}",
                "sources": "${gather_legal_info.sources}"
            },
            "hr_perspective": {
                "content": "${gather_hr_info.answer}",
                "analysis": "${analyze_hr.analysis}"
            },
            "validation": "${final_validation.validation_result}",
            "quality_score": "${final_validation.quality_score}"
        }
    }

    orchestrator.register_workflow("multi_agent_research", research_workflow)
    logger.info("Registered multi-agent research workflow")


    logger.info("✓ All reference workflows registered successfully")
    logger.info(f"  - {len(orchestrator.list_workflows())} workflows available")


def get_workflow_examples() -> Dict[str, Any]:
    """
    Get example input data for each workflow

    Returns:
        Dict mapping workflow names to example inputs
    """
    return {
        "hr_onboarding": {
            "employee_name": "John Doe",
            "employee_type": "full-time",
            "department": "Engineering",
            "start_date": "2024-01-15"
        },
        "cs_ticket_response": {
            "ticket_content": "I can't access my account after the password reset. I've tried 3 times and it keeps saying invalid credentials.",
            "customer_type": "premium",
            "customer_history": "Customer for 2 years, no previous issues",
            "priority": "medium",
            "category": "account_access"
        },
        "legal_hr_compliance": {
            "policy_topic": "employee leave and vacation",
            "context": "We want to review our vacation policy to ensure legal compliance"
        },
        "simple_qa": {
            "domain": "hr",
            "question": "What is the vacation policy for new employees?",
            "context": "Full-time employee starting next month"
        },
        "multi_agent_research": {
            "research_question": "What are the requirements and implications for maternity leave?",
            "context": "Need to understand both legal requirements and HR policy aspects"
        }
    }


def get_workflow_descriptions() -> Dict[str, str]:
    """
    Get user-friendly descriptions for each workflow

    Returns:
        Dict mapping workflow names to descriptions
    """
    return {
        "hr_onboarding": "Complete employee onboarding with personalized guide generation, benefits information, and validation",
        "cs_ticket_response": "Intelligent customer service ticket handling with sentiment analysis, routing, response generation, and quality validation",
        "legal_hr_compliance": "Cross-domain workflow checking HR policy compliance against Hong Kong legal requirements",
        "simple_qa": "Simple question answering with validation (can work with any domain)",
        "multi_agent_research": "Comprehensive multi-perspective research using Legal + HR agents with analysis and synthesis"
    }
