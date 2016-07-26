from bs4 import BeautifulSoup
import sys,urllib2
import json
import os
import re

DETAILS_LINK = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber='
AUTHORS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='
REFERENCE_LINK = 'http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber='
CITATIONS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?arnumber='
KEYWORDS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber='
METRICS_LINK = 'http://ieeexplore.ieee.org/xpl/abstractMetrics.jsp?arnumber='

# Creating existence of the required directory 
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

# getting the parseable object for an url
def get_soup(aurl):
	hdr = {'User-Agent':'Mozilla/5.0'}
	areq = urllib2.Request(aurl,headers=hdr)
	apage = urllib2.urlopen(areq).read()
	asoup = BeautifulSoup(apage,'html.parser')
	return asoup


def get_id_from_link(link):
    try:
        searchObj = re.search(r'(.*)arnumber=(\d*).*', link)
        if searchObj:
            return searchObj.group(2)
        else:
            return None
    except:
        return None


def get_details(id):
    link = DETAILS_LINK + str(id)

    details = {}

    abstract = ""

    try:
        # page = urllib2.urlopen(link).read()
        # soup = BeautifulSoup(page, 'html.parser')

        soup = get_soup(link)

        # abstract
        divs = soup.find_all("div", attrs={"class": "article"})
        for div in divs:
            if div.find("p") != None:
                abstract = div.find("p").string
                break

        details["abstract"] = abstract

        conference = soup.find("meta", attrs={"name": "citation_conference"})
        publisher = soup.find("meta", attrs={"name": "citation_publisher"})
        title = soup.find("meta", attrs={"name": "citation_title"})
        date = soup.find("meta", attrs={"name": "citation_date"})
        volume = soup.find("meta", attrs={"name": "citation_volume"})
        issue = soup.find("meta", attrs={"name": "citation_issue"})
        firstpage = soup.find("meta", attrs={"name": "citation_firstpage"})
        lastpage = soup.find("meta", attrs={"name": "citation_lastpage"})
        doi = soup.find("meta", attrs={"name": "citation_doi"})
        isbn = soup.find("meta", attrs={"name": "citation_isbn"})
        journal_title = soup.find("meta", attrs={"name": "citation_journal_title"})


        pages = soup.find("dt", text="Page(s):")
        meeting_date = soup.find("dt", text="Meeting Date :")
        inspec = soup.find("dt", text="INSPEC Accession Number:")
        conference_location = soup.find("dt", text="Conference Location :")
        issn = soup.find("dt", text="ISSN :")
        date_publication = soup.find("dt", text="Date of Publication :")
        date_current_version = soup.find("dt", text="Date of Current Version :")
        issue_date = soup.find("dt", text="Issue Date :")
        sponsor = soup.find("dt", text="Sponsored by :")


        if conference : details["conference"] = conference["content"]
        if publisher : details["publisher"] = publisher["content"]
        if title : details["title"] = title["content"]
        if date : details["date"] = date["content"]
        if volume : details["volume"] = volume["content"]
        if issue : details["issue"] = issue["content"]
        if firstpage : details["firstpage"] = firstpage["content"]
        if lastpage : details["lastpage"] = lastpage["content"]
        if doi : details["doi"] = doi["content"]
        if isbn : details["isbn"] = isbn["content"]
        if journal_title : details["journal_title"] = journal_title["content"]

        try :
            if pages : details["pages"] = " ".join(pages.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if meeting_date : details["meeting_date"] = " ".join(meeting_date.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if inspec : details["inspec"] = " ".join(inspec.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if conference_location : details["conference_location"] = " ".join(conference_location.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if issn : details["issn"] = " ".join(issn.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if date_publication : details["date_publication"] = " ".join(date_publication.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if date_current_version : details["date_current_version"] = " ".join(date_current_version.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if issue_date : details["issue_date"] = " ".join(issue_date.findNext("dd").contents[0].strip().split())
        except : pass
        try :
            if sponsor : details["sponsor"] = sponsor.findNext("dd").find("a").text
        except : pass


    except Exception,e: print str(e)


    return details


def get_authors(id):
    link = AUTHORS_LINK + str(id)

    authors = []
    try:
        # page = urllib2.urlopen(link).read()
        # soup = BeautifulSoup(page, 'html.parser')

        soup = get_soup(link)

        metas = soup.find_all("meta", attrs={"name": "citation_author"})

        for meta in metas:
            if meta['name'] == 'citation_author':
                authors.append(meta['content'])
    except:
        pass

    return authors


def get_references(id):
    link = REFERENCE_LINK + str(id)

    references = []
    try:
        # page = urllib2.urlopen(link).read()
        # soup = BeautifulSoup(page, 'html.parser')

        soup = get_soup(link)

        divs = soup.find_all("div", attrs={"class": "links"})

        for div in divs:
            a_tags = div.find_all("a")

            arnumber = get_id_from_link(a_tags[0]["href"])

            if arnumber != None:
                references.append(arnumber)

    except:
        pass

    return references


def get_citations(id):
    link = CITATIONS_LINK + str(id)

    citations = []
    try:
        # page = urllib2.urlopen(link).read()
        # soup = BeautifulSoup(page, 'html.parser')
        soup = get_soup(link)
        divs = soup.find_all("div", attrs={"class": "links"})

        for div in divs:
            a_tags = div.find_all("a")

            arnumber = get_id_from_link(a_tags[0]["href"])

            if arnumber != None:
                citations.append(arnumber)

    except:
        pass

    return citations


def get_keywords(id):
    link = KEYWORDS_LINK + str(id)

    keywords = []
    try:
        # page = urllib2.urlopen(link).read()
        # soup = BeautifulSoup(page, 'html.parser')
        soup = get_soup(link)
        meta = soup.find("meta", attrs={"name": "citation_keywords"})

        for keyword in meta["content"].strip().split(";"):
            keywords.append(keyword.strip())
    except Exception:
    	pass
    return keywords


def get_article(arnumber):
    article = {}
    article["arnumber"] = arnumber
    article["details"] = get_details(arnumber)
    article["authors"] = get_authors(arnumber)
    article["references"] = get_references(arnumber)
    article["citations"] = get_citations(arnumber)
    article["keywords"] = get_keywords(arnumber)

    return article



# Article numbers of each article in the issue link
def get_articles(aurl,adir):
	soup = get_soup(aurl)
	link1 = soup.find('input',{'id':'oqs'})
	link0 = soup.find('input',{'id':'submitUrl'})
	total_number = soup.find('div',{'class':'results-display'}).find_all('b')[1].get_text()
	newurl = 'http://ieeexplore.ieee.org' + link0['value'] + link1['value'] + '&rowsPerPage=' + total_number

	fsoup = get_soup(newurl)
	articles = fsoup.find('ul',{'class':'results'}).find_all('li')
	count = 0
	for article in articles:
		if article.find('h3').find('a') != None:
			count += 1
			article_dir = adir + '/Article ' + str(count)
			ckdir(article_dir)
			article_no = article.find('span').find('input')['id']
			print(article_no)
			article = get_article(article_no)
			with open(article_dir+'/ArticleData.json','w') as outfile:
				json.dump(article,outfile)


# Creates directories for all the volumes,all the issues of a volume
def get_issues(aurl,adir):
	soup = get_soup(aurl)

	volumes_dir = adir + '/Volumes'
	ckdir(volumes_dir)
	METRICS_dict = {}
	metrics = soup.find('div',{'class':'jrnl-metrics cf'}).find_all('span')
	if metrics == []:
		METRICS_dict['Imfact Factor'] = '0'
		METRICS_dict['Eigenfactor'] = '0'
		METRICS_dict['Article Influence Score'] = '0'
	else:
		METRICS_dict['Imfact Factor'] = str(metrics[0].get_text())
		METRICS_dict['Eigenfactor'] = str(metrics[2].get_text())
		METRICS_dict['Article Influence Score'] = str(metrics[4].get_text())

	with open(adir+'metrics.json','w') as outfile:
		json.dump(METRICS_dict,outfile)

	try:
		volumes = soup.find("div",{"class":'volumes'})
		years = volumes.find_all('ul')

	except AttributeError:
		volumes = soup.find("div",{'id':'past-issues'}).find('div',{'class':'oa_years'})
		for volume in volumes.find_all('li'):
			volume_dir = volumes_dir + '/' + str(volume.get_text())
			ckdir(volume_dir)
			issue_dir = volume_dir + '/Issue 1' 
			ckdir(issue_dir)
			issue_url = 'http://ieeexplore.ieee.org' + str(volume.find('a')['href'])
			get_articles(issue_url,issue_dir)
		return

	for year in years:
		issues = year.find_all('a')
		volume_dir = volumes_dir + '/' + str(year['id'].split('-')[1])
		ckdir(volume_dir)
		for issue in issues:
			issue_no = re.findall(r'Issue: [0-9]+',str(issue.get_text()))[0]
			issue_no = re.sub('[^a-zA-Z0-9 ]','',issue_no)
			issue_dir = volume_dir + '/' + issue_no
			ckdir(issue_dir)
			issue_url = 'http://ieeexplore.ieee.org' + str(issue['href'])
			get_articles(issue_url,issue_dir)


# loading journal links from data file
with open('../data/Journal_data.json','r') as infile:
	Journals_data = json.load(infile)

base_dir = '../output/Journal Data'
ckdir(base_dir)

for record in Journals_data['records']:
	if record['vj'] != True:
		print(record['title'])
		journal_dir = base_dir + '/'+record['title']
		ckdir(journal_dir)
		full_url = 'http://ieeexplore.ieee.org' + str(record['publicationLink'])
		get_issues(full_url,journal_dir) 