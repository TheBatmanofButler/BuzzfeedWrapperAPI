# BuzzfeedWrapperAPI
Wrapper API over the Buzzfeed API

## Compiling and running code
1. Check for dependencies (`urllib`, `json`, `datetime`), should come with any standard Python 2.7 distribution
2. Open any Python interpreter (I used IPython with Anaconda 4.1.1)
3. `import wrapper`
4. Call any methods in `wrapper.py`

## Testing
I ran the following tests using `tests.test()` to ensure that the wrapper API had the expected behavior, and verified manually using the Buzzfeed API results in my browser. I have listed the lengths of each wrapper endpoint, which I used to verify my results:

### Base case
input:
```
a, b, c = test(feed = "lol", start = "2016-12-13 21:01:04", end = "2016-12-14 14:30:08", keywords = ["Laugh"], threshold = 0)
```

output:
```
len(a) = 4
len(b) = 1
len(c) = 4
```

### Dates swapped
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:08", end = "2016-12-13 21:01:04", keywords = ["Laugh"], threshold = 0)
```

output:
```
len(a) = 0
len(b) = 1
len(c) = 0
```

### Empty string keyword, dates swapped
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:08", end = "2016-12-13 21:01:04", keywords = [""], threshold = 0)
```

output:
```
len(a) = 0
len(b) = 8
len(c) = 0
```

### Impossible keyword, dates swapped
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:08", end = "2016-12-13 21:01:04", keywords = ["98123yr"], threshold = 0)
```

output:
```
len(a) = 0
len(b) = 0
len(c) = 0
```

### Impossible keyword, dates swapped
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:08", end = "2016-12-13 21:01:04", keywords = ["i", "a", "u"], threshold = 0)
```

output:
```
len(a) = 0
len(b) = 8
len(c) = 0
```

### Threshold increased to 5, dates swapped
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:08", end = "2016-12-13 21:01:04", keywords = ["i", "a", "u"], threshold = 5)
```

output:
```
len(a) = 0
len(b) = 8
len(c) = 0
```

### Testing lol feed, guaranteed keywords, threshold set to 500
input:
```
a, b, c = test(feed = "lol", start = "2016-12-13 21:01:04", end = "2016-12-14 14:30:08", keywords = ["i", "a", "u"], threshold = 500)
```

output:
```
len(a) = 4
len(b) = 8
len(c) = 0
```

### Guaranteed keywords, threshold set to 50
input:
```
a, b, c = test(feed = "lol", start = "2016-12-13 21:01:04", end = "2016-12-14 14:30:08", keywords = ["i", "a", "u"], threshold = 50)
```

output:
```
len(a) = 4
len(b) = 8
len(c) = 1
```

### Testing news feed at threshold 0 (news articles do not have comments)
input:
```
a, b, c = test(feed = "news", start = "2016-12-13 21:01:04", end = "2016-12-14 14:30:08", keywords = ["Laugh"], threshold = 0)
```

output:
```
len(a) = 4
len(b) = 1
len(c) = 4
```

### Impossible keyword, dates not swapped
input:
```
a, b, c = test(feed = "news", start = "2017-01-12 00:00:00", end = "2017-01-12 23:59:59", keywords = ["98123yr"], threshold = 0)
```

output:
```
len(a) = 24
len(b) = 0
len(c) = 24
```

### start param not formatted properly
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:", end = "2016-12-13 21:01:04", keywords = ["i", "a", "u"], threshold = 0)
```

output:
```
ValueError: time data '2016-12-14 14:30:' does not match format '%Y-%m-%d %H:%M:%S'
```

### end param not formatted properly
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:", end = "2016-12-13 21:01:", keywords = ["i", "a", "u"], threshold = 0)
```

output:
```
ValueError: time data '2016-12-14 14:30:' does not match format '%Y-%m-%d %H:%M:%S'
```

### Nonexistent feed
input:
```
a, b, c = test(feed = "lo", start = "2016-12-14 14:30:", end = "2016-12-13 21:01:04", keywords = ["i", "a", "u"], threshold = 0)

```
output:
```
ValueError: No JSON object could be decoded
```

### Keywords given a tuple instead of a list (this does not break anything in this implementation, but I raised an error for consistency)
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:00", end = "2016-12-13 21:01:04", keywords = ("i", "a", "u"), threshold = 0)
```

output:
```
TypeError: keywords must be a list
```

### Threshold given negative value
input:
```
a, b, c = test(feed = "lol", start = "2016-12-14 14:30:08", end = "2016-12-13 21:01:04", keywords = ["i", "a", "u"], threshold = -100)
```

output:
```
ValueError: threshold must be a non-negative integer
```

## Design decisions

For the first endpoint, `buzzes_in_timeframe()`, I pull buzzes using the Feeds API and return those that are in between the start and end timestamps. The time complexity is O(n), where n is the number of buzzes. For the second endpoint, `keyword_search()`, I pull buzzes using the Feeds API again and check for each keyword in each buzz, which is done in O(n * m) time, where n is the number of buzzes and m is the number of keywords Lastly, for the third endpoint, comments_threshold(), I use `buzzes_in_timeframe()` to retrieve the buzzes within the timeframe given, and then check the `"total_count"` of each buzz using the Comments API against the threshold.

Some observations:
- I wanted to use the Articles API for the third endpoint, as the instructions asked for articles to be returned, but the Articles API does not seem to be functioning properly (even the examples in the API documentation lead to a 404 page), so I used the Feeds API to return Buzzes.
- I built two helper functions, `pull_JSON` and `remove_repeated_buzzes`, since their functionality was used multiple times within the three endpoint functions. `pull_JSON` takes in the Buzzfeed REST API endpoint and a query, and returns the JSON data. I built remove_repeated_buzzes because I noticed that the data being returned by the Feeds API had repeats of Buzzes and their respective metadata. remove_repeated_buzzes essentially removes any repeated data and returns a list of unique buzzes.
- Based on testing, I raised Errors in keyword_search and comments_threshold to streamline user behavior. In keyword_search, I raise a TypeError if the keywords param is not a list. If a user inputs a non-list iterable, it would not break the current code but I added the Error for consistency. In comments_threshold, I raise a ValueError if the threshold was negative, since threshold is expected to be an integer greater than or equal to zero.

## Algorithms/Packages
- I used the `urllib` package to pull JSON from the Buzzfeed API, `json` to decode the JSON, and `datetime` to conduct time-based mathematics. Alternatively I could have parsed the timestamps myself, but since there was a third-party package available, it seemed fitting to use it.
- In `keyword_search()`, I wanted to make the nested for loop as efficient as possible, so once any of the keywords is found in the buzz title or description, the inner for loop breaks to save time.
