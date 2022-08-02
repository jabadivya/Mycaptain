import requests
from bs4 import Beautifulsoup
import pandas
import argparse
import connect

parser = argparse.Argumentparser()
parser.add_argument("--page_num_max" , help="Enter the number of pages to parse", type=int)
parse.add_argument("--dbname", help="Enter the name of db, type=str)
arg = parse.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = args.page_num_max
scrapped_info_list = []
connect.connect(args.dbname)
                   
for page_num in range(1, page_num_max):
    url = oyo_url + str(page_num)
    print("GET request for: " + url)
    req = requests.get(url)
    content = req.content
    
    soup = Beautifulsoup(content,"html.parser")
    all_hotels = soup.find_all("div", {"class": "hotelcardListing"})
                   
    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] =hotel.find("h3",{"class": "listingHotelDescription_hotelname"}).text
        hotel_dict["addresss"] = hotel.find("span", {"itemprop" : "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class": "listingPrice_finalprice"}).text
                   
        # try ... except
        try:
           hotel_dict["rating"] = hotel.find("span",{"class": "hotelRating__ratingSummary"}).text
        except attributeError:
           hotel_dict["rating"] = None
                   
        parent_amenities_element = hotel.find("div",{"class":"amenityWrapper"})
                   
                   
        amentities_list = []
        for amenity in parent_amenities_element.find_all("div", {"class","amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())
                   
        hotel_dict["amenities"] = ','.join(amenities_list[:-1])
                   
        scraped_info_list.append(hotel_dict)
        connect.insert_into_table(args.dbname, tuple(hotel_dict.values()))
                   
         # print(hotel_names, hotel_address, hotel_price, hotel_rating, amenities_list)
                   
dataFrame = pandas.dataFame(scraped_info_list)
print("creating csv file..")
dataFame.to_csv("Oyo.csv")
