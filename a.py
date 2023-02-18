
def rev_string(string):
    '''
    description: A function that reverses a string

    input: A string -> String(string)

    output: A reversed string -> String(reversed_string)
    '''
    return string[::-1] # the string is reversed by slicing the string from the end to the beginning

#2
print(rev_string("Hello World"))

def calculate(numbers:list):
    '''
    description: A function that calculates the average,mean,median and stdev

    input: A list of integers -> List(int(numbers))

    output: A tuple of average,mean,median and stdev -> Tuple(float(average),float(stdev),float(median))
    '''
    total=0 
    for num in numbers:  #this for loop iterates over the list and adds the numbers to the total variable intially set to 0
        total+=num 
    average=total/len(numbers)  # the average is calculated by dividing the total by the length of the list
    variance=sum([(num-average)**2 for num in numbers])/len(numbers) # the variance is calculated by subtracting the average from each number in the list and squaring the result and then dividing the sum of the results by the length of the list
    stdev=variance**0.5 # the standard deviation is calculated by taking the square root of the variance
    sorted_num=sorted(numbers) # the list is sorted in ascending order
    if len(sorted_num)%2==0: # the median is calculated by sorting the list and then finding the middle number if the list is odd and if the list is even then the median is calculated by adding the two middle numbers and dividing the sum by 2
        median=(sorted_num[len(sorted_num)//2]+sorted_num[len(sorted_num)//2-1])/2 
    else:
        median=sorted_num[len(sorted_num)//2]
    return total,average,stdev,median


print(calculate([43, 61, 92, 25, 20, 44, 90, 98, 89, 60]))
import re


# def convert_lower_to_upper(string):
#     # regex pattern to match lowercase alphabetic characters
#     pattern = re.compile(r'[a-z]')
#     # loop through each character in the string and replace lowercase alphabetic characters with uppercase ones
#     output_str = ''
#     for char in string:
#         if pattern.match(char):
#             output_str += chr(ord(char) - 32)
#         else:
#             output_str += char
#     return output_str

def convert_lower_to_upper(string):
# loop through each character in the string and replace lowercase alphabetic characters with uppercase ones
    output_str = ''
    for char in string:
    # check if the character is a lowercase alphabetic character
        if 'a' <= char <= 'z':
    # convert the character to uppercase by adding the difference between the ASCII codes of 'a' and 'A'
            output_str += chr(ord(char) - ord('a') + ord('A'))
        else:
            output_str += char
    return output_str

if  __name__=="__main__":
    print(convert_lower_to_upper("Hello World"))