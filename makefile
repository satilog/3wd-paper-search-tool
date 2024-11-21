# Define variables for environment name and output file
ENV_NAME := paper_search_tool
OUTPUT_FILE := environment.yaml

# Help command to display available targets (Keep this first so default is help command)
help:
	@echo "Available commands:"
	@echo "  make export-env     Export Conda environment to YAML without prefix"
	@echo "  make create-env     Create a new Conda environment from YAML file"
	@echo "  make remove-env     Remove the Conda environment"
	@echo "  make list-envs      List all Conda environments"
	@echo "  make clean          Clean up generated files"

# Export Conda environment without prefix
export-env:
	@echo "Exporting environment $(ENV_NAME) to $(OUTPUT_FILE) without prefix..."
	conda env export --name $(ENV_NAME) --no-builds | grep -v '^prefix:' > $(OUTPUT_FILE)
	@echo "Environment exported successfully to $(OUTPUT_FILE)."

# Create Conda environment from YAML file
create-env:
	@echo "Creating environment $(ENV_NAME) from $(OUTPUT_FILE)..."
	conda env create -f $(OUTPUT_FILE)
	@echo "Environment $(ENV_NAME) created successfully."

# Remove existing environment
remove-env:
	@echo "Removing environment $(ENV_NAME)..."
	conda remove --name $(ENV_NAME) --all -y
	@echo "Environment $(ENV_NAME) removed successfully."

# List all Conda environments
list-envs:
	@echo "Listing all Conda environments..."
	conda env list

# Clean temporary or unnecessary files
clean:
	@echo "Cleaning up generated files..."
	rm -f $(OUTPUT_FILE)
	@echo "Clean-up completed."