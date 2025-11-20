"""
Pre-Built Workflow Definitions

Defines the 5 standard workflows for the Legal AI Platform.
"""

from workflows.workflow_engine import Workflow, WorkflowStep


def create_hr_onboarding_workflow() -> Workflow:
    """
    HR Onboarding Workflow

    Steps:
    1. HR Policy Agent - Answer employee questions
    2. Analysis Agent - Extract key onboarding points
    3. Synthesis Agent - Create personalized onboarding guide
    """
    workflow = Workflow(
        name="HR Employee Onboarding",
        description="Complete employee onboarding with personalized guides based on HR policies"
    )

    # Step 1: Get HR policy information
    workflow.add_step(WorkflowStep(
        name="hr_policy_query",
        agent_name="hr_policy",
        task_builder=lambda ctx, inp: {
            "question": inp.get("employee_question", "What are the key onboarding steps for a new employee?"),
            "context": inp.get("hr_policies", ""),
            "task_type": "onboarding"
        },
        description="Retrieve HR policy information relevant to onboarding"
    ))

    # Step 2: Analyze the HR information
    workflow.add_step(WorkflowStep(
        name="analyze_policies",
        agent_name="analysis",
        task_builder=lambda ctx, inp: {
            "data": ctx["hr_policy_query"].get("answer", ""),
            "focus": "Extract key onboarding steps, requirements, and important dates"
        },
        description="Extract actionable onboarding insights"
    ))

    # Step 3: Create personalized onboarding guide
    workflow.add_step(WorkflowStep(
        name="create_guide",
        agent_name="synthesis",
        task_builder=lambda ctx, inp: {
            "task_type": "synthesis",
            "sources": [
                {
                    "title": "HR Policy Information",
                    "content": ctx["hr_policy_query"].get("answer", "")
                },
                {
                    "title": "Key Onboarding Points",
                    "content": str(ctx["analyze_policies"])
                }
            ],
            "focus": f"Create personalized onboarding guide for {inp.get('employee_name', 'new employee')} ({inp.get('role', 'employee')})"
        },
        description="Generate comprehensive onboarding guide"
    ))

    return workflow


def create_cs_ticket_workflow() -> Workflow:
    """
    Customer Service Ticket Response Workflow

    Steps:
    1. CS Agent - Generate initial response
    2. Analysis Agent - Sentiment analysis and priority detection
    3. Synthesis Agent - Create final polished response
    """
    workflow = Workflow(
        name="CS Ticket Response",
        description="Intelligent customer ticket handling with sentiment analysis"
    )

    # Step 1: Generate initial CS response
    workflow.add_step(WorkflowStep(
        name="initial_response",
        agent_name="cs_document",
        task_builder=lambda ctx, inp: {
            "question": inp.get("customer_query", ""),
            "context": inp.get("support_docs", ""),
            "customer_name": inp.get("customer_name", "Customer")
        },
        description="Generate initial support response"
    ))

    # Step 2: Analyze sentiment and priority
    workflow.add_step(WorkflowStep(
        name="sentiment_analysis",
        agent_name="analysis",
        task_builder=lambda ctx, inp: {
            "data": f"Customer Query: {inp.get('customer_query', '')}\n\nInitial Response: {ctx['initial_response'].get('answer', '')}",
            "focus": "Analyze customer sentiment (positive/neutral/negative), urgency level, and satisfaction risk"
        },
        description="Detect sentiment and priority level"
    ))

    # Step 3: Create polished final response
    workflow.add_step(WorkflowStep(
        name="final_response",
        agent_name="synthesis",
        task_builder=lambda ctx, inp: {
            "task_type": "synthesis",
            "sources": [
                {
                    "title": "Initial Support Response",
                    "content": ctx["initial_response"].get("answer", "")
                },
                {
                    "title": "Sentiment & Priority Analysis",
                    "content": str(ctx["sentiment_analysis"])
                }
            ],
            "focus": "Create empathetic, professional final response addressing customer needs"
        },
        description="Generate final customer response"
    ))

    return workflow


def create_legal_hr_compliance_workflow() -> Workflow:
    """
    Legal-HR Compliance Check Workflow

    Steps:
    1. Legal Research - Get relevant ordinances
    2. Validation - Check HR policy compliance
    3. Synthesis - Create compliance report
    """
    workflow = Workflow(
        name="Legal-HR Compliance",
        description="Cross-domain compliance checking of HR policies against HK law"
    )

    # Step 1: Research relevant legal requirements
    workflow.add_step(WorkflowStep(
        name="legal_research",
        agent_name="legal_research",
        task_builder=lambda ctx, inp: {
            "question": inp.get("compliance_area", "What are the legal requirements for employee leave policies in Hong Kong?")
        },
        description="Research relevant Hong Kong ordinances"
    ))

    # Step 2: Validate HR policy against legal requirements
    workflow.add_step(WorkflowStep(
        name="compliance_validation",
        agent_name="validation",
        task_builder=lambda ctx, inp: {
            "documents": [
                {
                    "title": inp.get("policy_name", "HR Policy"),
                    "content": inp.get("policy_content", "")
                }
            ],
            "validation_type": "comprehensive",
            "sources": [
                {
                    "title": "Legal Requirements",
                    "content": ctx["legal_research"].get("answer", "")
                }
            ]
        },
        description="Validate policy compliance with legal requirements"
    ))

    # Step 3: Create compliance report
    workflow.add_step(WorkflowStep(
        name="compliance_report",
        agent_name="synthesis",
        task_builder=lambda ctx, inp: {
            "task_type": "synthesis",
            "sources": [
                {
                    "title": "Legal Requirements",
                    "content": ctx["legal_research"].get("answer", "")
                },
                {
                    "title": "Validation Results",
                    "content": str(ctx["compliance_validation"])
                }
            ],
            "focus": "Create compliance report with specific recommendations for policy improvements"
        },
        description="Generate comprehensive compliance report"
    ))

    return workflow


