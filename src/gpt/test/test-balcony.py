from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain

balcony_chain = [
    balcony_summary_chain, balcony_rating_chain,
]

main_output_variables = [
    "balcony_summary", "balcony_rating",
]
