from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

import os
import shutil
import time


def download_csv(page_url, driver):

    driver.switch_to.window(driver.window_handles[1]) 

    # if page_url.isspace():
    #     page_url = page_url.replace(" ", "%20")

    # Open the webpage
    driver.get(page_url)

    # Find the button by its ID or other attributes
    element = driver.find_element(By.XPATH, "//a[span[text()='Download As']]")
    # element = driver.find_element(By.XPATH, "//div[@class='dt-button buttons-collection']")

    element.click()

    # sample of the tag <a class="dt-button buttons-csv buttons-html5" tabindex="0" aria-controls="results" href="#"><span>CSV</span></a>
    a_tag = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='CSV']]")))
    a_tag.click()

    time.sleep(2)
    # Close the browser
    driver.close()


class TreeNode:
    def __init__(self, value, link=None):
        self.value = value
        self.link = link
        self.children = []
        self.download_file_name = "PAGER3 A Pathways, Annotated-lists and Gene signatures Electronic Repository Version 3"
        self.old_path = os.path.join("/Users/qi/Downloads", f"{self.download_file_name}.csv")

    def add_child(self, child):
        self.children.append(child)

    def make_tree_directory(self, path, driver):
        # Ensure the path exists
        ns_name = '_'.join(self.value.split())
        current_path = os.path.join(path, ns_name)
        os.makedirs(current_path, exist_ok=True)

        if self.link:
            download_link = self.link.replace(" ", "%20")
            download_csv(download_link, driver)
            new_path = os.path.join(current_path, f"{ns_name}.csv")
            
            try:
                # This will move the file from the current directory to new_path
                shutil.move(self.old_path, new_path)
                print(f"Moved the file {self.old_path} to {current_path}")
            except FileNotFoundError:
                print(f"The file {self.old_path} was not found.")
            except Exception as e:
                print(f"An error occurred while moving the file: {e}")
        
        # Recursively create directories for children
        for child in self.children:
            child.make_tree_directory(current_path, driver)



    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.value)
        if self.link:
            ret += f" ({self.link})"
        ret += "\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

def parse_list(ul):
    root = TreeNode('mesh')
    for li in ul.find_all('li', recursive=False):
        a_tag = li.find('a')
        text = a_tag.get_text(strip=True) if a_tag else li.get_text(strip=True)
        link = a_tag['href'] if a_tag and a_tag.has_attr('href') else None
        node = TreeNode(text, link)
        if nested_ul := li.find('ul'):
            node.children = parse_list(nested_ul).children
        root.add_child(node)
    return root

