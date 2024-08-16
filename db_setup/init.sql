-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table to store repository information
CREATE TABLE repositories (
    repo_id SERIAL PRIMARY KEY,
    repo_name TEXT NOT NULL,
    repo_owner TEXT NOT NULL,
    repo_url TEXT NOT NULL,
    repo_description TEXT
);

-- Table to store file information
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    repo_id INTEGER NOT NULL REFERENCES repositories(repo_id),
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_ext TEXT NOT NULL,
    programming_language TEXT
);

-- Table to store function abstractions
CREATE TABLE function_abstractions (
    function_id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(file_id),
    function_name TEXT NOT NULL,
    function_signature TEXT NOT NULL,
    abstract_functionality TEXT NOT NULL,
    complexity_score FLOAT,
    input_output_description TEXT,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL
);

-- Table to store vector embeddings for function abstractions
CREATE TABLE function_embeddings (
    embedding_id SERIAL PRIMARY KEY,
    function_id INTEGER NOT NULL REFERENCES function_abstractions(function_id),
    vector VECTOR(1536) NOT NULL
);


CREATE TABLE syntax_nodes (
    node_id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(file_id),
    node_type TEXT NOT NULL,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL,
    node_content TEXT,
    language TEXT NOT NULL
);

-- Table to store node relationships
CREATE TABLE node_relationships (
    relationship_id SERIAL PRIMARY KEY,
    parent_node_id INTEGER NOT NULL REFERENCES syntax_nodes(node_id),
    child_node_id INTEGER NOT NULL REFERENCES syntax_nodes(node_id),
    relationship_type TEXT NOT NULL
);

-- Table to store node properties
CREATE TABLE node_properties (
    property_id SERIAL PRIMARY KEY,
    node_id INTEGER NOT NULL REFERENCES syntax_nodes(node_id),
    property_name TEXT NOT NULL,
    property_value TEXT NOT NULL
);