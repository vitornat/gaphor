"""Parse a SysML Gaphor Model and generate a SysML data model."""

from collections import deque
from typing import Deque, Dict, List, Optional, Set, TextIO

from gaphor import UML
from gaphor.core.modeling.element import Element
from gaphor.core.modeling.elementfactory import ElementFactory
from gaphor.storage import storage
from gaphor.UML.modelinglanguage import UMLModelingLanguage


def type_converter(association, enumerations: Dict = {}) -> Optional[str]:
    type_value = association.typeValue
    if type_value is None:
        return None
        # raise ValueError(
        #     f"ERROR! type is not specified for property {association.name}"
        # )
    if type_value.lower() == "boolean":
        return "int"
    elif type_value.lower() in ("integer", "unlimitednatural"):
        return "int"
    elif type_value.lower() == "string":
        return "str"
    elif type_value.endswith("Kind") or type_value.endswith("Sort"):
        # e = list(filter(lambda e: e["name"] == type_value, list(enumerations.values())))[0]
        return None
    else:
        return str(type_value)


def write_attributes(cls: UML.Class, filename: TextIO) -> None:
    a: UML.Property
    have_features = False

    for a in cls.attribute["not it.association"]:  # type: ignore
        type_value = type_converter(a)
        filename.write(f"    {a.name}: attribute[{type_value}]\n")
        have_features = True

    for a in cls.attribute["it.association and it.name"]:  # type: ignore
        if a.name == "baseClass":
            continue
        type_value = type_converter(a)
        if a.upperValue == "1":
            filename.write(f"    {a.name}: relation_one[{type_value}]\n")
        else:
            filename.write(f"    {a.name}: relation_many[{type_value}]\n")
        have_features = True

    for o in cls.ownedOperation:
        filename.write(f"    {o}: operation\n")
        have_features = True

    if not have_features:
        filename.write("    pass\n\n")


def write_class_def(cls, trees, f, cls_written=set()):
    if cls in cls_written:
        return

    generalizations = trees[cls]
    for g in generalizations:
        write_class_def(g, trees, f, cls_written)

    f.write(f"class {cls.name}({', '.join(g.name for g in generalizations)}):\n")
    write_attributes(cls, filename=f)
    cls_written.add(cls)


def find_root_nodes(
    trees: Dict[UML.Class, List[UML.Class]], referenced: List[UML.Class]
) -> List[UML.Class]:
    """Find the root nodes of tree models.

    The root nodes aren't generalizing other UML.Class objects, but are being
    referenced by others through their own generalizations.

    """
    return [key for key, value in trees.items() if not value and key in referenced]


def breadth_first_search(
    trees: Dict[UML.Class, List[UML.Class]], root: UML.Class
) -> List[UML.Class]:
    """Perform Breadth-First Search."""

    explored: List[UML.Class] = []
    queue: Deque[UML.Class] = deque()
    queue.appendleft(root)
    while queue:
        node = queue.popleft()
        if node not in explored:
            explored.append(node)
            neighbors: List[UML.Class] = []
            for key, value in trees.items():
                if node in value:
                    neighbors.append(key)
            if neighbors:
                for neighbor in neighbors:
                    queue.appendleft(neighbor)
    return explored


def generate(filename, outfile=None, overridesfile=None) -> None:
    element_factory = ElementFactory()
    modeling_language = UMLModelingLanguage()
    with open(filename):
        storage.load(
            filename, element_factory, modeling_language,
        )
    with open(outfile, "w") as f:
        trees: Dict[UML.Class, List[UML.Class]] = {}
        referenced: List[UML.Class] = []
        uml_directory: List[str] = dir(UML.uml)
        uml_classes: List[UML.Class] = []

        classes: List = element_factory.lselect(lambda e: e.isKindOf(UML.Class))
        # Order classes, make output predictable
        classes = sorted(
            (cls for cls in classes if cls.name[0] != "~"), key=lambda c: c.name
        )

        for cls in classes:
            if modeling_language.lookup_element(cls.name):
                uml_classes.append(cls)
            else:
                trees[cls] = [g for g in cls.general]
                for gen in cls.general:
                    referenced.append(gen)

                # Also take into account Stereotype extensions ('baseClass')
                for attr in cls.attribute["it.name == 'baseClass'"]:
                    meta_class = attr.association.ownedEnd.class_
                    trees[cls].append(meta_class)
                    referenced.append(meta_class)

        f.write(f"from gaphor.UML import Element\n")
        f.write(
            f"from gaphor.core.modeling.properties import attribute, association, relation_one, relation_many\n"
        )
        for cls in uml_classes:
            f.write(f"from gaphor.UML import {cls.name}\n\n")

        cls_written: Set[Element] = set(uml_classes)
        for cls in trees.keys():
            write_class_def(cls, trees, f, cls_written)

    element_factory.shutdown()
