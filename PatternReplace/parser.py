import ast
from _ast import *
import astor
from PatternReplace.pattern import *


def parseFile(filename, pattern):
    """
    Parse through a given file to create ast tree, then send to optimize based on the given pattern type
    :param filename:
    :param pattern: pattern to be searched through this file, 1 for list comp, 2 for string joins, and 3 for attribute replacements
    :return: String of the input file after pattern replacement optimizations were applied
    """
    with open(filename, "r") as source:
        tree = ast.parse(source.read())
    return traverseReplace(tree, pattern)


class JoinAnalyzer(ast.NodeVisitor):
    def __init__(self, patterns):
        self.patterns = patterns

    def visit_FunctionDef(self, node):
        """
        Using NodeVisitor, visit every function definition within ast tree, search for patterns of code to be replaced, and
        if found, replace that section of code with a String join().
        :param node: FunctionDef node
        :return:
        """
        for sequence in self.patterns:
            o = Pattern().find_occurrences(node.body, sequence)
            for i in o:
                for_loop = node.body[i]
                old_node = for_loop
                for j in for_loop.body:
                    if isinstance(j,ast.AugAssign) and isinstance(j.op,ast.Add):
                        if isinstance(j.value, ast.Name) and j.value.id == for_loop.target.id:
                            new_node = ast.Assign(targets=[ast.Name(id=j.target.id)],
                                                  value=ast.Call(func=ast.Attribute(value=ast.Str(s=''), attr='join'),
                                                                 args=[ast.Name(id=for_loop.iter.id)], keywords=[]))
                            node.body[i] = new_node
                        elif isinstance(j.value, ast.BinOp):
                            if isinstance(j.value.left, ast.Name) and j.value.left.id == for_loop.target.id:
                                new_node = ast.Assign(targets=[ast.Name(id=j.target.id)],
                                                      value=ast.Call(func=ast.Attribute(value=ast.Str(s=j.value.right.s),
                                                                                        attr='join'),
                                                                     args=[ast.Name(id=for_loop.iter.id)], keywords=[]))
                                node.body[i] = new_node
                            elif isinstance(j.value.right, ast.Name) and j.value.right.id == for_loop.target.id:
                                new_node = ast.Assign(targets=[ast.Name(id=j.target.id)],
                                                      value=ast.Call(func=ast.Attribute(value=ast.Str(s=j.value.left.s),
                                                                                        attr='join'),
                                                                     args=[ast.Name(id=for_loop.iter.id)], keywords=[]))
                                node.body[i] = new_node
                    elif isinstance(j,ast.Assign) and isinstance(j.value,ast.BinOp) and isinstance(j.targets[0],ast.Name):
                        if( isinstance(j.value.left, ast.Name) and j.value.left.id == j.targets[0].id and
                           isinstance(j.value.op, ast.Add) and j.value.right.id ==for_loop.target.id):
                            new_node = ast.Assign(targets=[ast.Name(id=j.targets[0].id)],
                                                  value=ast.Call(func=ast.Attribute(value=ast.Str(s=''), attr='join'),
                                                                 args=[ast.Name(id=for_loop.iter.id)], keywords=[]))
                            node.body[i] = new_node
                        elif(isinstance(j.value.left, ast.BinOp) and isinstance(j.value.left.left, ast.Name) and 
                             j.value.left.left.id == j.targets[0].id) and isinstance(j.value.left.op, ast.Add) and j.value.left.right.id ==for_loop.target.id and isinstance(j.value.op, ast.Add) and isinstance(j.value.right, ast.Str):
                                new_node = ast.Assign(targets=[ast.Name(id=j.targets[0].id)],
                                                      value=ast.Call(func=ast.Attribute(value=ast.Str(s=j.value.right.s),
                                                                                        attr='join'),
                                                                     args=[ast.Name(id=for_loop.iter.id)], keywords=[]))
                                node.body[i] = new_node
                    
        self.generic_visit(node)


