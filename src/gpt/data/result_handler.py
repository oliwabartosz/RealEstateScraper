TAKEN_FROM_PARAMS_STR = 'Information taken from parameters'
RATED_STR = 'Rated by user'


def handle_result(chain_result_rating_val: str, chain_result_summary_val: str, param: int) -> tuple[int, str]:

    if chain_result_rating_val == -9:
        if param == -9:
            return int(chain_result_rating_val), chain_result_summary_val
        else:
            return param, TAKEN_FROM_PARAMS_STR

    return int(chain_result_rating_val), chain_result_summary_val


# @TODO: rethink and delete eventually: handle_result_kwargs
def handle_result_kwargs(**kwargs) -> tuple[int, str]:
    rated_val = kwargs.get('rated_value', False)

    if not rated_val:

        # Check if the required keyword arguments are present
        required_args = ['rating', 'summary', 'param']
        for arg in required_args:
            if arg not in kwargs:
                raise ValueError(f"Missing required argument: {arg}")

            if kwargs['rating'] == -9:
                if kwargs['param'] == -9:
                    return int(kwargs['rating']), kwargs['summary']
                else:
                    return kwargs['param'], TAKEN_FROM_PARAMS_STR

            return int(kwargs['rating']), kwargs['summary']
        else:
            return int(rated_val), RATED_STR
