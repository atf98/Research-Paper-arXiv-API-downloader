import itertools
import requests
from pathlib import Path

# Define a dictionary that maps query terms to their corresponding options.
q_options = {
    'Title':'ti',
    'Author':'au',
    'Abstract':'abs',
    'Comment':'co',
    'Journal Reference':'jr',
    'Subject Category':'cat',
    'Report Number':'rn',
    'Id (use id_list instead)':'id',
    'All of the above':'all'
}
# Define pre-closure and post-closure symbols.
preclose = '('
postclose = ')'

# Initialize a global index variable for keeping track of the position in the options list.
idx = 0

# Function to check if a DataFrame has a tag with a given name and return the downloaded value if so.
def check_col_downloaded_value(df, tag, column_name='tag', download_column_name='downloaded'):
  """Checks if the given DataFrame has a tag with the given name and if so, returns the downloaded value.

  Args:
    df (pd.DataFrame): The DataFrame to check.
    tag (str): The name of the tag to check for.
    column_name (str): The name of the column containing the tags.
    download_column_name (str): The name of the column containing the download values.

  Returns:
    bool: True if the DataFrame has a tag with the given name and the downloaded value is True, False otherwise.
  """

  # Check if the DataFrame has a tag with the given name.
  if tag in df[column_name].values:

    # Get the downloaded value for the tag.
    download_value = df[df[column_name] == tag][download_column_name].values[0]

    # Return True if the downloaded value is True, False otherwise.
    return download_value

  else:

    # Return False if the DataFrame does not have a tag with the given name.
    return False


# Function to download a file from a URL and save it to a specified location.
def downloader(url, filepath, file_name):
    """
    Downloads a file from a URL and saves it to a specified location.

    Args:
        url (str): The URL of the file to download.
        filepath (pathlib.Path): The path to the directory where the file should be saved.
        file_name (str): The name of the file to save.
    """

    path = filepath / file_name
    file = Path(path)
    
    # Send a GET request to the URL and store the response.
    response = requests.get(url)

    # Write the content of the response to the file.
    file.write_bytes(response.content)

def flat_same_dim(qs, options):
    """
    Flattens a list of query terms and options while maintaining the same dimensions.

    Args:
        qs (list): A list of lists or tuples representing query terms.
        options (list): A list of options corresponding to the query terms.

    Returns:
        list: A flattened list of query terms and options, where each element is a string of the format "option:value".
    """

    def checker(q, options):
        global idx
        # Check the type of q and perform the appropriate action.
        if isinstance(q, list):
            # If all elements in the list are strings, zip them with options from options[idx:] and increment idx by the length of q.
            if all([isinstance(i, str) for i in q]):
                r = list(f"{opt}:{val}" for val, opt  in zip(q, options[idx:idx+len(q)]))
                idx += len(q)
                return r
            return list(flat_same_dim(q, options))
        elif isinstance(q, tuple):
            if all([isinstance(i, str) for i in q]):
                # If all elements in the tuple are strings, zip them with options from options[idx:] and increment idx by the length of q.
                r = tuple(f"{opt}:{val}" for val, opt in zip(q, options[idx:idx+len(q)]))
                idx += len(q)
                return r
            return tuple(flat_same_dim(q, options))
        elif isinstance(q, str):
            # If q is a string, return a list with a single element of the format "option:value".
            r = list(f"{opt}:{val}" for val, opt in zip([q], options[idx:idx+len(q)]))
            idx += 1
            return r
        else:
            # If q is not a list, tuple, or string, raise an error.
            raise ValueError(f"Unsupported type for query term: {type(q)}")

    # Apply the checker function to each element of qs and collect the results.
    query_parts = [checker(q, options) for q in qs]

    # Return the flattened list of query terms and options.
    return query_parts


# if it list has > 2 elements then AND between elements
# if it list has one element then AND between that element
# the next element
# if it tuple it inharent the OPERATOR that of the parent level
# all the element in tuple put into two prenthses () 
def create_q(qs: list = [], options: list = [], operator: str = ' OR ', check_dict: bool = False, fl_element: str = None):
    """
    Create a query string based on input queries and options.

    Args:
        qs (list): List of queries.
        options (list): List of options.
        operator (str): Logical operator to use between elements.
        check_dict (bool): Not used in the provided code.
        fl_element (str): Not used in the provided code.

    Returns:
        str: The constructed query string.
    """

    # If both qs and options are provided, flatten them into a list of strings
    if qs and options: 
        qs = flat_same_dim(qs, options)
        global idx
        idx = 0

    # If qs has only one element and it's not a tuple or list, wrap it in parentheses with the specified operator
    if not isinstance(qs[0], (tuple, list)) and len(qs) == 1:
        return f'({qs[0]}){operator}'
    def operator_checker(q, qs):
        # Determine the logical operator based on the type of q and qs
        return ' AND ' if isinstance(q, list) or isinstance(q, str) and isinstance(qs, list) else ' OR '
    
    def checker(q, operator, p_operator):
        # Recursively build the query string based on the type of q
        if isinstance(q, list):
            if all([isinstance(i, str) for i in q]):
                return create_q(q, operator=operator, fl_element=[q[0], q[-1]])
            return create_q(q[0], operator=operator, fl_element=[q[0][0], q[0][-1]])
        elif isinstance(q, tuple):
            if all([isinstance(i, str) for i in q]):
                return create_q(q, operator=operator, fl_element=[q[0], q[-1]])
            return create_q(q[0], operator=operator, fl_element=[q[0][0], q[0][-1]])
        else:
            # Wrap the element in parentheses based on its position in the fl_element list
            if fl_element[0]==q: return f'({q}{operator}'
            if fl_element[1]==q: return f'{q}){p_operator}'
            return f'{q}{operator}'


    # Apply the checker function to each element in qs and join them into a single string
    query_parts = [checker(q, operator_checker(q, qs), operator) for q in qs]
    return ''.join(query_parts)
    
    

# if __name__=='__main__':
#     # WRONG EXAMPLE: ====>
#     # qs = [(['KDD', 'cs.cv']), (['ICML', 'cs.gl', 'machine']), ['Adam'], ('VDD', 'cs.cv')]
#     # options = ['co', 'cat', 'co', 'cat', 'ti', 'au', 'co', 'cat']

#     # qs = [(['co:KDD', 'cat:cs.cv'],), [(['co:ICML', 'cat:cs.gl', 'ti:machine'],),], ['au:Adam'], ('co:VDD', 'cat:cs.cv',)]
#     # result_query = create_q(qs)
#     # qs = [(['KDD', 'cs.cv'],), [(['ICML', 'cs.gl', 'machine'],),], ['Adam',], ('VDD', 'cs.cv',), ['cs.AI'], ('NeurIPS OR CIKM OR AAAI',), ]
#     # options = ['co', 'cat', 'co', 'cat', 'ti', 'au', 'co', 'cat', 'cat', 'co']
    
#     qs = [['cs.AI'], ('NeurIPS OR CIKM OR AAAI',), ]
#     options = ['cat', 'co']
#     result_query = create_q(qs, options)
#     print(result_query)