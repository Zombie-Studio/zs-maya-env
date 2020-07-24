import Katana
import v1 as ArnoldAOVs

if ArnoldAOVs:
    PluginRegistry = [
        ("SuperTool", 2, "ArnoldAOVs_LS",
                (ArnoldAOVs.ArnoldAOVsNode,
                        ArnoldAOVs.GetEditor)),
    ]
