from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import time

# For now, only testable on local Windows machine
URL = "http://192.168.2.65:5000/" # localhost
CHROME_PATH = r"C:\Users\matth\Downloads\chromedriver_win32\chromedriver.exe"
BUA_PATH = r"C:\Users\matth\OneDrive\Opleidingen\Master_WUR\__Thesis\thesis_repo\test_runs\bua_seq.fasta"
d = webdriver.Chrome(ChromeDriverManager().install())
#                                      options=options)
settings = {}
# break clustering
def send_chars(elem_id, chars):
    elem = d.find_element_by_id(elem_id)
    elem.clear()
    elem.send_keys(chars)

try:
    for _ in range(10):
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

        print(f"Testing with gap={max_gap}, min_unique={min_unique}, min_hits={min_hits}")

        d.find_element_by_id("submitSearchForm").click()

        id = d.find_element_by_id("givenJobID").text

        settings[id] = {"max_intergenic_gap": max_gap,
                        "min_unique_query_hits": min_unique,
                        "min_hits_in_clusters": min_hits}

except Exception as e:
    print(f"Encountered an error: {e}. Dumping previous runs..")

with open("testing.log", "a") as outf:
    print(f"\n{settings}", file=outf)

print("Dumped. Exiting..")

d.close()
print("Finished")