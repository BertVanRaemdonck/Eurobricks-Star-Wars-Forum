## Purpose:
##    To generate the Star Wars Pictures and Rumors' first post containing the sets programatically.
##
## Method:
##    Starting from a given year, Brickset is consulted to get a list of the sets that come out. Every found set
##    is listed with name, number and category. With those data, URL's for LEGO Shop at Home are generated. The
##    corresponding webpages are searched for additional information as description, prices across different
##    countries, piece count and minifigures included. Finally, also Brickipedia URL's are generated, where
##    resized images of the sets are extracted from. All found information is put out as a string that can be
##    pasted in the first post. This does not include the images and the sources. The resized images are saved
##    on the computer, and a temporary source is included.
##
## Input:
##    When the program is started, it will ask for the following values:
##        Period in which the sets come out: e.g. January 2015
##        Range of accepted set numbers: e.g. range(30272,30275) + range(75072,75091)
##        Path on the computer to where the images will be saved: e.g. C:\Users\Luke\Downloads
##
##Output:
##    Code that can be copy-pasted to the Eurobricks post appears in the terminal. It already contains all
##    layout. Everything apart from the images and the sources are included. The images are donwloaded on to
##    the computer, but still have to be hosted (preferably in the Eurobricks member gallery). They can be
##    included in the post in the regular way. The sources also have to be added manually.     


import urllib
import re
import os

class LEGO_set:
    # A class representing a LEGO set, with all the relevant information for the index
    
    def __init__(self, number, name, category):
        # Sets a default value for all properties of the set
        self.number = str(number)
        self.name = str(name)
        self.category = str(category)
        self.release = release
        self.description = ""
        self.image = ""
        self.prices = ""
        self.piece_amount = ""
        self.minifigs = ""

        converted_name = name.replace(" ", "-").replace("'", "-")
        self.lego_url = "http://shop.lego.com/en-US/" + converted_name + "-" + str(number)

    def get_data(self):
        # Assigns values to the properties using the destined functions
        page_data = open_pages(self.lego_url)

        self.description = get_description(page_data)
        self.image = get_image(self.number, self.name)
        self.prices = get_prices(page_data, self.lego_url)
        self.piece_amount = get_piece_amount(page_data)
        self.minifigs = get_minifigs(page_data)

    def print_data(self):
        # Outputs the actual string that will be pasted in the post
        output_string = "[newline][newline] [size=5][b]" + self.number + " " + self.name + "[/b][/size]" + \
                        "[newline][hr] Subtheme: " + self.category + \
                        "[newline]Release: " + self.release + \
                        "[newline][newline]" + self.description + \
                        "[newline][newline]" + "INSERT IMAGE" + \
                        "[newline][newline]" + self.prices + \
                        "[newline]" + self.piece_amount + \
                        "[newline]" + self.minifigs + \
                        "[newline]Source(s): [url=" + self.lego_url + "]LEGO[/url]" + "         INCOMPLETE!!!"\
                        "[newline][newline][newline] [center]" + \
                        "[img]http://eurobricksstarwarsforum.files.wordpress.com/2013/06/blogicon.png[/img] "*3 +\
                        "[/center]"

        return output_string

        
def open_pages(url):
    # Loads the HTML code of the webpage into the variable page_code
    page = urllib.urlopen(url)
    page_code = ""
    part = True
    while part:
        part = page.read()
        page_code += part
    page.close()
    return page_code


# ------------------------------------------------
# Gets set numbers, themes and names from Brickset
# ------------------------------------------------


def get_sets(year, set_numbers):
    # Visits Brickset for a list of sets in the given year.
    categories = ["Episode-I", "Episode-II", "Episode-III", "Episode-IV-VI", "Expanded-Universe",\
                  "MicroFighters", "Mini-Building-Set", "Rebels", "Seasonal", "The-Clone-Wars",\
                  "Ultimate-Collector-Series", "None"]
    category_tag = ["Prequel Trilogy", "Prequel Trilogy", "Prequel Trilogy", "Original Trilogy",
                    "Expanded Universe", "Microfighters", "Polybag set", "Rebels", "Seasonal",
                    "The Clone Wars", "???????", "Polybag set"]

    brickset_main_url = "http://brickset.com/sets/theme-Star-Wars/category-Normal/year-" +\
                        str(year) + "/subtheme-"

    sets = []
    for i in range(len(categories)):
        # Goes through every category and checks whether there are sets that fall under the given constraints
        cat_url = brickset_main_url + categories[i]
        main_page_code = open_pages(cat_url)

        set_pages = re.findall(r'(<div\sclass=\'meta\'>)((.|\n)*?)(</a>)', str(main_page_code))
        
        for set_entry in set_pages:
            # If sets are found, the function creates a LEGO_set object with the found name, number and category
            set_number = re.findall(r'(<span>)(\d*)', set_entry[1])[0][1]
            set_name = re.findall(r'(</span>\s)(.*)', set_entry[1])[0][1]

            if eval(set_number) in set_numbers:
                sets.append(LEGO_set(set_number, set_name, category_tag[i]))

    return sets



