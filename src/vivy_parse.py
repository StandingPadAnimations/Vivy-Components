# BSD 3-Clause License
# 
# Copyright (c) 2024, Mahid Sheikh
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import TextIO
from pathlib import Path
import json

from . import vivy_types as vt

def read_vivy_materials(vivy_materials_dict: dict[str, vt.VIVY_JSON_MATERIAL]) -> dict[str, vt.VivyMaterial]:
    """Reads the "materials" portion of the Vivy JSON.

    vivy_materials_dict: dict[str, vt.VIVY_JSON_MATERIAL]
        The materials portion of the Vivy JSON.

    Returns:  dict[str, vt.VivyMaterial]
    """
    final_dict: dict[str, vt.VivyMaterial] = {}
    for key in vivy_materials_dict:
        md = vivy_materials_dict[key]
        final_dict[key] = vt.VivyMaterial(
            base_material=md["base_material"],
            desc=md["desc"],
            passes=vt.VivyPasses(
                diffuse=md["passes"]["diffuse"],
                specular=(
                    md["passes"]["specular"] if "specular" in md["passes"] else None
                ),
                normal=md["passes"]["normal"] if "normal" in md["passes"] else None,
            ),
            refinements=(
                None
                if "refinements" not in md
                else vt.VivyRefinements(
                    emissive=(
                        md["refinements"]["emissive"]
                        if "emissive" in md["refinements"]
                        else None
                    ),
                    reflective=(
                        md["refinements"]["reflective"]
                        if "reflecive" in md["refinements"]
                        else None
                    ),
                    metallic=(
                        md["refinements"]["metallic"]
                        if "metallic" in md["refinements"]
                        else None
                    ),
                    glass=(
                        md["refinements"]["glass"]
                        if "glass" in md["refinements"]
                        else None
                    ),
                    fallback_s=(
                        md["refinements"]["fallback_s"]
                        if "fallback_s" in md["refinements"]
                        else None
                    ),
                    fallback_n=(
                        md["refinements"]["fallback_n"]
                        if "fallback_n" in md["refinements"]
                        else None
                    ),
                    fallback=(
                        md["refinements"]["fallback"]
                        if "fallback" in md["refinements"]
                        else None
                    ),
                )
            ),
        )
    
    return final_dict

def read_vivy_mappings(vivy_mappings_dict: dict[str, list[vt.VIVY_JSON_MAPPING]]) -> dict[str, list[vt.VivyMapping]]:
    """Reads the "mappings" portion of the Vivy JSON.

    vivy_mappings_dict: dict[str, list[vt.VIVY_JSON_MAPPING]]
        The mapping portion of the Vivy JSON.

    Returns: dict[str, list[vt.VivyMapping]] 
    """
    final_dict: dict[str, list[vt.VivyMapping]] = {}
    for mat in vivy_mappings_dict:
        maps = vivy_mappings_dict[mat]
        final_dict[mat] = []
        for m in maps:
            final_dict[mat].append(vt.VivyMapping(
                                   material=m["material"],
                                   refinement=m["refinement"] if "refinement" in m else None 
                            ))
    return final_dict

def dict_to_vivy_data(raw_dict: vt.VIVY_JSON_TOP_LEVEL) -> vt.VivyData:
    """Converts a raw dictionary into a dictionary mapping
    names to a VivyMaterial dataclass.

    raw_dict: VIVY_JSON_TOP_LEVEL
        The raw dictionary from the Vivy JSON.

    Returns: dict[str, VivyMaterial]
    """
    
    return vt.VivyData(
            materials=read_vivy_materials(raw_dict["materials"]),
            mapping=read_vivy_mappings(raw_dict["mapping"])
    )

def read_vivy_json(f: TextIO) -> vt.VivyData:
    """Reads a file object and parses the contents.

    f: TextIO
        The file object to load JSON
        data from.

    Returns: dict[str, VivyMaterial]
    """
    data: vt.VIVY_JSON_TOP_LEVEL = json.load(f)
    return dict_to_vivy_data(data)


def get_vivy_data(file: Path) -> vt.VivyData:
    """Opens a file at the specified path and parses the contents.

    file: Path
        The filepath of the file to parse.

    Returns: dict[str, VivyMaterial]
    """
    with open(file, "r") as f:
        return read_vivy_json(f)
