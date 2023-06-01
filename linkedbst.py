"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            stringe = ""
            if node != None:
                stringe += recurse(node.right, level + 1)
                stringe += "| " * level
                stringe += str(node.data) + "\n"
                stringe += recurse(node.left, level + 1)
            return stringe

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node=self._root
        while True:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                node=node.left
            else:
                node=node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node=self._root
            while True:
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node=node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    break
                else:
                    node=node.right
                # End of recurse
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            liftMaxInLeftSubtreeToTop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is not None:
                if top.right or top.left:
                    return 1+max(height1(top.right),height1(top.left))
                else:
                    return 0
            else:
                return -1
        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        num=self._size
        if self.height()<(2*log(num+1)-1):
            return True
        else:
            return False

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree where low <= item <= high.
        """
        cont = []

        def recurse_search(top):
            if top is not None:
                if low<=top.data<=high:
                    cont.append(top.data)
                    if top.data is not low:
                        recurse_search(top.left)
                    if top.data is not high:
                        recurse_search(top.right)
                if top.data < low:
                    recurse_search(top.right)
                if top.data > high:
                    recurse_search(top.left)

        recurse_search(self._root)
        return cont


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        balance_list=list(self.inorder())
        self.clear()

        def recurse_add(balance_list):
            if len(balance_list) == 0:
                return None
            mid_ind=len(balance_list)//2
            self.add(balance_list[mid_ind])
            balance_left=balance_list[:mid_ind]
            recurse_add(balance_left)
            balance_right=balance_list[mid_ind+1:]
            recurse_add(balance_right)
        recurse_add(balance_list)



    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """
        checker = None
        node = self._root
        while node:
            if node.data > item:
                checker = node.data
                node = node.left
            else:
                node = node.right
        return checker

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """
        checker = None
        node = self._root
        while node:
            if node.data < item:
                checker = node.data
                node = node.right
            else:
                node = node.left
        return checker


    @staticmethod
    def from_list(num, lines):
        start = time.time()
        for _ in range(num):
            word = random.choice(lines)
            lines.index(word)
        end = time.time()
        return end - start
    # @staticmethod
    # def from_list(num, lines):
    #     start = time.time()
    #     sorted(random.sample(lines, num))
    #     end = time.time()
    #     return end - start
    def search1(self,lines):
        for elem in lines:
            self.add(elem)
        start = time.time()
        for elem in lines:
            self.find(elem)
        end = time.time()
        return end - start

    def search2(self,lines, num):
        lines = random.sample(lines, num)
        for elem in lines:
            self.add(elem)
        start = time.time()
        for elem in lines:
            self.find(elem)
        end = time.time()
        return end - start

    # @staticmethod
    def search3(self,lines):
        self.rebalance()
        for elem in lines:
            self.add(elem)
        start = time.time()
        for elem in lines:
            self.find(elem)
        end = time.time()
        return end - start


    
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        num=10
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file.readlines()]
        # rand = random.sample(lines, num)
        tree1=LinkedBST()
        tree2=LinkedBST()
        tree3=LinkedBST()
        print('Search time for 10,000 random words in an alphabetically ordered dictionary =', self.from_list(num, lines))
        print('Search time for 10,000 random words ordered', tree1.search1(lines))
        print('Search time for 10,000 random words not ordered', tree2.search2(lines, num))
        print('Search time for 10,000 random words in a dictionary represented as a binary search tree after its balancing', tree3.search3(lines))

if __name__ == "__main__":
    tree_search = LinkedBST()
    tree_search.demo_bst('words.txt')