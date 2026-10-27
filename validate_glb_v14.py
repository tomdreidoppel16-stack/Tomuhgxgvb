"""Offline GLB audit for the TomGPT Vortex GT."""
import argparse, json, sys
from pathlib import Path
import trimesh

def inspect(path):
    scene=trimesh.load(path,force="scene",process=False)
    geoms=list(scene.geometry.items())
    mesh_count=sum(isinstance(g,trimesh.Trimesh) for _,g in geoms)
    triangles=sum(len(g.faces) for _,g in geoms if isinstance(g,trimesh.Trimesh))
    bounds=scene.bounds.tolist() if scene.bounds is not None else None
    return {"file":str(path),"geometry_count":len(geoms),"mesh_count":mesh_count,"triangles":triangles,"bounds":bounds,
            "gta5_native_ready":False,"warnings":["GLB is not a GTA V .yft/.ytd export","Inspect scale, axes, topology, UVs, materials and pivots in Blender/Sollumz"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("files",nargs="+")
    p.add_argument("--json",default=None)
    a=p.parse_args()
    results=[inspect(Path(f)) for f in a.files]
    print(json.dumps(results,indent=2))
    if a.json: Path(a.json).write_text(json.dumps(results,indent=2),encoding="utf-8")
    return 0 if all(x["mesh_count"]>0 and x["triangles"]>0 for x in results) else 1

if __name__=="__main__": sys.exit(main())
