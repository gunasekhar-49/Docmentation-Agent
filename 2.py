# Function 1: Add two numbers
def add_numbers(a, b):

    return a + b


def is_palindrome(text):

    text = text.lower().replace(" ", "")
    return text == text[::-1]



def find_max(numbers):

    if not numbers:
        return None
    return max(numbers)



if __name__ == "__main__":

    sum_result = add_numbers(10, 20)
    print("Sum:", sum_result)


    word = "Madam"
    print("Is Palindrome:", is_palindrome(word))


    nums = [5, 12, 3, 19, 7]
    print("Maximum Number:", find_max(nums))
    