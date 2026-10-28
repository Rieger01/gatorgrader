from gator import constants
from tree_sitter import Language, Parser
import tree_sitter_python as tsPython
import tree_sitter_java as tsJava

def parse_tree_sitter(code, language, multiline=False):

    def get_node_types(node, node_types):
        node_types.append(node.type)
        for child in node.children:
            get_node_types(child, node_types)

    if language == "Python":
        PARSE_LANGUAGE = Language(tsPython.language())
    else:
        PARSE_LANGUAGE = Language(tsJava.language())

    parser = Parser(PARSE_LANGUAGE)
    tree = parser.parse(code.encode("utf-8"))

    node_types = []
    get_node_types(tree.root_node, node_types)

    if language == "Java":
        if multiline:
            comment_count = node_types.count("block_comment")
        else:
            comment_count = node_types.count("line_comment")
    else:
        if not multiline:
            comment_count = node_types.count("comment")
        else:
            if multiline and language == "Python":
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
    matches_count = parse_tree_sitter(contents, "Java", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_python_comment(contents):
    """Count the number of singleline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, "Python", False)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_java_comment(contents):
    """Count the number of multiline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, "Java", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_python_comment(contents):
    """Count the number of multiline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, "Python", True)
    return matches_count, {constants.markers.First: matches_count}