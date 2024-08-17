#!/bin/bash

# Directory to store the language libraries
LANGUAGE_DIR="tree_sitter_languages"

# List of languages to install
LANGUAGES=(
    "python"
    "javascript"
    "typescript"
    "rust"
)

# Create the language directory if it doesn't exist
mkdir -p "$LANGUAGE_DIR"

# Function to install a language
install_language() {
    lang=$1
    echo "Installing Tree-sitter parser for $lang..."
    
    # Clone the repository if it doesn't exist
    if [ ! -d "$LANGUAGE_DIR/tree-sitter-$lang" ]; then
        git clone "https://github.com/tree-sitter/tree-sitter-$lang" "$LANGUAGE_DIR/tree-sitter-$lang"
    fi
    
    # Navigate to the repository directory
    cd "$LANGUAGE_DIR/tree-sitter-$lang"
    
    # Update submodules
    git submodule update --init
    
    # Build the parser using tree-sitter CLI
    tree-sitter generate
    
    # Navigate back to the original directory
    cd ../..
    
    echo "Tree-sitter parser for $lang installed successfully."
}

# Install each language
for lang in "${LANGUAGES[@]}"; do
    install_language $lang
done

echo "All Tree-sitter parsers have been installed."