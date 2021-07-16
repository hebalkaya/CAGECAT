from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from random import randint
from random import choice
import time

URL = "http://127.0.0.1:5000/" # localhost
CHROME_PATH = r"C:\Users\matth\Downloads\chromedriver_win32\chromedriver.exe"
BUA_PATH = r"C:\Users\matth\OneDrive\Opleidingen\Master_WUR\__Thesis\thesis_repo\test_runs\bua_seq.fasta"
d = webdriver.Chrome(ChromeDriverManager().install())

# Expected results: True -> everything ok; None -> will fail during execution; False -> will not start
search_options = ["genomeFile"]#, "radioNCBIEntries", "radioPrevSession"]

OPTIONALS = {"genomeFile": [(BUA_PATH, True)],
            "database_type": [("nr", True),
                              ("", False),
                              ("tasd", False),
                              ("pdb", True),
                              ("AASD", None)],
             "entrez_query": [("", True),
                        ("jHJKSDAS", None),
                        ("Aspergillus[organism]", True),
                        ("Aspergillus", "?"),
                        ("Aspergillus[orgnism]", None)]}

def send_chars(elem_id, chars):
    elem = d.find_element_by_id(elem_id)
    elem.clear()
    elem.send_keys(chars)

def click_element(elem_id):
    d.find_element_by_id(elem_id).click()


def do_input_method():
    search_option = choice(search_options)
    options = OPTIONALS[search_option]

    if search_option == "genomeFile":
        o = choice(options)
    elif search_option == "radioNCBIEntries":
        pass
    elif search_option == "radioPrevSession":
        pass
    else:
        raise IOError("Invalid input method")


if __name__ == "__main__":
    d.get(URL)
    time.sleep(1)

    all_results = []
    log_settings = []

    for key, value in OPTIONALS.items():
        # do_input_method()

        to_send, result = choice(value)
        all_results.append(result)
        log_settings.append((key, to_send))

        send_chars(key, to_send)

        time.sleep(0.5)

    print(all_results)
    print(f"Program will: {all(all_results)}")

    time.sleep(2)
    d.close()

    print("Finished :)")

    # send_chars("database_type", choice(OPTIONALS["database_type"])[0])
    # send_chars("entrez_query", choice(OPTIONALS["entrez_query"])[0])



