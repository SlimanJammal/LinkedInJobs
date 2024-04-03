from time import sleep
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_to_bottom(driver, wait):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroller__show-more-button")))


# Function to click the "See more jobs" button
def click_see_more_button(driver):
    see_more_button = driver.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button")
    see_more_button.click()


def scroll_slightly_up(driver):
    driver.execute_script("window.scrollBy(0, -window.innerHeight / 2);")


def reload_page_if_needed(driver, original_url):
    current_url = driver.current_url
    if current_url != original_url:
        driver.quit()
        driver = webdriver.Chrome()
        driver.get(original_url)
        print("Reloading page...")
        driver.get(original_url)

    return current_url == original_url, driver


def find_job_id(driver):
    job_posting_number = 0
    element = driver.find_element(By.CLASS_NAME, "semaphore__toggle")

    # Extract the href attribute containing the URL
    href = element.get_attribute("href")

    # Split the URL by delimiter separating jobPosting and the number
    parts = href.split("jobPosting:")

    # Check if the split resulted in more than one part
    if len(parts) > 1:
        # Extract the number (assuming it's the second part)
        job_posting_number = parts[1]
        print(job_posting_number)
    else:
        print("Number not found in the URL")

    return job_posting_number


def no_login_scraper(job_title, location, reload_threshold=4, scroll_threshold=20):
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome()

    original_url = f"https://il.linkedin.com/jobs/{job_title}-jobs-{location}?trk=homepage-jobseeker_suggested-search&position=1&pageNum=0"
    driver.get(original_url)
    sleep(5)
    wait = WebDriverWait(driver, 10)

    reload_threshold = reload_threshold
    while True:
        status, driver = reload_page_if_needed(driver, original_url)
        if status:
            break
        if reload_threshold == 0:
            exit()
        else:
            reload_threshold -= 1

    driver.maximize_window()
    scroll_threshold = scroll_threshold
    while True:
        try:
            scroll_to_bottom(driver, wait)
            click_see_more_button(driver)
        except:
            if scroll_threshold == 0:
                break
            delay = random.uniform(2, 3)
            scroll_slightly_up(driver)
            time.sleep(delay + 1)
            scroll_threshold -= 1
            # try:
            #     if driver.find_element(By.CLASS_NAME,"inline-notification__text"):
            #         print("You've viewed all jobs for")
            #         break

            # except:

    parent_ul = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")

    job_cards = parent_ul.find_elements(By.CLASS_NAME, "base-card")

    jobs_data = []

    for i, job_card in enumerate(job_cards):
        if i == 2:
            break #todo remove. for testing only !!!!!

        job_title = job_card.find_element(By.CLASS_NAME, "base-search-card__title").text
        company_name = job_card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
        location = job_card.find_element(By.CLASS_NAME, "job-search-card__location").text
        job_url = job_card.find_element(By.CSS_SELECTOR,"a.base-card__full-link").get_attribute("href")

        job_card.click()



        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='i18n_show_more']"))
            )
            button.click()
            time.sleep(1)
        except:

            random_index = random.randint(0, len(job_cards) - 1)
            job_cards[random_index].click()
            sleep(2)

            random_index = random.randint(0, len(job_cards) - 1)
            job_cards[random_index].click()
            delay = random.uniform(2, 3)
            scroll_slightly_up(driver)
            time.sleep(delay + 1)


            job_card.click()
            sleep(2)
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='i18n_show_more']"))
                )
                button.click()
                time.sleep(1)
            except:
                print("job failed to read")
                # continue

        sleep(1)

        try:
            number_of_applicants = job_card.find_element(By.XPATH,
                                                             "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[2]").text
        except Exception as e:
            try:
                number_of_applicants = job_card.find_element(By.XPATH,"/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/figure/figcaption").text
            except Exception as e:
                number_of_applicants = None
        try:
            post_date = job_card.find_element(By.XPATH,
                                                  "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span").text

        except Exception as e:
            try:
                post_date = job_card.find_element(By.XPATH,"/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span").text
            except Exception as e:
                post_date = None


        try:  # Get the job description text
            job_description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))
            )
            job_description = job_description_element.text

            if job_description:
                job_data = {
                    "Job Title": job_title,
                    "Company Name": company_name,
                    "Location": location,
                    "Job Description": job_description,
                    "Job URL": job_url,
                    "Applicants Number": number_of_applicants,
                    "post_date": post_date
                }

                jobs_data.append(job_data)
                sleep(0.2)
        except Exception as e:
            print("An error occurred:", e)
            continue

    return jobs_data



jobs = no_login_scraper("water", "haifa",4,1)

