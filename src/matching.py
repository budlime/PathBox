"""
Mod by budRich 2018,2021,2022
Written by Ross Hemsley and other collaborators 2013.
See LICENSE for details.
"""

from unittest import TestCase
from os.path import commonprefix, split, isdir, expanduser, join, sep
from os import listdir
from typing import List, Tuple, Optional


class COMPLETION_TYPE:
    CompleteButNotUnique = 0
    Complete = 1
    NoMatch = 2


def get_completion(path: str) -> Tuple[str, int]:
    """
    Function to find and return longest possible
    completion for a path p from a list of
    candidates l. Returns new_path, status,
    completed. Find filename and directory.
    """
    directory, filename = split(path)

    if not isdir(expanduser(directory)):
        return path, COMPLETION_TYPE.NoMatch

    directory_listing = listdir(expanduser(directory))
    new_filename, completion_type = complete_path(filename, directory_listing)

    if (
        new_filename != ""
        and isdir(expanduser(join(directory, new_filename)))
        and completion_type != COMPLETION_TYPE.CompleteButNotUnique
    ):
        new_filename += sep

    return join(directory, new_filename), completion_type


def complete_path(filename: str, directory_listing: List[str]) -> Tuple[str, int]:
    lcs_completion = get_lcs_completion_or_none(filename, directory_listing)

    if lcs_completion is not None:
        return lcs_completion, COMPLETION_TYPE.Complete

    matches = get_matches(filename, directory_listing)

    if len(matches) > 1:
        new_filename = longest_completion(filename, matches)
        return new_filename, COMPLETION_TYPE.CompleteButNotUnique

    elif len(matches) == 1:
        return matches[0], COMPLETION_TYPE.Complete
    else:
        return filename, COMPLETION_TYPE.NoMatch


def get_matches(filename: str, directory_listing: List[str]) -> List[str]:
    return [f for f in directory_listing if f.lower().startswith(filename.lower())]


def longest_completion(filename: str, matches: List[str]) -> str:
    return filename + commonprefix(matches)[len(filename) :]


def get_lcs_completion_or_none(filename: str, directory_listing: List[str]) -> Optional[str]:
    """
    If there is a unique way to complete the path
    such that the LCS is the same as the query
    string, return that (similar to the way Fish
    shell works)
    """
    completion = None

    for candidate in directory_listing:
        if lcs(filename, candidate) == filename:
            if completion is not None:
                return None
            else:
                completion = candidate

    return completion


def lcs(A: str, B: str):
    """
    Taken and adapted from
    http://rosettacode.org/wiki/Longest_common_subsequence#Dynamic_Programming_7
    """
    lengths = [[0 for _ in range(len(B) + 1)] for _ in range(len(A) + 1)]

    for i, x in enumerate(A):
        for j, y in enumerate(B):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    result = ""
    x, y = len(A), len(B)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x - 1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y - 1]:
            y -= 1
        else:
            result = A[x - 1] + result
            x -= 1
            y -= 1
    return result


##
# Unit tests
##


class TestLCSCompletion(TestCase):
    def test1(self):
        directory_listing = [
            "filename1",
            "filename2",
            "test",
        ]

        output1 = get_lcs_completion_or_none("file1", directory_listing)
        self.assertEqual("filename1", output1)

        output2 = get_lcs_completion_or_none("file2", directory_listing)
        self.assertEqual("filename2", output2)

        output3 = get_lcs_completion_or_none("tst", directory_listing)
        self.assertEqual("test", output3)

        output4 = get_lcs_completion_or_none("tes", directory_listing)
        self.assertEqual("test", output4)

        output5 = get_lcs_completion_or_none("django", directory_listing)
        self.assertIsNone(output5)


class TestLCS(TestCase):
    def test1(self):
        self.assertEqual("hel", lcs("hello", "heal"))
        self.assertEqual("oe", lcs("hope", "oe"))
        self.assertEqual("", lcs("this", "xyz"))
        self.assertEqual("bcd", lcs("abcdefg", "bcd"))
        self.assertEqual("test", lcs("test", "test"))
        self.assertEqual("rd", lcs("read", "rd"))
        self.assertEqual("round", lcs("round", "arounded"))


class TestCompletion(TestCase):
    def test1(self):
        filename = "test"
        matches = ["testable", "testa", "testand", "testand"]
        output = longest_completion(filename, matches)
        expected = "testa"

        self.assertEqual(expected, output)

    def test2(self):
        filename = "test"
        matches = ["testable", "testa", "testand", "Testand"]
        output = longest_completion(filename, matches)
        expected = "test"

        self.assertEqual(expected, output)

    def test3(self):
        filename = "test"
        matches = ["tester", "testable", "testa", "testand", "Testand"]
        output = longest_completion(filename, matches)
        expected = "test"

        self.assertEqual(expected, output)


class TestMatches(TestCase):
    def test1(self):
        directory_listing = [
            "filename",
            "filen",
            "fi",
            "Filename",
        ]

        output = get_matches("file", directory_listing)
        expected = [
            "filename",
            "filen",
        ]

        self.assertListEqual(expected, output)

    def test2(self):
        directory_listing = [
            "filename",
            "filen",
            "fi",
            "Filename",
        ]

        output = get_matches("file", directory_listing)
        expected = [
            "filename",
            "filen",
            "Filename",
        ]

        self.assertListEqual(expected, output)

    def test3(self):
        directory_listing = ["test"]
        output = get_matches("", directory_listing)
        self.assertListEqual(["test"], output)
