from gator import constants
from tree_sitter import Language, Parser
import tree_sitter_python as tsPython
import tree_sitter_java as tsJava
import tree_sitter_cpp as tsCPP
import tree_sitter_c as tsC
import tree_sitter_javascript as tsJavaScript

def parse_tree_sitter(code, language, multiline=False):

    def get_node_types(node, node_types):
        comments = []
        nodes.append(node)
        node_types.append(node.type)
        if node.type == "comment":
            comments.append(code[node.start_byte:node.end_byte])
        for child in node.children:
            comments.extend(get_node_types(child, node_types))
        return comments

    if language == "Python":
        PARSE_LANGUAGE = Language(tsPython.language())
    elif language == "Java":
        PARSE_LANGUAGE = Language(tsJava.language())
    elif language == "CPP":
        PARSE_LANGUAGE = Language(tsCPP.language())
    elif language == "C":
        PARSE_LANGUAGE = Language(tsC.language())
    else:
        PARSE_LANGUAGE = Language(tsJavaScript.language())

    parser = Parser(PARSE_LANGUAGE)
    tree = parser.parse(code.encode("utf-8"))

    nodes = []
    node_types = []
    coms = get_node_types(tree.root_node, node_types)

    if language == "Java":
        if multiline:
            comment_count = node_types.count("block_comment")
        else:
            comment_count = node_types.count("line_comment")
    elif language == "Python":
        if not multiline:
            comment_count = node_types.count("comment")
        else:
            comment_count = 0
            for node in nodes:
                if node.type == "string":
                    if code[node.start_byte:node.end_byte].startswith('"""'):
                        comment_count += 1
    else:
        comment_count = 0
        if multiline:
            for com in coms:
                if com.startswith("/*"):
                    comment_count += 1
        else:
            for com in coms:
                if com.startswith("//"):
                    comment_count += 1

    return comment_count


def count_singleline_java_comment(contents):
    """Count the number of singleline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, "Java", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_cpp_comment(contents):
    """Count the number of singleline CPP comments in the code."""
    matches_count = parse_tree_sitter(contents, "CPP", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_c_comment(contents):
    """Count the number of singleline C comments in the code."""
    matches_count = parse_tree_sitter(contents, "C", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_javascript_comment(contents):
    """Count the number of singleline JavaScript comments in the code."""
    matches_count = parse_tree_sitter(contents, "JavaScript", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_python_comment(contents):
    """Count the number of singleline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, "Python", False)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_java_comment(contents):
    """Count the number of multiline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, "Java", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_cpp_comment(contents):
    """Count the number of multiline CPP comments in the code."""
    matches_count = parse_tree_sitter(contents, "CPP", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_c_comment(contents):
    """Count the number of multiline C comments in the code."""
    matches_count = parse_tree_sitter(contents, "C", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_javascript_comment(contents):
    """Count the number of multiline JavaScript comments in the code."""
    matches_count = parse_tree_sitter(contents, "JavaScript", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_python_comment(contents):
    """Count the number of multiline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, "Python", True)
    return matches_count, {constants.markers.First: matches_count}