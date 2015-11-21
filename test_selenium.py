from selenium import webdriver
import time

#auxiliary functions
def read_saved_track_names(track_file):
    tracks = set()
    with open(track_file) as f:
        for line in f:
            line2 = line.strip()
            tracks.add(line2)
    return tracks

def save_garmin_tracks(activity_links, track_file, mode):
    with open(track_file, mode) as myfile:
        for link in activity_links:
            link = link.strip()
            print(link)
            myfile.write(link+'\n')


def extract_activity_links(browser, new_links, activity_links):
    activities_el = browser.find_element_by_id('gridForm:gridList:tb')
    for anchor in activities_el.find_elements_by_tag_name('a'):
        activity_link = anchor.get_attribute("href")
        if not activity_link is None:
            if '/activity/' in activity_link:
                activity_links.add(activity_link)
                new_links.add(activity_link)


def move_to_next_page(browser):
    footer_el = browser.find_element_by_class_name('resultsFooter')
    btn_found = False
    for btn in footer_el.find_elements_by_class_name('rich-datascr-button'):
        if btn.text == '»':
            btn_found = True
            btn.click()
            break
    return btn_found


def select_start_date(browser, n_years):
    #move one year back..
    for i in range(1, n_years):
        calendar1 = browser.find_element_by_id('exploreSearchForm:startDateCalendarPopupButton')
        calendar1.click()
        time.sleep(1)
        calendar_button = browser.find_element_by_class_name('rich-calendar-tool-btn')
        calendar_button.click()
        time.sleep(1)
        #choose date..
        date_button = browser.find_element_by_id('exploreSearchForm:startDateCalendarDayCell7')
        date_button.click()
        time.sleep(2)

################################################
# saves the GARMIN activity links for selected
# CITY and the number of the past years
################################################
def save_garmin_activity_links(city, n_years, track_file):

    activity_links = read_saved_track_names(track_file)
    new_links = set()
    browser = webdriver.Firefox()
    url = "https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2FminExplore&webhost=olaxpw-connect00&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false"
    browser.get(url)
    time.sleep(10)
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    username.send_keys("jirikadlec2@gmail.com")
    password.send_keys("AnnAgnps(v1)")
    login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
    login_attempt.submit()

    #now show filters..
    time.sleep(10)
    show_filters = browser.find_element_by_id("showFilters")
    show_filters.click()

    #select the activity type option
    el = browser.find_element_by_id('exploreSearchForm:activityType')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Cross Country Skiing':
            option.click()
            break

    #select the time period option
    time.sleep(2)
    time_el = browser.find_element_by_id('exploreSearchForm:timePeriodSelect')
    for option in time_el.find_elements_by_tag_name('option'):
        if option.text == 'Custom Dates':
            option.click()
            break

    #select the start date (10 years back..)
    select_start_date(browser, n_years)

    #select the end date (start of current month..)
    time.sleep(2)
    calendar2 = browser.find_element_by_id('exploreSearchForm:endDateCalendarPopupButton')
    calendar2.click()
    date_button = browser.find_element_by_id('exploreSearchForm:endDateCalendarDayCell7')
    date_button.click()

    #now search a new location ..
    time.sleep(5)
    location = browser.find_element_by_id("exploreSearchForm:location")
    location.send_keys(city)

    searchButton = browser.find_element_by_id("searchButton")
    searchButton.submit()

    time.sleep(5)

    #find the grid list
    next_active = True
    while next_active:
        time.sleep(10)
        len1 = len(new_links)
        extract_activity_links(browser, new_links, activity_links)
        len2 = len(new_links)
        next_active = len2 > len1
        time.sleep(2)
        move_to_next_page(browser)

    save_garmin_tracks(activity_links, track_file, "w")
    browser.close()


f = "garmin_tracks.txt"
trk = read_saved_track_names(f)
save_garmin_tracks(trk, f, "w")
trk = []

#save_garmin_activity_links('Brno', 10, f)
#save_garmin_activity_links('Karlovy Vary', 10, f)
#save_garmin_activity_links('Chomutov', 10, f)
#save_garmin_activity_links('Kvilda', 10, f)
#save_garmin_activity_links('Klingenthal', 10, f)
#save_garmin_activity_links('Jablunkov', 10, f)
#save_garmin_activity_links('Svratka', 10, f)
#save_garmin_activity_links('Jilemnice', 10, f)
#save_garmin_activity_links('Trutnov', 10, f)
#save_garmin_activity_links('Mladkov', 10, f)
#save_garmin_activity_links('Mikulovice', 10, f)
#save_garmin_activity_links('Olomouc', 10, f)
#save_garmin_activity_links('Protivanov', 10, f)
#save_garmin_activity_links('Karolinka', 10, f)
#save_garmin_activity_links('Jihlava', 10, f)
#save_garmin_activity_links('Kocelovice', 10, f)
#save_garmin_activity_links('Altenberg', 10, f)
save_garmin_activity_links('Oberwiesenthal', 10, f)
save_garmin_activity_links('Zittau', 10, f)
save_garmin_activity_links('Heroltovice', 10, f)
save_garmin_activity_links('Rokytno', 10, f)