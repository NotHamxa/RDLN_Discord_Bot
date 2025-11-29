def recursive_multiple(val, lst, n1, newlst):
    """
    Recursive function to find all multiples of val in lst.
    
    Args:
        val: The number for which multiples are being calculated (dictionary key)
        lst: The original list of numbers
        n1: The number of elements in the original list (used as index counter)
        newlst: A list that will hold elements that are multiples of val
    
    Note: This function does NOT use loops or return values - only recursion.
    """
    # Base case: when n1 reaches 0, we've checked all elements
    if n1 > 0:
        # Check if the current element (at index n1-1) is a multiple of val
        current_element = lst[n1 - 1]
        if current_element % val == 0:
            newlst.append(current_element)
        
        # Recursive call with decremented n1
        recursive_multiple(val, lst, n1 - 1, newlst)


def main():
    """
    Main function that takes a list as input, iterates over elements,
    and builds a dictionary where keys are list elements and values are
    lists of their multiples.
    """
    # Take input from user
    lst = list(eval(input()))
    
    # Initialize the result dictionary
    result = {}
    
    # Iterate over each element in the list using a loop
    for val in lst:
        # Create a new list to hold multiples for this value
        newlst = []
        
        # Call recursive function to find all multiples
        recursive_multiple(val, lst, len(lst), newlst)
        
        # Sort the multiples list to match expected output format
        newlst.sort()
        
        # Update the dictionary with this key-value pair
        result[val] = newlst
    
    # Print the result dictionary
    print(result)


if __name__ == "__main__":
    main()
