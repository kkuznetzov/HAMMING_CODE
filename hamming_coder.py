#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday August 27 19:30:10 2023

@author: kkuznetzov
"""

from os.path import dirname, join as pjoin
import numpy as np
import os

# Hamming code 7:4, encoder


def encode_half_byte_to_word(half_byte):
    # Values for bits
    # Значения для отдельных бит
    # Get bit values
    # Получим значения бит
    input_bit_1_value = half_byte & 0x01
    input_bit_2_value = (half_byte >> 0x01) & 0x01
    input_bit_3_value = (half_byte >> 0x02) & 0x01
    input_bit_4_value = (half_byte >> 0x03) & 0x01

    # Calculate the values of the check symbols
    # Вычисляем значения проверочных символов
    check_symbol_123 = input_bit_1_value ^ input_bit_2_value ^ input_bit_3_value
    check_symbol_234 = input_bit_2_value ^ input_bit_3_value ^ input_bit_4_value
    check_symbol_124 = input_bit_1_value ^ input_bit_2_value ^ input_bit_4_value

    # Coded word, 7 bits
    # Кодированное слово
    # Make the encoded word
    # Собираем кодированное слово
    coded_word = input_bit_1_value
    coded_word += input_bit_2_value << 0x01
    coded_word += input_bit_3_value << 0x02
    coded_word += input_bit_4_value << 0x03
    coded_word += check_symbol_123 << 0x04
    coded_word += check_symbol_234 << 0x05
    coded_word += check_symbol_124 << 0x06

    return coded_word


# Input data file
# Имя файла с входными данными, в текстовом файле
data_file_in_name = 'raw_data.txt'
data_file_in_name = os.path.join(os.path.dirname(__file__), data_file_in_name)

# Name of the output data file
# Имя выходного файла с данными
data_file_out_name = 'coded_data.txt'
data_file_out_name = os.path.join(os.path.dirname(__file__), data_file_out_name)

# Open input txt file for reading
# Открываем файл на чтение
data_in_file = open(data_file_in_name, "rb")

# Reading input file
# Читаем входной файл
input_signal_data = bytearray(data_in_file.read())
input_signal_length_bytes = len(input_signal_data)
input_signal_length_bits = input_signal_length_bytes * 8

# Output file length, rounding up to integer number of bytes
# Длина выходного файла, округление до целого числа байт
output_signal_length_bits = (input_signal_length_bits / 4) * 7
output_signal_length_bits = output_signal_length_bits + (8 - output_signal_length_bits % 8)
output_signal_length_bytes = int(output_signal_length_bits // 8)

# Empty array for output
# Пустой массив для выходных данных
output_signal_data = bytearray(output_signal_length_bytes)

# Half byte
# Четыре бита, половина байта
input_low_half_byte_value = 0
input_high_half_byte_value = 0

# Coded word, 7 bits
coded_low_word_value = 0
coded_high_word_value = 0
coded_full_word_value = 0

# Output bit and byte
# Выходной бит и байт
output_bit_value = 0
output_byte_value = 0

# Counter of output bits and bytes
# Счётчик выходных бит и байт
output_bit_counter = 0
output_byte_counter = 0

# Encoding data
for i in range(input_signal_length_bytes):
    # Select four high bits
    input_high_half_byte_value = (input_signal_data[i] >> 0x04) & 0x0F

    # Encode half byte to 7 bits word
    coded_high_word_value = encode_half_byte_to_word(input_high_half_byte_value)

    # Select four low bits
    input_low_half_byte_value = (input_signal_data[i] & 0x0F)

    # Encode half byte to 7 bits word
    coded_low_word_value = encode_half_byte_to_word(input_low_half_byte_value)

    # 14 bits size word
    coded_full_word_value = (coded_high_word_value << 0x07) + coded_low_word_value

    # Put the encoded word into the output stream
    # Помещаем кодированное слово в выходной поток
    for j in range(14):
        # Get high (14) bit value
        output_bit_value = (coded_full_word_value & 0x2000) >> 13

        # Shift word
        coded_full_word_value = coded_full_word_value << 0x01

        # Put bit to byte
        output_byte_value = output_byte_value << 0x01
        output_byte_value = output_byte_value + output_bit_value

        # Increment bit counter
        # And put data to output
        output_bit_counter += 1
        if output_bit_counter == 0x08:
            output_bit_counter = 0
            output_signal_data[output_byte_counter] = output_byte_value
            output_byte_value = 0
            output_byte_counter += 1

# Last byte
if output_bit_counter == 0x04:
    output_signal_data[output_byte_counter] = output_byte_value << 0x04

# Write the data file
# Записываем файл с данными
file = open(data_file_out_name, "wb")
file.write(output_signal_data)
file.close()








