"""
Agent-Mesh: Lightweight Decentralized Multi-Agent Swarm Framework
Created by Kush Aggarwal (@kushaggarwal2007-byte)
"""
import asyncio
import logging
from typing import Dict, Any, Optional, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("agent_mesh")

class AgentNode:
    def __init__(self, name: str, role: str, handler: Optional[Callable] = None):
        self.name = name
        self.role = role
        self.handler = handler or self.default_handler
        self.memory: list = []

    async def default_handler(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success", "result": f"Executed by {self.name}: {task}"}

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        logger.info(f"[{self.name}] Executing task: {task}")
        res = await self.handler(task, context)
        self.memory.append({"task": task, "result": res})
        return res

    async def delegate(self, peer: "AgentNode", task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"[{self.name}] Delegating to peer [{peer.name}]: {task}")
        return await peer.execute(task, context)

class MeshNetwork:
    def __init__(self):
        self.nodes: Dict[str, AgentNode] = {}

    def register(self, node: AgentNode) -> None:
        self.nodes[node.name] = node
        logger.info(f"Registered node: {node.name} ({node.role})")

    def get_node(self, name: str) -> Optional[AgentNode]:
        return self.nodes.get(name)
