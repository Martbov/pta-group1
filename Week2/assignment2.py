#!usr/bin/python3.4

from nltk.corpus import wordnet as wn


def main():
	print(wn.synsets('dog'))


if __name__ == '__main__':
	main()