def create_simple_qa_workflow() -> Workflow:
    """
    Simple Q&A with Validation Workflow

    Steps:
    1. Legal Research - Answer the question
    2. Validation - Verify the answer accuracy
    """
    workflow = Workflow(
        name="Simple Q&A with Validation",
        description="Question answering with automatic accuracy validation"
    )

    # Step 1: Research and answer the question
    workflow.add_step(WorkflowStep(
        name="answer_question",
        agent_name="legal_research",
        task_builder=lambda ctx, inp: {
            "question": inp.get("question", "")
        },
        description="Research and provide answer"
    ))

    # Step 2: Validate the answer
    workflow.add_step(WorkflowStep(
        name="validate_answer",
        agent_name="validation",
        task_builder=lambda ctx, inp: {
            "documents": [
                {
                    "title": "Generated Answer",
                    "content": ctx["answer_question"].get("answer", "")
                }
            ],
            "validation_type": "accuracy",
            "question": inp.get("question", "")
        },
        description="Validate answer accuracy against legal sources"
    ))

    return workflow


def create_multi_agent_research_workflow() -> Workflow:
    """
    Multi-Agent Research Workflow

    Steps:
    1. Legal Research
    2. HR Policy Research (parallel conceptually, sequential in execution)
    3. CS Perspective (parallel conceptually, sequential in execution)
    4. Analysis - Extract patterns
    5. Synthesis - Comprehensive report
    """
    workflow = Workflow(
        name="Multi-Agent Research",
        description="Comprehensive multi-perspective analysis on a topic"
    )

    # Step 1: Legal perspective
    workflow.add_step(WorkflowStep(
        name="legal_perspective",
        agent_name="legal_research",
        task_builder=lambda ctx, inp: {
            "question": f"From a legal perspective: {inp.get('research_topic', '')}"
        },
        description="Research legal perspective"
    ))

    # Step 2: HR perspective
    workflow.add_step(WorkflowStep(
        name="hr_perspective",
        agent_name="hr_policy",
        task_builder=lambda ctx, inp: {
            "question": f"From an HR policy perspective: {inp.get('research_topic', '')}",
            "context": inp.get("hr_context", ""),
            "task_type": "general"
        },
        description="Research HR policy perspective"
    ))

    # Step 3: Customer service perspective
    workflow.add_step(WorkflowStep(
        name="cs_perspective",
        agent_name="cs_document",
        task_builder=lambda ctx, inp: {
            "question": f"From a customer service perspective: {inp.get('research_topic', '')}",
            "context": inp.get("cs_context", "")
        },
        description="Research customer service perspective"
    ))

    # Step 4: Analyze all perspectives
    workflow.add_step(WorkflowStep(
        name="cross_analysis",
        agent_name="analysis",
        task_builder=lambda ctx, inp: {
            "data": f"""Legal Perspective:\n{ctx['legal_perspective'].get('answer', '')}\n\n
                          HR Perspective:\n{ctx['hr_perspective'].get('answer', '')}\n\n
                          CS Perspective:\n{ctx['cs_perspective'].get('answer', '')}""",
            "focus": "Identify common themes, conflicts, and unique insights across all perspectives"
        },
        description="Cross-analyze all perspectives"
    ))

    # Step 5: Synthesize comprehensive report
    workflow.add_step(WorkflowStep(
        name="final_report",
        agent_name="synthesis",
        task_builder=lambda ctx, inp: {
            "task_type": "synthesis",
            "sources": [
                {
                    "title": "Legal Analysis",
                    "content": ctx["legal_perspective"].get("answer", "")
                },
                {
                    "title": "HR Policy Analysis",
                    "content": ctx["hr_perspective"].get("answer", "")
                },
                {
                    "title": "Customer Service Analysis",
                    "content": ctx["cs_perspective"].get("answer", "")
                },
                {
                    "title": "Cross-Perspective Insights",
                    "content": str(ctx["cross_analysis"])
                }
            ],
            "focus": f"Create comprehensive research report on: {inp.get('research_topic', '')}"
        },
        description="Generate final research report"
    ))

    return workflow


def get_all_workflows():
    """Get all available workflow definitions"""
    return {
        "hr_onboarding": create_hr_onboarding_workflow(),
        "cs_ticket": create_cs_ticket_workflow(),
        "legal_hr_compliance": create_legal_hr_compliance_workflow(),
        "simple_qa": create_simple_qa_workflow(),
        "multi_agent_research": create_multi_agent_research_workflow()
    }
