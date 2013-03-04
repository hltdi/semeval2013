
import argparse
import nltk
import stanford

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=True)

    args = parser.parse_args()
    stanford.taggerhome = args.taggerhome
    sourcefn = args.sourcetext

    tagger = stanford.get_tagger()

    with open(sourcefn) as infile:
        sents = [line.strip().split() for line in infile]
    tagged_sents = tagger.batch_tag(sents)
    print("tagged.")

    with open(sourcefn + ".pretagged", "w") as outfile:
        for tagged_sent in tagged_sents:
            print(" ".join(list(map(nltk.tag.tuple2str, tagged_sent))),
                  file=outfile)

if __name__ == "__main__": main()
