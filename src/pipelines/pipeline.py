from src.agents.agents import search_agent,scrape_agent,writer_chain,critic_chain

def research_pipeline(topic):
    state={}

    print("\n")

    srch_agent=search_agent()
    print("Search agent working...\n")
    search_result=srch_agent.invoke({
        "messages":[("user",f"Find recent,reliable infromation and urls on:{topic}"
                     "with the help of tool,dont ask any question or give any suggestions.")]
    })
    state["search_result"]=search_result['messages'][-1].content

    print("\nSearch result:",state['search_result'])

    reader_agent=scrape_agent()
    print("\nReader agent working...\n")
    reader_result=reader_agent.invoke({
        "messages":[("user",
                     f"based on the following search results about:{topic},"
                     f"pick the most relevant URL and scrape it for deeper content."
                     f"Search results:{state['search_result'][:800]}"
                     "Dont ask any question or give any suggestions.")]
    })
    state["scrape_content"]=reader_result['messages'][-1].content
    
    print("\nScrape result:",state['scrape_content'])

    print("\nWriter agent working...\n")
    research_combined=(
        f"SEARCH RESULT:\n{state['search_result']}\n"
        f"DETAILED CONTENT:\n{state['scrape_content']}"
    )

    state["report"]=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("Final Report: ",state["report"])

    print("\n\n")

    print("\nCritic agent working...\n")
    state["feedback"]=critic_chain.invoke({
        "report":state["report"]
    })

    print("Feedback:",state["feedback"])

    return state