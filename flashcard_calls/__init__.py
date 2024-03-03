import pandas as pd

def parse(definitions_text, df):
    lines = definitions_text.split("\n")
    term_definitions = {}
    current_term = None

    for line in lines:
        if line.startswith("Term:"):
            current_term = line[len("Term:"):].strip()
        elif line.startswith("Definition:"):
            definition = line[len("Definition:"):].strip()
            term_definitions[current_term] = definition

    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame(list(term_definitions.items()), columns=['Term', 'Definition'])

    # Concatenate the new DataFrame with the existing one
    df = pd.concat([df, new_df], ignore_index=True)

    return df