# ----------------------------------------------------
# Gets data about every set from the LEGO Shop at Home
# ----------------------------------------------------


def get_description(page_code):
    # Extracts the description of the set
    try:
        description = re.findall(r'<p>(\w|\d)(.*?)</p>', str(re.findall(\
            r'<div\sid="tab-content-product-summary"((.|\n)*?)</div>', str(page_code))))    
        description = "Official description: [i]" +  description[0][0] + description[0][1] + "[/i]"
        description = description.replace("\\xc2\\xae", "\xae")         # makes (R) symbol readable
        description = description.replace("\\xe2\\x84\\xa2", "\x99")    # makes TM symbol readable
        description = description.replace("\\xe2\\x80\\x99", "'")       # makes apostrophes readable
        description = description.replace("\\xe2\\x80\\xa6", "\x85")    # makes ellipsis readable
        description = description.replace("<i>", "[i]")                 # transfers HTML to BBCode italics
        description = description.replace("</i>", "[/i]")               # transfers HTML to BBCode italics
        description = description.replace("<em>", "[i]")                # transfers HTML to BBCode italics
        description = description.replace("</em>", "[/i]")              # transfers HTML to BBCode italics

    except Exception:
        description = "Official description: [i]?[/i]"

    return description


def get_piece_amount(page_code):
    # Extracts the amount of pieces in the set
    try:
        return "Pieces: [b]" + re.findall(r'\d+', str(re.findall(r'Pieces(.*?)</em>', str(page_code))))[0]\
               + "[/b]"
    except Exception:
        return "Pieces: [b]?[/b]"


def get_minifigs(page_code):
    # Extracts the information about the minifigures
    try:
        minif_descr = re.findall(r'<li>((.|\n)*?)</li>', str(re.findall(\
            r'<div\sid="tab-content-product-summary"((.|\n)*?)</div>', str(page_code))))[0][0]
        minif_descr = str(minif_descr) + "\\"
        
        try:
            minif_descr = re.findall(r':\s(.*?)\\', str(minif_descr))[0]
        except Exception:
            minif_descr = minif_descr[9:-1]

        # These are the words that have to be removed, we want just the names
        minif_descr = " " + minif_descr
        words_to_delete = ["minifigures", "minifigure", "figures", "figure", " A "]
        for word in words_to_delete:
            minif_descr = minif_descr.replace(word, "")

        # Splits the sentence describing the minifigs in parts    
        minif_descr = re.split(r'( and | a |,| an | with )', minif_descr)

        # Goes through all the words in the previously generated list
        word = 0
        while word < len(minif_descr):
            i = 0
            amount = ""
            # checks whether an entry in the list is a minifigure by looking at the first character of the
            # entry to be a capital letter (and it remembers the numbers it meets along the way).
            while i < len(minif_descr[word]) and not minif_descr[word][i] in set(chr(x) for x in range(65,91)):
                if  minif_descr[word][i] in set(chr(x) for x in range(49,58)):
                    amount += minif_descr[word][i]
                i += 1
                    
            if (i >= len(minif_descr[word])):
                # when there was no capital letter found
                del minif_descr[word]
            else:
                # when we're dealing with a minifigure
                # to get rid of the initial spaces
                minif_descr[word] = minif_descr[word][i:]

                # to get rid of the spaces in the end
                j = -1
                while abs(j) < len(minif_descr[word])-1 and minif_descr[word][j] == " ":
                    j -= 1
                if j < -1:
                    minif_descr[word] = minif_descr[word][:j+1]

                # ends an "s" if there are multiple minifigs of the sort. This "s" might have gone lost
                # because we're deleting the word "figures" etc. Also puts the amoutn in the correct format
                if len(amount) > 0:
                    if minif_descr[word][-1] != "s":
                        minif_descr[word] += "s"
                    minif_descr[word] = minif_descr[word] + " (" + amount + ")"
                        
                word += 1

        # Constructs the eventual string from the list with minifigures
        minifigs = "[b]"
        for m in range(len(minif_descr)):
            minifigs += minif_descr[m]
            if m == len(minif_descr) - 2:
                minifigs += " and "
            elif m != len(minif_descr) - 1:
                minifigs += ", "
        minifigs += "[/b]"

    except Exception:
        minifigs = "[b]none[/b]"

    return "Minifigs: " + minifigs


