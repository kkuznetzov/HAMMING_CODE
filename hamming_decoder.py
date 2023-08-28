#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sunday August 28 15:30:10 2023

@author: kkuznetzov
"""

from os.path import dirname, join as pjoin
import numpy as np
import os

# Hamming code 7:4, decoder


def decode_word_to_half_byte(word):
    # Values for bits
    # Значения для отдельных бит
    # Get bit values
    # Получим значения бит
    input_bit_1_value = word & 0x01
    input_bit_2_value = (word >> 0x01) & 0x01
    input_bit_3_value = (word >> 0x02) & 0x01
    input_bit_4_value = (word >> 0x03) & 0x01
    check_symbol_123 = (word >> 0x04) & 0x01
    check_symbol_234 = (word >> 0x05) & 0x01
    check_symbol_124 = (word >> 0x06) & 0x01

    # Calculate the syndrome
    # Вычислим синдром
    syndrom_123_r1 = input_bit_1_value ^ input_bit_2_value ^ input_bit_3_value ^ check_symbol_123
    syndrom_234_r2 = input_bit_2_value ^ input_bit_3_value ^ input_bit_4_value ^ check_symbol_234
    syndrom_124_r3 = input_bit_1_value ^ input_bit_2_value ^ input_bit_4_value ^ check_symbol_124

    # Error correction
    # Коррекция ошибки
    if (syndrom_123_r1 == 0x01) and (syndrom_124_r3 == 0x01):
        # Bit 1 error
        input_bit_1_value = (~input_bit_1_value) & 0x01
    if (syndrom_123_r1 == 0x01) and (syndrom_234_r2 == 0x01) and (syndrom_124_r3 == 0x01):
        # Bit 2 error
        input_bit_2_value = (~input_bit_2_value) & 0x01
    if (syndrom_123_r1 == 0x01) and (syndrom_234_r2 == 0x01):
        # Bit 3 error
        input_bit_3_value = (~input_bit_3_value) & 0x01
    if (syndrom_234_r2 == 0x01) and (syndrom_124_r3 == 0x01):
        # Bit 4 error
        input_bit_4_value = (~input_bit_4_value) & 0x01

    output_byte = input_bit_1_value
    output_byte += input_bit_2_value << 0x01
    output_byte += input_bit_3_value << 0x02
    output_byte += input_bit_4_value << 0x03

    return output_byte


# Input data file
# Имя файла с входными данными, в текстовом файле
data_file_in_name = 'coded_data.txt'
data_file_in_name = os.path.join(os.path.dirname(__file__), data_file_in_name)

# Name of the output data file
# Имя выходного файла с данными
data_file_out_name = 'decoded_data.txt'
data_file_out_name = os.path.join(os.path.dirname(__file__), data_file_out_name)

# Open input txt file for reading
# Открываем файл на чтение
data_in_file = open(data_file_in_name, "rb")

# Reading input file
# Читаем входной файл
input_signal_data = bytearray(data_in_file.read())
input_signal_length_bytes = len(input_signal_data)

# Длина выходного файла
output_signal_length_bytes = (input_signal_length_bytes * 4) // 7

# Empty array for output
# Пустой массив для выходных данных
output_signal_data = bytearray(output_signal_length_bytes)

# Coded word, 7 bits
coded_low_word_value = 0
coded_high_word_value = 0
coded_full_word_value = 0

# Input bit and byte, bit counter
input_bit_value = 0
input_byte_value = 0
input_bit_counter = 0

# Counter of output bytes
# Счётчик выходных байт
output_byte_counter = 0

# Half byte
# Четыре бита, половина байта
output_low_half_byte_value = 0
output_high_half_byte_value = 0

# Output byte
# Выходной байт
output_byte_value = 0

# Decoding data
for i in range(input_signal_length_bytes):
    # Get input data byte
    input_byte_value = input_signal_data[i]

    # Put input bits to coded word
    for j in range(0x08):
        # Get high (7) bit value
        input_bit_value = (input_byte_value & 0x80) >> 0x07
        input_byte_value = input_byte_value << 0x01

        # Put bit to word
        coded_full_word_value = coded_full_word_value << 0x01
        coded_full_word_value = coded_full_word_value + input_bit_value

        # Increment bit counter
        # Decode data and put data to output stream
        input_bit_counter += 1
        if input_bit_counter == 14:
            input_bit_counter = 0

            # Get half word
            coded_low_word_value = coded_full_word_value & 0x7F
            coded_high_word_value = (coded_full_word_value >> 0x07) & 0x7F
            coded_full_word_value = 0x00

            # Decode data
            output_low_half_byte_value = decode_word_to_half_byte(coded_low_word_value)
            output_high_half_byte_value = decode_word_to_half_byte(coded_high_word_value)
            output_byte_value = output_low_half_byte_value + (output_high_half_byte_value << 0x04)

            # Put data to output stream
            output_signal_data[output_byte_counter] = output_byte_value

            # Increment output byte
            output_byte_counter += 1

# Write the data file
# Записываем файл с данными
file = open(data_file_out_name, "wb")
file.write(output_signal_data)
file.close()
