import formula
import random
import math

def generate_formula(category, number):
    formulas = formula.Formulas()
    for i in range(number):
        if(category==formula.POLYNOMIAL):
            f = generate_polynomial()
            formulas.put(category, f)
        elif(category==formula.POLYHEDRON):
            f = generate_polyhedron()
            formulas.put(category, f)

    return formulas

def generate_polynomial():
    #TODO variable number is up to 10
    y=random.randint(-10,10)
    variableNumber=random.randint(1,10)
    variableNumber=2
    coefficientList=[]
    for i in range(variableNumber):
        powerNumber=random.randint(1,4)
        powerNumber=1
        tmpList=[]
        for j in range (powerNumber):
            tmpList.append(random.randint(-5,5))
        coefficientList.append(tmpList)
    coefficientList.append(y)
    return coefficientList

def generate_polyhedron():
    #TODO variable number is up to 10
    # generate center point and radius and number of circles
    num_of_center = random.randint(1, 10)
    num_of_dimension = random.randint(2, 10)
    # num_of_dimension = 2
    centers = []
    radiuses = []
    for i in range(num_of_center):
        center = []
        for j in range(num_of_dimension):
            center_coordinate = random.randint(-300, 300)
            center.append(center_coordinate)
        radius = random.randint(10, 50)
        centers.append(center)
        radiuses.append(radius)
    formula = [centers, radiuses]

    return formula

def generate_specific_formula():
    formulas = formula.Formulas()
    formulas.put(formula.POLYNOMIAL, [1, 2])
    formulas.put(formula.POLYHEDRON, [[[1, 1], [-1, -1]], [0.5, 0.5]])
    # formulas.put([[[12,0],[-12,0]],[4,4]])

    return formulas