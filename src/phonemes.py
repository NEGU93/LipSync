import numpy as np


class Phoneme:
    def __init__(self, phoneme_name, formants):
        self.phoneme_name = phoneme_name
        self.formants = formants


class PhonemeA(Phoneme):
    def __init__(self):
        # Phoneme.__init__(self, '/a/', np.array([753, 1278, 2483]))
        Phoneme.__init__(self, '/a/', np.array([850, 1610]))


class PhonemeE(Phoneme):
    def __init__(self):
        # Phoneme.__init__(self, '/e/', np.array([406, 1955, 2540]))
        Phoneme.__init__(self, '/e/', np.array([350, 2300]))


class PhonemeI(Phoneme):
    def __init__(self):
        # Phoneme.__init__(self, '/i/', np.array([297, 2150, 2925]))
        Phoneme.__init__(self, '/i/', np.array([220, 2400]))


class PhonemeO(Phoneme):
    def __init__(self):
        # Phoneme.__init__(self, '/o/', np.array([411, 832, 2376]))
        Phoneme.__init__(self, '/o/', np.array([360, 640]))


class PhonemeU(Phoneme):
    def __init__(self):
        # Phoneme.__init__(self, '/u/', np.array([345, 799, 2351]))
        Phoneme.__init__(self, '/u/', np.array([320, 595]))


def best_phoneme(formants):
    phonemes = [PhonemeA(), PhonemeE(), PhonemeI(), PhonemeO(), PhonemeO(), PhonemeU()]
    mean_first_formant = 301
    mean_second_formant = 1434
    for it in range(0, len(phonemes)):
        phoneme1 = []
        phoneme1.append(phonemes[it].formants[0] / mean_first_formant)
        phoneme1.append(phonemes[it].formants[1] / mean_second_formant)
        phoneme1 = np.array(phoneme1)

        phoneme2 = []
        phoneme2.append(formants[0] / mean_first_formant)
        phoneme2.append(formants[1] / mean_second_formant)
        phoneme2 = np.array(phoneme2)

        if it == 0:
            min_error = ((phoneme1 - phoneme2) ** 2).mean(axis=0)
            phoneme_matched = phonemes[it]
        else:
            if ((phoneme1 - phoneme2) ** 2).mean(axis=0) < min_error:
                min_error = ((phoneme1 - phoneme2) ** 2).mean(axis=0)
                phoneme_matched = phonemes[it]

    return phoneme_matched