def get_prices(page_code, url):
    # Extracts the prices for various countries, as listed in the "countries" variable
    # Not to be used in sales periods
    countries = ["en-US", "en-CA", "en-DK", "en-DE", "en-GB"]
    price_pref = ["$ ", "$ ", "", "€ ", "£ "]
    price_suff = [" USD", " CDN", " DKK", " EUR", " GBP"]
    prices_list = []

    try:
        # Visits the web page for each country where we want to know the price
        for country in range(len(countries)):
            page_code = open_pages(url[:21] + countries[country] + url[26:])
            
            price = re.findall(r'(\d*)(\.|,)(\d*)',\
                               str(re.findall(r'<span\sclass="product-price((.|\n)*?)</span>', \
                                              str(page_code))))[0]
            price_str = ""
            for el in price:
                price_str += el
            
            prices_list.append(price_pref[country] + price_str + price_suff[country])

        prices = "Price: [b]"
        for i in range(len(prices_list)):
            prices += prices_list[i]
            if i < len(prices_list)-1:
                prices += ", "
        prices += "[/b]"

    except Exception:
        prices = "Price: [b]?[/b]"

    return prices

def get_image(set_number, set_name):
    # Searches the image on Brickipedia and saves a resized picture to the earlier specified path.
    # Brickipedia was chosen because images can be resized via URL name only.
    set_name = set_name.replace(" ", "_")
    set_name = set_name.replace("'", "%27")
    brickipedia_url = "http://lego.wikia.com/wiki/" + str(set_number) + "_" + set_name

    try:
        brickipedia_code = open_pages(brickipedia_url)

        image_str = re.findall(r'(<tr\sstyle="text-align:center;)((.|\n)*?)(</tr>)', brickipedia_code)
        image_str = re.findall(r'(<noscript>)((.|\n)*?)(</noscript>)', image_str[0][1])
        image_str = re.findall(r'(img\ssrc=")(.*?)(")', image_str[0][1])[0][1]
        image_url = re.sub(r'(scale-to-width/)(\d*?)(\?)', "scale-to-width/500?", image_str)

        urllib.urlretrieve(image_url, set_number + "_" + set_name + ".png")

    except Exception:
        image_url = "None"
    
    return image_url
    

# ---------------------------------------------------------------
# Determines when the previously defined functions will be called
# ---------------------------------------------------------------

## Example values:
##      release = January 2015
##      set_numbers = range(30272,30276) + range(75072,75091) + [5002938,5002947]
##      output_path = C:\Users\Bert\Downloads

valid_year = False
release = raw_input("Year in which the sets come out: ") # Just the number representing the year.
                                                      # No quotation marks please



                                                      
year = re.findall(r'\s(\d*?)\s', " " + release + " ")
for entry in year:
    if len(entry) == 4:
        year = entry
        valid_year = True
        
while valid_year == False: # Keeps cycling to get a valid input

    
    release = raw_input("Year in which the sets come out: ") # Just the number representing the year.
                                                      # No quotation marks please



                                                      
    year = re.findall(r'\s(\d*?)\s', " " + release + " ")
    for entry in year:
        if len(entry) == 4:
            year = entry
            valid_year = True
            
accepted_nbs = input("Range of accepted set numbers: ") # A list/set with the allowed numbers. Examples:
                    # [75072, 75083, 75120]  or  (75072, 75083, 75120)  or  {75072, 75083, 75120}
                    # However, it is tedious to write a long list, so you can also say "Between value a and b",
                    # like this:
                    #   range(30272,30275)         , this is equivalent to: [30272,30273,30274].
                    # So ATTENTION!!! The second argument will not be included in the list, so add 1 to the
                    #   highest number you want to include.
                    # To make a union of several ranges, just add them together, for instance:
                    #   range(30272,30275) + range(75072,75091)     , represents all sets 30272 to
                    #   (and including) 30274, and all sets 75072 to (and including) 75090.
output_path = raw_input("Path to where the images will be saved: ") # The path to which the images will be saved.
                    # For example: C:\Users\USERNAME\Downloads   on a Windows computer.
                    # No quotation marks please

os.chdir(output_path)

print
print "Finding sets to process..."



    
sets = get_sets(year, accepted_nbs)

# Gets the sets in the right order: first all regular sets with increasing number, then all polybag sets with
# increasing number
sets = sorted(sets, key= lambda SW_set: SW_set.number)
poly_sets = []
regular_sets = []
for SW_set in sets:
    if SW_set.category == "Polybag set":
        poly_sets.append(SW_set)
    else:
        regular_sets.append(SW_set)
sets = regular_sets + poly_sets
        

output = ""

for i in range(len(sets)):
    SW_set = sets[i]
    print "Processing", i+1, "out of", len(sets), ":     ", SW_set.name
    SW_set.get_data()
    output += SW_set.print_data()

print
print
print
print
print
print output
print
print
print
print "Images saved to" , output_path
print "ATTENTION !  Quality of the images may vary. Check before uploading them."






