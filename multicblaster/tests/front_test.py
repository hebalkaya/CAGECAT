from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from random import randint
import time
from sys import argv
from multicblaster.utils import fetch_job_from_db

# For now, only testable on local Windows machine
URL = "http://192.168.2.65:5000/" # localhost
CHROME_PATH = r"C:\Users\matth\Downloads\chromedriver_win32\chromedriver.exe"
BUA_PATH = r"C:\Users\matth\OneDrive\Opleidingen\Master_WUR\__Thesis\thesis_repo\test_runs\bua_seq.fasta"
d = webdriver.Chrome(ChromeDriverManager().install())
#                                      options=options)
settings = {}

PREV_SEARCH_ID = "K149K560H721G19 "
PREV_SESSION_FILE = r"C:\Users\matth\OneDrive\Opleidingen\Master_WUR\__Thesis\thesis_repo\test_runs\K149K560H721G19_session.json"
new_job_ids = []
# break clustering
def send_chars(elem_id, chars):
    elem = d.find_element_by_id(elem_id)
    elem.clear()
    elem.send_keys(chars)

def click_element(elem_id):
    d.find_element_by_id(elem_id).click()


def test_search_module():
    d.get(URL)
    time.sleep(2)
    max_gap = str(randint(-50, 40000))
    min_unique = str(randint(0, 15))
    min_hits = str(randint(0, 15))
    elem = d.find_element_by_id("genomeFile")
    elem.send_keys(BUA_PATH)
    send_chars("max_intergenic_gap", max_gap)
    send_chars("min_unique_query_hits", min_unique)
    send_chars("min_hits_in_clusters", min_hits)
    print(
        f"Testing with gap={max_gap}, min_unique={min_unique}, min_hits={min_hits}")
    d.find_element_by_id("submitSearchForm").click()
    id = d.find_element_by_id("givenJobID").text
    settings[id] = {"max_intergenic_gap": max_gap,
                    "min_unique_query_hits": min_unique,
                    "min_hits_in_clusters": min_hits}


def test_gne_module():
    d.get(URL)

    click_element("showGNE")
    if randint(0, 1) == 0:
        send_chars("gneEnteredJobId", PREV_SEARCH_ID)
    else:
        click_element("gnePrevSessFile")
        send_chars("gneUploadedSessionFile", PREV_SESSION_FILE)

    send_chars("gneSumTableDelim", chr(randint(0, 10000))) # from " " to "~"
    send_chars("gneSumTableDecimals", randint(0, 100))

    if randint(0, 1) == 0:
        click_element("gneSumTableHideHeaders")

    send_chars("max_intergenic_distance", randint(0, 10000000))
    send_chars("sample_number", randint(0, 15000))

    dropdown = Select(d.find_element_by_id("sampling_space"))
    dropdown.select_by_index(randint(0, 1))

    click_element("submitGNEForm")
    time.sleep(1)

    id = d.find_element_by_id("givenJobID").text
    settings[id] = {"job_type": "gne"}

    new_job_ids.append(id)



def test_recompute():
    pass


if __name__ == "__main__":
    try:
        for _ in range(20):
            test_gne_module()
            time.sleep(10)

    # for _ in range(10):
    #     test_search_module()

    except Exception as e:
        print(f"Encountered an error: {e}. Dumping previous runs..")


    with open("testing.log", "a") as outf:
        print(f"\n{settings}", file=outf)

    with open("ids_to_check.txt", "a") as outf:
        for id in new_job_ids:
            outf.write(f"{id}\n")

    print("Dumped. Exiting..")

    d.close()
    print("Finished")