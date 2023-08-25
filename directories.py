"""
CLI to help organize file in directories.

Possible commands:
    - CREATE: Creates a directory; can be nested
    - MOVE: Moves a directory from source to destination
    - DELETE: Removes a directory from 'filesystem'
    - LIST: Displays all directories in the 'filesystem'
"""
import logging
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

PARENT_FILESYSTEM: str = "home"
PATH_SEPARATOR: str = "/"


class COMMANDS(Enum):
    """Maintain a finite options of commands."""

    CREATE: str = "CREATE"
    MOVE: str = "MOVE"
    DELETE: str = "DELETE"
    LIST: str = "LIST"

    @classmethod
    def list_commands(cls):
        """Return a list of all possible command enums."""
        return list(map(lambda c: c.value, cls))


@dataclass
class Node:
    """Represent a single parent node and it's child(ren) sub-nodes."""

    parent: str
    children: list = field(default_factory=list)


@dataclass
class DirectoryCommands:
    """Parent class to hold dir commands implementation."""

    dir_command: str
    root_node: str = Node(PARENT_FILESYSTEM)

    def factory(self) -> None:
        """Factory method to a command."""
        command_args = self.dir_command.split(" ")
        first_command = command_args[0]
        allowed_commands = COMMANDS.list_commands()
        if first_command not in allowed_commands:
            logger.error(
                f"{first_command} is not an allowed command. "
                f"Use any of {allowed_commands}"
            )

        match first_command:
            case COMMANDS.CREATE.value:
                path = self.process_path(command_args[1])
                return self.create(self.root_node, path)

            case COMMANDS.LIST.value:
                return self.list()

            case COMMANDS.DELETE.value:
                path = self.process_path(command_args[1])
                deleted = self.delete(self.root_node, path)
                if not deleted:
                    raise SystemError("error")

                return self.root_node

            case COMMANDS.MOVE.value:
                path = self.process_path(command_args[1])
                parent = path[len(path) - 1]
                child = command_args[2]
                return self.move(self.root_node, parent, child)

            case _:
                pass

    def process_path(self, path: str) -> list:
        """Parse path's string input."""
        if PATH_SEPARATOR in path:
            return path.split(PATH_SEPARATOR)

        return [path]

    def process_node(
        self,
        node: Node,
        node_list: list,
        indent: int = 0,
    ) -> None:
        """Process a nested node into human readable output."""
        node_list.append(node)
        print(" " * indent + node.parent + "/")

        for child in node.children:
            self.process_node(child, node_list, indent + 1)

    def search(self, node: Node, parent: str) -> Node | None:
        """Retrieve a parent node given it's name."""
        if node.parent == parent:
            return node

        for child in node.children:
            results = self.search(child, parent)
            if results:
                return results

        return None

    def create(self, node: Node, dir: list) -> Node:
        """CREATE command implementation."""
        parent_node = node
        for each in dir:
            if each != parent_node.parent:
                child_node = Node(each)
                parent_node.children.append(child_node)
                parent_node = child_node

        return node

    def move(self, node: Node, parent: str, target_child: str) -> bool:
        """MOVE command implementation."""
        for child in node.children:
            if child.parent == target_child:
                node.children.remove(child)
                new_parent = self.search(self.root_node, parent)
                if new_parent:
                    new_parent.children.append(child)
                    return True
                else:
                    logger.error(f"parent directory {parent} not found")
                    return False

            elif child.children:
                if self.move(child, parent, target_child):
                    return True

        return False

    def delete(self, node: Node, dir: list) -> bool:
        """DELETE command implementation."""
        target_parent = dir[len(dir) - 1]
        for child in node.children:
            if child.parent == target_parent:
                node.children.remove(child)
                return True

            elif child.children:
                if self.delete(child, dir):
                    return True

        return False

    def list(self) -> list:
        """LIST command implementation."""
        node_list: list = []
        self.process_node(self.root_node, node_list)
        return node_list


if __name__ == "__main__":
    while True:
        inp = input()
        commands = DirectoryCommands(inp)
        commands.factory()
