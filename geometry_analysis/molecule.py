"""
molecule.py
A python package for the MolSSI Software Summer School.

Contains a molecule class
"""

#module w.o. 2 fxns

import numpy as np
#only import fxns that you need! you need .measure (the directory we're in)
#if you didnt import, you would need to do measure.thing
from .measure import calculate_angle, calculate_distance
#below works too, if you know the directory
#import geometry_analysis.measure import calculate_angle, calculate distance
#import .measure import * if you want to pass everything

class Molecule:
    def __init__(self, name, symbols, coordinates):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("Name is not a string.")

        self.symbols = symbols
        self._coordinates = coordinates
        self.bonds = self.build_bond_list()

    @property  #num atoms would be fxn w/o @property, use molecule.numatoms()
    def num_atoms(self):
        return len(self._coordinates)

    @property
    def coordinates(self): #just self
        return self._coordinates

    @coordinates.setter  #setter will udpate if bonds change, refers back to @property def coordinates
    def coordinates(self, new_coordinates): #self and some new parameter
        self._coordinates = new_coordinates  #private var. passed from coordinates, bonds reformed
        self.bonds = self.build_bond_list()

    def build_bond_list(self, max_bond=2.93, min_bond=0):
        """
        Build a list of bonds based on a distance criteria.

        Atoms within a specified distance of one another will be considered bonded.

        Parameters
        ----------
        max_bond : float, optional

        min_bond : float, optional

        Returns
        -------
        bond_list : list
            List of bonded atoms. Returned as list of tuples where the values are the atom indices.
        """

        bonds = {}

        for atom1 in range(self.num_atoms):
            for atom2 in range(atom1, self.num_atoms):
                distance = calculate_distance(self.coordinates[atom1], self.coordinates[atom2])

                if distance > min_bond and distance < max_bond:
                    bonds[(atom1, atom2)] = distance

        return bonds


if __name__ == "__main__":
    # Do something if this file is invoked on its own
    random_coordinates = np.random.random([3, 3])
    name = "my molecule"
    symbols = ["H", "O", "O"]
    my_molecule = Molecule(name, symbols, random_coordinates)
    print(F'There are {len(my_molecule.bonds)} bonds')
    print(F'The coordinates are {my_molecule.coordinates}')

    #random_coordinates = np.random.random([3,3])
    random_coordinates[0] += 100  #first coordinate, extending bond distance

    my_molecule.coordinates = random_coordinates

    print(F'There are {len(my_molecule.bonds)} bonds')
    print(F'\n\nThe coordinates are {my_molecule.coordinates}')
