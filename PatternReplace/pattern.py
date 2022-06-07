from collections import deque
import functools

class Condition(object):
    """
    The Condition class holds typing, values of certain attributes, sub Conditions, other options that can then be matched to ast node to see
    if all conditions are met.
    """

    def __init__(self, main, sub: list, strict_history=False, match_value=False, immediate_follow=False):
        """
        :param main_condition: A tuple that contains the type of class we want to match and the attribute returned if the node matches the type, and optionally the variable to match an attribute if match_value is selected
        :param sub_conditions: list of sub conditions that can verify other attributes of the same node
        :param strict_history: flag that sets how strictly we map the sequence of conditions past this condition. If true, any progress
        made matching other conditions will be forgotten, else progress will be carried if all subsequent conditions aren't met
        within this node
        :param match_value: flag that states if we're matching the typing of a node or a value of an attribute of the node
        :param immediate_follow: flag that determines if this condition must immediately follow the previous one in the
        sequence, otherwise the condition isn't met, even if all requirements are met later
        """
        self.main_condition = main
        self.strict_history = strict_history
        self.sub_conditions = sub
        self.match_value = match_value
        self.immediate_follow = immediate_follow

    def check_condition(self, node):
        """
        Check whether a given node matches the main conditions and the subconditions
        :param node: Node to be checked
        :return: The attribute specified in main condition that will become the next node to be traveled, else if the
        input node if the attribute was marked as EndOfChain or this condition matches the value of an attribute, meaning
         we no longer want to traverse through node,
        else None, meaning some condition in this class wasn't met
        """
        result = True
        if self.sub_conditions is not None:
            for s in self.sub_conditions:
                sub_check = s.check_condition(node)
                if sub_check is None:
                    result = False
        if result:
            if isinstance(node, self.main_condition[0]):
                if self.match_value:
                    length_split = self.main_condition[1].split("_")
                    if len(length_split) == 2 and length_split[1] == "length":
                        return node if len(self.rgetattr(node, length_split[0], None)) == self.main_condition[
                            2] else None
                    return node if self.rgetattr(node, self.main_condition[1], None) == self.main_condition[2] else None
                return self.rgetattr(node, self.main_condition[1], None) if self.main_condition[
                                                                                1] != "EndOfChain" else node
            return None
        return None

    def rgetattr(self, obj, attr, *args):
        """Helper function to get nested attributes of a given object, modeled after base getattr"""
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)

        return functools.reduce(_getattr, [obj] + attr.split('.'))


class Pattern(object):
    """
    The Pattern class looks to find positions in an ast tree of a certain pattern that is specified by a sequence of
    conditions
    """
    def __init__(self):
        pass

    def find_occurrences(self, astTree, seq: deque):
        """
        Find all occurrences of a pattern specified by a sequence of conditions given in an astTree
        :param astTree: List of ast nodes from the body of a function_def ast node
        :param seq: Queue of Condition objects
        :return: Indices of the starting position of all found patterns relative to the list of ast nodes given
        """
        pattern_indices = []
        i = 0
        for e in astTree:
            result = self.__find_occurrence(e, seq.copy())
            if result:
                pattern_indices.append(i)
            i += 1
        return pattern_indices

    def __find_occurrence(self, astTree, seq: deque):
        """
        Private method for carrying out find_occurrences. If an ast node matches a Condition in the sequence, recursively
        travel into that node to match more conditions from the sequence.
        :param astTree: Node within original astTree given in find_occurrences
        :param seq: Remaining sequence of Conditions left to match
        :return: True, if seq is empty, meaning all conditions describing the pattern have been met, else False if some Condition
        failed
        """
        if isinstance(astTree, list):
            for e in astTree:
                head = seq[0]
                if head.strict_history:
                    result = self.__find_occurrence(e, seq.copy())
                else:
                    result = self.__find_occurrence(e, seq)
                if result:
                    return True
                if head.immediate_follow:
                    return False
            return False
        else:
            head = seq[0]
            next_element = head.check_condition(astTree)
            if next_element is not None:
                seq.popleft()
                return self.__find_occurrence(next_element, seq) if len(seq) != 0 else True
            return False
