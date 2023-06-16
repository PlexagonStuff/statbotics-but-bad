import numpy

from colormath import color_diff_matrix


def _get_lab_color1_vector(color):
    """
    Converts an LabColor into a NumPy vector.

    :param LabColor color:
    :rtype: numpy.ndarray
    """
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return numpy.array([color.lab_l, color.lab_a, color.lab_b])


def _get_lab_color2_matrix(color):
    """
    Converts an LabColor into a NumPy matrix.

    :param LabColor color:
    :rtype: numpy.ndarray
    """
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return numpy.array([(color.lab_l, color.lab_a, color.lab_b)])


# noinspection PyPep8Naming
def delta_e_cie1976(color1, color2):
    """
    Calculates the Delta E (CIE1976) of two colors.
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie1976(color1_vector, color2_matrix)[0]
    return delta_e.item()