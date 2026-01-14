import logging
from pymed import PubMed
from datetime import datetime, timedelta
import re
import json
import pandas as pd
import itertools
import os


# Create a logger object
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all messages

# Create a handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Log debug and above messages to the console

# Create a handler for logging to a file
file_handler = logging.FileHandler('log/pubmed_log.log')
file_handler.setLevel(logging.INFO)  # Log info and above messages to the file

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

CN_EMAIL_FILTER = ["aliyun.com", ".cn", "qq.com","163.com","@126.com","sina.com "]
# Journal 名字必须符合pubmed 要求，在 https://pubmed.ncbi.nlm.nih.gov/advanced/ 验证
JOURNALS = ["The Lancet. Neurology", "Nature", "Cell"]

# init pubmed
def query_pubmed(query, max_results=9000):
    """Query PubMed for articles matching the search term within the past N years."""
    pubmed = PubMed(tool="PubMedSearcher", email="info@chemgood.com")

    logger.info(f"Querying PubMed: {query}")

    try:
        results = pubmed.query(query,max_results=max_results)
        return results
    except Exception as e:
        logger.error(f"Error querying PubMed: {e}")
        return None

def build_query(keywordA, keywordB='', input_date='', year_window=3):
    # 改时间/年份： -1 (end year -1) 表示去年到起点年份 -2 表示前年到起点年份
    # 起点年份固定为 end year - 3
    
    end_date = datetime.today()
    if input_date:
        end_date = datetime.strptime(input_date, "%Y/%m")
    
    start_date = end_date - timedelta(days=year_window * 365)

    start_str = start_date.strftime("%Y/%m/%d")
    end_str = end_date.strftime("%Y/%m/%d")

    terms = []

    terms.append(f'{keywordA}[Title/Abstract]')
    if keywordB:
        terms.append(f"{keywordB}[Title/Abstract]")

    # journal_terms = [f'"{j}"[Journal]' for j in JOURNALS]
    # journal_query = "(" + " OR ".join(journal_terms) + ")"
    # terms.append(journal_query)

    # concat time
    terms.append(f'("{start_str}"[Date - Publication] : "{end_str}"[Date - Publication])')

    query = " AND ".join(terms)
    return query

def validate_article(article, search_term):
    if (
        (article.title and search_term.casefold() in article.title.casefold()) or
        (article.abstract and search_term.casefold() in article.abstract.casefold()) 
    ):
        return True
    else:
        return False
    

def process_authors(authors):
    """Extract the last valid author from the authors list."""
    for author in reversed(authors):
        if author.get('firstname') and author.get('lastname'):
            full_name = f"{author['firstname']} {author['lastname']}"
            # logger.info(f"last author: {full_name}")
            return full_name
    return None

def process_emails(authors, email_pattern):
    """Extract all email addresses from the authors' affiliations.

    return tuple(email, name)
    """
    email_list = []
    for author in authors:
        if author.get('affiliation'):
            match = re.search(email_pattern, author['affiliation'])
            if match:
                firstname = author.get("firstname", "NoName")
                lastname = author.get("lastname", "NoName")
                email_list.append((match.group(0), f"{firstname} {lastname}"))
    return email_list

def safe_filename(name):
    # 替换所有非法字符为下划线
    return re.sub(r'[\\/:"*?<>|]', '_', name)

def output_to_excel(search_term, info):
    """Output the results to an Excel file."""
    # sort by article_id
    info_list = sorted(info, key=lambda x: int(x[3]),reverse=True)
    name = safe_filename(search_term)

    if info_list:
        df = pd.DataFrame({
            'Emails': [info[0] for info in info_list],
            'Name':   [info[1] for info in info_list],
            'Date':   [info[2] for info in info_list],
            'PubID':  [info[3] for info in info_list],
            'Journal':[info[4] for info in info_list],
            'Title':  [info[5] for info in info_list]
        })
        df.to_excel(os.path.join(output_dir, f"{name}_output.xlsx"), index=False)
    else:
        logger.info(f"No valid authors or emails found in {search_term}.")

def medpro_search(keywordA, keywordB='', input_date=''):
    """Main function to handle PubMed searching and processing."""
    # info store tuple(title, author name, journal)
    cn_list  = []
    info_list = []
    seen_emails = set()
    article_count = 0
    email_count = 0
    MAX_EMAILS = 10000
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    filename = f"{keywordA}_{keywordB}_" if keywordB else keywordA
    
    # Query PubMed
    query = build_query(keywordA, keywordB, input_date)
    results = query_pubmed(query)

    if results is None:
        logger.error("No results returned from PubMed.")
        return

    for article in results:
        if email_count > MAX_EMAILS:
            logger.info(f"Reached the maximum number of emails: {MAX_EMAILS}. Stop further processing.")
            break
        if validate_article(article, keywordA):
            if not keywordB or validate_article(article, keywordB):
                article_count+=1
                article_id = article.pubmed_id.splitlines()[0].strip()
                logger.debug(f"Processing article {article_id}")
                # logger.info(json.dumps(article.toJSON()))
                
                authors = article.authors
                emails = process_emails(authors, email_pattern)
                count = 0
                for email in reversed(emails):
                    if email[0] not in seen_emails:
                        count+=1
                        if count > 10:
                            break #Only keep 10 emails in 1 article
                        
                        seen_emails.add(email[0])
                        email_count+=1
                        item = (
                            email[0],
                            email[1],
                            article.publication_date,
                            article_id,
                            getattr(article, 'journal', 'No Journal'),
                            getattr(article, 'title', 'No Title')
                        )
                        if any(keyword in email[0] for keyword in CN_EMAIL_FILTER):
                            cn_list.append(item)
                        else:
                            info_list.append(item)

    logger.info(f"Processing article {article_count}, stored email {email_count} ")
    output_to_excel(filename, info_list)
    output_to_excel(f"CN_{filename}", cn_list)


# Example usage
keywordA = input("Please enter the first keyword: ")
# keywordB = input("Please enter the second keyword(optional): ")
keywordB = ''
input_date = input("Enter Search end date(YYYY/MM),or leave blank for today: ").strip()

# query = build_query(keywordA, keywordB, input_date)
# print("pubmed query：\n", query)
medpro_search(keywordA, keywordB, input_date)
