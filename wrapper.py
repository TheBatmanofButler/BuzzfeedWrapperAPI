import urllib, json, datetime

# root URL for Buzzfeed REST API
API_URL = "http://www.buzzfeed.com/api/v2/"

def pull_JSON(endpoint, query):
	"""Returns JSON from Buzzfeed API endpoints as Python dictionary
	Args:
		endpoint (str): Buzzfeed API endpoint (currently either "feeds" or "comments")
		query (str): string to be queried using API

	Returns:
		dict: JSON data from Buzzfeed API as per input params
	"""
	if type(query) != str:
		print "*query* must be a string"
		return

	url = API_URL + endpoint + query
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	return data

def remove_repeated_buzzes(data):
	"""Removes repeats from Feeds API data
	Args:
		data (dict): JSON data from Feeds API

	Returns:
		list: Unique list of buzzes
	"""

	buzzes = []
	for buzz in data["buzzes"]:
		if buzz in buzzes:
			continue
		else:
			buzzes.append(buzz)

	return buzzes

def buzzes_in_timeframe(feed, start, end):
	"""Returns all buzzes within start and end timestamps
	Args:
        feed (str): Name of any feed page from buzzfeed.com, except for news
        start (str): Start timestamp in the format YYYY-MM-DD HH:MM:SS
        end (str): End timestamp in the format YYYY-MM-DD HH:MM:SS

    Returns:
        list: JSON for all buzzes matching input params
	"""

	# Converting string inputs to datetime objects
	start_timestamp = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
	end_timestamp = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

	# Pulling JSON from Feeds API
	buzzes = pull_JSON("feeds/", feed)
	buzzes = remove_repeated_buzzes(buzzes)

	# Iterating through all buzzes from feed
	matches = []
	for buzz in buzzes:
		
		# Converting buzz timestamp to datetime object
		timestamp = datetime.datetime.strptime(buzz["published_date"], "%Y-%m-%d %H:%M:%S")
		if start_timestamp <= timestamp <= end_timestamp:
			matches.append(buzz)

	return matches

def keyword_search(feed, keywords = []):
	"""Returns buzzes containing given keywords in title or description
	Args:
        feed (str): Name of any feed page from buzzfeed.com, except for news
        keywords (list): all strings to be searched for

    Returns:
        list: JSON for all buzzes matching input params
	"""
	if type(keywords) != list:
		raise TypeError("keywords must be a list")

	# Pulling JSON from Feeds API
	buzzes = pull_JSON("feeds/", feed)
	buzzes = remove_repeated_buzzes(buzzes)

	# Iterating through all buzzes from feed
	matches = []
	for buzz in buzzes:

		# Checking each keyword
		for keyword in keywords:
			# Ignoring cases in string comparison
			if keyword.lower() in buzz["title"].lower() or keyword in buzz["description"].lower():
				matches.append(buzz)
				break

	return matches

def comments_threshold(feed, start, end, threshold):
	"""Returns articles with comment count at least at threshold
	Args:
        feed (str): Name of any feed page from buzzfeed.com, except for news
        start (str): Start timestamp in the format YYYY-MM-DD HH:MM:SS
        end (str): End timestamp in the format YYYY-MM-DD HH:MM:SS
        threshold (int): Comment threshold, non-negative integer

    Returns:
        list: JSON for all buzzes matching input params
	"""
	if threshold < 0:
		raise ValueError("threshold must be a non-negative integer")

	# Retrieving all buzzes within timeframe
	buzzes = buzzes_in_timeframe(feed, start, end)

	# Iterating through buzzes
	matches = []

	for buzz in buzzes:
		# Pulling JSON from Comments API
		comments = pull_JSON("comments/", str(buzz["id"]))
		if int(comments["total_count"]) >= threshold:
			matches.append(buzz)

	return matches