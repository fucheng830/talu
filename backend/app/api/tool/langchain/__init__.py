from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools import BraveSearch
from langchain_community.tools import DuckDuckGoSearchRun
import os

tools = []

if os.environ.get('BING_SUBSCRIPTION_KEY') and os.environ.get('BING_SEARCH_URL'):
    tools.append(
        (
            "bing_search",
            BingSearchAPIWrapper(),
        )
    )

if os.environ.get('BRAVE_API_KEY'):
    tools.append(
        (
            "BraveSearch",
            BraveSearch(api_key=os.environ.get('BRAVE_API_KEY')),
        )
    )




