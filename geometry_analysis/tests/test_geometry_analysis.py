"""
Unit and regression test for the geometry_analysis package.
"""

# Import package, test suite, and other packages as needed
import geometry_analysis
import numpy as np
import pytest
import sys

#define fixtures at the top
@pytest.fixture() #this makes a structure or variable available to whole test, no need to define in each test
def water_molecule():
    name = "water"
    symbols = ["H", "O", "H"]
    coordinates = np.array([[2,0,0], [0,0,0], [-2,0,0]])

    water = geometry_analysis.Molecule(name, symbols, coordinates)

    return water


def test_create_failure(): #this function tests if an error is raised
    name = 25
    symbols = ["H","O","H"]
    coordinates = np.zeros([3,3])

    with pytest.raises(TypeError): #we know what the error would be
        water = geometry_analysis.Molecule(name, symbols, coordinates)

    #return water

#if we want to use it in our test fxn, we must pass it as an argument to our test fxn
def test_molecule_set_coordinates(water_molecule):
    """Test that bond list is rebuilt when we reset coordinates."""

    num_bonds = len(water_molecule.bonds)

    assert num_bonds==2
    new_coordinates = np.array([[5,0,0], [0,0,0], [-2,0,0]]) #move one of the coordinates far away
    water_molecule.coordinates = new_coordinates #update the coordinates

    new_bonds = len(water_molecule.bonds)
    assert new_bonds ==1
    #check to see if the coordinates are updated
    assert np.array_equal(new_coordinates, water_molecule.coordinates)


def test_geometry_analysis_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "geometry_analysis" in sys.modules

def test_calculate_distance():
    """Test the calculate_distance function"""

    r1 = np.array([0,0,-1])
    r2 = np.array([0,1,0])

    expected_distance = np.sqrt(2.)
    calculated_distance = geometry_analysis.calculate_distance(r1,r2)
    assert expected_distance == calculated_distance

def test_calculate_angle_90():
    """Test the calculate_angle function"""
    r1 = np.array([1,0,0])
    r2 = np.array([0,0,0])
    r3 = np.array([0,1,0])

    expected_value = 90
    calculated_value = geometry_analysis.calculate_angle(r1,r2,r3,degrees=True)

    assert expected_value == calculated_value

def test_calculate_angle_60():
    """Test the calculate_angle function"""
    r1 = np.array([0,0,-1])
    r2 = np.array([0,1,0])
    r3 = np.array([1,0,0])

    expected_value = 60
    calculated_value = geometry_analysis.calculate_angle(r1,r2,r3,degrees=True)

    #evaluate to true of close enough
    assert np.isclose(expected_value, calculated_value) #add ,rtol=... to change default tolerance
    #assert expected_value == calculated_value will be off, but it's essentially right

#special decorator, test variables in argument
@pytest.mark.parametrize("p1, p2, p3, expected_angle", [
    (np.array([1,0,0]), np.array([0,0,0]), np.array([0,1,0]), 90 ), #3inputs and expected angle
    (np.array([0,0,-1]), np.array([0,1,0]), np.array([1,0,0]), 60 ),
])
def test_calculate_angle(p1, p2, p3, expected_angle):

        calculated_angle = geometry_analysis.calculate_angle(p1, p2, p3, degrees=True)
        assert np.isclose(expected_angle, calculated_angle)
