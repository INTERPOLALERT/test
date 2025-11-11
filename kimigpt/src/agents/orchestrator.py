"""
KimiGPT - Master Orchestrator Agent
Coordinates all other agents and manages workflow
"""

import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    Master Orchestrator Agent
    - Analyzes user requests
    - Breaks down tasks into subtasks
    - Assigns tasks to specialized agents
    - Coordinates between agents
    - Validates final output
    - Manages API rotation and failover
    """

    def __init__(self, api_manager):
        """Initialize Orchestrator Agent"""
        self.api_manager = api_manager
        self.workflow_state = {}
        self.task_history = []

    def analyze_request(self, user_input: str,
                       attachments: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Analyze user request and create execution plan

        Args:
            user_input: User's text prompt
            attachments: List of uploaded files

        Returns:
            Execution plan with tasks assigned to agents
        """
        logger.info("Orchestrator: Analyzing user request...")

        # Build analysis prompt
        analysis_prompt = f"""Analyze this website generation request and create a structured execution plan:

User Request: "{user_input}"

Attachments: {len(attachments) if attachments else 0} files

Provide analysis in JSON format:
{{
    "website_type": "portfolio|business|ecommerce|blog|landing_page|etc",
    "complexity": "simple|moderate|advanced",
    "key_features": ["feature1", "feature2"],
    "design_style": "modern|minimal|professional|creative|etc",
    "color_preferences": ["color1", "color2"] or "auto",
    "has_images": true/false,
    "has_video": true/false,
    "page_count": number,
    "sections": ["section1", "section2"],
    "special_requirements": ["req1", "req2"]
}}

Analyze carefully and provide complete JSON."""

        # Get analysis from API
        response = self.api_manager.generate(
            analysis_prompt,
            preferred_provider="groq",
            task_type="text",
            temperature=0.3
        )

        if not response.get("success"):
            logger.error("Failed to analyze request")
            return {"error": "Analysis failed"}

        # Parse analysis
        try:
            # Extract JSON from response
            analysis_text = response["response"]
            # Find JSON in response
            start_idx = analysis_text.find("{")
            end_idx = analysis_text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = analysis_text[start_idx:end_idx]
                analysis = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")

        except Exception as e:
            logger.error(f"Failed to parse analysis: {e}")
            # Fallback to basic analysis
            analysis = {
                "website_type": "business",
                "complexity": "moderate",
                "key_features": ["responsive", "modern"],
                "design_style": "modern",
                "color_preferences": "auto",
                "has_images": bool(attachments),
                "has_video": False,
                "page_count": 1,
                "sections": ["hero", "features", "contact"],
                "special_requirements": []
            }

        logger.info(f"Analysis complete: {analysis['website_type']} website, {analysis['complexity']} complexity")

        return analysis

    def create_execution_plan(self, analysis: Dict[str, Any],
                             attachments: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """
        Create execution plan based on analysis

        Args:
            analysis: Analysis results from analyze_request
            attachments: User attachments

        Returns:
            List of tasks with assigned agents
        """
        logger.info("Orchestrator: Creating execution plan...")

        tasks = []
        task_id = 1

        # Task 1: Understanding & Requirements (always first)
        tasks.append({
            "id": task_id,
            "agent": "understanding",
            "task": "process_requirements",
            "description": "Process and understand detailed requirements",
            "inputs": {
                "analysis": analysis,
                "attachments": attachments
            },
            "status": "pending"
        })
        task_id += 1

        # Task 2: Image Processing (if images attached)
        if attachments and any(a.get("type") == "image" for a in attachments):
            tasks.append({
                "id": task_id,
                "agent": "image",
                "task": "process_images",
                "description": "Process, optimize, and analyze images",
                "inputs": {
                    "images": [a for a in attachments if a.get("type") == "image"]
                },
                "depends_on": [],
                "status": "pending"
            })
            task_id += 1

        # Task 3: Design Creation
        tasks.append({
            "id": task_id,
            "agent": "design",
            "task": "create_design",
            "description": "Create UI/UX design and styling",
            "inputs": {
                "analysis": analysis,
                "has_images": bool(attachments)
            },
            "depends_on": [1],
            "status": "pending"
        })
        design_task_id = task_id
        task_id += 1

        # Task 4: Content Generation (if needed)
        if analysis.get("complexity") != "simple":
            tasks.append({
                "id": task_id,
                "agent": "content",
                "task": "generate_content",
                "description": "Generate website content and copy",
                "inputs": {
                    "analysis": analysis,
                    "sections": analysis.get("sections", [])
                },
                "depends_on": [1],
                "status": "pending"
            })
            content_task_id = task_id
            task_id += 1
        else:
            content_task_id = None

        # Task 5: Code Generation
        depends_on = [design_task_id]
        if content_task_id:
            depends_on.append(content_task_id)

        tasks.append({
            "id": task_id,
            "agent": "code",
            "task": "generate_code",
            "description": "Generate HTML/CSS/JavaScript code",
            "inputs": {
                "analysis": analysis,
                "page_count": analysis.get("page_count", 1)
            },
            "depends_on": depends_on,
            "status": "pending"
        })
        code_task_id = task_id
        task_id += 1

        # Task 6: Quality Assurance
        tasks.append({
            "id": task_id,
            "agent": "qa",
            "task": "test_website",
            "description": "Test and validate generated website",
            "inputs": {
                "requirements": analysis
            },
            "depends_on": [code_task_id],
            "status": "pending"
        })
        qa_task_id = task_id
        task_id += 1

        # Task 7: Deployment Preparation
        tasks.append({
            "id": task_id,
            "agent": "deployment",
            "task": "package_website",
            "description": "Package website for deployment",
            "inputs": {
                "analysis": analysis
            },
            "depends_on": [qa_task_id],
            "status": "pending"
        })

        logger.info(f"Execution plan created with {len(tasks)} tasks")

        return tasks

    def execute_workflow(self, tasks: List[Dict[str, Any]],
                        agents: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute workflow by coordinating agents

        Args:
            tasks: List of tasks to execute
            agents: Dictionary of initialized agents

        Returns:
            Final result with generated website
        """
        logger.info("Orchestrator: Executing workflow...")

        results = {}
        task_outputs = {}

        for task in tasks:
            task_id = task["id"]
            agent_name = task["agent"]
            task_name = task["task"]

            logger.info(f"Executing Task {task_id}: {task['description']}")

            # Check dependencies
            depends_on = task.get("depends_on", [])
            if depends_on:
                dependencies_met = all(dep in task_outputs for dep in depends_on)
                if not dependencies_met:
                    logger.warning(f"Task {task_id} dependencies not met, skipping")
                    continue

            # Get agent
            agent = agents.get(agent_name)
            if not agent:
                logger.error(f"Agent {agent_name} not found!")
                continue

            # Prepare inputs
            inputs = task["inputs"].copy()

            # Add outputs from dependent tasks
            for dep_id in depends_on:
                if dep_id in task_outputs:
                    inputs[f"task_{dep_id}_output"] = task_outputs[dep_id]

            # Execute task
            try:
                task_method = getattr(agent, task_name)
                output = task_method(**inputs)

                task_outputs[task_id] = output
                task["status"] = "completed"
                task["output"] = output

                logger.info(f"✓ Task {task_id} completed successfully")

            except Exception as e:
                logger.error(f"✗ Task {task_id} failed: {e}")
                task["status"] = "failed"
                task["error"] = str(e)

        # Compile final result
        final_result = {
            "success": True,
            "tasks": tasks,
            "outputs": task_outputs,
            "website": task_outputs.get(max(task_outputs.keys())) if task_outputs else None
        }

        logger.info("Workflow execution completed")

        return final_result

    def handle_request(self, user_input: str,
                      attachments: Optional[List[Dict]] = None,
                      agents: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point: Handle complete user request

        Args:
            user_input: User's prompt
            attachments: Uploaded files
            agents: Dictionary of agent instances

        Returns:
            Complete result with generated website
        """
        logger.info("=" * 60)
        logger.info("ORCHESTRATOR: Starting new website generation request")
        logger.info("=" * 60)

        try:
            # Step 1: Analyze request
            analysis = self.analyze_request(user_input, attachments)
            if "error" in analysis:
                return {"success": False, "error": analysis["error"]}

            # Step 2: Create execution plan
            tasks = self.create_execution_plan(analysis, attachments)

            # Step 3: Execute workflow
            result = self.execute_workflow(tasks, agents)

            # Step 4: Return result
            result["analysis"] = analysis

            logger.info("=" * 60)
            logger.info("ORCHESTRATOR: Request completed successfully")
            logger.info("=" * 60)

            return result

        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
