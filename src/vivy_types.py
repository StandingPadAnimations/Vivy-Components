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

"""This module defines all of the types used in Vivy Components"""

from dataclasses import dataclass, fields
from typing import Optional, TypedDict, cast, NotRequired

# All of these TypedDict classes
# are used for function annotations
# so that my IDE doesn't scream at me
#
# Sadly my IDE still screams at me for
# the use of deprecated annotations, as
# we have to support 3.7


class VIVY_JSON_PASSES(TypedDict):
    """TypedDict representation of passes
    in Vivy JSON.

    This maps to the following JSON structure:
    ```json
    {
        "diffuse"  : "Diffuse",
        "specular" : "Specular",
        "normal"   : "Normal"
    }
    ```

    specular and normal are not required in the JSON structure
    """

    diffuse: str
    specular: NotRequired[str]
    normal: NotRequired[str]


class VIVY_JSON_REFINE(TypedDict):
    """TypedDict representation of
    refinements in Vivy JSON.

    This maps to the following JSON structure:
    ```json
    {
        "emissive"   : "Some Material Fallback",
        "reflective" : "Some Material Fallback",
        "metallic"   : "Some Material Fallback",
        "glass"      : "Some Material Fallback",
        "fallback_n" : "Some Material Fallback",
        "fallback_s" : "Some Material Fallback",
        "fallback"   : "Some Material Fallback"
    }
    ```

    None of these are required in the JSON structure
    """

    emissive: NotRequired[str]
    reflective: NotRequired[str]
    metallic: NotRequired[str]
    glass: NotRequired[str]
    fallback_n: NotRequired[str]
    fallback_s: NotRequired[str]
    fallback: NotRequired[str]


class VIVY_JSON_MATERIAL(TypedDict):
    """TypedDict representation of
    materials in Vivy JSON.

    This maps to the following JSON structure:
    ```json
    {
        "base_material" : "Some material name",
        "desc"          : "Description",
        "passes"        : {...},
        "refinements"   : {...}
    }
    ```
    """

    base_material: str
    desc: str
    passes: VIVY_JSON_PASSES
    refinements: VIVY_JSON_REFINE


class VIVY_JSON_MAPPING(TypedDict):
    """TypedDict representation of
    mappings in Vivy JSON.

    This maps to the following JSON structure:
    ```json
    {
        "material"   : "Some material",
        "refinement" : "Refinement"
    }
    ```

    refinement is not required in the JSON structure
    """

    material: str
    refinement: NotRequired[str]


class VIVY_JSON_TOP_LEVEL(TypedDict):
    """TypedDict representation of all
    items in the Vivy JSON.

    This maps to the following JSON structure:
    ```json
    {
        "materials" : {
                        "Some material" : {...},
                        ...
                      },
        "mapping"   : {
                        "Some material" : [{...}, ...]
                        ...
                      }
    }
    ```
    """

    materials: dict[str, VIVY_JSON_MATERIAL]
    mapping: dict[str, list[VIVY_JSON_MAPPING]]


# TODO: Figure out how to avoid the use of type: ignore
# in dump_json functions without manually having to write
# out the dictionary


@dataclass
class VivyPasses:
    """All passes a Vivy material
    can support. Each pass is a
    Node name in the actual material
    """

    diffuse: str
    specular: Optional[str]
    normal: Optional[str]

    def dump_json(self) -> VIVY_JSON_PASSES:
        """Dumps a Vivy JSON structure that would
        represent this object.

        Note: Dumping is done by iterating over the fields
        in the class and using a dictionary comprehension
        to construct a dictionary with little effort.

        Returns: VIVY_JSON_PASSES
        """
        return cast(
            VIVY_JSON_PASSES,
            {  # type: ignore
                f.name: getattr(self, f.name)  # type: ignore
                for f in fields(self)  # type: ignore
                if getattr(self, f.name) is not None  # type: ignore
            },
        )


@dataclass
class VivyRefinements:
    """All refinements a Vivy material
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

    def dump_json(self) -> VIVY_JSON_REFINE:
        """Dumps a Vivy JSON structure that would
        represent this object.

        Note: Dumping is done by iterating over the fields
        in the class and using a dictionary comprehension
        to construct a dictionary with little effort.

        Returns: VIVY_JSON_REFINE
        """
        return cast(
            VIVY_JSON_REFINE,
            {  # type: ignore
                f.name: getattr(self, f.name)  # type: ignore
                for f in fields(self)  # type: ignore
                if getattr(self, f.name) is not None  # type: ignore
            },
        )


@dataclass
class VivyMaterial:
    """A full Vivy material.

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

    def dump_json(self) -> VIVY_JSON_MATERIAL:
        """Dumps a Vivy JSON structure that would
        represent this object.

        Note: Dumping is done by iterating over the fields
        in the class and using a dictionary comprehension
        to construct a dictionary with little effort.

        Returns: VIVY_JSON_MATERIAL
        """

        # To satisfy static analysis, we pretend the dictionary
        data: VIVY_JSON_MATERIAL = cast(
            VIVY_JSON_MATERIAL,
            {
                "base_material": self.base_material,
                "desc": self.desc,
                "passes": self.passes.dump_json(),
            },
        )
        if self.refinements is not None:
            data["refinements"] = self.refinements.dump_json()
        return data


@dataclass
class VivyMapping:
    """
    A mapping to a material and its relationship

    Attributes:
    -----------
    material: str
        Material mapped to

    refinement: Optional[str]
        The type of refinement
    """

    material: str
    refinement: Optional[str]

    def dump_json(self) -> VIVY_JSON_MAPPING:
        """Dumps a Vivy JSON structure that would
        represent this object.

        Note: Dumping is done by iterating over the fields
        in the class and using a dictionary comprehension
        to construct a dictionary with little effort.

        Returns: VIVY_JSON_PASSES
        """
        return cast(
            VIVY_JSON_MAPPING,
            {  # type: ignore
                f.name: getattr(self, f.name)  # type: ignore
                for f in fields(self)  # type: ignore
                if getattr(self, f.name) is not None  # type: ignore
            },
        )


@dataclass
class VivyData:
    """
    All data in the Vivy JSON, converted to Python
    Objects

    Attributes:
    -----------
    materials: dict[str, VivyMaterial]
        All Vivy materials

    mapping: dict[str, list[VivyMapping]]
        All Vivy mappings
    """

    materials: dict[str, VivyMaterial]
    mapping: dict[str, list[VivyMapping]]

    def dump_json(self) -> VIVY_JSON_TOP_LEVEL:
        """Dumps the data as a Vivy JSON structure.

        Returns: VIVY_JSON_TOP_LEVEL
        """
        data: VIVY_JSON_TOP_LEVEL = {"materials": {}, "mapping": {}}

        for mat in self.materials:
            data["materials"][mat] = self.materials[mat].dump_json()

        for map in self.mapping:
            data["mapping"][map] = [item.dump_json() for item in self.mapping[map]]

        return data

    def base_to_vivy(self, name: str) -> Optional[VivyMaterial]:
        """Takes a base material name and retrieves the VivyMaterial
        associated with the base material.

        This is done by iterating through self.mapping[name] and finding the
        entry with just the base material and no refinements.

        name: str
            The base material name. The base material refers to the material's
            name in 3D software, which is distinct from the Vivy material name

        Returns:
            VivyMaterial if name is mapped to a material, None otherwise
        """

        mapping_list = self.mapping[name]
        for m in mapping_list:
            if m.refinement is None:
                return self.materials[m.material]
        return None
