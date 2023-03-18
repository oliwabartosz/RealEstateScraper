# LOGIN

XPATH_LOGIN_INPUT: str = "//input[@name='email']"
XPATH_PASSWORD_INPUT: str = "//input[@name='password']"

# LOGOUT
CLASS_LOGOUT_BTN_ARROW: str = 'x-btn-arrow'
XPATH_LOGOUT_BTN_ARROW: str = "//em[@class='x-btn-arrow']"
XPATH_LOGOUT_BTN: str = "//*/button[text()='Wyloguj']"

# SEARCHBAR
XPATH_SEARCHBAR: str = "//*/div[@id='topListingSearch']//input"

# OFFERS DATA
XPATH_KEYS: str = '//*[@class="x-grid3-cell-inner x-grid3-col-0"]'
XPATH_VALUES: str = '//*[@class="x-grid3-cell-inner x-grid3-col-1"]'
XPATH_OFFER_ID: str = '//*[@id="idlabel"]'
XPATH_OFFER_NOT_EXISTS: str = "//*[@class='x-combo-list-inner' and text()='Nie znaleziono takiej oferty. Spróbuj " \
                                "wyszukać ponownie.']"

# OFFERS IMAGES
XPATH_IMAGES_FOR_OFFER: str = "(//a[contains(@class,'-images')])"

