# gen_gadm_screens.py
"""
读取 hotel_list/gadm41_*.json，每个行政区按示例 screen 大小切片生成网格。
输出为 JSONL，每行嵌入完整 example_data（只替换 destination.geo 和 screen）。
"""
import json, copy
from pathlib import Path

# 基准屏幕尺寸：引用示例的宽高（单位：度），再乘以缩放系数 SIZE_SCALE 可微调颗粒度
from hotel_list_map.data_example import example_data

SIZE_SCALE = 1.0  # 设为 0.5 可让单屏宽高减半，更细；设为 2 则更粗
OVERLAP = 0.2     # 相邻视窗的重叠比例；调大减少漏网，调小减少输出量

BASE_LON = example_data["screen"]["rightTop"]["lng"] - example_data["screen"]["leftBottom"]["lng"]
BASE_LAT = example_data["screen"]["rightTop"]["lat"] - example_data["screen"]["leftBottom"]["lat"]
TILE_LON = BASE_LON * SIZE_SCALE
TILE_LAT = BASE_LAT * SIZE_SCALE
STEP_LON = TILE_LON * (1 - OVERLAP)  # 水平方向步长
STEP_LAT = TILE_LAT * (1 - OVERLAP)  # 垂直方向步长


def flatten_coords(geom):
    """将 Polygon/MultiPolygon 的坐标展平成 [lon, lat] 列表。"""
    coords = []
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            coords.extend(ring)
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                coords.extend(ring)
    return coords


def make_screen(lb_lat, lb_lon, rt_lat, rt_lon):
    """根据左下/右上角生成 screen 字典。"""
    return {
        "rightTop": {"lat": rt_lat, "lng": rt_lon, "type": "wgs84"},
        "leftBottom": {"lat": lb_lat, "lng": lb_lon, "type": "wgs84"},
        "center": {
            "lat": (lb_lat + rt_lat) / 2,
            "lng": (lb_lon + rt_lon) / 2,
            "type": "wgs84",
        },
    }


def point_in_ring(pt, ring):
    """射线法判断点是否在单个线环内部（GeoJSON 顺序不要求顺时针）。"""
    x, y = pt
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        # 边跨越射线的条件
        if ((y1 > y) != (y2 > y)):
            xinters = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xinters > x:
                inside = not inside
    return inside


def point_in_polygon(pt, coords):
    """
    判断点是否在 Polygon（含洞）或 MultiPolygon 内。
    Polygon: coords 为 [外环, 洞1, ...]；
    MultiPolygon: coords 为 [[[外环,...]], [[外环,...]], ...]
    """
    if not coords:
        return False
    # Polygon
    if isinstance(coords[0][0][0], (float, int)):  # [[x,y], ...]
        rings = coords
        if not point_in_ring(pt, rings[0]):
            return False
        for hole in rings[1:]:
            if point_in_ring(pt, hole):
                return False
        return True
    # MultiPolygon
    for poly in coords:  # 每个 poly 是一组 rings
        rings = poly
        if not rings:
            continue
        if not point_in_ring(pt, rings[0]):
            continue
        hit_hole = any(point_in_ring(pt, hole) for hole in rings[1:])
        if not hit_hole:
            return True
    return False


def tile_bbox(min_lon, max_lon, min_lat, max_lat):
    """
    用固定视窗大小对外接矩形做网格切片：
    - 按 STEP_LON/STEP_LAT 步进，保证 OVERLAP 比例的重叠。
    - 若区域尺寸小于单个视窗，直接返回覆盖全域的一个 screen。
    """
    screens = []
    lon = min_lon
    while lon < max_lon:
        lat = min_lat
        rt_lon = min(lon + TILE_LON, max_lon)
        while lat < max_lat:
            rt_lat = min(lat + TILE_LAT, max_lat)
            screens.append(make_screen(lat, lon, rt_lat, rt_lon))
            lat += STEP_LAT
        lon += STEP_LON
    if not screens:  # 极小区域兜底
        screens.append(make_screen(min_lat, min_lon, max_lat, max_lon))
    return screens


def main():
    """遍历所有 gadm41 JSON，逐个 feature 输出 screen JSONL。"""
    for path in sorted(Path("hotel_list").glob("gadm41_JPN_2.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for feat in data.get("features", []):
            coords = flatten_coords(feat["geometry"])
            lons = [p[0] for p in coords]
            lats = [p[1] for p in coords]
            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)

            screens = tile_bbox(min_lon, max_lon, min_lat, max_lat)
            props = feat.get("properties", {})
            area_name = ", ".join(
                p for p in (props.get("NAME_3"), props.get("NAME_2"), props.get("NAME_1"), props.get("COUNTRY"))
                if p and p != "NA"
            )
            gid = props.get("GID_2") or props.get("GID_1") or props.get("GID_0")

            selected = []
            geom_coords = feat["geometry"]["coordinates"]
            for idx, s in enumerate(screens):
                # 先按中心点落区内筛选，保证精度
                center_pt = (s["center"]["lng"], s["center"]["lat"])
                if point_in_polygon(center_pt, geom_coords):
                    selected.append((idx, s))
            # 如果全部被筛掉（极窄区域），兜底保留第一块，确保覆盖
            if not selected and screens:
                selected.append((0, screens[0]))

            for idx, s in selected:
                payload = copy.deepcopy(example_data)
                payload["destination"]["geo"] = {"name": area_name}
                payload["screen"] = s
                print(json.dumps({
                    "area": area_name,
                    "gid": gid,
                    "screen_index": idx,
                    "data": payload,
                }, ensure_ascii=False))



if __name__ == "__main__":
    main()
