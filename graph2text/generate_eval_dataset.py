"""
A program to process RDF data and generate dataset for evaluation and testing.
"""

from utils import rdf_utils
import argparse
from GraphModel import *

def generate():
    """
    Read options from user input, and generate eval dataset.
    """

    DISCR = 'Generate dataset from XML files of RDF to Text Entries.'
    parser = argparse.ArgumentParser(description=DISCR)
    parser.add_argument('-path', type=str, help='Path to data.', required=True)
    parser.add_argument('-src_mode', help='source mode: flat or structured.',
                choices=['flat', 'structured'], default = 'flat', nargs = '?')

    parser.add_argument('-src', type=str, help='Path to output file for src.',
                    required=True)
    parser.add_argument('-tgt', type=str, help='Path to output file for tgt.',
                    required=True)
    parser.add_argument('-ref', type=str, help='Path to ref files.',
                    required=True)


    args = parser.parse_args()

    instances, _, _ = rdf_utils.generate_instances(args.path, eval=True)

    for (size, ins) in instances.items():
        for i in ins:
            lexs = i.Lexicalisation

            for k in range(len(lexs), 3):
                lexs.append(rdf_utils.Lexicalisation('', '', ''))

            tripleset = (i.originaltripleset, i.modifiedtripleset)
            G = KnowledgeGraph(tripleset, lexs[0].lex)

            print(G.lexicalization)

            # write src
            with open(args.src, 'a+', encoding="utf8") as srcFile:
                if args.src_mode == 'structured':
                    srcFile.write(G.linearize_graph(structured=True).replace('\n', ' ') + '\n')
                else:
                    srcFile.write(G.linearize_graph() + '\n')

            # write tgt
            with open(args.tgt, 'a+', encoding="utf8") as tgtFile:
                tgtFile.write(G.delexicalize_text(advanced=True).replace('\n', ' ')  + '\n')

            # write ref
            for i in range(3):
                ref_str = text_utils.tokenize_and_concat(lexs[i].lex)
                with open(args.ref + str(i + 1), 'a+', encoding="utf8") as refFile:
                    refFile.write(ref_str.replace('\n', ' ') + '\n')


def main():
    generate()

if __name__ == '__main__':
    main()