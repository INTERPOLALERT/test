"""
KimiGPT - Multi-Agent System Coordinator
Main system that initializes and coordinates all agents
"""

import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.api.api_manager import get_api_manager
from src.agents.orchestrator import OrchestratorAgent
from src.agents.understanding_agent import UnderstandingAgent
from src.agents.design_agent import DesignAgent
from src.agents.code_agent import CodeAgent
from src.agents.image_agent import ImageAgent
from src.agents.content_agent import ContentAgent
from src.agents.qa_agent import QAAgent
from src.agents.deployment_agent import DeploymentAgent

logger = logging.getLogger(__name__)


class MultiAgentSystem:
    """
    Multi-Agent System Coordinator
    Initializes and manages all AI agents
    """

    def __init__(self):
        """Initialize the multi-agent system"""
        logger.info("Initializing Multi-Agent System...")

        # Initialize API Manager
        self.api_manager = get_api_manager()

        # Initialize all agents
        self.agents = self._initialize_agents()

        # Initialize orchestrator
        self.orchestrator = OrchestratorAgent(self.api_manager)

        logger.info("✓ Multi-Agent System initialized successfully")

    def _initialize_agents(self) -> dict:
        """Initialize all specialized agents"""
        agents = {}

        try:
            agents["understanding"] = UnderstandingAgent(self.api_manager)
            logger.info("✓ Understanding Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Understanding Agent: {e}")

        try:
            agents["design"] = DesignAgent(self.api_manager)
            logger.info("✓ Design Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Design Agent: {e}")

        try:
            agents["code"] = CodeAgent(self.api_manager)
            logger.info("✓ Code Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Code Agent: {e}")

        try:
            agents["image"] = ImageAgent(self.api_manager)
            logger.info("✓ Image Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Image Agent: {e}")

        try:
            agents["content"] = ContentAgent(self.api_manager)
            logger.info("✓ Content Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Content Agent: {e}")

        try:
            agents["qa"] = QAAgent(self.api_manager)
            logger.info("✓ QA Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize QA Agent: {e}")

        try:
            agents["deployment"] = DeploymentAgent(self.api_manager)
            logger.info("✓ Deployment Agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Deployment Agent: {e}")

        return agents

    def generate_website(self, user_prompt: str, attachments=None) -> dict:
        """
        Main entry point for website generation

        Args:
            user_prompt: User's text input
            attachments: List of uploaded files

        Returns:
            Complete generation result
        """
        logger.info("=" * 80)
        logger.info("MULTI-AGENT SYSTEM: Starting website generation")
        logger.info("=" * 80)

        try:
            # Pass request to orchestrator
            result = self.orchestrator.handle_request(
                user_input=user_prompt,
                attachments=attachments,
                agents=self.agents
            )

            logger.info("=" * 80)
            logger.info("MULTI-AGENT SYSTEM: Website generation completed")
            logger.info("=" * 80)

            return result

        except Exception as e:
            logger.error(f"Multi-Agent System error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_system_status(self) -> dict:
        """Get current system status"""
        return {
            "agents": {
                name: "active" for name in self.agents.keys()
            },
            "api_status": self.api_manager.get_status()
        }


# Global instance
_multi_agent_system = None


def get_multi_agent_system() -> MultiAgentSystem:
    """Get global multi-agent system instance"""
    global _multi_agent_system
    if _multi_agent_system is None:
        _multi_agent_system = MultiAgentSystem()
    return _multi_agent_system


if __name__ == "__main__":
    # Test the system
    system = MultiAgentSystem()
    result = system.generate_website("Create a modern portfolio website")
    print(result)
