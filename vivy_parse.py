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

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, TextIO, TypedDict
from pathlib import Path
import json

# All of these TypedDict classes
# are used for function annotations
# so that my IDE doesn't scream at me
#
# Sadly my IDE still screams at me for 
# the use of deprecated annotations, as
# we have to support 3.7

class VIVY_JSON_PASSES(TypedDict):
    """
    TypedDict representation of passes
    in Vivy JSON
    """
    diffuse: str
    specular: Optional[str]
    normal: Optional[str]

class VIVY_JSON_REFINE(TypedDict):
    """
    TypedDict representation of 
    refinements in Vivy JSON
    """
    emissive   : Optional[str]
    reflective : Optional[str] 
    metallic   : Optional[str]
    glass      : Optional[str]
    fallback_n : Optional[str]
    fallback_s : Optional[str]
    fallback   : Optional[str]

class VIVY_JSON_MATERIAL(TypedDict): 
    """
    TypedDict representation of 
    materials in Vivy JSON
    """
    base_material : str
    desc          : str
    passes        : VIVY_JSON_PASSES
    refinements   : VIVY_JSON_REFINE

class VIVY_JSON_MAPPING(TypedDict):
    """
    TypedDict representation of
    mappings in Vivy JSON
    """
    material: str 
    refinement: str

class VIVY_JSON_TOP_LEVEL (TypedDict):
    """
    TypedDict representation of all
    items in the Vivy JSON
    """
    materials : Dict[str, VIVY_JSON_MATERIAL]
    mapping   : Dict[str, List[VIVY_JSON_MAPPING]]


class Fallback(Enum):
    """
    Fallback strings in Vivy
    """
    FALLBACK_S = "fallback_s"
    FALLBACK_N = "fallback_n"
    FALLBACK = "fallback"


@dataclass
class VivyPasses:
    """
    All passes a Vivy material 
    can support. Each pass is a 
    Node name in the actual material
    """
    diffuse: str
    specular: Optional[str]
    normal: Optional[str]


@dataclass
class VivyRefinements:
    """
    All refinements a Vivy material
    can support. Each attribute can 
    point to the material name that 
    the refinement is based on
    """
    emissive: Optional[str]
    reflective: Optional[str]
    metallic: Optional[str]
    glass: Optional[str]
    fallback_n: Optional[str]
    fallback_s: Optional[str]
    fallback: Optional[str]


@dataclass
class VivyMaterial:
    """
    A full Vivy material.

    Attributes:
    -----------
    base_material: str
        The material that the Vivy entry
        uses 

    desc: str
        Description of the Vivy material

    passes: VivyPasses
        All passes

    refinements: Optional[VivyRefinements]
        All refinements (if supported)
    """
    base_material: str
    desc: str
    passes: VivyPasses
    refinements: Optional[VivyRefinements]


def dict_to_vivy(raw_dict: VIVY_JSON_TOP_LEVEL) -> Dict[str, VivyMaterial]:
    """
    Converts a raw dictionary into a dictionary mapping
    names to a VivyMaterial dataclass

    raw_dict: VIVY_JSON_TOP_LEVEL
        The raw dictionary from the Vivy JSON

    Returns: Dict[str, VivyMaterial]
    """
    final_dict: Dict[str, VivyMaterial] = {}
    for key in raw_dict["materials"]:
        md = raw_dict["materials"][key]
        final_dict[key] = VivyMaterial(
            base_material=md["base_material"],
            desc=md["desc"],
            passes=VivyPasses(
                diffuse=md["passes"]["diffuse"],
                specular=(
                    md["passes"]["specular"] if "specular" in md["passes"] else None
                ),
                normal=md["passes"]["normal"] if "normal" in md["passes"] else None,
            ),
            refinements=(
                None
                if "refinements" not in md
                else VivyRefinements(
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


def read_vivy_json(f: TextIO) -> Dict[str, VivyMaterial]:
    """
    Reads a file object and parses the contents

    f: TextIO
        The file object to load JSON
        data from

    Returns: Dict[str, VivyMaterial]
    """
    data: VIVY_JSON_TOP_LEVEL = json.load(f)
    return dict_to_vivy(data)


def get_vivy_data(file: Path) -> Dict[str, VivyMaterial]:
    """
    Opens a file at the specified path and parses the contents

    file: Path
        The filepath of the file to parse

    Returns: Dict[str, VivyMaterial]
    """
    with open(file, "r") as f:
        return read_vivy_json(f)
