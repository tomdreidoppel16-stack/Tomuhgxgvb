"""Run inside Blender: blender -b --python blender_prepare_v14.py -- --input v13_tuned.glb --out prepared_vehicle.blend
Prepares a generic GLB for manual Sollumz GTA V conversion; does NOT create GTA native files.
"""
import bpy, argparse, sys, json, re
from pathlib import Path

def args():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="v13_tuned.glb")
    p.add_argument("--out",default="prepared_vehicle.blend")
    return p.parse_args(argv)

def categorize(name):
    n=name.lower()
    if any(x in n for x in ["wheel","tire","tyre","rim","brake","caliper"]): return "WHEELS_BRAKES"
    if any(x in n for x in ["door","hood","bonnet","trunk","boot","hatch"]): return "MOVING_PANELS"
    if any(x in n for x in ["seat","dash","steer","interior","cockpit","console","pedal"]): return "INTERIOR"
    if any(x in n for x in ["lamp","light","indicator","headlight","taillight"]): return "LIGHTS"
    if any(x in n for x in ["glass","window","windscreen","windshield"]): return "GLASS"
    if any(x in n for x in ["collision","chassis_col"]): return "COLLISION_REFERENCE"
    return "BODY"

def main():
    a=args()
    input_path=Path(a.input).resolve()
    if not input_path.exists(): raise SystemExit(f"Input missing: {input_path}")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(input_path))
    scene=bpy.context.scene
    scene.unit_settings.system="METRIC"
    scene.unit_settings.scale_length=1.0
    buckets={}
    for group in ["BODY","WHEELS_BRAKES","MOVING_PANELS","INTERIOR","LIGHTS","GLASS","COLLISION_REFERENCE"]:
        buckets[group]=bpy.data.collections.new("V14_"+group)
        scene.collection.children.link(buckets[group])
    objects=[o for o in scene.objects if o.type=="MESH"]
    report={"source":input_path.name,"mesh_count":len(objects),"groups":{},"warnings":[]}
    for obj in objects:
        group=categorize(obj.name)
        buckets[group].objects.link(obj)
        for col in list(obj.users_collection):
            if col != buckets[group]: col.objects.unlink(obj)
        obj["tomgpt_category"]=group
        obj["gta5_export_status"]="needs_manual_sollumz_setup"
        report["groups"][group]=report["groups"].get(group,0)+1
    # Reference markers only. Correct GTA vehicle bones, pivots and collisions must be authored in Sollumz.
    for marker,location in [
        ("REF_chassis_origin",(0,0,0)),("REF_driver_seat",(0.45,-0.25,0.65)),
        ("REF_passenger_seat",(-0.45,-0.25,0.65))
    ]:
        empty=bpy.data.objects.new(marker,None)
        scene.collection.objects.link(empty)
        empty.location=location
        empty.empty_display_type="ARROWS"
        empty.empty_display_size=0.2
    report["warnings"]=[
        "This is a Blender staging scene, not a native GTA V vehicle.",
        "Validate model forward axis, scale, pivots, vehicle skeleton, textures, LODs and collisions manually.",
        "Install and use Sollumz in Blender for actual GTA V fragment/drawable authoring."
    ]
    out=Path(a.out).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    out.with_suffix(".report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print("TOMGPT_V14_READY",out,report["mesh_count"])
if __name__=="__main__": main()
