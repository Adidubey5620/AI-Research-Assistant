import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from pipelines.pipeline import run_research_pipeline


topic = "The impact of AI on the job market in 2026"
run_research_pipeline(topic)