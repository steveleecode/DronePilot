from __future__ import annotations

from pathlib import Path

from OCP.IFSelect import IFSelect_RetDone  # type: ignore[import-not-found]
from OCP.STEPCAFControl import STEPCAFControl_Reader  # type: ignore[import-not-found]
from OCP.TCollection import TCollection_ExtendedString  # type: ignore[import-not-found]
from OCP.TDataStd import TDataStd_Name  # type: ignore[import-not-found]
from OCP.TDF import TDF_Label, TDF_LabelSequence  # type: ignore[import-not-found]
from OCP.TDocStd import TDocStd_Document  # type: ignore[import-not-found]
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ShapeTool  # type: ignore[import-not-found]

from drone_cad.models.cad import CadAssemblyComponent, CadAssemblyMetadata


def read_step_assembly_metadata(step_path: Path) -> CadAssemblyMetadata:
    reader = STEPCAFControl_Reader()
    reader.SetNameMode(True)
    reader.SetColorMode(True)
    reader.SetLayerMode(True)
    reader.SetPropsMode(True)

    status = reader.ReadFile(str(step_path))
    if status != IFSelect_RetDone:
        return CadAssemblyMetadata(
            warnings=[f"STEPCAF reader could not read assembly metadata: {status}"]
        )

    document = TDocStd_Document(TCollection_ExtendedString("dronepilot"))
    if not reader.Transfer(document):
        return CadAssemblyMetadata(warnings=["STEPCAF reader could not transfer document."])

    shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(document.Main())
    free_shapes = TDF_LabelSequence()
    shape_tool.GetFreeShapes(free_shapes)
    if free_shapes.Length() == 0:
        return CadAssemblyMetadata(warnings=["STEPCAF reader found no free root shapes."])

    if free_shapes.Length() > 1:
        warnings = [
            f"STEPCAF reader found {free_shapes.Length()} free root shapes; using first root."
        ]
    else:
        warnings = []

    root = free_shapes.Value(1)
    direct_components = TDF_LabelSequence()
    XCAFDoc_ShapeTool.GetComponents_s(root, direct_components)

    components: list[CadAssemblyComponent] = []
    for index in range(1, direct_components.Length() + 1):
        component_label = direct_components.Value(index)
        referred_label = TDF_Label()
        referenced_name: str | None = None
        is_assembly = False
        is_simple_shape = False
        child_count = 0
        if XCAFDoc_ShapeTool.GetReferredShape_s(component_label, referred_label):
            referenced_name = _label_name(referred_label)
            is_assembly = bool(XCAFDoc_ShapeTool.IsAssembly_s(referred_label))
            is_simple_shape = bool(XCAFDoc_ShapeTool.IsSimpleShape_s(referred_label))
            child_count = int(XCAFDoc_ShapeTool.NbComponents_s(referred_label, False))

        components.append(
            CadAssemblyComponent(
                id=f"component-{index:03d}",
                name=_label_name(component_label) or f"Component {index:03d}",
                referenced_name=referenced_name,
                is_assembly=is_assembly,
                is_simple_shape=is_simple_shape,
                child_count=child_count,
            )
        )

    if components:
        warnings.append(
            "STEPCAF recovered assembly component labels, but these labels are not yet "
            "correlated one-to-one with the tessellated solid list."
        )

    return CadAssemblyMetadata(
        root_name=_label_name(root),
        direct_component_count=direct_components.Length(),
        total_component_usage_count=int(XCAFDoc_ShapeTool.NbComponents_s(root, True)),
        components=components,
        warnings=warnings,
    )


def _label_name(label: TDF_Label) -> str | None:
    name_attribute = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), name_attribute):
        value = str(name_attribute.Get().ToExtString()).strip()
        return value or None
    return None
