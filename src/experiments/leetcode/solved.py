def removeElement(nums, val):
    """
    Removes all occurrences of val in nums in-place and returns the number of elements in nums which are not equal to val.
    :param nums: list of integers
    :param val: integer
    :return: integer
    """
    # initialize two pointers, one for iterating through the array and one for keeping track of the next non-val index
    i = 0
    non_val_index = 0

    # iterate through the array
    while i < len(nums):
        # if the current element is not equal to val, swap it with the element at the next non-val index
        if nums[i] != val:
            nums[i], nums[non_val_index] = nums[non_val_index], nums[i]
            # increment the non-val index
            non_val_index += 1
        # increment the iterator
        i += 1

    # return the non-val index as the number of elements in nums which are not equal to val
    return non_val_index


# Custom Judge:
# The judge will test your solution with the following code:
nums = [3, 2, 2, 3]  # Input array
val = 3  # Value to remove
expectedNums = [2, 2]  # The expected answer with correct length.
# It is sorted with no values equaling val.
k = removeElement(nums, val)  # Calls your implementation
assert k == len(
    expectedNums
)  # Checks if the returned k is equal to the expected length
nums.sort()  # Sort the first k elements of nums
for i in range(k):
    print(nums[i], expectedNums[i])
    assert (
        nums[i] == expectedNums[i]
    )  # Checks if the first k elements of nums are equal to the expected elements
