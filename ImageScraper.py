from bs4 import BeautifulSoup as bs
import requests as rq
import os.path
from os import path

if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("url", nargs='+', help = "Enter url to scrape images.")

    args = p.parse_args()

    preurl = args.url[0].lstrip("['\"")
    url = preurl.rstrip("\"']")

    print("Getting Page Url: " + url)
    try:
        resp = rq.get(url)
    except:
        print("Failed to get Page Url: " + url)
    print(resp.status_code)
    soup = bs(resp.content, features="html.parser")

    tb = soup.find_all("table", attrs={"id":"QueryResults"})[0]

    imgpgs = tb.find_all("a", attrs={"target":"_blank"})


    searchPreFix = "https://eol.jsc.nasa.gov/SearchPhotos/"

    imgpgs = [searchPreFix + a.attrs['href'] for a in imgpgs]


    for a in imgpgs:
        # imgpg = searchPreFix + a.attrs['href'] REPEATED LINE (LN26)
        try:
            resp = rq.get(a)
        except:
            print("Unable to get link: {}".format(a))
        if(resp.status_code == 200):
            soup = bs(resp.content, features="html.parser")
            #Getting the image id from the webpage
            imgid_div = soup.find_all("div", attrs={'class':'top_header'})[0]
            img_id = imgid_div.contents[0]
            imgtitle = img_id + '.jpeg'
            if(path.exists(imgtitle)):
                continue

            #Getting the nadir points from the webpage (NOT NEEDED FOR IMAGE CLASSIFICATION)
            # nadir_div = soup.find_all("div", attrs={'class':'span5'})[0]
            # nadir_points = nadir_div.contents[2]
            #Getting the download link from the webpage
            imglink_a = soup.find_all("a", attrs={'class':'DownloadLink'})
            imgurlprefix = "https://eol.jsc.nasa.gov"
            imglink = [imgurlprefix + l.attrs['href'] for l in imglink_a][0]
            try:
                imgresp = rq.get(imglink)
            except:
                print("Unable to get image: {}".format(imglink))

            if(imgresp.status_code == 200):
                print("Success!")
                # nadir_points_edit = nadir_points.lstrip("['")
                # nadir_points_new = nadir_points_edit.rstrip("']")
                #
                # nadir = nadir_points_new.encode('ascii', 'ignore')
                # nadir_old = nadir.replace(", ", "_")
                # nadir_final = nadir_old.replace(" ", "")

                # imgtitle = img_id + '_' + nadir_final + '.jpeg'
                with open(imgtitle, 'wb') as f:
                    f.write(imgresp.content)
            else:
                print("Failed. Status Code: " + str(imgresp.status_code))


        else:
            print("Status Code: " + str(resp.status_code))