class ListCompAnalyzer(ast.NodeVisitor):
    """
    Class for traversing through an ast tree searching to replace code sections list comprehensions wherever possible
    """
    def __init__(self, patterns):
        """
        :param patterns: list of conditions sequences that represent patterns of code that should be replaced
        """
        self.patterns = patterns

    def visit_FunctionDef(self, node: FunctionDef):
        """
        Using NodeVisitor, visit every function definition within ast tree, search for patterns of code to be replaced, and
        if found, replace that section of code with a list comprehension.
        :param node: FunctionDef node
        :return:
        """
        for sequence in self.patterns:
            o = Pattern().find_occurrences(node.body, sequence)
            for i in o:
                for_loop = node.body[i]
                if type(for_loop.body[0]) == ast.If:
                    if_block = for_loop.body[0]
                    if type(if_block.body[0]) == ast.If:
                        # Nested If For Loop
                        nested_if_expr = if_block.body[0]
                        nested_if_block = if_block
                        tests = [if_block.test]
                        while type(nested_if_expr) == ast.If:
                            if len(nested_if_expr.body) == 1:
                                next_node = nested_if_expr.body[0]
                                if type(next_node) != ast.If:
                                    nested_if_block = nested_if_expr
                                    nested_if_expr = next_node
                                else:
                                    if len(nested_if_expr.orelse) == 0:
                                        tests.append(nested_if_expr.test)
                                        nested_if_block = nested_if_expr
                                        nested_if_expr = next_node
                                    else:
                                        nested_if_expr = None
                            else:
                                nested_if_expr = None
                        if nested_if_expr is not None:
                            test_expr = rgetattr(nested_if_expr, "value.func.attr", "not_append")
                            if test_expr == "append":
                                new_node = self.loop_if_to_assign(for_loop, nested_if_block, tests)
                                if new_node is not None:
                                    node.body[i] = new_node
                    else:
                        # Single If For Loop
                        new_node = self.loop_if_to_assign(for_loop, if_block, [])
                        if new_node is not None:
                            node.body[i] = new_node
                else:
                    # Plain For Loop, Direct List Comp Replace
                    new_node = AugAssign(op=Add(), target=for_loop.body[0].value.func.value,
                                      value=ListComp(elt=for_loop.body[0].value.args[0],
                                                     generators=[
                                                         comprehension(target=for_loop.target,
                                                                       iter=for_loop.iter, ifs=[])]))
                    node.body[i] = new_node

        self.generic_visit(node)

    def loop_if_to_assign(self, for_loop, if_block, tests):
        """
        Convert a for loop with an if statement into a list comprehension that returns an expr or returns an if_expr if
        there is an if-else statement
        :param for_loop: for loop ast node
        :param if_block: if node within for loop, can be nested node within multiple if statements
        :param tests: if if_block is nested, tests included all previous compare conditions from previous if statements
        :return: New node converting for loop to list comprehension, else None if some error
        """
        if len(if_block.orelse) == 0:
            # Add if statement tests
            tests.append(if_block.test)
            new_node = AugAssign(op=Add(), target=if_block.body[0].value.func.value,
                              value=ListComp(elt=if_block.body[0].value.args[0],
                                             generators=[
                                                 comprehension(target=for_loop.target,
                                                               iter=for_loop.iter,
                                                               ifs=tests)]))
            return new_node
        else:
            # Generate if_exp
            elt_node = self.if_to_ifexp(if_block)
            if elt_node is not None:
                new_node = AugAssign(op=Add(), target=if_block.body[0].value.func.value,
                                  value=ListComp(elt=elt_node,
                                                 generators=[
                                                     comprehension(target=for_loop.target,
                                                                   iter=for_loop.iter,
                                                                   ifs=tests)]))
                return new_node
        return None

    def if_to_ifexp(self, node):
        """Recursive function for creating if_exp from a if, elif, else block of code.
        each statement within the body of each if statement must be a append call """
        if type(node) == ast.If:
            if len(node.orelse) == 1:
                orelse_node = self.if_to_ifexp(node.orelse[0])
                return IfExp(test=node.test, body=node.body[0].value.args[0],
                             orelse=orelse_node) if len(node.body) == 1 and rgetattr(node.body[0], "value.func.attr",
                                                                                     "not_append") == "append" and orelse_node is not None else None
        else:
            return node.value.args[0] if rgetattr(node, "value.func.attr", "not_append") == "append" else None


class AttributeAnalyzer(ast.NodeVisitor):
    def __init__(self, patterns):
        self.patterns = patterns

    # We'll use the Analyzer to visit certain node types for code blocks, most likely just function definitions
    def visit_FunctionDef(self, node: FunctionDef):
        """
        Using NodeVisitor, visit every function definition within ast tree, search for patterns of code to be replaced, and
        if found, replace that section of code with local variable reference instead of class attribute reference, along with
        lines to create that local variable and reassign it to the class attribute after the local variable is done being used.
        :param node: FunctionDef node
        :return:
        """
        attributes_seen = set(())
        for sequence in self.patterns:
            o = Pattern().find_occurrences(node.body, sequence)
            # Reverse occurrence order minimizing extra assign statements generated, as you move up occurrences you don't
            # add assign statements if it was already done before.
            o.reverse()
            occurrence_offset = 0
            for i in o:
                values = {}
                i += occurrence_offset
                AttributePatternAnalyzer(values).visit(node.body[i])
                offset = 1
                for k, v in values.items():
                    if k not in attributes_seen:
                        node.body.insert(i + offset,
                                         Assign(
                                             targets=[
                                                 Attribute(value=Name(id='self', ctx=Store()), attr=k, ctx=Store())],
                                             value=Name(v, Load())
                                         ))
                        node.body.insert(0, Assign(targets=[Name(v, Store())],
                                                   value=Attribute(value=Name(id='self', ctx=Load()), attr=k,
                                                                   ctx=Load())
                                                   ))
                        occurrence_offset += 1
                        offset += 1
                attributes_seen = attributes_seen | values.keys()
        self.generic_visit(node)


