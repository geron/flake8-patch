import ast
from typing import Any, List, Set, Union

from flake8_plugin_utils import Visitor

from flake8_patch.errors import AssignmentError


class TargetVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.mutating_targets: List[ast.Name] = []

    def visit_Attribute(self, node: Union[ast.Attribute, ast.Subscript]) -> None:
        if isinstance(node.value, ast.Name):
            self.mutating_targets.append(node.value)
        elif isinstance(node.value, (ast.Attribute, ast.Subscript)):
            self.visit_Attribute(node.value)
        elif not isinstance(node.value, ast.Call):
            self.generic_visit(node.value)

    visit_Subscript = visit_Attribute


def get_mutating_targets(node: ast.AST) -> List[ast.Name]:
    visitor = TargetVisitor()
    visitor.visit(node)
    return visitor.mutating_targets


class AssignmentVisitor(Visitor[None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.imported_names: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imported_names.add(alias.asname or alias.name)

    visit_ImportFrom = visit_Import

    def check_target(self, target: ast.AST) -> None:
        for mutating_target in get_mutating_targets(target):
            name = mutating_target.id
            if name in self.imported_names:
                self.error_from_node(AssignmentError, mutating_target, name=name)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            self.check_target(target)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.check_target(node.target)
