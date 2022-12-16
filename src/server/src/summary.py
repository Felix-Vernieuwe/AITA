from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def lexrank_summary(*documents, sentences=3):
    parser = PlaintextParser.from_string("\n".join(documents), Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LexRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    summary = summarizer(parser.document, sentences)
    return " ".join([f"{sentence}" for sentence in summary])

from summarizer import Summarizer, TransformerSummarizer

# taken from https://medium.com/analytics-vidhya/text-summarization-using-bert-gpt2-xlnet-5ee80608e961
def bert_summary(*documents, num_sentences=3):
    bert_model = Summarizer()
    return "".join(bert_model("\n".join(documents), num_sentences=num_sentences))