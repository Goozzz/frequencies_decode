# -*- coding: utf-8 -*-
'''
Module for text decoding.
'''

import textstatistics
import random


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

    return u''.join(result)


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
    original_alphabet = list(u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

    alphabet = language.get_alphabet()
    alphabet = {char: frequency for (char, frequency) in
                alphabet.items()}
    alphabet_encode_text = textstatistics.get_char_frequencies(text)
    alphabet_encode_text = {char: frequency for (char, frequency) in
                            alphabet_encode_text.items() if char in original_alphabet}
    dif_dict = {key: 0 for key in alphabet.keys()
                if key not in alphabet_encode_text.keys()}
    alphabet_encode_text.update(dif_dict)

    list_alphabet = list(alphabet.items())   
    list_alphabet_encode_text = list(alphabet_encode_text.items())

    char_to_char = {}
    for (item_list_1, item_list_2) in zip(list_alphabet, list_alphabet_encode_text):
        char_to_char[item_list_2[0]] = item_list_1[0]

    decoded_text = ''

    for char in text:
        if char in original_alphabet:
            decoded_text += char_to_char[char]
        else:
            decoded_text += char

    word_fitness = evalutate_decoding(decoded_text, language)

    while word_fitness != 1.0:
        old_list = list_alphabet.copy()
        n = 0
        while n < 32:
            n += 1
            i = 0
            old_list = list_alphabet.copy()
            while i < len(list_alphabet) - 1:
                if (i + n) > len(list_alphabet_encode_text) - 1:
                    break
                list_alphabet[i], list_alphabet[i + n] =  list_alphabet[i + n], list_alphabet[i] 
                
                char_to_char = {}
                for (item_list_1, item_list_2) in zip(list_alphabet, list_alphabet_encode_text):
                    char_to_char[item_list_2[0]] = item_list_1[0]

                decoded_text = ''
                for char in text:
                    if char in original_alphabet:
                        decoded_text += char_to_char[char]
                    else:
                        decoded_text += char

                new_word_fitness = evalutate_decoding(decoded_text, language)

                if new_word_fitness > word_fitness:
                    word_fitness = new_word_fitness
                    old_list = list_alphabet.copy()
                    i += 1
                else:
                    list_alphabet = old_list.copy()
                    i += 1

                if word_fitness == 1.0:
                    return decoded_text

    return decoded_text
