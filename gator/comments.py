from gator import constants
from tree_sitter import Language, Parser
import tree_sitter_python as tspython

def parse_tree_sitter(code, multiline=False):

    def find_comments(node, node_types):
        comments = []
        node_types.append(node.type)
        if node.type == "comment":
            comments.append(code[node.start_byte:node.end_byte])
        for child in node.children:
            comments.extend(find_comments(child, node_types))
        return comments

    PY_LANGUAGE = Language(tspython.language())
    parser = Parser(PY_LANGUAGE)
    tree = parser.parse(code.encode("utf-8"))

    node_types = []

    comment_count = len(find_comments(tree.root_node, node_types))

    if multiline:
        comment_prev = False
        comment_count = 0
        i = 0
        for _ in range(len(node_types)):
            if node_types[i] == "comment":
                if comment_prev:
                    j = 0
                    comment_count += 1
                    for _ in range(len(node_types[i:])):
                        if node_types[i+j] != "comment":
                            i = i + j
                            break
                        j = j + 1
                comment_prev = True
            else:
                comment_prev = False
            i = i+1
            if i >= len(node_types):
                break

    return comment_count


def count_singleline_java_comment(contents):
    """Count the number of singleline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_python_comment(contents):
    """Count the number of singleline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, False)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_java_comment(contents):
    """Count the number of multiline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_python_comment(contents):
    """Count the number of multiline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, True)
    return matches_count, {constants.markers.First: matches_count}