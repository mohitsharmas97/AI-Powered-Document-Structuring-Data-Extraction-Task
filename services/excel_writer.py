import pandas as pd
import json
import os

def write_to_excel(json_string, output_path):
    try:
        # Parse the JSON string from AI
        data = json.loads(json_string)

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns if they exist to match "Expected Output" format
        # We expect: Key, Value, Comments
        expected_cols = ["Key", "Value", "Comments"]
        
        # Filter to ensure we have the right columns, adding missing ones as empty
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ""
                
        # Reorder to ensure visual consistency
        df = df[expected_cols]

        # Save to Excel
        df.to_excel(output_path, index=False)
        
        return output_path

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw AI response: {json_string}")
        return None
    except Exception as e:
        print(f"Error saving Excel: {e}")
        return None