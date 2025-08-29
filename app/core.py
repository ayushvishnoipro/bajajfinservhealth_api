"""
Core processing logic for the BFHL API.
Contains helper functions for token classification and processing.
"""
import re
from typing import List, Tuple


def split_tokens(data: List[str]) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Split input data into categorized lists.
    
    Args:
        data: List of string tokens to classify
        
    Returns:
        Tuple of (odd_numbers, even_numbers, alphabets_upper, special_characters)
    """
    odd_numbers = []
    even_numbers = []
    alphabets_upper = []
    special_characters = []
    
    for token in data:
        token_str = str(token)  # Ensure it's a string
        
        # Check if token is a pure number (digits only)
        if re.match(r'^\d+$', token_str):
            num = int(token_str)
            if num % 2 == 0:
                even_numbers.append(token_str)
            else:
                odd_numbers.append(token_str)
        # Check if token is pure alphabetic (letters only)
        elif re.match(r'^[A-Za-z]+$', token_str):
            alphabets_upper.append(token_str.upper())
        else:
            # Anything else is a special character
            special_characters.append(token_str)
    
    return odd_numbers, even_numbers, alphabets_upper, special_characters


def sum_numbers_as_string(odd_nums: List[str], even_nums: List[str]) -> str:
    """
    Calculate the sum of all numeric tokens and return as string.
    
    Args:
        odd_nums: List of odd number strings
        even_nums: List of even number strings
        
    Returns:
        Sum as a string
    """
    total = 0
    
    # Sum all odd numbers
    for num_str in odd_nums:
        total += int(num_str)
    
    # Sum all even numbers
    for num_str in even_nums:
        total += int(num_str)
    
    return str(total)


def alternating_caps_reverse_concat(data: List[str]) -> str:
    """
    Extract alphabetic characters, reverse, and apply alternating capitalization.
    
    Rule:
    1. Extract all alphabetic characters from tokens in order
    2. Reverse the character sequence
    3. Apply alternating caps: UPPER for 1st char, lower for 2nd, UPPER for 3rd, etc.
    
    Args:
        data: List of input tokens
        
    Returns:
        Processed string with alternating capitalization
    """
    # Step 1: Extract all alphabetic characters in order
    alpha_chars = []
    for token in data:
        token_str = str(token)
        for char in token_str:
            if char.isalpha():
                alpha_chars.append(char)
    
    # Step 2: Reverse the character sequence
    alpha_chars.reverse()
    
    # Step 3: Apply alternating capitalization
    result = []
    for i, char in enumerate(alpha_chars):
        if i % 2 == 0:  # Even index (0, 2, 4, ...) -> uppercase
            result.append(char.upper())
        else:  # Odd index (1, 3, 5, ...) -> lowercase
            result.append(char.lower())
    
    return ''.join(result)