mesh_html_content = """
<div class="tab-pane fade show active" id="mesh" role="tabpanel" mesh-tab"="">
            <div id="wrapper">
                <ul class="collapsibleList">
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Bacterial Infections and Mycoses">Bacterial
                            Infections and Mycoses(208)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Bacterial Infections">Bacterial
                                    Infections(54)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.100">Bacteremia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400">Gram-Negative
                                            Bacterial Infections(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.825.820.470">Lupus
                                            Vulgaris(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.890.731.649">Rheumatic
                                            Heart Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.890.731">Rheumatic
                                            Fever(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.090.072">Anthrax(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.552.846.583.470">Lupus
                                            Vulgaris(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.552.846">Tuberculosis(35)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.552.386.850">Leprosy,
                                            Paucibacillary()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.552.386.775.500">Leprosy,
                                            Lepromatous(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.552.386">Leprosy(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.552">Mycobacterium
                                            Infections(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410.040.246.388">Diphtheria()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.126.100.150">Cat-Scratch
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.167">Brucellosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.200">Cat-Scratch
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.310.821.873">Typhoid
                                            Fever(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.388.750">Rat-Bite
                                            Fever(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.466">Helicobacter
                                            Infections(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.625.549">Meningococcal
                                            Infections(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.400.771">Rat-Bite
                                            Fever(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.252.410">Gram-Positive
                                            Bacterial Infections(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Infection">Infection(158)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539">Infection(135)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.160.412">Osteitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.800.200.383.249">Aspergillosis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.160.495">Osteomyelitis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.160.762">Spondylitis(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.800.720.820.470">Lupus
                                            Vulgaris(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.757.100">Bacteremia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.757">Sepsis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.539.597.050">AIDS-Related
                                            Opportunistic Infections(7)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Mycoses">Mycoses(3)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.703.513.249">Aspergillosis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.703.160">Candidiasis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C01.703.295.328.249">Aspergillosis(3)</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Virus Diseases">Virus
                            Diseases(136)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Arbovirus Infections">Arbovirus
                                    Infections(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.081.270">Dengue(2)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/DNA Virus Infections">DNA
                                    Virus Infections(32)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.466.313.165">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.466.313">Epstein-Barr
                                            Virus Infections(10)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.430.400.100">Hepatitis
                                            B, Chronic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.430.400">Hepatitis
                                            B(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.650.810">Warts(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.743.929">Vaccinia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.256.743.826">Smallpox(8)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Hepatitis, Viral, Human">Hepatitis,
                                    Viral, Human(34)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.420">Hepatitis
                                            A(34)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.450.100">Hepatitis
                                            D, Chronic(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.450">Hepatitis
                                            D(34)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.440.120">Hepatitis
                                            C, Chronic(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.440">Hepatitis
                                            C(16)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.435.100">Hepatitis
                                            B, Chronic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.440.435">Hepatitis
                                            B(11)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Opportunistic Infections">Opportunistic
                                    Infections(7)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.597.050">AIDS-Related
                                            Opportunistic Infections(7)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/RNA Virus Infections">RNA
                                    Virus Infections(115)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.350.250.214">Dengue(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.616.400.100">AIDS-Related
                                            Opportunistic Infections(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.616.400.400">HIV-Associated
                                            Lipodystrophy Syndrome(32)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.600.550.200.750">Severe
                                            Acute Respiratory Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.580.600.080.600">Newcastle
                                            Disease(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.450.100">Hepatitis
                                            D, Chronic(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.450">Hepatitis
                                            D(34)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.417.214">Dengue(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.350.350.120">Hepatitis
                                            C, Chronic(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.350.350">Hepatitis
                                            C(16)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.616.400.080">AIDS-Related
                                            Complex(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.616.400.050">AIDS-Associated
                                            Nephropathy(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.616.400.040">Acquired
                                            Immunodeficiency Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.616.400">HIV
                                            Infections(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.687.359.500">Hepatitis
                                            A(34)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.200.480">HTLV-II
                                            Infections(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.782.815.200.470">HTLV-I
                                            Infections(6)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Sexually Transmitted Diseases">Sexually
                                    Transmitted Diseases(41)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.800.801.400.080">AIDS-Related
                                            Complex(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.800.801.400.400">HIV-Associated
                                            Lipodystrophy Syndrome(32)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.800.801.400.050">AIDS-Associated
                                            Nephropathy(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.800.801.400.040">Acquired
                                            Immunodeficiency Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.800.801.400">HIV
                                            Infections(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Skin Diseases, Viral">Skin
                                    Diseases, Viral(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.825.810">Warts(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Slow Virus Diseases">Slow
                                    Virus Diseases(9)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.839.080">AIDS-Related
                                            Complex(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.839.040">Acquired
                                            Immunodeficiency Syndrome(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Tumor Virus Infections">Tumor
                                    Virus Infections(13)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.928.313">Epstein-Barr
                                            Virus Infections(10)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.928.914">Warts(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C02.928.313.165">Burkitt
                                            Lymphoma(2)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Parasitic Diseases">Parasitic
                            Diseases(18)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Central Nervous System Parasitic Infections">Central
                                    Nervous System Parasitic Infections(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.105.300.500">Malaria,
                                            Cerebral(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Opportunistic Infections">Opportunistic
                                    Infections(7)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.684.050">AIDS-Related
                                            Opportunistic Infections(7)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Protozoan Infections">Protozoan
                                    Infections(11)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.300.500.510">Leishmaniasis,
                                            Visceral(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.300.500.400">Leishmaniasis,
                                            Cutaneous(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.300.500">Leishmaniasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.300.900.200.190">Chagas
                                            Cardiomyopathy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.530.650.675">Malaria,
                                            Cerebral(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.530">Malaria(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.752.530.620">Malaria,
                                            Cerebral(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Skin Diseases, Parasitic">Skin
                                    Diseases, Parasitic(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.858.560">Leishmaniasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C03.858.560.400">Leishmaniasis,
                                            Cutaneous(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplasms">Neoplasms(1973)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04">Neoplasms(33)</a>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Cysts">Cysts(9)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.182">Cysts(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.182.089">Bone
                                            Cysts()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.182.612.765">Polycystic
                                            Ovary Syndrome(8)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Hamartoma">Hamartoma()</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.445.622">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.445.810">Tuberous
                                            Sclerosis()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplasms by Histologic Type">Neoplasms
                                    by Histologic Type(1840)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.465.124">Mast-Cell
                                            Sarcoma(29)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.550.312">Carney
                                            Complex()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.575.650">Osteosarcoma(29)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.575.650.800">Sarcoma,
                                            Ewing(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.590.350">Fibrosarcoma(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.590.425">Histiocytoma(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.835">Sarcoma,
                                            Synovial()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.590.450">Leiomyoma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.590.455">Leiomyosarcoma(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.590.550.660">Rhabdomyosarcoma(16)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795">Sarcoma(59)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.300">Chondrosarcoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025.455">Choriocarcinoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025.455.750">Choriocarcinoma,
                                            Non-gestational(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.165">Carcinoma,
                                            Basal Cell(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.240">Carcinoma
                                            in Situ(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.240.250">Cervical
                                            Intraepithelial Neoplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.240.500">Prostatic
                                            Intraepithelial Neoplasia(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.360">Carcinoma,
                                            Papillary()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.400">Carcinoma,
                                            Squamous Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.565.165">Carcinoma,
                                            Basal Cell(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.660.510">Mesothelioma(14)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.380">Glioma(33)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.380.080">Astrocytoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.380.080.335">Glioblastoma(26)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.380.515">Medulloblastoma(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.380.590">Oligodendroglioma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.590.500">Medulloblastoma(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.590.650.550">Neuroblastoma(40)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.670.725">Retinoblastoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.700.360">Carcinoma,
                                            Papillary()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.700.400">Carcinoma,
                                            Squamous Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.700.600">Papilloma(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.475.750.847">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.520">Meningioma(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.600.580.590.650">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625">Neuroectodermal
                                            Tumors(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.380">Glioma(33)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337">Leukemia(672)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428">Leukemia,
                                            Lymphoid(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.080">Leukemia,
                                            B-Cell(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.080.125">Leukemia,
                                            Lymphocytic, Chronic, B-Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.580">Leukemia,
                                            T-Cell(668)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.580.100">Leukemia-Lymphoma,
                                            Adult T-Cell(668)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.600">Precursor
                                            Cell Lymphoblastic Leukemia-Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.600.600">Precursor
                                            B-Cell Lymphoblastic Leukemia-Lymphoma(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.428.600.620">Precursor
                                            T-Cell Lymphoblastic Leukemia-Lymphoma(24)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.539">Leukemia,
                                            Myeloid(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.337.539.275">Leukemia,
                                            Myeloid, Acute(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386">Lymphoma(271)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.355">Hodgkin
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480">Lymphoma,
                                            Non-Hodgkin(264)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.100">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.150">Lymphoma,
                                            B-Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.150.165">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.150.570">Lymphoma,
                                            B-Cell, Marginal Zone(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.350">Lymphoma,
                                            Follicular(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.487">Lymphoma,
                                            Large-Cell, Anaplastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.493">Lymphoma,
                                            Large-Cell, Immunoblastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.750">Lymphoma,
                                            T-Cell(267)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.750.399">Lymphoma,
                                            Large-Cell, Anaplastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.750.800">Lymphoma,
                                            T-Cell, Cutaneous(271)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.386.480.750.825">Lymphoma,
                                            T-Cell, Peripheral(271)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.435.380">Hepatoblastoma(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.435.595">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.435.850">Thymoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.550.400">Lipoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.550.420">Liposarcoma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.280">Chondrosarcoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.565.370">Gastrointestinal
                                            Stromal Tumors(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.380.080">Astrocytoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.380.080.335">Glioblastoma(26)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.380.515">Medulloblastoma(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.380.590">Oligodendroglioma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.590.500">Medulloblastoma(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.590.650.550">Neuroblastoma(40)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.600.725">Retinoblastoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.650.200">Carcinoid
                                            Tumor(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.580.625.650.510">Melanoma(44)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.595.500">Multiple
                                            Myeloma(74)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.595.600">Plasmacytoma(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.645.520">Meningioma(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.665">Nevi
                                            and Melanomas(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.665.510">Melanoma(44)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.665.560">Nevus(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.665.560.260">Dysplastic
                                            Nevus Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.350">Fibrosarcoma(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.455">Leiomyosarcoma(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.465">Liposarcoma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.550.660">Rhabdomyosarcoma(16)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.620">Osteosarcoma(29)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.620.800">Sarcoma,
                                            Ewing(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.450.795.875">Sarcoma,
                                            Synovial()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.220">Chordoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.330">Germinoma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.330.800">Seminoma(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625">Neuroectodermal
                                            Tumors(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.380">Glioma(33)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.380.080">Astrocytoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.380.080.335">Glioblastoma(26)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.380.515">Medulloblastoma(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.380.590">Oligodendroglioma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.590.500">Medulloblastoma(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.590.650.550">Neuroblastoma(40)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.600.725">Retinoblastoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.650.200">Carcinoid
                                            Tumor(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.625.650.510">Melanoma(44)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.900">Teratocarcinoma(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.910">Teratoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.955.207">Choriocarcinoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.955.207.750">Choriocarcinoma,
                                            Non-gestational(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.465.955.416.202">Choriocarcinoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.035">Adenoma(11)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.035.012">ACTH-Secreting
                                            Pituitary Adenoma()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.035.100.852">Insulinoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.035.215.100">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.035.415">Growth
                                            Hormone-Secreting Pituitary Adenoma(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.035.510">Mesothelioma(14)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200">Carcinoma(365)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025">Adenocarcinoma(42)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025.152">Adrenocortical
                                            Carcinoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025.200">Carcinoid
                                            Tumor(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025.255">Carcinoma,
                                            Hepatocellular(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.557.470.200.025.390">Carcinoma,
                                            Renal Cell(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplasms by Site">Neoplasms
                                    by Site(490)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.476.411.307.180">Colonic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.476.411.307.180.089">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.476.411.307.089">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.476.411.307">Colorectal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.476.205">Esophageal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.120.401">Gallbladder
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.947.960">Urinary
                                            Bladder Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.947.535.585">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.947.535.160">Carcinoma,
                                            Renal Cell(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.440.915.500">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.440.915">Testicular
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.440.770">Prostatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.418.948.585">Endometrial
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.945.418.948">Uterine
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.894.949.500">Thymoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.894.797.520.109.220.624">Small
                                            Cell Lung Carcinoma(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.894.797.520.109.220.249">Carcinoma,
                                            Non-Small-Cell Lung(350)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.894.797.520">Lung
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.476.767">Stomach
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.623">Liver
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.623.160">Carcinoma,
                                            Hepatocellular(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.761">Pancreatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.274.761.249.500">Insulinoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.078.265.750">Adrenocortical
                                            Carcinoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.400">Multiple
                                            Endocrine Neoplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.455">Ovarian
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.455.648">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.475">Pancreatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.475.249.500">Insulinoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.609.145">ACTH-Secreting
                                            Pituitary Adenoma()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.609.292">Growth
                                            Hormone-Secreting Pituitary Adenoma(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.762">Testicular
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.762.500">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.322.894">Thyroid
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.364.818.760">Retinoblastoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.443">Head
                                            and Neck Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.443.353">Esophageal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.443.591">Mouth
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.443.665.710.650">Nasopharyngeal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.443.915">Thyroid
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.614.250.195.885.500.299">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.614.250.580">Meningeal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.614.250.580.500">Meningioma(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.614.550.112">Anti-N-Methyl-D-Aspartate
                                            Receptor Encephalitis(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.805">Skin
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.588.894.309.500">Carney
                                            Complex()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplasms, Experimental">Neoplasms,
                                    Experimental(12)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.619.935.313.165">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.619.935.313">Epstein-Barr
                                            Virus Infections(10)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplasms, Multiple Primary">Neoplasms,
                                    Multiple Primary(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.651.600">Multiple
                                            Endocrine Neoplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.651.800">Tuberous
                                            Sclerosis()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplastic Processes">Neoplastic
                                    Processes(7)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.697.098">Carcinogenesis(7)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neoplastic Syndromes, Hereditary">Neoplastic
                                    Syndromes, Hereditary(8)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.700.100">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.700.645.650">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.700.305">Dysplastic
                                            Nevus Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.700.630">Multiple
                                            Endocrine Neoplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.700.632">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.700.635">Wilms
                                            Tumor(5)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Paraneoplastic Syndromes">Paraneoplastic
                                    Syndromes(88)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.730.856.112">Anti-N-Methyl-D-Aspartate
                                            Receptor Encephalitis(88)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Precancerous Conditions">Precancerous
                                    Conditions(3)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.834.867">Xeroderma
                                            Pigmentosum(3)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pregnancy Complications, Neoplastic">Pregnancy
                                    Complications, Neoplastic(3)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.850.908.416.186">Choriocarcinoma(3)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Tumor Virus Infections">Tumor
                                    Virus Infections(13)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.925.744">Warts(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.925.313.165">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C04.925.313">Epstein-Barr
                                            Virus Infections(10)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Musculoskeletal Diseases">Musculoskeletal
                            Diseases(100)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Bone Diseases">Bone
                                    Diseases(29)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116">Bone
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.070">Bone
                                            Cysts()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.343.250">Cockayne
                                            Syndrome(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.370.231.480">Hypertelorism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.370.535">Klippel-Feil
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.370.797">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.370.894.819">Syndactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.674">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.099.708.702.678">Osteopetrosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.165.412">Osteitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.165.495">Osteomyelitis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.165.762">Spondylitis(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.198.579">Osteoporosis(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.198.579.610">Osteoporosis,
                                            Postmenopausal(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.198.816">Rickets(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.264">Bone
                                            Resorption(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.540.310">Exostoses()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.680">Osteitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.692">Osteitis
                                            Deformans(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.852">Osteonecrosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.852.087">Bisphosphonate-Associated
                                            Osteonecrosis of the Jaw(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.900.800.875">Scoliosis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.900.853">Spondylitis(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.900.853.625.800">Spondylarthropathies(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.900.853.625.800.424">Arthritis,
                                            Psoriatic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.900.853.625.800.850">Spondylitis,
                                            Ankylosing(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.116.900.938">Spondylosis(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Jaw Diseases">Jaw
                                    Diseases(9)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.500.086">Bisphosphonate-Associated
                                            Osteonecrosis of the Jaw(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.500.460">Jaw
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.500.460.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.500.460.606">Pierre
                                            Robin Syndrome()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Joint Diseases">Joint
                                    Diseases(50)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.154">Arthritis,
                                            Rheumatoid(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.154.774">Sjogren's
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.264">Chondrocalcinosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.423">Gout(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.606">Osteoarthritis(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.606.500">Osteoarthritis,
                                            Knee(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.843">Rheumatic
                                            Fever(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.865.800">Spondylarthropathies(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.865.800.424">Arthritis,
                                            Psoriatic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.865.800.850">Spondylitis,
                                            Ankylosing(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.150">Arthrogryposis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.323">Contracture(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.069.680">Spondylitis,
                                            Ankylosing(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114">Arthritis(37)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.629">Nail-Patella
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.145">Arthritis,
                                            Psoriatic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.550.114.122">Arthritis,
                                            Juvenile(4)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Muscular Diseases">Muscular
                                    Diseases(9)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.515">Muscle
                                            Weakness()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.324">Fibromyalgia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.290">Eosinophilia-Myalgia
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.197.270">Dupuytren
                                            Contracture(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.197">Contracture(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.180.297">Intra-Abdominal
                                            Hypertension(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.102">Arthrogryposis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651">Muscular
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.534.500">Muscular
                                            Dystrophies(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.651.701.450">Hypokalemic
                                            Periodic Paralysis(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Musculoskeletal Abnormalities">Musculoskeletal
                                    Abnormalities(15)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.077">Arthrogryposis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.142">Campomelic
                                            Dysplasia(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.906.819">Syndactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.585.800">Syndactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.585.600.374">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.585.600">Polydactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.585.262">Brachydactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.551">Klippel-Feil
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.925">Silver-Russell
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.850">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.103.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.231.480">Hypertelorism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.410">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.536">Macrocephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.540.460">Jaw
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.540.460.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.540.460.606">Pierre
                                            Robin Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.620">Microcephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.660.207.690">Noonan
                                            Syndrome(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Rheumatic Diseases">Rheumatic
                                    Diseases(19)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.613">Osteoarthritis(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.414">Gout(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.321">Fibromyalgia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.114.774">Sjogren's
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.825">Rheumatic
                                            Fever(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.056">Arthritis,
                                            Juvenile(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799">Rheumatic
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.613.500">Osteoarthritis,
                                            Knee(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C05.799.114">Arthritis,
                                            Rheumatoid(3)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Digestive System Diseases">Digestive
                            System Diseases(540)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Biliary Tract Diseases">Biliary
                                    Tract Diseases(14)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.120.123">Biliary
                                            Atresia(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.120.135">Cholestasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.120.135.250.250">Liver
                                            Cirrhosis, Biliary(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.120.200">Cholangitis(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.120.200.110">Cholangitis,
                                            Sclerosing(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.320.401">Gallbladder
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.409">Cholelithiasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.564.401">Gallbladder
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.409.633">Gallstones(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.564">Gallbladder
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.130.564.332.500">Gallstones(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Digestive System Abnormalities">Digestive
                                    System Abnormalities(3)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.198.125">Biliary
                                            Atresia(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.198.439">Hirschsprung
                                            Disease(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Digestive System Neoplasms">Digestive
                                    System Neoplasms(16)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.623">Liver
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.623.160">Carcinoma,
                                            Hepatocellular(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.761">Pancreatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.761.249.500">Insulinoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.120.401">Gallbladder
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.371.205">Esophageal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.371.308">Gastrointestinal
                                            Stromal Tumors(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.371.411.307">Colorectal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.371.411.307.180">Colonic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.371.411.307.180.089">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.301.371.767">Stomach
                                            Neoplasms(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Gastrointestinal Diseases">Gastrointestinal
                                    Diseases(420)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405">Gastrointestinal
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.748.789">Stomach
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.117.119.500.484">Gastroesophageal
                                            Reflux()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.117.430">Esophageal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.117.620">Esophagitis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.117.620.209">Eosinophilic
                                            Esophagitis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.265">Colitis(18)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.265.231">Colitis,
                                            Ulcerative(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.663">Esophagitis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.663.209">Eosinophilic
                                            Esophagitis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.697">Gastritis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.731">Inflammatory
                                            Bowel Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.731.249">Colitis,
                                            Ulcerative(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.205.731.500">Crohn
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.249.205">Esophageal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.249.308">Gastrointestinal
                                            Stromal Tumors(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.249.411.307">Colorectal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.249.411.307.180">Colonic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.249.411.307.180.089">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.249.767">Stomach
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469">Intestinal
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.188">Colitis(18)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.188.231">Colitis,
                                            Ulcerative(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.272.608">Irritable
                                            Bowel Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.356">Colorectal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.356.180">Colonic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.356.180.089">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.158.701.439">Hirschsprung
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.275.800.348">Duodenal
                                            Ulcer(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.432">Inflammatory
                                            Bowel Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.432.249">Colitis,
                                            Ulcerative(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.432.500">Crohn
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.491.307">Colorectal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.491.307.180">Colonic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.491.307.180.089">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.578.249">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.637.250">Celiac
                                            Disease(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.637.506">Lactose
                                            Intolerance(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.818">Protein-Losing
                                            Enteropathies(364)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.469.860.180">Colorectal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.608.173">Duodenal
                                            Ulcer(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.748.340.690">Pyloric
                                            Stenosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.748.340.690.500">Pyloric
                                            Stenosis, Hypertrophic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.748.398">Gastritis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.405.117.119">Deglutition
                                            Disorders(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Liver Diseases">Liver
                                    Diseases(98)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.074">alpha
                                            1-Antitrypsin Deficiency()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.697.160">Carcinoma,
                                            Hepatocellular(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.195">Drug-Induced
                                            Liver Injury(48)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.195.200">Drug-Induced
                                            Liver Injury, Chronic(52)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.241">Fatty
                                            Liver(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380">Hepatitis(34)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.350.050">Hepatitis,
                                            Autoimmune(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.350.100">Hepatitis
                                            B, Chronic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.350.120">Hepatitis
                                            C, Chronic(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.350.220">Hepatitis
                                            D, Chronic(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.422">Hepatitis
                                            A(34)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.437">Hepatitis
                                            B(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.437.100">Hepatitis
                                            B, Chronic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.440">Hepatitis
                                            C(16)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.440.120">Hepatitis
                                            C, Chronic(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.450">Hepatitis
                                            D(34)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.380.705.450.100">Hepatitis
                                            D, Chronic(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.630">Liver
                                            Cirrhosis(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.630.400">Liver
                                            Cirrhosis, Biliary(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.697">Liver
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.552.150.250">Liver
                                            Cirrhosis, Biliary(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pancreatic Diseases">Pancreatic
                                    Diseases(12)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.689.202">Cystic
                                            Fibrosis(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.689.667">Pancreatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.689.750.830">Pancreatitis,
                                            Chronic(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.689.750">Pancreatitis(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C06.689.667.249.500">Insulinoma()</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Stomatognathic Diseases">Stomatognathic
                            Diseases(32)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Jaw Diseases">Jaw
                                    Diseases(9)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.320.440">Jaw
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.320.086">Bisphosphonate-Associated
                                            Osteonecrosis of the Jaw(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.320.440.606">Pierre
                                            Robin Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.320.440.185">Cleft
                                            Palate(7)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Mouth Diseases">Mouth
                                    Diseases(26)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.815.929.669">Sjogren's
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.864.500">Stevens-Johnson
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.525.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.533.324">Chronic
                                            Periodontitis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.075">Behcet
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.409.225">Cleft
                                            Lip(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.525.164">Cleft
                                            Lip(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.804">Tooth
                                            Loss(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.525.304">Fibromatosis,
                                            Gingival()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.525.480">Macrostomia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.565">Mouth
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.654">Oral
                                            Submucous Fibrosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.693">Peri-Implantitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.258.428.200">Fibromatosis,
                                            Gingival()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.258.428.250">Gingival
                                            Hyperplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.258.480">Gingivitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.282">Peri-Implantitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.465.714.533">Periodontitis(7)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pharyngeal Diseases">Pharyngeal
                                    Diseases(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.550.745.650">Nasopharyngeal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.550.350.650">Nasopharyngeal
                                            Neoplasms(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Stomatognathic System Abnormalities">Stomatognathic
                                    System Abnormalities(10)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.800">Tooth
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.800.255.500">Amelogenesis
                                            Imperfecta()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.525.480">Macrostomia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.525.304">Fibromatosis,
                                            Gingival()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.500.460">Jaw
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.500.460.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.500.460.606">Pierre
                                            Robin Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.525.164">Cleft
                                            Lip(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.650.525.185">Cleft
                                            Palate(7)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Tooth Diseases">Tooth
                                    Diseases(5)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.793.700">Tooth
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.793.700.255.500">Amelogenesis
                                            Imperfecta()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.793.720.210">Dental
                                            Caries(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C07.793.870">Tooth
                                            Loss(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Respiratory Tract Diseases">Respiratory
                            Tract Diseases(567)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Bronchial Diseases">Bronchial
                                    Diseases(49)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.127.108">Asthma(45)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.127.108.054">Asthma,
                                            Aspirin-Induced(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.127.210">Bronchial
                                            Hyperreactivity(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.127.446">Bronchitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.127.446.135">Bronchiolitis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.127.446.135.140">Bronchiolitis
                                            Obliterans(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Lung Diseases">Lung
                                    Diseases(514)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381">Lung
                                            Diseases(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.495.146">Bronchitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.495.146.135">Bronchiolitis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.495.146.135.140">Bronchiolitis
                                            Obliterans(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.495.389">Pulmonary
                                            Disease, Chronic Obstructive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.520">Lung
                                            Injury(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.520.500">Acute
                                            Lung Injury(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.520.702.125">Asbestosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.520.702.760">Silicosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.520.750.500">Bronchopulmonary
                                            Dysplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.540">Lung
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.540.140.500">Carcinoma,
                                            Non-Small-Cell Lung(350)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.540.140.750">Small
                                            Cell Lung Carcinoma(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.677">Pneumonia(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.742">Pulmonary
                                            Edema(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.765">Pulmonary
                                            Fibrosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.765.500">Idiopathic
                                            Pulmonary Fibrosis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.495.108">Asthma(45)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.483.950">Wegener
                                            Granulomatosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.483.581.760">Silicosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.483.581.125">Asbestosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.483">Lung
                                            Diseases, Interstitial(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.483.156">Anti-Glomerular
                                            Basement Membrane Disease(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.483.487.500">Idiopathic
                                            Pulmonary Fibrosis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.472.850">Pulmonary
                                            Aspergillosis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.423">Hypertension,
                                            Pulmonary(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.187">Cystic
                                            Fibrosis(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.381.112">alpha
                                            1-Antitrypsin Deficiency()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nose Diseases">Nose
                                    Diseases(6)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.460.799">Rhinitis(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.460.799.633">Rhinitis,
                                            Allergic, Seasonal(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Respiration Disorders">Respiration
                                    Disorders(55)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.618">Respiration
                                            Disorders(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.618.085">Apnea(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.618.248">Cough(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.618.846.688">Positive-Pressure
                                            Respiration, Intrinsic(51)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Respiratory Hypersensitivity">Respiratory
                                    Hypersensitivity(46)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.674.095.054">Asthma,
                                            Aspirin-Induced(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.674.095">Asthma(45)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.674.815">Rhinitis,
                                            Allergic, Seasonal(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Respiratory Tract Infections">Respiratory
                                    Tract Infections(13)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.730.730">Severe
                                            Acute Respiratory Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.730.674">Rhinitis(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.730.610">Pneumonia(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.730.099.135">Bronchiolitis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.730.099">Bronchitis(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Respiratory Tract Neoplasms">Respiratory
                                    Tract Neoplasms(360)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.785.520">Lung
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.785.520.100.220.500">Carcinoma,
                                            Non-Small-Cell Lung(350)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C08.785.520.100.220.750">Small
                                            Cell Lung Carcinoma(8)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Otorhinolaryngologic Diseases">Otorhinolaryngologic
                            Diseases(16)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Ear Diseases">Ear
                                    Diseases(8)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.458.341">Hearing
                                            Loss(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.458.341.186">Deafness(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.458.341.887">Hearing
                                            Loss, Sensorineural(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.458.341.887.460">Hearing
                                            Loss, Noise-Induced(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.568.900.883">Vertigo()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.705">Otitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.705.663">Otitis
                                            Media(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.218.768">Otosclerosis(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nose Diseases">Nose
                                    Diseases(6)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.603.799">Rhinitis(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.603.799.633">Rhinitis,
                                            Allergic, Seasonal(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Otorhinolaryngologic Neoplasms">Otorhinolaryngologic
                                    Neoplasms(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.647.710.650">Nasopharyngeal
                                            Neoplasms(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pharyngeal Diseases">Pharyngeal
                                    Diseases(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.775.174">Deglutition
                                            Disorders(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.775.350.650">Nasopharyngeal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C09.775.549.650">Nasopharyngeal
                                            Neoplasms(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nervous System Diseases">Nervous
                            System Diseases(457)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Autoimmune Diseases of the Nervous System">Autoimmune
                                    Diseases of the Nervous System(25)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.114.375.500">Multiple
                                            Sclerosis(22)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.114.656">Myasthenia
                                            Gravis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.114.875.700">Giant
                                            Cell Arteritis(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Autonomic Nervous System Diseases">Autonomic
                                    Nervous System Diseases(101)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.177.575.550.750">Shy-Drager
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.177.575.600.537">Post-Exercise
                                            Hypotension(100)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Central Nervous System Diseases">Central
                                    Nervous System Diseases(330)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.163.100.680.760">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.163.100.937.249">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.199.250.500">Post-Concussion
                                            Syndrome(100)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.211.885.500.299">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.252.190">Cerebellar
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.252.190.530.060">Ataxia
                                            Telangiectasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.252.300">Dandy-Walker
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.252.700.150">Friedreich
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.150">Brain
                                            Ischemia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.150.477">Brain
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.150.477.200">Cerebral
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.150.716">Hypoxia-Ischemia,
                                            Brain(49)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.200">Carotid
                                            Artery Diseases(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.200.345.350">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.200.357">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.200.360">Carotid
                                            Stenosis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.200.600">Moyamoya
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.350.500.350">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.400">Dementia,
                                            Vascular(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.510.200.200">Cerebral
                                            Amyloid Angiopathy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.510.200.737">Moyamoya
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.510.600">Intracranial
                                            Aneurysm(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.510.800.500">Dementia,
                                            Vascular(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.535.200">Cerebral
                                            Hemorrhage(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.535.800">Subarachnoid
                                            Hemorrhage(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.775">Stroke(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.775.200">Brain
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.775.200.200">Cerebral
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.300.850.500">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380">Dementia(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380.100">Alzheimer
                                            Disease(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380.165">Creutzfeldt-Jakob
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380.230">Dementia,
                                            Vascular(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380.266">Frontotemporal
                                            Lobar Degeneration(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380.266.299">Frontotemporal
                                            Dementia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.380.278">Huntington
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.430.124">Anti-N-Methyl-D-Aspartate
                                            Receptor Encephalitis(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490">Epilepsy(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490.250.670">Myoclonic
                                            Epilepsy, Juvenile()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490.360">Epilepsies,
                                            Partial(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490.360.280">Epilepsy,
                                            Rolandic()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490.375">Epilepsy,
                                            Generalized(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490.631">Seizures(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.490.650">Seizures,
                                            Febrile(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.399.750">Migraine
                                            Disorders(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.399.750.250">Migraine
                                            with Aura(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.399.750.450">Migraine
                                            without Aura(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.399.875">Tension-Type
                                            Headache(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.399.937.500">Cluster
                                            Headache(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.699.124">Post-Dural
                                            Puncture Headache(100)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.546.699.249">Post-Traumatic
                                            Headache(100)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.602">Hydrocephalus()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.602.288">Dandy-Walker
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.617.477.299">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.617.738.675.149">ACTH-Secreting
                                            Pituitary Adenoma()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.617.738.675.299">Growth
                                            Hormone-Secreting Pituitary Adenoma(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.624.500">Hypoxia-Ischemia,
                                            Brain(49)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.631.450">Hydrocephalus()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.631.450.500">Dandy-Walker
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.695.500">Dementia,
                                            Vascular(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.744.320">Pantothenate
                                            Kinase-Associated Neurodegeneration()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.228.205.300.500">Malaria,
                                            Cerebral(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.228.507">Meningitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.228.800">Prion
                                            Diseases(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.228.800.230">Creutzfeldt-Jakob
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.566">Meningitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.075">Angelman
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.262.249.750">Huntington
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.300.750">Torticollis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.350">Essential
                                            Tremor(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.550.700">Shy-Drager
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.575">Pantothenate
                                            Kinase-Associated Neurodegeneration()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.600.400">Parkinson
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.700">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.662.825.800">Tourette
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.854.139">Amyotrophic
                                            Lateral Sclerosis(12)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.854.787.200">Friedreich
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.079.545">Huntington
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.079.612.700">Shy-Drager
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.079.800">Pantothenate
                                            Kinase-Associated Neurodegeneration()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.079.862.500">Parkinson
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.079.882">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.079.898">Tourette
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.140.254">Cerebral
                                            Palsy()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.163.100.435.825.400">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.228.140.163.100.435.825.775">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Cranial Nerve Diseases">Cranial
                                    Nerve Diseases(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.292.562.750.500">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.292.562.250">Duane
                                            Retraction Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.292.700.225">Optic
                                            Atrophy()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.292.562.887">Strabismus()</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Demyelinating Diseases">Demyelinating
                                    Diseases(22)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.314.350.500">Multiple
                                            Sclerosis(22)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nervous System Malformations">Nervous
                                    System Malformations(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.034.687">Aicardi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.034.875">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.205">Dandy-Walker
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.300.099">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.300.200">Charcot-Marie-Tooth
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.300.780">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.507.249">Lissencephaly(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.507.249.249.500">Walker-Warburg
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.507.374">Macrocephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.507.500">Microcephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.507.750.750">Periventricular
                                            Nodular Heterotopia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.507.875">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.500.680">Neural
                                            Tube Defects(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nervous System Neoplasms">Nervous
                                    System Neoplasms(4)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.551.240.500.500">Meningioma(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.551.240.500">Meningeal
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.551.240.250.700.500.249">Pallister-Hall
                                            Syndrome()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neurocutaneous Syndromes">Neurocutaneous
                                    Syndromes(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.562.850">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.562.600.500">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.562.100">Ataxia
                                            Telangiectasia()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neurodegenerative Diseases">Neurodegenerative
                                    Diseases(122)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.700">Pantothenate
                                            Kinase-Associated Neurodegeneration()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.950.300.299">Frontotemporal
                                            Dementia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.850">Tourette
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.865">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.562">Motor
                                            Neuron Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.562.250">Amyotrophic
                                            Lateral Sclerosis(12)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.625.700">Shy-Drager
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.781.249">Anti-N-Methyl-D-Aspartate
                                            Receptor Encephalitis(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.812">Parkinson
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.843">Prion
                                            Diseases(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.875">Shy-Drager
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.945.249">Alzheimer
                                            Disease(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.945.500">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.950.050">Amyotrophic
                                            Lateral Sclerosis(12)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.950.300">Frontotemporal
                                            Lobar Degeneration(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.549.400">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.497">Huntington
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.495.780">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.495.200">Charcot-Marie-Tooth
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.495.099">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.362">Cockayne
                                            Syndrome(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.574.500.825.200">Friedreich
                                            Ataxia()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neurologic Manifestations">Neurologic
                                    Manifestations(46)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.636">Paresis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.636.500">Paraparesis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.742">Seizures(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.751.418.341">Hearing
                                            Loss(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.751.418.341.186">Deafness(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.751.418.341.887">Hearing
                                            Loss, Sensorineural(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.751.418.341.887.460">Hearing
                                            Loss, Noise-Induced(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.951">Vertigo()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.350.300">Dystonia(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.350.300.800">Torticollis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.350.850">Tremor(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606">Neurobehavioral
                                            Manifestations(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.150.500.300">Dyslexia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.150.500.800.750">Stuttering()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.150.550.200">Dyslexia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.350.090">Ataxia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.350.090.500">Cerebellar
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.350.090.500.530.060">Ataxia
                                            Telangiectasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.643">Intellectual
                                            Disability(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.643.220">Down
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.643.455">Mental
                                            Retardation, X-Linked()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.643.455.249">Coffin-Lowry
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.643.700">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.606.762.300">Hallucinations(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.613.593">Muscle
                                            Weakness()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.613.612">Muscular
                                            Atrophy(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.613.750">Spasm(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.617">Pain(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.617.470">Headache(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.622">Paralysis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.622.447.690">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.622.669">Paraplegia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.597.622.669.300">Brown-Sequard
                                            Syndrome(8)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neuromuscular Diseases">Neuromuscular
                                    Diseases(22)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.467">Motor
                                            Neuron Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.467.250">Amyotrophic
                                            Lateral Sclerosis(12)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.829.800.300.780">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.829.800.300.200">Charcot-Marie-Tooth
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.829.800.300.099">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.829.675">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.829.380">Hand-Arm
                                            Vibration Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.758.725">Myasthenia
                                            Gravis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.491.650.450">Hypokalemic
                                            Periodic Paralysis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.491.425">Fibromyalgia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.491.387">Eosinophilia-Myalgia
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.491.175.500">Muscular
                                            Dystrophies(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.668.491">Muscular
                                            Diseases(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Neurotoxicity Syndromes">Neurotoxicity
                                    Syndromes(30)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.720.112">Alcohol-Induced
                                            Disorders, Nervous System(30)</a></li>
                                </ul>
                            </li>
                            <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.803">Restless Legs
                                    Syndrome(3)</a>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Sleep Disorders">Sleep
                                    Disorders(16)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.886.425.800.700">Restless
                                            Legs Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.886.425.800.200.750.500">Cataplexy(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.886">Sleep
                                            Disorders(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.886.659.634">Restless
                                            Legs Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.886.659.700">Sleep-Wake
                                            Transition Disorders(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.886.425.800.200.750">Narcolepsy(5)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Trauma, Nervous System">Trauma,
                                    Nervous System(111)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.900.250.300.400">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.900.300.087.125.500">Post-Concussion
                                            Syndrome(100)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C10.900.300.350.300.500">Post-Concussion
                                            Syndrome(100)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Male Urogenital Diseases">Male
                            Urogenital Diseases(181)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Genital Diseases, Male">Genital
                                    Diseases, Male(24)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.260.937">Testicular
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.365.700">Infertility,
                                            Male(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.260.750">Prostatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.365">Infertility(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.260.937.500">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.365.700.253">Asthenozoospermia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.365.700.380">Azoospermia(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.365.700.508">Oligospermia(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.365.700.754">Sertoli
                                            Cell-Only Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.494.400">Hypospadias(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.565.500">Prostatic
                                            Hyperplasia(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.565.625">Prostatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.644.486">Erectile
                                            Dysfunction(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.294.829.258">Cryptorchidism(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Urogenital Abnormalities">Urogenital
                                    Abnormalities(33)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.258">Cryptorchidism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.316.064.500">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.316.096.500">Androgen-Insensitivity
                                            Syndrome(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.316.096.750">Kallmann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.316.129.750">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.316.309">Gonadal
                                            Dysgenesis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.706.516">Hypospadias(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Urogenital Neoplasms">Urogenital
                                    Neoplasms(12)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.758.409.750">Prostatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.758.409.937">Testicular
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.758.409.937.500">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.758.820.750.160">Carcinoma,
                                            Renal Cell(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.758.820.750.585">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.758.820.968">Urinary
                                            Bladder Neoplasms(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Urologic Diseases">Urologic
                                    Diseases(126)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.050">AIDS-Associated
                                            Nephropathy(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419">Kidney
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.967.249">Nephrolithiasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.967">Urolithiasis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.934.734.269">Albuminuria(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.934.284">Enuresis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.829.813">Urinary
                                            Bladder Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.829.495">Cystitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.936.463">Hemolytic-Uremic
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.936">Uremia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.815.885.250">Cystinuria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.815.770">Pseudohypoaldosteronism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.780.750.500">Kidney
                                            Failure, Chronic(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.630.643">Nephrotic
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.600">Nephrolithiasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.570.363.680">Lupus
                                            Nephritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.570.363.625">Glomerulonephritis,
                                            Membranous(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.570.363.608">Glomerulonephritis,
                                            IGA(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.570.363.304">Anti-Glomerular
                                            Basement Membrane Disease(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.570.363">Glomerulonephritis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.570">Nephritis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.473.585">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.135">Diabetes
                                            Insipidus(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.192">Diabetic
                                            Nephropathies(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C12.777.419.473.160">Carcinoma,
                                            Renal Cell(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Eye Diseases">Eye
                            Diseases(62)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Corneal Diseases">Corneal
                                    Diseases(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.204.236.438">Fuchs'
                                            Endothelial Dystrophy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.204.627">Keratoconus(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.204.564">Keratitis(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Eye Abnormalities">Eye
                                    Abnormalities(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.250.110">Coloboma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.250.060">Aniridia(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Eye Diseases, Hereditary">Eye
                                    Diseases, Hereditary(5)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.060">Aniridia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.040.545">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.040">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.019">Aicardi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.235">Duane
                                            Retraction Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.516">Leber
                                            Congenital Amaurosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.684">Retinitis
                                            Pigmentosa(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.684.249">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.881">Walker-Warburg
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.270.162.438">Fuchs'
                                            Endothelial Dystrophy(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Eye Neoplasms">Eye
                                    Neoplasms(6)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.319.475.760">Retinoblastoma(6)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Lacrimal Apparatus Diseases">Lacrimal
                                    Apparatus Diseases()</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.496.260.719">Sjogren's
                                            Syndrome(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Lens Diseases">Lens
                                    Diseases()</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.510.245">Cataract()</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Ocular Hypertension">Ocular
                                    Hypertension(12)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.525.381">Glaucoma(12)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Ocular Motility Disorders">Ocular
                                    Motility Disorders(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.590.224">Duane
                                            Retraction Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.590.472.500">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.590.810">Strabismus()</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Optic Nerve Diseases">Optic
                                    Nerve Diseases()</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.640.451">Optic
                                            Atrophy()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Orbital Diseases">Orbital
                                    Diseases(5)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.675.349.500">Graves
                                            Disease(5)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Refractive Errors">Refractive
                                    Errors(10)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.744.212">Astigmatism(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.744.636">Myopia(7)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Retinal Diseases">Retinal
                                    Diseases(30)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.364">Leber
                                            Congenital Amaurosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.257">Diabetic
                                            Retinopathy(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.585.439">Macular
                                            Degeneration(14)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.585.439.245">Macular
                                            Edema(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.585.658.500">Retinitis
                                            Pigmentosa(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.648">Retinal
                                            Detachment(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.717.760">Retinoblastoma(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.773">Retinitis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.836">Retinopathy
                                            of Prematurity(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.768.585">Retinal
                                            Degeneration()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Uveal Diseases">Uveal
                                    Diseases(3)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.941.375.060">Aniridia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.941.879">Uveitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C11.941.879.780.880.200">Behcet
                                            Syndrome(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Hemic and Lymphatic Diseases">Hemic
                            and Lymphatic Diseases(1241)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Hematologic Diseases">Hematologic
                                    Diseases(285)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.085">Anemia,
                                            Aplastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.085.080.280">Fanconi
                                            Anemia(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.141.150.150">Anemia,
                                            Sickle Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.141.150.875">Thalassemia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.141.150.875.100">alpha-Thalassemia(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.141.150.875.150">beta-Thalassemia(66)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.141.150.875.575">delta-Thalassemia(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.141.610">Hemolytic-Uremic
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071.750">Red-Cell
                                            Aplasia, Pure(9)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.100.100.500">Hemophilia
                                            A(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.100.141.500">Hemophilia
                                            A(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.231.335">Eosinophilia-Myalgia
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.231.341">Eosinophilic
                                            Esophagitis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.546">Leukopenia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.546.184">Agranulocytosis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.546.184.564">Neutropenia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.546.184.564.750.500">Chemotherapy-Induced
                                            Febrile Neutropenia(9)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.546.605">Lymphopenia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.925">Thrombophilia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.120">Blood
                                            Group Incompatibility(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.140.855">Thrombocytopenia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.140.855.925.500">Hemolytic-Uremic
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.147.142">Agammaglobulinemia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.147.333.249">Hyper-IgM
                                            Immunodeficiency Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.147.333.249.500">Hyper-IgM
                                            Immunodeficiency Syndrome, Type 1(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.147.542.640">Monoclonal
                                            Gammopathy of Undetermined Significance(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.147.780.650">Multiple
                                            Myeloma(74)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.190.196">Anemia,
                                            Aplastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.190.196.080.280">Fanconi
                                            Anemia(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.190.615">Myelodysplastic-Myeloproliferative
                                            Diseases(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.190.636">Myeloproliferative
                                            Disorders(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.420.155">Anemia,
                                            Sickle Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.420.826">Thalassemia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.420.826.100">alpha-Thalassemia(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.420.826.150">beta-Thalassemia(66)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.420.826.200">delta-Thalassemia(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.463.500">Hemophilia
                                            A(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.463.515.460">Multiple
                                            Myeloma(74)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.463.515.530">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.463.515.900">Telangiectasia,
                                            Hereditary Hemorrhagic()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.553.231">Eosinophilia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.378.071">Anemia(19)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Lymphatic Diseases">Lymphatic
                                    Diseases(964)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.250">Histiocytosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.861.800">Thymoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.250.410.800">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.315">Lymphadenitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.315.249">Cat-Scratch
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.451.249.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.496">Lymphedema()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.032">Agammaglobulinemia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560">Leukemia,
                                            Lymphoid(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.080">Leukemia,
                                            B-Cell(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.080.125">Leukemia,
                                            Lymphocytic, Chronic, B-Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.575">Leukemia,
                                            T-Cell(668)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.575.100">Leukemia-Lymphoma,
                                            Adult T-Cell(668)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.600">Precursor
                                            Cell Lymphoblastic Leukemia-Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.600.600">Precursor
                                            B-Cell Lymphoblastic Leukemia-Lymphoma(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.560.600.620">Precursor
                                            T-Cell Lymphoblastic Leukemia-Lymphoma(24)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569">Lymphoma(271)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.355">Hodgkin
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480">Lymphoma,
                                            Non-Hodgkin(264)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.100">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.150">Lymphoma,
                                            B-Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.150.165">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.150.570">Lymphoma,
                                            B-Cell, Marginal Zone(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.350">Lymphoma,
                                            Follicular(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.487">Lymphoma,
                                            Large-Cell, Anaplastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.493">Lymphoma,
                                            Large-Cell, Immunoblastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.750">Lymphoma,
                                            T-Cell(267)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.750.800">Lymphoma,
                                            T-Cell, Cutaneous(271)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.569.480.750.825">Lymphoma,
                                            T-Cell, Peripheral(271)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.515.827">Sarcoidosis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.560">Mucocutaneous
                                            Lymph Node Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.816">Thymus
                                            Hyperplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C15.604.250.410">Histiocytosis,
                                            Non-Langerhans-Cell()</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Female Urogenital Diseases and Pregnancy Complications">Female
                            Urogenital Diseases and Pregnancy Complications(299)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Female Urogenital Diseases">Female
                                    Urogenital Diseases(186)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.570.363.625">Glomerulonephritis,
                                            Membranous(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.570.363.608">Glomerulonephritis,
                                            IGA(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.600">Nephrolithiasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.630.643">Nephrotic
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.780.750.500">Kidney
                                            Failure, Chronic(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.815.770">Pseudohypoaldosteronism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.815.885.250">Cystinuria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.936">Uremia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.936.463">Hemolytic-Uremic
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.829.495">Cystitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.829.707">Urinary
                                            Bladder Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.934.252">Enuresis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.934.734.269">Albuminuria(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.967">Urolithiasis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.967.249">Nephrolithiasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.570.363.680">Lupus
                                            Nephritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.570.363.304">Anti-Glomerular
                                            Basement Membrane Disease(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.570.363">Glomerulonephritis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.570">Nephritis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.473.585">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.473.160">Carcinoma,
                                            Renal Cell(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.192">Diabetic
                                            Nephropathies(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.135">Diabetes
                                            Insipidus(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419.050">AIDS-Associated
                                            Nephropathy(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.968.419">Kidney
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.056.630.580.765">Polycystic
                                            Ovary Syndrome(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.056.630.705">Ovarian
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.056.630.705.648">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.056.630.750">Primary
                                            Ovarian Insufficiency(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.163">Endometriosis(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.365">Infertility(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.365.700">Infertility,
                                            Female(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.852.113">Adenomyosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.852.762">Uterine
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.852.762.200">Endometrial
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.852.833">Uterine
                                            Prolapse(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.500.944.902.368">Vulvar
                                            Vestibulitis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.875.253.064.500">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.875.253.096.500">Androgen-Insensitivity
                                            Syndrome(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.875.253.096.750">Kallmann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.875.253.129.750">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.875.253.309">Gonadal
                                            Dysgenesis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.875.466">Hypospadias(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.418.685">Ovarian
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.418.685.648">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.418.875">Uterine
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.418.875.200">Endometrial
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.820.535.160">Carcinoma,
                                            Renal Cell(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.820.535.585">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.351.937.820.945">Urinary
                                            Bladder Neoplasms(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pregnancy Complications">Pregnancy
                                    Complications(113)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.844.253">Depression,
                                            Postpartum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.720.949.416.218">Choriocarcinoma(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.590.132">Abruptio
                                            Placentae(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.420.491.500">Premature
                                            Birth(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.170">Diabetes,
                                            Gestational(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.395.249">Pre-Eclampsia(101)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.395.124">Eclampsia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.395">Hypertension,
                                            Pregnancy-Induced(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.277.370">Fetal
                                            Growth Retardation(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C13.703.420.078">Abruptio
                                            Placentae(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Cardiovascular Diseases">Cardiovascular
                            Diseases(712)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14">Cardiovascular
                                    Diseases(1)</a>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Cardiovascular Abnormalities">Cardiovascular
                                    Abnormalities(68)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.240.400.145">Arrhythmogenic
                                            Right Ventricular Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.240.850.906">May-Thurner
                                            Syndrome(63)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.240.400.787">Noonan
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.240.400.849">Tetralogy
                                            of Fallot(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.240.400.021.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.240.400.725">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280">Heart
                                            Diseases(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Heart Diseases">Heart
                                    Diseases(286)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067">Arrhythmias,
                                            Cardiac(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.198">Atrial
                                            Fibrillation(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.248">Atrial
                                            Flutter(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.322">Brugada
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.558.323">Bundle-Branch
                                            Block(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.565">Long
                                            QT Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.780">Pre-Excitation
                                            Syndromes(102)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.780.770">Pre-Excitation,
                                            Mahaim-Type(102)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.067.845">Tachycardia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.195">Cardiomegaly(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.195.160">Cardiomyopathy,
                                            Dilated(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.195.400">Hypertrophy,
                                            Left Ventricular(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.238.028">Arrhythmogenic
                                            Right Ventricular Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.238.070">Cardiomyopathy,
                                            Dilated(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.238.190">Chagas
                                            Cardiomyopathy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.238.625">Myocarditis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.383.220">Death,
                                            Sudden, Cardiac(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.383.610">Out-of-Hospital
                                            Cardiac Arrest(97)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.400.044.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.400.145">Arrhythmogenic
                                            Right Ventricular Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.400.725">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.400.787">Noonan
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.400.849">Tetralogy
                                            of Fallot(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.434">Heart
                                            Failure(9)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.459.500">Carney
                                            Complex()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.484.400.500">Mitral
                                            Valve Prolapse(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647">Myocardial
                                            Ischemia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.124">Acute
                                            Coronary Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.187.074">Acute
                                            Coronary Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.250">Coronary
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.250.260">Coronary
                                            Artery Disease(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.250.285.200">Coronary
                                            Restenosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.250.647">Coronary-Subclavian
                                            Steal Syndrome(46)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.647.500">Myocardial
                                            Infarction(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.874">Rheumatic
                                            Heart Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.280.945">Ventricular
                                            Dysfunction(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Vascular Diseases">Vascular
                                    Diseases(524)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.055.239">Aortic
                                            Aneurysm(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.055.239.075">Aortic
                                            Aneurysm, Abdominal(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.055.635">Intracranial
                                            Aneurysm(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.077.410">Klippel-Trenaunay-Weber
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.109.139">Aortic
                                            Aneurysm(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.109.139.075">Aortic
                                            Aneurysm, Abdominal(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.137.126.307">Atherosclerosis(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.137.126.339">Coronary
                                            Artery Disease(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.137.126.372.500">Dementia,
                                            Vascular(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.137.230">Carotid
                                            Stenosis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.137.615">Moyamoya
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.184">Arteritis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.184.438">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.092">Brain
                                            Ischemia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.092.477">Brain
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.092.477.200">Cerebral
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.092.716">Hypoxia-Ischemia,
                                            Brain(49)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.123">Carotid
                                            Artery Diseases(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.123.345.400">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.123.357">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.123.360">Carotid
                                            Stenosis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.123.620">Moyamoya
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.535.500.350">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.560.200.200">Cerebral
                                            Amyloid Angiopathy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.560.200.737">Moyamoya
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.560.300">Intracranial
                                            Aneurysm(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.560.350.500">Dementia,
                                            Vascular(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.573.200">Cerebral
                                            Hemorrhage(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.573.800">Subarachnoid
                                            Hemorrhage(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.855">Stroke(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.855.200">Brain
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.855.200.200">Cerebral
                                            Infarction(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.253.946.700">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.303.297">Intra-Abdominal
                                            Hypertension(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.320.382">Diabetic
                                            Retinopathy(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.355.590">Thromboembolism(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.355.590.700">Venous
                                            Thromboembolism(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.355.830">Thrombosis(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.355.830.850">Thromboembolism(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.355.830.850.700">Venous
                                            Thromboembolism(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.355.830.925">Venous
                                            Thrombosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.440">Hand-Arm
                                            Vibration Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.454.460">Multiple
                                            Myeloma(74)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.454.530">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.454.900">Telangiectasia,
                                            Hereditary Hemorrhagic()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.489">Hypertension(28)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.489.480">Hypertension,
                                            Pregnancy-Induced(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.514">Hypotension(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.514.611">Post-Exercise
                                            Hypotension(100)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.514.741">Shy-Drager
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585">Myocardial
                                            Ischemia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.124">Acute
                                            Coronary Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.187.074">Acute
                                            Coronary Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.250">Coronary
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.250.260">Coronary
                                            Artery Disease(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.250.285.200">Coronary
                                            Restenosis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.250.647">Coronary-Subclavian
                                            Steal Syndrome(46)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.585.500">Myocardial
                                            Infarction(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.617.648">May-Thurner
                                            Syndrome(63)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.823.213">Ataxia
                                            Telangiectasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.823.780">Telangiectasia,
                                            Hereditary Hemorrhagic()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.927">Varicose
                                            Veins(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940">Vasculitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.090">Arteritis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.090.530">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.100">Behcet
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.560">Mucocutaneous
                                            Lymph Node Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.897.249">Anti-Neutrophil
                                            Cytoplasmic Antibody-Associated Vasculitis(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.897.249.750">Wegener
                                            Granulomatosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.940.907.700">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907">Vascular
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C14.907.055">Aneurysm(10)</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Congenital, Hereditary, and Neonatal Diseases and Abnormalities">Congenital,
                            Hereditary, and Neonatal Diseases and Abnormalities(367)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Congenital Abnormalities">Congenital
                                    Abnormalities(136)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.850.968">Telangiectasia,
                                            Hereditary Hemorrhagic()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.019.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.040">Angelman
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.080">Beckwith-Wiedemann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.260">Down
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.380">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.790">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.260.870">Silver-Russell
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.314.125">Biliary
                                            Atresia(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.314.439">Hirschsprung
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.384.079">Aniridia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.384.282">Coloboma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.482.249.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.077">Arthrogryposis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.142">Campomelic
                                            Dysplasia(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.103.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.231.480">Hypertelorism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.410">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.532">Macrocephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.540.460">Jaw
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.540.460.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.540.460.606">Pierre
                                            Robin Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.620">Microcephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.690">Noonan
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.207.850">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.551">Klippel-Feil
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.585.262">Brachydactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.019.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.080">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.095">Angelman
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.133">Beckwith-Wiedemann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.229">Carney
                                            Complex()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.250">Cockayne
                                            Syndrome(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.585.600">Polydactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.585.600.374">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.585.800">Syndactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.621.906.819">Syndactyly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.034.687">Aicardi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.034.875">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.205">Dandy-Walker
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.300.099">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.300.200">Charcot-Marie-Tooth
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.300.780">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.410">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.507.186">Lissencephaly(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.507.186.249.500">Walker-Warburg
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.507.343">Macrocephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.507.500">Microcephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.507.812.750">Periventricular
                                            Nodular Heterotopia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.507.875">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.666.680">Neural
                                            Tube Defects(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.831.108">Carney
                                            Complex()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.831.350">Ectodermal
                                            Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.831.512">Ichthyosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.831.512.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.831.766">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.831.936">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.500.460">Jaw
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.500.460.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.500.460.606">Pierre
                                            Robin Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.525.164">Cleft
                                            Lip(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.525.185">Cleft
                                            Palate(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.525.304">Fibromatosis,
                                            Gingival()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.525.480">Macrostomia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.800">Tooth
                                            Abnormalities(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.850.800.255.500">Amelogenesis
                                            Imperfecta()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.258">Cryptorchidism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.316.064.500">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.316.096.500">Androgen-Insensitivity
                                            Syndrome(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.316.096.750">Kallmann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.316.129.750">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.316.309">Gonadal
                                            Dysgenesis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.939.516">Hypospadias(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.327">Down
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.350">Ectodermal
                                            Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.410">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.550">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.606">Nail-Patella
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.690">Pallister-Hall
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.804">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.855">Silver-Russell
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.077.938">Waardenburg
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.162">Aicardi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.400.021.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.400.145">Arrhythmogenic
                                            Right Ventricular Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.400.715">Long
                                            QT Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.400.720">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.400.784">Noonan
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.400.849">Tetralogy
                                            of Fallot(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.131.240.850.890">May-Thurner
                                            Syndrome(63)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Fetal Diseases">Fetal
                                    Diseases(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.300.390">Fetal
                                            Growth Retardation(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Genetic Diseases, Inborn">Genetic
                                    Diseases, Inborn(276)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.202.607.500">alpha-Mannosidosis(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.202.607.750">beta-Mannosidosis(68)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.240">Cytochrome-c
                                            Oxidase Deficiency(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.398.641.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.398.641.803.441">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.398.641.803.850">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.595.554.825.400">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.595.554.825.775">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.595.577.500">alpha-Mannosidosis(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.595.577.750">beta-Mannosidosis(68)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.618.337">Hemochromatosis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.618.711.550">Hypokalemic
                                            Periodic Paralysis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.663.760">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.753">Progeria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.798">Purine-Pyrimidine
                                            Metabolism, Inborn Errors(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.798.368">Gout(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.861.770">Pseudohypoaldosteronism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.861.885.250">Cystinuria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.577">Muscular
                                            Dystrophies(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.577.750">Walker-Warburg
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.600">Nail-Patella
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.700.100">Adenomatous
                                            Polyposis Coli()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.700.305">Dysplastic
                                            Nevus Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.700.630">Multiple
                                            Endocrine Neoplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.700.636">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.700.642">Wilms
                                            Tumor(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.700.645.650">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.080">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.080.100">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.210">Dermatitis,
                                            Atopic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.250">Ectodermal
                                            Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.475">Keratoderma,
                                            Palmoplantar()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.730">Porokeratosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.750">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.820">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.850.970">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.077.280">Fanconi
                                            Anemia(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.080">Ataxia
                                            Telangiectasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.099.500">Hemophilia
                                            A(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.100">Brugada
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.019.500">DiGeorge
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.040">Angelman
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.080">Beckwith-Wiedemann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.260">Down
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.380">Holoprosencephaly()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.790">Rubinstein-Taybi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.180.870">Silver-Russell
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.190">Cystic
                                            Fibrosis(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.240.562">Cockayne
                                            Syndrome(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.240.937">Silver-Russell
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.019">Aicardi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.040">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.040.100">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.078">Aniridia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.162.410">Fuchs'
                                            Endothelial Dystrophy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.235">Duane
                                            Retraction Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.684">Retinitis
                                            Pigmentosa(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.290.684.249">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.322.030">Aicardi
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.322.061">Androgen-Insensitivity
                                            Syndrome(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.322.237">Hyper-IgM
                                            Immunodeficiency Syndrome, Type 1(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.322.500">Mental
                                            Retardation, X-Linked()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.322.500.249">Coffin-Lowry
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.322.968">X-Linked
                                            Combined Immunodeficiency Diseases(24)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.365.155">Anemia,
                                            Sickle Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.365.826">Thalassemia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.365.826.100">alpha-Thalassemia(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.365.826.150">beta-Thalassemia(66)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.365.826.575">delta-Thalassemia(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.382.625">Familial
                                            Mediterranean Fever(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.200">Cockayne
                                            Syndrome(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.375.099">Alstrom
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.375.200">Charcot-Marie-Tooth
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.375.780">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.430">Huntington
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.525">Mental
                                            Retardation, X-Linked()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.525.249">Coffin-Lowry
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.560.400">Neurofibromatosis
                                            1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.650">Pantothenate
                                            Kinase-Associated Neurodegeneration()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.780.200">Friedreich
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.820">Tourette
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.400.880">Tuberous
                                            Sclerosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.413">Hyper-IgM
                                            Immunodeficiency Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.467">Kallmann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.540">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.100.102">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.100.102.100">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.100.940.249">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.176">Amyloidosis,
                                            Familial(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.189.435.825.400">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.189.435.825.775">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.189.680.760">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.189.937.249">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.202.251.221">Fructose-1,6-Diphosphatase
                                            Deficiency(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.565.202.589">Lactose
                                            Intolerance(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.060">alpha
                                            1-Antitrypsin Deficiency()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.070.150">Anemia,
                                            Sickle Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.070.875">Thalassemia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.070.875.100">alpha-Thalassemia(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.070.875.150">beta-Thalassemia(66)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.320.070.875.575">delta-Thalassemia(13)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Infant, Newborn, Diseases">Infant,
                                    Newborn, Diseases(31)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.614.521.731">Retinopathy
                                            of Prematurity(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.614.815.500">X-Linked
                                            Combined Immunodeficiency Diseases(24)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.614.521.125">Bronchopulmonary
                                            Dysplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.614.492">Ichthyosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.614.492.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C16.614.213">Cystic
                                            Fibrosis(3)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Skin and Connective Tissue Diseases">Skin
                            and Connective Tissue Diseases(113)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Connective Tissue Diseases">Connective
                                    Tissue Diseases(19)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.200.425">Keloid(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.270">Dupuytren
                                            Contracture(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.480">Lupus
                                            Erythematosus, Systemic(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.480.680">Lupus
                                            Nephritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.500">Marfan
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.799">Scleroderma,
                                            Systemic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.766">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.775">Rheumatic
                                            Diseases(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.775.049">Arthritis,
                                            Juvenile(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.775.099">Arthritis,
                                            Rheumatoid(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.775.099.774">Sjogren's
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.300.690">Noonan
                                            Syndrome(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Skin Diseases">Skin
                                    Diseases(96)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.838.765.820.470">Lupus
                                            Vulgaris(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.838.775.560">Leishmaniasis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.838.775.560.400">Leishmaniasis,
                                            Cutaneous(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.838.790.810">Warts(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.849.391.400">HIV-Associated
                                            Lipodystrophy Syndrome(32)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.859.675">Psoriasis(9)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.859.675.175">Arthritis,
                                            Psoriatic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.862.150">Behcet
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.862.252">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.862.560">Mucocutaneous
                                            Lymph Node Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.862.945">Urticaria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.865.187">Blister(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.865.475.683">Stevens-Johnson
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.865.716">Pemphigus(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.882">Skin
                                            Neoplasms(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.946.350">Hyperhidrosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.174">Dermatitis(9)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.174.193">Dermatitis,
                                            Atopic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.174.600.587">Hand-Foot
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.174.600.900">Stevens-Johnson
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.174.620">Eczema(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.174.826">Radiodermatitis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.229">Erythema()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.229.400.683">Stevens-Johnson
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.329.875">Hypertrichosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.329.937">Hypotrichosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.329.937.122">Alopecia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.329.937.122.147">Alopecia
                                            Areata(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.428.333">Ichthyosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.428.333.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.428.435">Keratoderma,
                                            Palmoplantar()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.428.750">Porokeratosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.529.400">Nail-Patella
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.600.725">Sunburn(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.600.925">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.621.430">Hyperpigmentation()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.621.430.530">Melanosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.621.440.102">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.621.440.102.100">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.621.440.895">Vitiligo(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.621.936">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.784">Scleroderma,
                                            Systemic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.804.350">Ectodermal
                                            Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.804.512">Ichthyosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.804.512.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.804.766">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.804.936">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.815.193">Dermatitis,
                                            Atopic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.815.620">Eczema(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.080">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.080.100">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.210">Dermatitis,
                                            Atopic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.250">Ectodermal
                                            Dysplasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.475">Keratoderma,
                                            Palmoplantar()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.730">Porokeratosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.750">Pseudoxanthoma
                                            Elasticum(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.820">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.827.970">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C17.800.838.208.416.249">Aspergillosis(3)</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nutritional and Metabolic Diseases">Nutritional
                            and Metabolic Diseases(774)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Metabolic Diseases">Metabolic
                                    Diseases(414)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.174.451">Hypercalcemia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.174.451">Hypercalcemia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.174.845">Rickets(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.284">DNA
                                            Repair-Deficiency Disorders(10)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.284.060">Ataxia
                                            Telangiectasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.284.250">Cockayne
                                            Syndrome(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.284.280">Fanconi
                                            Anemia(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.284.975">Xeroderma
                                            Pigmentosum(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394">Glucose
                                            Metabolism Disorders(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.750">Diabetes
                                            Mellitus(14)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.750.124">Diabetes
                                            Mellitus, Type 1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.750.149">Diabetes
                                            Mellitus, Type 2(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.750.448">Diabetes,
                                            Gestational(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.952">Hyperglycemia(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.968.500">Insulin
                                            Resistance(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.968.500.570">Metabolic
                                            Syndrome X(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.394.984">Hypoglycemia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.753">Progeria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.798">Purine-Pyrimidine
                                            Metabolism, Inborn Errors(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.798.368">Gout(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.861.770">Pseudohypoaldosteronism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.861.885.250">Cystinuria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.660.097">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.660.195">Cytochrome-c
                                            Oxidase Deficiency(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.660.300">Friedreich
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.845.500">Amyloidosis(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.845.500.075">Amyloidosis,
                                            Familial(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.845.500.100">Cerebral
                                            Amyloid Angiopathy(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.845.800.050">Amyotrophic
                                            Lateral Sclerosis(12)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.845.800.300">Frontotemporal
                                            Lobar Degeneration(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.845.800.300.299">Frontotemporal
                                            Dementia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.880.391.400">HIV-Associated
                                            Lipodystrophy Syndrome(32)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.950">Water-Electrolyte
                                            Imbalance(13)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.950.340">Hypercalcemia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.076">Acid-Base
                                            Imbalance(129)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.132.100.435.825.400">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.132.100.435.825.775">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.132.100.680.760">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.132.100.937.249">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.398.641.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.398.641.803.441">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.398.641.803.850">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.595.554.825.400">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.595.554.825.775">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.595.577.500">alpha-Mannosidosis(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.595.577.750">beta-Mannosidosis(68)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.618.337">Hemochromatosis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.618.711.550">Hypokalemic
                                            Periodic Paralysis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.663.760">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.565.500">Iron
                                            Overload(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.565.500.480">Hemochromatosis(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584">Lipid
                                            Metabolism Disorders(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584.500.500.396">Hypercholesterolemia(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584.500.500.851">Hypertriglyceridemia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584.625.400">HIV-Associated
                                            Lipodystrophy Syndrome(32)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584.687.723">Sjogren-Larsson
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584.687.803.441">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.584.687.803.850">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.603.250">Celiac
                                            Disease(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.603.506">Lactose
                                            Intolerance(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.625">Metabolic
                                            Syndrome X(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.100.102">Albinism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.100.102.100">Albinism,
                                            Oculocutaneous()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.100.940.249">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.176">Amyloidosis,
                                            Familial(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.189.435.825.400">Gaucher
                                            Disease(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.189.435.825.775">Sea-Blue
                                            Histiocyte Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.189.680.760">Refsum
                                            Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.189.937.249">Carbamoyl-Phosphate
                                            Synthase I Deficiency Disease()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.202.251.221">Fructose-1,6-Diphosphatase
                                            Deficiency(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.202.589">Lactose
                                            Intolerance(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.202.607.500">alpha-Mannosidosis(80)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.648.202.607.750">beta-Mannosidosis(68)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.452.174.130.780">Vascular
                                            Calcification(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Nutrition Disorders">Nutrition
                                    Disorders(399)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.521.500.133.628">Vitamin
                                            A Deficiency(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.521.500.133.770">Vitamin
                                            D Deficiency(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.521.500.133.770.734">Rickets(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.726.500.700">Obesity,
                                            Morbid(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.521.750">Starvation(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.726.500">Obesity(29)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C18.654.521.500.708.626">Protein-Energy
                                            Malnutrition(364)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Immune System Diseases">Immune
                            System Diseases(1309)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Autoimmune Diseases">Autoimmune
                                    Diseases(140)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111">Autoimmune
                                            Diseases(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.193.875">Wegener
                                            Granulomatosis()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.197">Antiphospholipid
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.198">Arthritis,
                                            Juvenile(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.199">Arthritis,
                                            Rheumatoid(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.199.774">Sjogren's
                                            Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.258.124">Anti-N-Methyl-D-Aspartate
                                            Receptor Encephalitis(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.258.250.500">Multiple
                                            Sclerosis(22)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.258.500">Myasthenia
                                            Gravis(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.258.962.800">Giant
                                            Cell Arteritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.327">Diabetes
                                            Mellitus, Type 1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.525">Glomerulonephritis,
                                            IGA(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.535">Glomerulonephritis,
                                            Membranous(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.555">Graves
                                            Disease(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.567">Hepatitis,
                                            Autoimmune(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.590">Lupus
                                            Erythematosus, Systemic(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.590.560">Lupus
                                            Nephritis(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.736">Pemphigus(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.750">Polyendocrinopathies,
                                            Autoimmune(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.190">Anti-Glomerular
                                            Basement Membrane Disease(88)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.111.193">Anti-Neutrophil
                                            Cytoplasmic Antibody-Associated Vasculitis(88)</a></li>
                                </ul>
                            </li>
                            <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.188">Blood Group
                                    Incompatibility(1)</a>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Hypersensitivity">Hypersensitivity(56)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543">Hypersensitivity(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480.904">Urticaria(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480.680.795">Rhinitis,
                                            Allergic, Seasonal(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480.680.095">Asthma(45)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.206">Drug
                                            Hypersensitivity(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480.343">Dermatitis,
                                            Atopic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480.149">Asthma,
                                            Aspirin-Induced(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480">Hypersensitivity,
                                            Immediate(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.206.380.900">Stevens-Johnson
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.206.189">Asthma,
                                            Aspirin-Induced(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.543.480.356">Eosinophilic
                                            Esophagitis(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Immunologic Deficiency Syndromes">Immunologic
                                    Deficiency Syndromes(88)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.600">Leukocyte-Adhesion
                                            Deficiency Syndrome(14)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.627">Lymphopenia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.483.480">HTLV-II
                                            Infections(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.483.470">HTLV-I
                                            Infections(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.480.400">HIV-Associated
                                            Lipodystrophy Syndrome(32)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.480.100">AIDS-Related
                                            Opportunistic Infections(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.480.080">AIDS-Related
                                            Complex(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.480.050">AIDS-Associated
                                            Nephropathy(7)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.480.040">Acquired
                                            Immunodeficiency Syndrome(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.480">HIV
                                            Infections(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.430.249.500">Hyper-IgM
                                            Immunodeficiency Syndrome, Type 1(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.430.249">Hyper-IgM
                                            Immunodeficiency Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.290">Ataxia
                                            Telangiectasia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.088">Agammaglobulinemia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.673.815.500">X-Linked
                                            Combined Immunodeficiency Diseases(24)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Immunoproliferative Disorders">Immunoproliferative
                                    Disorders(1033)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.460.640">Monoclonal
                                            Gammopathy of Undetermined Significance(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.780.650">Multiple
                                            Myeloma(74)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.080">Leukemia,
                                            B-Cell(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.080.125">Leukemia,
                                            Lymphocytic, Chronic, B-Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.582">Leukemia,
                                            T-Cell(668)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.582.100">Leukemia-Lymphoma,
                                            Adult T-Cell(668)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.600">Precursor
                                            Cell Lymphoblastic Leukemia-Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.600.600">Precursor
                                            B-Cell Lymphoblastic Leukemia-Lymphoma(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528.600.620">Precursor
                                            T-Cell Lymphoblastic Leukemia-Lymphoma(24)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761">Lymphoma(271)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.355">Hodgkin
                                            Disease(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480">Lymphoma,
                                            Non-Hodgkin(264)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.100">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.150">Lymphoma,
                                            B-Cell(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.150.165">Burkitt
                                            Lymphoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.150.570">Lymphoma,
                                            B-Cell, Marginal Zone(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.350">Lymphoma,
                                            Follicular(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.487">Lymphoma,
                                            Large-Cell, Immunoblastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.750">Lymphoma,
                                            T-Cell(267)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.750.399">Lymphoma,
                                            Large-Cell, Anaplastic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.750.800">Lymphoma,
                                            T-Cell, Cutaneous(271)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.761.480.750.825">Lymphoma,
                                            T-Cell, Peripheral(271)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.845">Multiple
                                            Myeloma(74)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.880">Plasmacytoma(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.780.640">Monoclonal
                                            Gammopathy of Undetermined Significance(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C20.683.515.528">Leukemia,
                                            Lymphoid(1)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pathological Conditions, Signs and Symptoms">Pathological
                            Conditions, Signs and Symptoms(941)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pathological Conditions, Anatomical">Pathological
                                    Conditions, Anatomical(35)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.035">Alopecia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.070">Atrophy(12)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.070.500">Muscular
                                            Atrophy(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.122">Blister(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.175.525">Gallstones(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.306">Cysts(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.707">Hernia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.775">Hypertrophy(12)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.775.250">Cardiomegaly(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.775.250.400">Hypertrophy,
                                            Left Ventricular(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.842">Prolapse(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.842.624">Pelvic
                                            Organ Prolapse()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.842.624.750">Uterine
                                            Prolapse(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.300.985">Ventricular
                                            Remodeling(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pathologic Processes">Pathologic
                                    Processes(819)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.414.913.850">Subarachnoid
                                            Hemorrhage(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.891">Ulcer(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.073">Arrhythmias,
                                            Cardiac(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.073.198">Atrial
                                            Fibrillation(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.073.248">Atrial
                                            Flutter(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.073.425.100">Bundle-Branch
                                            Block(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.073.547">Long
                                            QT Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.073.845">Tachycardia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.081">Ascites(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.050">Aneuploidy(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.050.500">Monosomy()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.050.625">Tetrasomy()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.050.750">Trisomy(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.110">Chromosomal
                                            Instability(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.182.249">Tetrasomy()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.182.500">Trisomy(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.760">Ring
                                            Chromosomes(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.210.870">Translocation,
                                            Genetic(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.260">Death(29)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.260.322">Death,
                                            Sudden(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.260.322.250">Death,
                                            Sudden, Cardiac(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.260.322.400">Sudden
                                            Infant Death(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.288">Disease(317)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.288.500">Syndrome(91)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.291.656">Disease
                                            Progression(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.291.687">Disease
                                            Susceptibility()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.291.812">Facies()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.291.937">Recurrence(19)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.325">Emphysema(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.325.500.500">alpha
                                            1-Antitrypsin Deficiency()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.355">Fibrosis(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.355.274.510">Keloid(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.362.180">Chromosomal
                                            Instability(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.362.590">Microsatellite
                                            Instability(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.369">Gliosis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.393">Growth
                                            Disorders(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.393.450">Fetal
                                            Growth Retardation(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.414">Hemorrhage(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.414.913.100">Cerebral
                                            Hemorrhage(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.444">Hyperplasia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.470">Inflammation(8)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.470.099">Acute-Phase
                                            Reaction(208)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.470.251">Foreign-Body
                                            Reaction(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.470.790">Systemic
                                            Inflammatory Response Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.470.790.500">Sepsis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.470.790.500.100">Bacteremia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.505.700">Malignant
                                            Hyperthermia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.513">Ischemia(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.513.355">Infarction(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.695">Muscle
                                            Weakness()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.717">Necrosis(9)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.717.489">Infarction(13)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.717.732">Osteonecrosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.717.732.183">Bisphosphonate-Associated
                                            Osteonecrosis of the Jaw(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.727.098">Carcinogenesis(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.767.115">Coronary-Subclavian
                                            Steal Syndrome(46)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.767.600">Malignant
                                            Hyperthermia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.823">Sclerosis(42)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.835">Shock(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.835.900">Systemic
                                            Inflammatory Response Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.550.429">Hyperbilirubinemia(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Signs and Symptoms">Signs
                                    and Symptoms(111)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.742">Seizures(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.763.393.341">Hearing
                                            Loss(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.763.393.341.186">Deafness(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.763.393.341.887">Hearing
                                            Loss, Sensorineural(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.763.393.341.887.460">Hearing
                                            Loss, Noise-Induced(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.796">Sleep
                                            Disorders(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.958">Vertigo()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.646">Pain(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.646.215.500.074">Acute
                                            Coronary Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.646.487">Headache(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.821.108">Anorexia(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.821.150">Constipation(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.821.214">Diarrhea(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.821.236">Dyspepsia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.821.645.500">Bulimia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.852.130">Apnea(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.852.293">Cough(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.852.889">Sneezing(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.942.337">Hypercalciuria()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.942.750.269">Albuminuria(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.119.344">Fever(5)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144">Body
                                            Weight(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144.186">Birth
                                            Weight(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144.243">Body
                                            Weight Changes(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144.243.926">Weight
                                            Gain(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144.243.963">Weight
                                            Loss(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144.699.500">Obesity(29)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.144.699.500.500">Obesity,
                                            Morbid(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.277">Edema(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.378">Feminization(6)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.350.090">Ataxia()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.350.090.200">Cerebellar
                                            Ataxia()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.350.300">Dystonia(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.350.300.800">Torticollis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.350.850">Tremor(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.604">Neurobehavioral
                                            Manifestations(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.604.150.500.300">Dyslexia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.604.150.500.800.750">Stuttering()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.604.150.550.200">Dyslexia(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.604.646">Intellectual
                                            Disability(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.604.764.300">Hallucinations(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.608.593">Muscle
                                            Weakness()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.608.612">Muscular
                                            Atrophy(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.608.750">Spasm(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.612">Pain(7)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.612.441">Headache(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.636">Paralysis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.636.447.690">Supranuclear
                                            Palsy, Progressive(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.636.637">Paraplegia(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.636.637.300">Brown-Sequard
                                            Syndrome(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.643">Paresis()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C23.888.592.643.500">Paraparesis(1)</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <!--<li>
		Disorders of Environmental Origin
		</li>-->
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Animal Diseases">Animal
                            Diseases(30)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Bird Diseases">Bird
                                    Diseases(30)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C22.131.630">Newcastle
                                            Disease(30)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Endocrine System Diseases">Endocrine
                            System Diseases(92)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Adrenal Gland Diseases">Adrenal
                                    Gland Diseases(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.053.347.500.750">Adrenocortical
                                            Carcinoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.053.098.265.750">Adrenocortical
                                            Carcinoma(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.053.800.604">Hyperaldosteronism()</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Diabetes Mellitus">Diabetes
                                    Mellitus(21)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246.099.875">Diabetic
                                            Nephropathies(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246.099">Diabetes
                                            Complications(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246">Diabetes
                                            Mellitus(14)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246.200">Diabetes,
                                            Gestational(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246.267">Diabetes
                                            Mellitus, Type 1(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246.300">Diabetes
                                            Mellitus, Type 2(4)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.246.099.500.382">Diabetic
                                            Retinopathy(3)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Endocrine Gland Neoplasms">Endocrine
                                    Gland Neoplasms(15)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.762.500">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.762">Testicular
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.609.292">Growth
                                            Hormone-Secreting Pituitary Adenoma(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.609.145">ACTH-Secreting
                                            Pituitary Adenoma()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.421.249.500">Insulinoma()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.421">Pancreatic
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.410.648">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.410">Ovarian
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.400">Multiple
                                            Endocrine Neoplasia(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.894">Thyroid
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.344.078.265.750">Adrenocortical
                                            Carcinoma(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Gonadal Disorders">Gonadal
                                    Disorders(44)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.119.096.750">Kallmann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.119.096.500">Androgen-Insensitivity
                                            Syndrome(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.119.064.500">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.119.129.750">Hyperandrogenism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.829.782.500">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.829.782">Testicular
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.829.258">Cryptorchidism(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.693">Puberty,
                                            Precocious(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.690">Puberty,
                                            Delayed(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.630.750">Primary
                                            Ovarian Insufficiency(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.630.705.648">Sertoli-Leydig
                                            Cell Tumor(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.630.705">Ovarian
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.630.580.765">Polycystic
                                            Ovary Syndrome(8)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.482.600">Kallmann
                                            Syndrome()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.482">Hypogonadism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.391.119.309">Gonadal
                                            Dysgenesis()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Parathyroid Diseases">Parathyroid
                                    Diseases(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.642.355">Hyperparathyroidism(2)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.642.482">Hypoparathyroidism()</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.642.482.500.500">DiGeorge
                                            Syndrome()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pituitary Diseases">Pituitary
                                    Diseases(7)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.700.734.292">Growth
                                            Hormone-Secreting Pituitary Adenoma(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.700.159">Diabetes
                                            Insipidus(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.700.734.145">ACTH-Secreting
                                            Pituitary Adenoma()</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Polyendocrinopathies, Autoimmune">Polyendocrinopathies,
                                    Autoimmune(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.787">Polyendocrinopathies,
                                            Autoimmune(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Thyroid Diseases">Thyroid
                                    Diseases(13)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.874.871">Thyroiditis(3)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.874.482">Hypothyroidism(4)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.874.788">Thyroid
                                            Neoplasms(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.874.397.370">Graves
                                            Disease(5)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.874.283">Goiter(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C19.874.283.605">Graves
                                            Disease(5)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Occupational Diseases">Occupational
                            Diseases(3)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Hand-Arm Vibration Syndrome">Hand-Arm
                                    Vibration Syndrome(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C24.400">Hand-Arm
                                            Vibration Syndrome(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Pneumoconiosis">Pneumoconiosis(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C24.800.834">Silicosis(1)</a>
                                    </li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C24.800.127">Asbestosis(1)</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Chemically-Induced Disorders">Chemically-Induced
                            Disorders(135)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25">Chemically-Induced
                                    Disorders(1)</a>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Drug-Related Side Effects and Adverse Reactions">Drug-Related
                                    Side Effects and Adverse Reactions(59)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.100.468">Drug
                                            Hypersensitivity(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.100.468.189">Asthma,
                                            Aspirin-Induced(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.100.468.380.587">Hand-Foot
                                            Syndrome(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.100.468.380.900">Stevens-Johnson
                                            Syndrome(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.100.562">Drug-Induced
                                            Liver Injury(48)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.100.562.200">Drug-Induced
                                            Liver Injury, Chronic(52)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Poisoning">Poisoning(82)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.723.260.200">Drug-Induced
                                            Liver Injury, Chronic(52)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.723.260">Drug-Induced
                                            Liver Injury(48)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.723.705.150">Alcohol-Induced
                                            Disorders, Nervous System(30)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Substance-Related Disorders">Substance-Related
                                    Disorders(77)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775">Substance-Related
                                            Disorders(36)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.100">Alcohol-Related
                                            Disorders(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.100.087">Alcohol-Induced
                                            Disorders(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.100.087.193">Alcohol-Induced
                                            Disorders, Nervous System(30)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.912">Tobacco
                                            Use Disorder(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.225">Amphetamine-Related
                                            Disorders()</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.300">Cocaine-Related
                                            Disorders(6)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.635">Marijuana
                                            Abuse(1)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.675">Opioid-Related
                                            Disorders(2)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C25.775.100.250">Alcoholism(7)</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class=" collapsibleListClosed">
                        <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Wounds and Injuries">Wounds
                            and Injuries(123)</a>
                        <ul class=" collapsibleList" style="display: none;">
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Burns">Burns(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.200.855">Sunburn(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Craniocerebral Trauma">Craniocerebral
                                    Trauma(100)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.260.118.150.500">Post-Concussion
                                            Syndrome(100)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Foreign Bodies">Foreign
                                    Bodies(3)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.392.500">Foreign-Body
                                            Migration(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.392.560">Foreign-Body
                                            Reaction(3)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Fractures, Bone">Fractures,
                                    Bone(4)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.404.505">Intra-Articular
                                            Fractures(3)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.404.545">Osteoporotic
                                            Fractures(1)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Radiation Injuries">Radiation
                                    Injuries(1)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.733.804">Radiodermatitis(1)</a>
                                    </li>
                                </ul>
                            </li>
                            <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.761">Rupture(1)</a>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Thoracic Injuries">Thoracic
                                    Injuries(2)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.891.554">Lung
                                            Injury(2)</a></li>
                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Trauma, Nervous System">Trauma,
                                    Nervous System(111)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.915.200.200.550">Carotid-Cavernous
                                            Sinus Fistula(11)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.915.300.200.150.500">Post-Concussion
                                            Syndrome(100)</a></li>

                                </ul>
                            </li>
                            <li class=" collapsibleListClosed">
                                <a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_supertree/Wounds, Nonpenetrating">Wounds,
                                    Nonpenetrating(100)</a>
                                <ul class=" collapsibleList collapsibleList" style="display: none;">
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.974.150.500">Post-Concussion
                                            Syndrome(100)</a></li>
                                    <li class=""><a href="http://discovery.informatics.uab.edu/PAGER/index.php/browse/gs_by_tree/C26.974.382.200.500">Post-Concussion
                                            Syndrome(100)</a></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>

        </div>
"""


service = Service('/Users/qi/Downloads/msedgedriver')
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(service=service,options=options)

driver.get("http://www.google.com") 
driver.execute_script("window.open('');")

# Parse the HTML content
soup = BeautifulSoup(mesh_html_content, 'html.parser')

# Start parsing from the top-level <ul>
hierarchy = parse_list(soup.ul)
hierarchy.make_tree_directory(".", driver)

driver.quit()


print(hierarchy)

