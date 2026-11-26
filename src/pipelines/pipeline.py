
from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str, progress_callback=None) -> dict:

    state = {}

    def update_progress(step, message):
        print(f"\n{message}")

        if progress_callback:
            progress_callback(step, message)

    # STEP 1: SEARCH AGENT
    update_progress(1, "Search Agent is discovering relevant sources...")

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, reliable and detailed information about: {topic}")
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    # STEP 2: READER AGENT
    update_progress(2, "Reader Agent is extracting detailed information...")

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    # STEP 3: WRITER CHAIN
    update_progress(3, "Writer Agent is preparing your research report...")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    # STEP 4: CRITIC CHAIN
    update_progress(4, "Critic Agent is evaluating the report...")

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    update_progress(5, "Research completed successfully!")

    return state
