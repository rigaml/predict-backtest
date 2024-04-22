# given a list of integers 'r' that are indexes on list 'a' create a new list 'b' removing from 'a' the indexes in 'r' 
def remove_indexes(lst, indexes):
    # Create a new list 'b' without the elements at the specified indices
    result = [lst[i] for i in range(len(lst)) if i not in indexes]
    return result

# Example usage:
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
indices_to_remove = [1, 3, 5]

b = remove_indexes(a, indices_to_remove)
print("List a:", a)
print("List b:", b)
