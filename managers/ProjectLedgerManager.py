"""
ProjectLedgerManager.py
#######################

This module provides the ProjectLedgerManager class, which is responsible for managing project ledgers.

Additionally, it provides a non-class function that is to be called upon project initalization which produces the empty ledger file for the project.
"""

# Imports
from datetime import datetime
import os
import json


class ProjectLedgerManager:
    def __init__(self, project_folder: str):
        """
        Loads the ledger into memory on initialization.
        
        project_folder (str): The path to the game project folder.
        """
        # Create instance attributes
        self.project_folder = project_folder
        self.ledger_path = os.path.join(self.project_folder, ".antigine", "ledger.json")
        project_file_path = os.path.join(self.project_folder, ".antigine", "project.json")
        # Load the ledger data from the JSON file into memory
        with open(self.ledger_path, 'r') as f:
            self.ledger_data = json.load(f) # This is our in-memory dictionary
        # Load the project data from the JSON file into memory
        with open(project_file_path, 'r') as f:
            self.project_data = json.load(f)
        self.project_name = self.project_data.get("project_name", "Unnamed Project")
        self.project_initials = self.project_data.get("project_initials", "F")  # Default to "NP" if not set
        
    def add_feature(self, feature_data: dict) -> str:
        """
        Adds a new feature to the ledger and returns its unique feature ID.

        feature_data (dict): A dictionary containing the feature data. See the 'example_ledger_entry' for fields to provide.

        Returns:
            str: The unique feature ID assigned to the new feature.
        """
        # Get max feature id number from existing data
        # and increment by one to get the new feature id number.
        if not self.ledger_data:
            new_feature_num = 1
        else:
            max_feature_id = max(int(fid.split("-")[1]) for fid in self.ledger_data.keys())
            new_feature_num = str(max_feature_id + 1)
        # Create the new feature ID
        feature_id = f"{self.project_initials}-{new_feature_num}"
        # Add the new feature to the ledger data
        self.ledger_data[feature_id] = {
            "type": feature_data.get("type", "new_feature"),
            "status": feature_data.get("status", "requested"),  # Default status is 'requested'
            "title": feature_data.get("title", ""),
            "description": feature_data.get("description", ""),
            "keywords": feature_data.get("keywords", []),
            "dates": {
                "created": datetime.today().strftime('%Y-%m-%d'),
                "fip_approved": "",
                "implemented": "",
                "validated": "",
                "superseded": ""
            },
            "artifacts": {
                "request": fr"{feature_id}/request.md",
                "fip": fr"{feature_id}/fip.md",
                "adr": fr"{feature_id}/adr.md"
            }
        }

    # METHOD 1: Direct Lookup (Very Fast)
    def get_feature_by_id(self, feature_id):
        """Returns the full data for a single feature."""
        return self.ledger_data.get(feature_id)

    # METHOD 2: Simple Filtering (Fast)
    def get_features_by_status(self, status):
        """Returns a list of all features matching a status."""
        return [
            {"feature_id": fid, **data} for fid, data in self.ledger_data.items()
            if data['status'] == status
        ]

    # METHOD 3: Traditional Keyword Search (The Core Search Logic)
    def keyword_search(self, search_terms: list[str]):
        """
        Performs a simple keyword search across summaries and returns a ranked list of feature IDs.
        """
        results = []
        for feature_id, data in self.ledger_data.items():
            score = 0
            # Combine all searchable text fields into one string
            searchable_text = (
                data['summary']['title'].lower() + " " +
                data['summary']['description'].lower() + " " +
                " ".join(data['summary']['keywords']).lower()
            )
            
            for term in search_terms:
                if term.lower() in searchable_text:
                    score += 1 # Add 1 point for each matching term
            
            if score > 0:
                results.append({"feature_id": feature_id, "score": score})
        
        # Return results sorted by relevance score, highest first
        return sorted(results, key=lambda x: x['score'], reverse=True)
