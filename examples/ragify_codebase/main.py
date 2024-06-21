from kaizen.retriever.llama_index_retriever import RepositoryAnalyzer

# Usage
analyzer = RepositoryAnalyzer(database_config={})
analyzer.analyze_repository("./kaizen")

# Query example
result = analyzer.query("How is function X related to function Y?")
print(result)
