import numpy as np

symbol_map = {'character_01_ka': 0, 'character_02_kha': 1, 'character_03_ga': 2,
              'character_04_gha': 3, 'character_05_kna': 4, 'character_06_cha': 5,
              'character_07_chha': 6, 'character_08_ja': 7, 'character_09_jha': 8,
              'character_10_yna': 9, 'character_11_taamatar': 10, 'character_12_thaa': 11,
              'character_13_daa': 12, 'character_14_dhaa': 13, 'character_15_adna': 14,
              'character_16_tabala': 15, 'character_17_tha': 16, 'character_18_da': 17,
              'character_19_dha': 18, 'character_20_na': 19, 'character_21_pa': 20,
              'character_22_pha': 21, 'character_23_ba': 22, 'character_24_bha': 23,
              'character_25_ma': 24, 'character_26_yaw': 25, 'character_27_ra': 26,
              'character_28_la': 27, 'character_29_waw': 28, 'character_30_motosaw': 29,
              'character_31_petchiryakha': 30, 'character_32_patalosaw': 31,
              'character_33_ha': 32, 'character_34_chhya': 33, 'character_35_tra': 34,
              'character_36_gya': 35, 'digit_0': 36, 'digit_1': 37, 'digit_2': 38,
              'digit_3': 39, 'digit_4': 40, 'digit_5': 41, 'digit_6': 42, 'digit_7': 43,
              'digit_8': 44, 'digit_9': 45}

letters = np.array(["क", "ख", "ग", "घ", "ङ",
                    "च", "छ", "ज", "झ", "ञ",
                    "ट", "ठ", "ड", "ढ", "ण",
                    "त", "थ", "द", "ध", "न",
                    "प", "फ", "ब", "भ", "म",
                    "य", "र", "ल", "व", "श",
                    "ष", "स", "ह", "ळ", "क्ष", "ज्ञ",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
