from langchain_community.utilities import BingSearchAPIWrapper

import os

tools = []
if os.environ.get('BING_SUBSCRIPTION_KEY') and os.environ.get('BING_SEARCH_URL'):
    tools.append(
        (
            "bing_search",
            BingSearchAPIWrapper(),
        )
    )

