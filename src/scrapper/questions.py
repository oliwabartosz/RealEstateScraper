from src.config import logger_cfg


def type_of_offers():
    answer = input("Please provide offers type that you want to download.\nType F for flats, H for houses, "
                   "P for plots: ").lower()

    match answer:
        case 'f':
            logger_cfg.logger1.info('Downloading: FLATS')
            return 'flats'
        case 'h':
            logger_cfg.logger1.info('Downloading: HOUSES')
            return 'houses'
        case 'p':
            logger_cfg.logger1.info('Downloading: PLOTS')
            return 'plots'
        case _:
            print("No information or information invalid. Cannot process further operations without this information.")
            exit(1)
