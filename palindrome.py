import argparse
import re

def add_arguments():
  '''Add command line argument for Palindrome string'''

  parser.add_argument("-s", "--string", type=str, required=True,
          help=("The string to test for palindrome."))

def is_palindrome(string):
  ''' Determines whether a string is a palindrome or not.

  Method is case insensitive and ignores white spaces. Returns `True`
  if the string is the same forward and backward, otherwise returns `False`.

  Paramaters
  ----------
  string: str
    The string to be tested
  '''


  new_s = re.sub('\s', '', string).lower()
  j = len(new_s) - 1

  for i, char in enumerate(new_s):
    if j <= i:
      return True

    if char == new_s[j]:
      j -= 1
      continue

    return False

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  add_arguments()
  args = parser.parse_args()

  print(is_palindrome(args.string))