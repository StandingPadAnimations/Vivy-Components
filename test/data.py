"""Raw JSON data that is used for unit tests"""

import os

DATA_JSON_FILE = os.path.join(os.path.dirname(__file__), "data.json")
DATA_JSON = {
    "materials": {
        "PBR": {
            "base_material": "PBR",
            "desc": "PBR material",
            "passes": {
                "diffuse": "Diffuse",
                "normal": "Normal",
                "specular": "Specular",
            },
            "refinements": {"emissive": "BPR_Emit", "fallback": "Simple"},
        },
        "Simple": {
            "base_material": "Simple",
            "desc": "Simple Material",
            "passes": {"diffuse": "Diffuse"},
        },
    },
    "mapping": {
        "PBR": [{"material": "PBR"}],
        "Simple": [
            {"material": "Simple"},
            {"material": "PBR", "refinement": "fallback"},
        ],
        "BPR_Emit": [{"material": "PBR", "refinement": "emissive"}],
    },
}