class AttributePatternAnalyzer(ast.NodeTransformer):
    """Hepler class for AttributeAnalyzer, performs replacement within loop section for class attribute calls with a local variable
    """
    def __init__(self, refs):
        """
        :param refs: Dictionary to keep tract of new local variable created to add extra assignment statements to create the local variable
        """
        self.new_names = refs

    def visit_Attribute(self, node: Attribute):
        """
        Visit every instance of attribute node, replace attributes called from self (ex self.x) with local version (local_x)
        :param node:
        :return:
        """
        if type(node.value) == ast.Subscript:
            return node
        if node.value.id == 'self':
            name = self.new_names.get(node.attr)
            if name is None:
                name = ''.join([node.attr, "_local"])
                self.new_names[node.attr] = name
            x = Name(name, Load())
            return x
        return node


def traverseReplace(a: Module, pattern):
    """
    Given an ast Tree of a entire file, perform tree traversal using NodeVistor classes and replacement code sections with
    optimized versions
    :param a: ast tree
    :param pattern: type of pattern to be searched, 1 for list comp, 2 for string joins, and 3 for attribute replacements
    :return: String representing optimized file
    """
    if pattern == 0:
        ListCompAnalyzer(generate_list_comp_patterns()).visit(a)
    elif pattern == 1:
        JoinAnalyzer(generate_join_patterns()).visit(a)
    elif pattern == 2:
        AttributeAnalyzer(generate_attri_patterns()).visit(a)
    else:
        return None
    ast.fix_missing_locations(a)
    return ASTtoString(a)


def generate_join_patterns():
    """
    Create list of Conditions sequences for recognizing code patterns that can be replaced with string joins
    :return:
    """
    patterns = []

    sequence = deque()
    sequence.append(Condition((ast.For, "body"), [Condition((ast.For, "body_length", 1), [], match_value=True)]))
    sequence.append(Condition((ast.Assign, "value"), []))
    patterns.append(sequence)

    sequence = deque()
    sequence.append(Condition((ast.For, "body"), [Condition((ast.For, "body_length", 1), [], match_value=True)]))
    sequence.append(Condition((ast.AugAssign, "value"), []))
    patterns.append(sequence)

    return patterns


def generate_list_comp_patterns():
    """
    Create list of Conditions sequences for recognizing code patterns that can be replaced with list comprehensions
    :return:
    """
    patterns = []

    # Plain list comp
    sequence = deque()
    sequence.append(Condition((ast.For, "body"), [Condition((ast.For, "body_length", 1), [], match_value=True)]))
    sequence.append(Condition((ast.Expr, "value"), []))
    sequence.append(Condition((ast.Call, "func"), []))
    sequence.append(Condition((ast.Attribute, "attr", "append"), [], match_value=True))
    patterns.append(sequence)

    # Single If
    sequence = deque()
    sequence.append(Condition((ast.For, "body"), [Condition((ast.For, "body_length", 1), [], match_value=True)]))
    sequence.append(Condition((ast.If, "body"), [Condition((ast.If, "body_length", 1), [], match_value=True)]))
    sequence.append(Condition((ast.Expr, "value"), []))
    sequence.append(Condition((ast.Call, "func"), []))
    sequence.append(Condition((ast.Attribute, "attr", "append"), [], match_value=True))
    patterns.append(sequence)

    # Nested If
    sequence = deque()
    sequence.append(Condition((ast.For, "body"), [Condition((ast.For, "body_length", 1), [], match_value=True)]))
    sequence.append(Condition((ast.If, "body"), [Condition((ast.If, "body_length", 1), [], match_value=True),
                                                 Condition((ast.If, "orelse_length", 0), [], match_value=True)]))
    sequence.append(Condition((ast.If, "body"), [Condition((ast.If, "body_length", 1), [], match_value=True)]))
    patterns.append(sequence)

    return patterns


def generate_attri_patterns():
    """
    Create list of Conditions sequences for recognizing code patterns that can be replaced with local variables for class attribute calls
    :return:
    """
    patterns = []

    sequence = deque()
    sequence.append(Condition((ast.Assign, "value"), []))
    sequence.append(Condition((ast.ListComp, "EndOfChain"), []))
    patterns.append(sequence)

    sequence = deque()
    sequence.append(Condition((ast.AugAssign, "value"), []))
    sequence.append(Condition((ast.ListComp, "EndOfChain"), []))
    patterns.append(sequence)

    sequence = deque()
    sequence.append(Condition((ast.For, "EndOfChain"), []))
    patterns.append(sequence)

    sequence = deque()
    sequence.append(Condition((ast.While, "EndOfChain"), []))
    patterns.append(sequence)

    return patterns


def ASTtoString(a):
    """
    Convert ast tree back into string for code file
    :param a:
    :return:
    """
    return astor.to_source(a)


def rgetattr(obj, attr, *args):
    """Helper function to get nested attributes of a given object, modeled after base getattr"""
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))
