from matador.utils.cell_utils import cart2abc, cart2frac


def optimade_to_basic_cif(structure):
    """ A simple CIF creator that is enough to trick ChemDoodle. """

    cif_string = ""
    lattice_abc = cart2abc(structure.attributes.lattice_vectors)
    positions_frac = cart2frac(
        structure.attributes.lattice_vectors,
        structure.attributes.cartesian_site_positions,
    )
    cif_string += f"_cell_length_a {lattice_abc[0][0]}\n"
    cif_string += f"_cell_length_b {lattice_abc[0][1]}\n"
    cif_string += f"_cell_length_c {lattice_abc[0][2]}\n"
    cif_string += f"_cell_angle_alpha {lattice_abc[1][0]}\n"
    cif_string += f"_cell_angle_beta {lattice_abc[1][1]}\n"
    cif_string += f"_cell_angle_gamma {lattice_abc[1][2]}\n"
    cif_string += "loop_\n"
    cif_string += "_atom_site_label\n"
    cif_string += "_atom_site_symbol\n"
    cif_string += "_atom_site_fract_x\n"
    cif_string += "_atom_site_fract_y\n"
    cif_string += "_atom_site_fract_z\n"

    print(structure.attributes.species_at_sites)
    for atom, pos in zip(structure.attributes.species_at_sites, positions_frac):
        cif_string += f"{atom} {atom} {pos[0]} {pos[1]} {pos[2]}\n"

    print(cif_string)

    return cif_string


__all__ = ["optimade_to_basic_cif"]
