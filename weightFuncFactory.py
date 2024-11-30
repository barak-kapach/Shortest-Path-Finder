"""
in this file we will write the weight functions and main funcions that based on the slope
value we will choose the relevant weight function
"""
import math


def combined_weight_and_distance(slope, factor, distance):
    """
    This function will return the combined weight and distance
    :param slope: the slope value
    :param factor: the factor that we want to multiply the slope
    :param distance: the distance between the two nodes
    :return: the combined weight and distance
    """
    return (1 + slope ** factor) * distance


def steep_hills_high_punishment(slope, factor, distance):
    """
    This function will return the weight of the edge based on the slope value
    :param slope: the slope value
    :param factor: the factor that we want to multiply the slope
    :param distance: the distance between the two nodes
    :return: the weight of the edge
    """
    return math.exp(factor * slope) * distance
