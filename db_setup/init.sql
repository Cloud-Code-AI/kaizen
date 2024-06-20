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

-- Table to store code snippets
CREATE TABLE code_snippets (
    snippet_id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(file_id),
    snippet_text TEXT NOT NULL,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL,
    functionality TEXT,
    context TEXT
);

-- Table to store vector embeddings for code snippets
CREATE TABLE embeddings (
    embedding_id SERIAL PRIMARY KEY,
    snippet_id INTEGER NOT NULL REFERENCES code_snippets(snippet_id),
    vector VECTOR NOT NULL
);

-- Table to store AI-generated summaries for code snippets
CREATE TABLE snippet_summaries (
    summary_id SERIAL PRIMARY KEY,
    snippet_id INTEGER NOT NULL REFERENCES code_snippets(snippet_id),
    summary TEXT NOT NULL,
    summary_quality_score FLOAT
);

-- Node level data for AST
CREATE TABLE ast_nodes (
    node_id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(file_id),
    node_type TEXT NOT NULL,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL
    -- Add other common node properties here
);

-- Table to store node properties
CREATE TABLE node_properties (
    property_id SERIAL PRIMARY KEY,
    node_id INTEGER NOT NULL REFERENCES ast_nodes(node_id),
    property_name TEXT NOT NULL,
    property_value TEXT NOT NULL
);

-- Table to store node relationships
CREATE TABLE node_relationships (
    relationship_id SERIAL PRIMARY KEY,
    parent_node_id INTEGER NOT NULL REFERENCES ast_nodes(node_id),
    child_node_id INTEGER NOT NULL REFERENCES ast_nodes(node_id),
    relationship_type TEXT NOT NULL
);