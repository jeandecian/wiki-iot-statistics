from bs4 import BeautifulSoup
import csv
import re
import requests


def get_html_text_data(path):
    BASE_URL = "https://fehmijaafar.net/wiki-iot/index.php"

    return requests.get(BASE_URL + path).text


def write_csv(file_name, header, data):
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def get_category_total_pages(category):
    text_data = get_html_text_data("/Category:" + category)
    soup = BeautifulSoup(text_data, "html.parser")
    mw_pages_div = soup.find("div", id="mw-pages")
    first_paragraph = mw_pages_div.find("p") if mw_pages_div else None

    if first_paragraph:
        numbers = re.findall(r"\d+", first_paragraph.get_text())

        if len(numbers) >= 2:
            total_pages = numbers[1]

            return category, total_pages

    return category, None


def get_total_pages():
    with open("statistics/total_pages.txt", "w") as f:
        f.write(str(get_category_total_pages("Classification")[1]))


def get_grade_distribution():
    grades = [
        "Grade_A%2B",
        "Grade_A",
        "Grade_A-",
        "Grade_B",
        "Grade_C",
        "Grade_D",
        "Grade_F",
    ]

    data = []
    for grade in grades:
        category, total_pages = get_category_total_pages(grade)
        category = category.replace("Grade_", "").replace("%2B", "+")
        data.append((category, total_pages))

    write_csv("statistics/grade_distribution.csv", ["Grade", "Count"], data)


def get_criteria_count():
    criteria = (
        ("device_known_hardware_tampering", "None", "Rare", "Very+common"),
        ("device_known_vulnerabilties", "None", "Rare", "Very+common"),
        ("device_prior_attacks", "None", "Rare", "Very+common"),
        ("device_updatability", "Very+common", "Rare", "None"),
        ("system_authentication_with_other_systems", "Full", "Partial", "No"),
        (
            "system_communications",
            "Encrypted+with+up-to-date+encryption",
            "Encrypted+with+obselete+encryption",
            "No+encryption",
        ),
        (
            "system_storage",
            "Encrypted+with+up-to-date+encryption",
            "Encrypted+with+obselete+encryption",
            "No+encryption",
        ),
        ("user_authentication_account_management", "Full", "Basic", "Absent"),
        ("user_authentication_authentication", "Secure", "Basic", "Absent"),
        ("user_authentication_brute_force_protection", "Exist", "Basic", "Absent"),
        (
            "user_authentication_event_logging",
            "Access+event+logged",
            "Partial+logging",
            "Absent",
        ),
        (
            "user_authentication_passwords",
            "Require+change+after+setup+with+complexity+requirements",
            "Require+change+after+setup",
            "Default%2FCommon%2FEasy+to+guess",
        ),
    )

    data = []
    for criterion, *values in criteria:

        rows = [criterion]
        for value in values:
            text_data = get_html_text_data(
                f"?search=%22{criterion}%3D{value}%22&title=Special%3ASearch&profile=default&fulltext=1"
            )
            soup = BeautifulSoup(text_data, "html.parser")
            results_info_div = soup.find("div", class_="results-info")
            total_results = (
                results_info_div["data-mw-num-results-total"]
                if results_info_div
                else None
            )

            if (
                criterion == "user_authentication_passwords"
                and value == "Require+change+after+setup"
            ):
                total_results = str(eval(f"{total_results} - {rows[-1]}"))

            rows.append(total_results)

        data.append(rows)

    write_csv("statistics/criteria_count.csv", ["Criterion", "0", "1", "2"], data)


get_total_pages()
get_grade_distribution()
get_criteria_count()
