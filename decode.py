# -*- coding: utf-8 -*-
'''
Module for text decoding.
'''

import textstatistics


def encode_text(text, code):
    '''
    Encodes the text with a substitution cipher defined with the code.
    Argument "code" is a dictionary with characters as keys 
    and corresponding coding characters as values. 
    For example:
        code = {'a': 'z', 'b': 'y' , 'c': 'x'}
    '''
    result = []
    for char in text:
        encoded_char = code.get(char, char)
        result.append(encoded_char)
        
    return  u''.join(result)


def evalutate_decoding(text, language):
    '''
    Evaluates how the decoded text corresponds to the language.
    Returns estimated fitness as a float value from the range [0; 1], where
    0 means doesn't correspond at all,
    1 means all words are correct.
    '''
    fitness_sum = 0.0
    words = textstatistics.split_to_words(text)
    for word in words:
        fitness_sum += language.word_fitness(word)
    return fitness_sum / len(words)


def decode_text(text, language):
    '''
    Decodes the text encoded with a substitution cipher
    '''
    
    alphabet = language.get_alphabet()
    alphabet_encode_text = textstatistics.get_char_frequencies(text)
    alphabet_encode_text = {char: frequency for (char, frequency) in 
                    alphabet_encode_text.items() if char in alphabet}
    
    #dictionary recovery for substitution
    char_to_char = dict()
    for encode_char in alphabet_encode_text.keys(): 
        for char in alphabet.keys():
            if alphabet_encode_text[encode_char] == alphabet[char]:
                char_to_char[encode_char] = char
                alphabet_encode_text[encode_char] = -1
                alphabet[char] = -1
                
    decoded_text = ''
    for char in text:
        if char in alphabet:
            decoded_text += char_to_char[char]
        else:
            decoded_text += char
    
    return decoded_text
