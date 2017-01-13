from wrapper import buzzes_in_timeframe, keyword_search, comments_threshold

def test(feed, start, end, keywords, threshold):
	"""Wrapper function that returns results from all three API endpoints"""
	a = buzzes_in_timeframe(feed, start, end)
	b = keyword_search(feed, keywords)
	c = comments_threshold(feed, start, end, threshold)

	return a,b,c