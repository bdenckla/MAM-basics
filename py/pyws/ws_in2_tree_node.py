""" Exports TreeNode """

from dataclasses import dataclass


@dataclass
class TreeNode:
    """Wikisource parser tree node"""

    name: str
    children: list
    named_children: dict = None

    def __init__(self, name: str = None, children: list = None):
        self.name = name
        self.children = children or []
        self.named_children = {}
