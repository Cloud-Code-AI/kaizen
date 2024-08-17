from kaizen.retriever.llama_index_retriever import RepositoryAnalyzer

# Initialize the analyzer
analyzer = RepositoryAnalyzer()

# Set up the repository (do this when you first analyze a repo or when you want to update it)
# analyzer.setup_repository("./github_app/")

# Perform queries (you can do this as many times as you want without calling setup_repository again)
results = analyzer.query("Find functions that handle authentication")
for result in results:
    print(f"File: {result['file_path']}")
    print(f"Abstraction: {result['abstraction']}")
    print(f"result:\n{result}")
    print(f"Relevance Score: {result['relevance_score']}")
    print("---")

# # If you make changes to the repository and want to update the analysis:
# analyzer.setup_repository("/path/to/your/repo")

# Then you can query again with the updated data
results = analyzer.query("authentication")
