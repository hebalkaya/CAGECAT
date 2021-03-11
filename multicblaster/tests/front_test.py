from selenium import webdriver
from random import randint
import time

# For now, only testable on local Windows machine
URL = "http://127.0.0.1:5000/" # localhost
CHROME_PATH = r"C:\Users\matth\Downloads\chromedriver_win32\chromedriver.exe"
BUA_PATH = r"C:\Users\matth\OneDrive\Opleidingen\Master_WUR\__Thesis\thesis_repo\test_runs\bua_seq.fasta"
d = webdriver.Chrome(executable_path=CHROME_PATH)
#                                      options=options)

d.get(URL)
time.sleep(1)

# break clustering
for _ in range(100):
    max_gap = str(randint(-50, 40000))
    min_unique = str(randint(0, 15))
    min_hits = str(randint(0, 15))

    elem = d.find_element_by_id("genomeFile")
    elem.send_keys(BUA_PATH)

    d.find_element_by_id("max_intergenic_gap").send_keys(max_gap)
    d.find_element_by_id("min_unique_query_hits").send_keys(min_unique)
    d.find_element_by_id("min_hits_in_clusters").send_keys(min_hits)

    print(f"Testing with gap={max_gap}, min_unique={min_unique}, min_hits={min_hits}")

    d.find_element_by_id("submitSearchForm").click()
    time.sleep(1)

    d.get(URL)
