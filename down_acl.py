import requests
from bs4 import BeautifulSoup
import os


def download_paper(folder, name, url):
    
    download_dir = os.path.join(folder , name)
    r = requests.get(url, stream=True)
    with open(download_dir, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return download_dir

def get_url(folder):
    root_link = "https://aclanthology.info/events/acl-2018"
    root = "http://aclweb.org/anthology/"
    headers = {
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    }

    r = requests.get(root_link, headers = headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html5lib")
        print("\n=============== {0:10} ===============\n".format('Start Downloading'))
        for paper in soup.find_all("p"):
            url = None
            name = None
            anchor = paper.find_all("a")
            strong = paper.find_all("strong")
            if strong:
                name = strong[0].string
            for a in anchor:
                if a["href"].startswith(root):
                    url = a["href"]
                    paper_num = url.split("-")[-1]
            if strong and url:
                download_paper(folder, paper_num + "_" + name + ".pdf", url)
                print("current downloading paper ==> {}".format(name))



if __name__ == "__main__":
    folder = "ACL2018"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    
    get_url(folder)