import spacy

from src.handlers import file_handler
from src.handlers.file_handler import FILE_PATH_LEMMAS_DICT

# Load the Polish language model
nlp = spacy.load("pl_core_news_sm")
lemmas_spacy_json = file_handler.load_json_file(FILE_PATH_LEMMAS_DICT)


def create_lemmatized_parameter_description(offer_type: str, offer_description: str, offer_parameter: str) -> str:
    """
    The function takes the description from the real estate offers and filter outs the sentences that do not relate
    to specified offer_parameter.

    :param offer_type: a string that must be equal to: flats | houses | plots
    :param offer_description: a string that contains offer description
    :param offer_parameter: choose one of the parameters:
        flats: balcony | elevator | basement | garage | garden | modernization | modernization | lawStatus | kitchen
        houses: @TODO: add params
        plots: @TODO: add params
    :return: combined sentences from description based on lemmas as one string.
    """

    if offer_type not in ['flats', 'houses', 'plots']:
        raise ValueError(f"{offer_type} is not one of the following strings: flats, houses, plots.")

    lemmas = lemmas_spacy_json[offer_type][offer_parameter]
    doc = nlp(offer_description)

    sentence_list = []
    for sentence in doc.sents:
        for lemma in lemmas:
            if lemma in sentence.lemma_.lower():
                print(lemma + ": " + sentence.lemma_ + "\n")
                sentence_list.append(sentence.text)
    sentence_result = list(set(sentence_list))

    # Make sure that at the end of the sentence is a period (.)
    sentence_result = ('. '.join(sentence_result)).replace('..', '.')
    return sentence_result
