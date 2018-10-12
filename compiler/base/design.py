from hierarchy_design import hierarchy_design
import contact
import globals
import verify
import debug
import os
from globals import OPTS


class design(hierarchy_design):
    """
    This is the same as the hierarchy_design class except it contains
    some DRC constants and analytical models for other modules to reuse.

    """

    def __init__(self, name):
        hierarchy_design.__init__(self,name)
        
        self.setup_drc_constants()
        self.setup_multiport_constants()

        self.m1_pitch = max(contact.m1m2.width,contact.m1m2.height) + max(self.m1_space, self.m2_space)
        self.m2_pitch = max(contact.m2m3.width,contact.m2m3.height) + max(self.m2_space, self.m3_space)
        # SCMOS doesn't have m4...
        #self.m3_pitch = max(contact.m3m4.width,contact.m3m4.height) + max(self.m3_space, self.m4_space)
        self.m3_pitch = self.m2_pitch

    def setup_drc_constants(self):
        """ These are some DRC constants used in many places in the compiler."""
        from tech import drc
        self.well_width = drc["minwidth_well"]
        self.poly_width = drc["minwidth_poly"]
        self.poly_space = drc["poly_to_poly"]        
        self.m1_width = drc["minwidth_metal1"]
        self.m1_space = drc["metal1_to_metal1"]
        self.m2_width = drc["minwidth_metal2"]
        self.m2_space = drc["metal2_to_metal2"]        
        self.m3_width = drc["minwidth_metal3"]
        self.m3_space = drc["metal3_to_metal3"]
        self.active_width = drc["minwidth_active"]
        self.contact_width = drc["minwidth_contact"]

        self.poly_to_active = drc["poly_to_active"]
        self.poly_extend_active = drc["poly_extend_active"]
        self.contact_to_gate = drc["contact_to_gate"]
        self.well_enclose_active = drc["well_enclosure_active"]
        self.implant_enclose_active = drc["implant_enclosure_active"]
        self.implant_space = drc["implant_to_implant"]
        
    def setup_multiport_constants(self):
        """ These are contants and lists that aid multiport design """
        self.total_write = OPTS.num_rw_ports + OPTS.num_w_ports
        self.total_read = OPTS.num_rw_ports + OPTS.num_r_ports
        self.total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports
        self.num_rw_ports = OPTS.num_rw_ports
        
        # Port indices used for data, address, and control signals
        # Port IDs used to identify port type
        self.write_index = []
        self.read_index = []
        self.port_id = []
        port_number = 0
        
        for port in range(OPTS.num_rw_ports):
            self.write_index.append(port_number)
            self.read_index.append(port_number)
            self.port_id.append("rw")
            port_number += 1
        for port in range(OPTS.num_w_ports):
            self.write_index.append(port_number)
            self.port_id.append("w")
            port_number += 1
        for port in range(OPTS.num_r_ports):
            self.read_index.append(port_number)
            self.port_id.append("r")
            port_number += 1

    def analytical_power(self, proc, vdd, temp, load):
        """ Get total power of a module  """
        total_module_power = self.return_power()
        for inst in self.insts:
            total_module_power += inst.mod.analytical_power(proc, vdd, temp, load)
        return total_module_power
    
    def __str__(self):
        """ override print function output """
        pins = ",".join(self.pins)
        insts = ["    {}".format(x) for x in self.insts]
        objs = ["    {}".format(x) for x in self.objs]  
        s = "********** design {0} **********\n".format(self.name)
        s += "\n  pins ({0})={1}\n".format(len(self.pins), pins)
        s += "\n  objs ({0})=\n{1}".format(len(self.objs), "\n".join(objs))
        s += "\n  insts ({0})=\n{1}\n".format(len(self.insts), "\n".join(insts))
        return s
